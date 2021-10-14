from django.utils import translation
from django.views.generic import ListView, DetailView
from .models import Article
from ..tags.models import Tag


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'article_list'

    def _get_tag_from_request(self) -> str:
        return self.request.GET.get('tag', '')

    def get_queryset(self):
        qs = super(ArticleListView, self).get_queryset().order_by('-creation_date')
        qs = qs.prefetch_related('tags')
        filter_tag = self._get_tag_from_request()
        if filter_tag != '':
            qs = qs.filter(**{'tags__' + Tag.get_translattion_name_field(): filter_tag})
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs.update({'tags_all': Tag.objects.all()})
        return super(ArticleListView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    query_pk_and_slug = 'slug'  # rewritten bellow

    def get_slug_field(self):
        # I want translatable slug so I need to get article based on localized fields
        return Article.get_translattion_slug_field()
