from django.contrib import admin
from article_app import models
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name','username','mobile','DOB',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('heading', 'uploaded_on', 'type', 'uploaded_by',)


admin.site.register(models.Users, UserAdmin),
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Tags)