from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    # 文章创建
    path('article-create/', views.article_create, name='article_create'),
    # 文章更新
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    # 文章删除
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # 文章附件下载
    path('article-download/<int:id>', views.download_file, name='download_file'),
]
