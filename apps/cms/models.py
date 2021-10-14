import os

from django.conf import settings
from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from apps.core.fields import TranslatedField
from apps.core.utils import create_jpg_thumbnail


class Article(models.Model):
    # todo translations as IDs like 'cms-model-article-slug'
    slug_en = models.SlugField(_('slug en'))
    slug_de = models.SlugField(_('slug de'))
    title_en = models.CharField(_('title en'), max_length=255)
    title_de = models.CharField(_('title de'), max_length=255)
    image = models.ImageField(_('image'))
    tags = models.ManyToManyField('tags.Tag', verbose_name=_('tags'), blank=True)
    content_en = models.TextField(_('content en'))
    content_de = models.TextField(_('content de'))
    creation_date = models.DateTimeField(_('creation_date'), auto_now_add=True)
    image_thumb = models.ImageField(_("image thumb"), blank=True, null=True)

    content = TranslatedField(
        'content_en', 'content_de'
    )
    slug = TranslatedField(
        'slug_en', 'slug_de'
    )
    title = TranslatedField(
        'title_en', 'title_de'
    )

    class Meta:
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return self.slug

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        self._image = self.image

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        if self._image != self.image or bool(self.image_thumb) is False:
            self._create_image_thumb()  # todo create async using celery
            super(Article, self).save(*args, **kwargs)

    def _create_image_thumb(self):
        thumb_name = self.image.name + '_thumb.jpg'
        create_jpg_thumbnail(self.image.name, thumb_name, (376, 220))
        self.image_thumb = thumb_name.replace(settings.MEDIA_ROOT, "")

    @staticmethod
    def get_translattion_slug_field() -> str:
        return 'slug_' + translation.get_language()
