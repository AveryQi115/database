from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from like.models import LikeRecord
from collect.models import CollectRecord
from taggit.managers import TaggableManager


# 博客文章板块模型
class ArticleColumn(models.Model):
    """ 文章板块

    每个用户发布的文章都隶属于一个版块。

    属性：
        title       ：板块标题
    """
    title = models.CharField(max_length=100, blank=True)

    # 创建时间 ------ 甲方目前无该需求
    # created = models.DataTimeField(default=timezone.now)

    def __str__(self):
        return self.title


# 博客文章数据模型
class ArticlePost(models.Model):
    """ 文章发布

    博客文章的数据模型。
    用户每发布一篇文章，将会实例化一个ArticlePost；
    用户每删除一篇文章，将会删除对应的ArticlePost实例。

    属性：
        author              ：文章作者
        column              ：文章栏目
        title               ：文章标题
        body                ：文章正文
        attachment          ：文章附件
        created             ：文章创建时间
        updated             ：文章更新时间
        forum               ：文章标签
        like_records        ：点赞记录
        collect_records     ：收藏记录
        total_views         ：浏览量
    """
    # 参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # “一对多”外键。
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )

    title = models.CharField(max_length=100)

    body = models.TextField()

    attachment = models.FileField(upload_to='article_file/%Y%m%d/', blank=True)

    # 参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    forum = TaggableManager(blank=True)

    like_records = GenericRelation(LikeRecord, related_query_name='articles')
    
    collect_records = GenericRelation(CollectRecord, related_query_name='articles')

    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以创建时间的倒序排列
        ordering = ('-created',)

    def __str__(self):
        # 将文章标题返回
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])

    # 文章是否点赞
    def article_is_liked(self, user):
        like_records = self.like_records.filter(user=user)
        return len(like_records) != 0

    # 文章是否收藏
    def article_is_collected(self, user):
        collect_records = self.collect_records.filter(user=user)
        return len(collect_records) != 0

    # 文章是否在错误时间创建
    def was_created_recently(self):
        diff = timezone.now() - self.created
        
        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            return True
        else:
            return False