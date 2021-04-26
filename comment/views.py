# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from article.models import ArticlePost
from .forms import CommentForm
from .models import Comment
#引入权限检查模块
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from notifications.signals import notify

# 文章评论
@login_required(login_url='/userprofile/login/')
# 新增参数 parent_comment_id
def post_comment(request, article_id, parent_comment_id=None):
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('comment.add_comment'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
    article = get_object_or_404(ArticlePost, id=article_id)

    # 处理 POST 请求
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user

            # 二级回复
            if parent_comment_id:
                parent_comment = Comment.objects.get(id=parent_comment_id)
                # 若回复层级超过二级，则转换为二级
                new_comment.parent_id = parent_comment.get_root().id
                # 被回复人
                new_comment.reply_to = parent_comment.user
                new_comment.save()

                notify.send(
                        request.user,
                        recipient=parent_comment.user,
                        verb='评论了你',
                        target=article,
                        action_object=new_comment,)

                return HttpResponse('200 OK')
            new_comment.save()
            notify.send(
                request.user,
                recipient=article.author,
                verb='评论了你',
                target=article,
                action_object=new_comment,
            )
            return redirect(article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
            'article_id': article_id,
            'parent_comment_id': parent_comment_id
        }
        return render(request, 'comment/reply.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")

#删除评论
@login_required(login_url='/userprofile/login/')
def comment_delete(request, article_id, comment_id):
    # 根据aritlce id获取需要删掉评论的文章
    article = get_object_or_404(ArticlePost, id=article_id)
    #
    # print(article_id)
    # 根据id删除comment
    comment = Comment.objects.get(id=comment_id)
    # 删除本人的评论或者提问问题的人可以删除
    if request.user != comment.user :
        # print ("无法删除")
        messages.error(request, "抱歉，你无权删除此评论")
        return redirect(article)
    #删除孩子
    children=comment.children.all()
    for chid in children:
        chid.delete()

    likes=comment.like_records.all();

    # 调用.delete()方法删除问题
    comment.delete()
    # 完成后返回主页面
    return redirect(article)

#评论的更新
def update_comment(request, article_id,comment_id):
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('comment.change_comment'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
    article = get_object_or_404(ArticlePost, id=article_id)
    new_comment=Comment.objects.get(id=comment_id)
    # 处理 POST 请求
    if request.user != new_comment.user:
        # print ("无法删除")
        # messages.error(request, "抱歉，你无权修改此评论")
        return HttpResponse('抱歉，你无权修改此评论')
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_cd = comment_form.cleaned_data
            new_comment.body = comment_cd['body']
            new_comment.save()
            return HttpResponse('200 OK')
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理 GET 请求
    elif request.method == 'GET':
        comment_form = CommentForm()

        context = {
            'comment_form': comment_form,
            'comment': new_comment,
            'comment_id': new_comment.id,
            'article_id': article_id,
        }
        return render(request, 'comment/update.html', context)
    # 处理其他请求
    else:
        return HttpResponse("仅接受GET/POST请求。")