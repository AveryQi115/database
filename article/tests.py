from django.contrib.contenttypes.models import ContentType
# Create your tests here.
from django.test import TestCase
import datetime
from django.utils import timezone
from article.models import ArticlePost
from django.contrib.auth.models import User
from like.models import LikeRecord
from collect.models import CollectRecord
from time import sleep
from django.urls import reverse


class ArticlePostModelTests(TestCase):

    def test_was_created_recently_with_future_article(self):
        # 若创建时间为未来 返回false
        author = User(username='user', password='test_password')
        author.save()

        future_article=ArticlePost(
            author=author,
            title='test',
            body='test',
            created=timezone.now()+datetime.timedelta(days=30)
        )
        self.assertIs(future_article.was_created_recently() , False)

    def test_was_created_recently_with_seconds_before_article(self):
         # 若文章创建时间为 1 分钟内，返回 True
         author = User(username='user1', password='test_password')
         author.save()
         seconds_before_article = ArticlePost(
             author=author,
             title='test1',
             body='test1',
             created=timezone.now() - datetime.timedelta(seconds=45)
         )

         self.assertIs(seconds_before_article.was_created_recently(), True)
    def test_was_created_recently_with_hours_before_article(self):
         # 若文章创建时间为几小时前，返回 False
         author = User(username='user2', password='test_password')
         author.save()
         hours_before_article = ArticlePost(
             author=author,
             title='test2',
             body='test2',
             created=timezone.now() - datetime.timedelta(hours=3)
         )
         hours_before_article.save()
         self.assertIs(hours_before_article.was_created_recently(), False)
    def test_was_created_recently_with_days_before_article(self):
         # 若文章创建时间为几天前，返回 False
         author = User(username='user3', password='test_password')
         author.save()
         months_before_article = ArticlePost(
             author=author,
             title='test3',
             body='test3',
             created=timezone.now() - datetime.timedelta(days=5)
         )
         months_before_article.save()
         self.assertIs(months_before_article.was_created_recently(), False)
     # python manage.py test
    
    def test_article_is_liked(self):
        # 刚创建一个文章，没有被喜欢，返回false，若创建一条喜欢记录后，则返回true
        author = User(username='user', password='test_password')
        author.save()
        liked_article = ArticlePost(
            author=author,
            title='test',
            body='test',
        )
        liked_article.save()
        self.assertIs(liked_article.article_is_liked(author), False)
        like_record=LikeRecord(content_type=ContentType.objects.get_for_model(ArticlePost),
                        object_id=liked_article.id,
                        user=author,
                        liked_time=timezone.now()
                        )
        like_record.save()
        sleep(0.5)
        self.assertIs(liked_article.article_is_liked(author), True)


    def test_article_is_collected(self):

        # 刚创建一个文章，没有被收藏，返回false，若创建一条收藏记录后，则返回true
        author = User(username='user', password='test_password')
        author.save()
        collected_article = ArticlePost(
            author=author,
            title='test',
            body='test',
        )
        collected_article.save()
        self.assertIs(collected_article.article_is_collected(author), False)
        collect_record=CollectRecord(content_type=ContentType.objects.get_for_model(ArticlePost),
                        object_id=collected_article.id,
                        user=author,
                        collected_time=timezone.now()
                        )
        collect_record.save()
        sleep(0.5)
        self.assertIs(collected_article.article_is_collected(author), True)


class ArtitclePostViewTests(TestCase):

    def test_article_detail(self):
        """
        文章创建后，进入详情页面，检查内容是否正确
        :return:
        """
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            body='test5',
        )
        article.save()

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'user5')
        self.assertContains(response, 'test5')

    def test_article_update_display(self):
        """
        更新文章内容，检查显示
        :return:
        """
        author = User(username='user', password='test_password')
        author.save()
        old_post_modified_time=timezone.now()
        article = ArticlePost(
            author=author,
            title='test',
            body='test',
            created=old_post_modified_time
        )
        article.save()
        sleep(0.5)
        article.body='new body'
        article.created=timezone.now()
        article.save()
        article.refresh_from_db()
        self.assertTrue(article.created >old_post_modified_time)

    def test_article_create(self):
        """
        登录用户创建自己的帖子
        :return:
        """
        user1 = User.objects.create(username='testuser', is_superuser=True)
        user1.set_password('12345')
        user1.save()
        article = ArticlePost(
            title='测试标题',
            body= '测试内容'
        )
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login) # 用户登陆以后 创建文章

        url = reverse('article:article_create')
        response = self.client.post(url, {'column': 'none', 'forum': 'tag', 'title': 'new1', 'body': 'new2'}, follow=True)
        self.assertEqual(response.status_code, 200)


    def test_login_then_update_myself_article(self):
        """
        用户只能删除自己的帖子
        :return:
        """
        user1 = User.objects.create(username='testuser', is_superuser=True)
        user1.set_password('12345')
        user1.save()

        article = ArticlePost(
            author=user1,
            title='test1',
            body='test2'
        )
        article.save()
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

        url = reverse('article:article_update',args=(article.id,))

        response = self.client.post(url, {'column': 'none', 'title':'new1', 'body':'new2', 'attachment': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        # print(str(response.content, encoding='utf-8'))
        # 测试修改后 内容是否更新   结果是修改成功！
        article.refresh_from_db()
        url2 = reverse('article:article_detail', args=(article.id,))
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'new1')
    

    def test_login_then_update_other_article(self):
        """
        用户删除别人的的帖子，然后失败
        :return:
        """
        user1 = User.objects.create(username='testuser', is_superuser=True)
        user1.set_password('12345')
        user1.save()
        user2 = User.objects.create(username='testuser2', is_superuser=True)
        user2.set_password('12345')
        user2.save()
        article = ArticlePost(
            author=user1,
            title='test1',
            body='test2'
        )
        article.save()
        login=self.client.login(username='testuser2', password='12345')
        self.assertTrue(login)
        url = reverse('article:article_update', args=(article.id,))
        response = self.client.post(url, {'column':'none','forum':'tag','title': 'new1', 'body': 'new2'},follow=True)
        self.assertEqual(response.status_code, 200)

        # 测试修改后 内容是否更新  结果是并没有修改成功
        article.refresh_from_db()
        url2 = reverse('article:article_detail', args=(article.id,))
        response2 = self.client.get(url2)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'test1')



    def test_increase_views_but_not_change_updated_field(self):
        # 请求详情视图时，不改变 updated 字段
        author = User(username='user5', password='test_password')
        author.save()
        article = ArticlePost(
            author=author,
            title='test5',
            body='test5',
            )
        article.save()

        sleep(0.5)

        url = reverse('article:article_detail', args=(article.id,))
        response = self.client.get(url)

        viewed_article = ArticlePost.objects.get(id=article.id)
        self.assertIs(viewed_article.updated - viewed_article.created < timezone.timedelta(seconds=0.1), True)

