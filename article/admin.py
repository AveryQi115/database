from django.contrib import admin
from .models import ArticlePost, ArticleColumn

# Register your models here.

# 注册文章
admin.site.register(ArticlePost)

# 注册文章板块
admin.site.register(ArticleColumn)