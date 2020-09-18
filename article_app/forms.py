from django import forms
from article_app.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('heading', 'article_content', 'type', 'image')
