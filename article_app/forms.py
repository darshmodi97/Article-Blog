from django import forms
from article_app.models import Article,Tags


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('heading', 'article_content', 'type', 'image')

class TagsForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ('tags_title',)

