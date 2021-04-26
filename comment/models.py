from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey  # django-ckeditor
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from article.models import ArticlePost
from question.models import QuestionPost
from like.models import LikeRecord
from collect.models import CollectRecord


# 问题的回答
class Comment(MPTTModel):
    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )
    article = models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    # 之前为 body = models.TextField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    # 点赞记录
    like_records = GenericRelation(LikeRecord, related_query_name='comments')
    # 收藏记录
    collect_records = GenericRelation(CollectRecord, related_query_name='comments')

    # 替换 Meta 为 MPTTMeta
    # class Meta:
    #     ordering = ('created',)
    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]

    # 评论是否点赞
    def comment_is_liked(self, user):
        like_records = self.like_records.filter(user=user)
        return len(like_records) != 0

    def comment_is_collected(self, user):
        collect_records = self.collect_records.filter(user=user)
        return len(collect_records) != 0
