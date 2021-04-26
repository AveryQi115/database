from django import forms
from .models import ArticlePost


# 发布文章的表单类
class ArticlePostForm(forms.ModelForm):

    class Meta:
        # 数据模型来源
        model = ArticlePost
        # 表单包含的字段
        fields = ('forum', 'title', 'body', 'attachment')

        '''
        forum       ：标签
        title       ：标题
        body        ：正文
        attachment  ：附件
        '''