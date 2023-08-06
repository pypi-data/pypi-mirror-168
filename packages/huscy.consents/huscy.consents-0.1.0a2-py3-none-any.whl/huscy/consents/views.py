import datetime
import json

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic
from weasyprint import HTML

from huscy.consents.forms import SignatureForm
from huscy.consents.models import Consent, ConsentFile, TextBlock


class CreateConsentView(generic.CreateView):
    fields = 'name', 'content'
    queryset = Consent.objects
    template_name = "consents/create-consent.html"

    def dispatch(self, request, *args, **kwargs):
        self.consent_id_list = list(map(int, self.request.GET.get('textblocks', '0').split(',')))
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        selected_textblocks = TextBlock.objects.filter(id__in=self.consent_id_list)
        content_blocks = selected_textblocks.values_list('content', flat=True)
        initial["content"] = '\n\n'.join(content_blocks)
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        unselected_textblocks = TextBlock.objects.exclude(id__in=self.consent_id_list)
        context['unselected_textblocks'] = unselected_textblocks
        return context

    def get_success_url(self):
        return reverse('sign-consent', args=[self.object.pk])


class SignConsentView(generic.FormView):
    form_class = SignatureForm
    template_name = 'consents/sign-consent.html'

    def dispatch(self, request, *args, **kwargs):
        self.consent = get_object_or_404(Consent, pk=self.kwargs['consent_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['consent'] = self.consent
        return context

    def form_valid(self, form):
        signature = form.cleaned_data.get('signature')
        html_template = get_template('consents/signed-consent.html')
        rendered_html = html_template.render({
            "consent": self.consent,
            "signature": json.dumps(signature),
            "today": datetime.date.today(),
        })
        content = HTML(string=rendered_html).write_pdf()
        filename = self.consent.name
        file_handle = SimpleUploadedFile(
            name=filename,
            content=content,
            content_type='application/pdf'
            )
        ConsentFile.objects.create(consent=self.consent, filehandle=file_handle)
        return HttpResponse(content, content_type="application/pdf")
