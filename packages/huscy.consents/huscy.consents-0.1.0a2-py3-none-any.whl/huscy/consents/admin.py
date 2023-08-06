from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Consent, ConsentFile, TextBlock


class ConsentAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', '_content'

    def _content(self, consent):
        return truncatechars(consent.content, 50)


class ConsentFileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = 'consent', 'created_at', 'filehandle'
    readonly_fields = 'created_at',


class TextBlockAdmin(admin.ModelAdmin):
    list_display = 'type', '_content'

    def _content(self, text_block):
        return truncatechars(text_block.content, 100)


admin.site.register(Consent, ConsentAdmin)
admin.site.register(ConsentFile, ConsentFileAdmin)
admin.site.register(TextBlock, TextBlockAdmin)
