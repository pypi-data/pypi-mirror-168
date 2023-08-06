from django.db import models
from django.utils.translation import gettext_lazy as _


class Consent(models.Model):
    name = models.CharField(max_length=128)
    content = models.TextField()

    def __str__(self):
        return self.name


class ConsentFile(models.Model):
    consent = models.ForeignKey(Consent, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    filehandle = models.FileField()

    def __str__(self):
        return f'{self.consent} {self.created_at.isoformat(sep=" ", timespec="seconds")}'


def calculate_order():
    return TextBlock.objects.count()


class TextBlock(models.Model):

    class TYPE(models.IntegerChoices):
        HEADER = 0, _('header')
        PARAGRAPH = 1, _('paragraph')

    content = models.TextField()
    type = models.IntegerField(choices=TYPE.choices)
    order = models.PositiveIntegerField(default=calculate_order)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['order']
