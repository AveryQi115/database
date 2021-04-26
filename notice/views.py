# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from article.models import ArticlePost
from question.models import QuestionPost

class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表

    每个用户对每个文章/问题/回答评论，都会实例化；

    属性：
        context_object_name   ：上下文的名称
        template_name      ：模板位置
        login_url ：重定向

    """
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice/list.html'
    # 登录重定向
    login_url = '/userprofile/login/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()

    # 函数名：  get
    # 作者：    wjq
    # 日期：    2020-7-19
    # 功能：    重写get请求
    # 输入参数：request 用户请求
    #
    # 返回值：  类型（重定向到对应网页路由）
    # 修改记录：
    # 处理 get 请求
class CommentNoticeUpdateView(View):

    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        verb=request.GET.get('verb')
        # 更新单条通知
        if notice_id:
            if verb=='评论了你':
                content = ArticlePost.objects.get(id=request.GET.get('id'))
            else:
                content = QuestionPost.objects.get(id=request.GET.get('id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect(content)
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return redirect('notice:list')