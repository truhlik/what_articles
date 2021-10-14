from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.core.fields import TranslatedField


class Tag(models.Model):
    name_en = models.CharField(_('name en'), max_length=255)
    name_de = models.CharField(_('name de'), max_length=255)

    name = TranslatedField(
        'name_en', 'name_de'
    )

    def __str__(self):
        return self.name

    @staticmethod
    def get_translattion_name_field() -> str:
        return 'name_' + translation.get_language()
