from django.contrib import admin
from . import models
# Register your models here.

# 配置应用
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'pub_time')
    list_filter = ('pub_time',)

admin.site.register(models.Article, ArticleAdmin)