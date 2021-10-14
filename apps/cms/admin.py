from django.contrib import admin
from django import forms
from django.forms import Media
from django.templatetags.static import static

from .models import Article


class TagInline(admin.StackedInline):
    model = Article.tags.through
    extra = 1


class ArticleEditForm(forms.ModelForm):

    class Meta:
        fields = '__all__'

    class Media:
        js = ("//cdn.ckeditor.com/4.14.1/standard/ckeditor.js", )

    @property
    def media(self):
        # this is workaround because there was a problem with manifest for static('js/admin.js')
        media = super(ArticleEditForm, self).media
        admin_media = Media(js=(static('js/admin.js'), ))
        media = media + admin_media
        return media


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title_en', 'title_de', 'slug_en', 'slug_de', 'tags_list', 'creation_date']
    list_filter = ['tags']
    fields = (('title_en', 'title_de'), 'tags', 'image', ('content_en', 'content_de'), ('slug_en', 'slug_de'), 'image_thumb')
    form = ArticleEditForm
    prepopulated_fields = {'slug_en': ('title_en', ), 'slug_de': ('title_de', )}
    # inlines = [TagInline]  # this is not good solution yet

    def get_queryset(self, request):
        return super(ArticleAdmin, self).get_queryset(request).prefetch_related('tags')

    def tags_list(self, obj):
        return ",".join([tag.name for tag in obj.tags.all()])
