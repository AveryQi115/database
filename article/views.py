from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render, redirect
import markdown
from comment.models import Comment
from .models import ArticleColumn  # 文章板块
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# 引入评论表单
from comment.forms import CommentForm
# 引入 Q 对象
from django.db.models import Q
from django.conf import settings
from django.utils.http import urlquote
import os
# 引入分页模块
from django.core.paginator import Paginator
#引入权限检查模块
from django.utils.html import strip_tags  #去掉所有html标签

#栏目内搜索文章
def search_article_in_column(request):
    """ 板块内搜索文章

        在指定的板块内搜索文章。

        属性：
            search      ：搜索操作
            column      ：板块
            context     ：上下文赋值
    """

    # 判断是否进行了搜索
    search = request.GET.get('search')
    column = request.GET.get('column')
    #先将栏目内文章过滤出来
    if column is not None and column.isdigit():
        articles = ArticlePost.objects.filter(column=column)
    else:
        articles = ArticlePost.objects.all()
    # 如果进行了搜索
    if search:
        articles = articles.filter(
            # 匹配标题(不区分大小写)
            Q(title__icontains=search) |
            # 匹配文章内容(不区分大小写)
            Q(body__icontains=search)
        ).order_by('-updated')
    #上下文赋值
    context = {'articles': articles,'search_a': search,'column_a':column}
    return context

#搜索文章
def search_article(request):
    """ 搜索文章

        搜索文章。

        属性：
            search      ：搜索操作
    """

    # 判断是否进行了搜索
    search = request.GET.get('search')
    # 如果进行了搜索
    if search:
        articles = ArticlePost.objects.filter(
            # 匹配标题(不区分大小写)
            Q(title__icontains=search) |
            # 匹配问题描述(不区分大小写)
            Q(body__icontains=search)
        ).order_by('-updated')
        context = {'articles': articles,'search_a': search}
    # 如果未进行搜索
    else:
        article_list = ArticlePost.objects.all()

        # 每页显示 1 篇文章
        paginator = Paginator(article_list, 5)
        # 获取 url 中的页码
        page = request.GET.get('page')
        # 将导航对象相应的页码内容返回给 articles
        articles = paginator.get_page(page)
        context = {'articles': articles,'search_a': search}
    return render(request, 'search/search_article.html', context)


# 热门文章
def hot_article_list(request):
    """ 热门文章

        对热门文章的排序

        属性：
            articles        ：所有文章
            hot_titles      ：文章标题集成
            hot_ids         ：文章id集成
            context         ：上下文
    """

    def sorts():
        sort = ['-total_views', '-updated']
        return sort
    
    ## 取出所有博客文章
    articles = list(ArticlePost.objects.order_by(*sorts())[:5])
    ## 将博客文章标题构成list
    hot_titles = [article.title for article in articles]
    ## 如果list长度不足5，则用'...'补齐
    hot_titles += ['...' for i in range(5 - len(articles))]
    ## 将博客文章id构成list
    hot_ids = [article.id for article in articles]
    ## 如果list长度不足5，则用'...'补齐
    hot_ids += [0 for i in range(5 - len(articles))]
    ## 将title list传递给模板（templates）

    ## 将整个article列表传递给前端页面，没有解决可能出现的列表不足默认内容补足5个的问题
    context = {'articles': articles}
    ## render函数：载入模板，并返回context对象
    return context


# 板块文章
def column_article_list():
    """ 板块文章list

        板块中的文章集成

        属性：
            articles        ：文章
            context         ：上下文
    """

    articles = ArticlePost.objects.all().order_by('column', '-updated')
    context = {'column_articles': articles}
    return context

# 文章详情
def article_detail(request, id):
    """ 文章详情

        获取文章的详细信息，包括浏览量、评论等。

        属性：
            articles        ：文章
            comments        ：评论
            comment_form    ：评论表单
            context         ：上下文
    """

    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # 更新浏览量
    article.total_views += 1
    # 保存新的浏览量
    article.save(update_fields=['total_views'])
     # 将markdown语法渲染成html样式
    article.body = strip_tags(article.body)
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])

    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 引入评论表单
    comment_form = CommentForm()
    # 添加comments上下文
    context = {'article': article, 'comments': comments, 'comment_form': comment_form, }
    # 载入模板，并返回context对象
    return render(request, 'article/detail.html', context)

# 发布文章
@login_required(login_url='/userprofile/login/')
def article_create(request):
    """ 创建文章

        创建文章。

        属性：
            myuser                      ：用户
            article_post_form           ：创建文章表单
            new_article                 ：新文章实体
            column                      ：文章所属板块
            context                     ：上下文
    """

    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.add_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')

    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            new_article.author = User.objects.get(id=request.user.id)
            article_cd = article_post_form.cleaned_data
            if 'attachment' in request.FILES:
                new_article.attachment = article_cd["attachment"]
            # 所有文章都需要归属于一个板块
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                new_article.column = None


            # 将新文章保存到数据库中
            new_article.save()
            # 保存 tags 的多对多关系
            article_post_form.save_m2m()
            # 完成后提示发表成功
            messages.success(request, "发表文章成功。")
            # 完成后返回到文章详情
            return redirect("article:article_detail", id=new_article.id)
        # 如果数据不合法，返回错误信息
        else:
            # 赋值上下文
            columns = ArticleColumn.objects.all()
            context = {'article_post_form': article_post_form, 'columns': columns}  # debug
            messages.error(request, "表单内容有误，请重新填写。")
            return render(request, "article/create.html", context)
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """ 更新文章

        更新文章的视图函数
        通过POST方法提交表单，更新titile、body字段
        GET方法进入初始表单页面

        属性：
            myuser                      ：用户
            article_post_form           ：文章表单
            article                     ：文章
            column                      ：文章所属板块
            context                     ：上下文
    """

    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.change_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 只能修改本人的回答
    if request.user != article.author:
        messages.error(request, "抱歉，你无权删除这篇文章")
        return redirect(article)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 数据清洗一遍
            article_cd = article_post_form.cleaned_data
            # 板块相关
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 保存新写入的 title、body 数据并保存
            article.forum = article_cd['forum']
            article.title = article_cd['title']
            article.body = article_cd['body']
            if 'attachment' in request.FILES:
                print("有文件")
                article.attachment=article_cd['attachment']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect(article)
        # 如果数据不合法，返回错误信息
        else:
            # 赋值上下文
            columns = ArticleColumn.objects.all()
            context = {
                'article': article,
                'article_post_form': article_post_form,
                'columns': columns
            }
            messages.error(request, "表单内容有误，请重新填写。")
            return render(request, "article/update.html", context)
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


# 删除文章
@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    """ 删除文章

        根据id获取需要删掉的文章

        属性：
            article                     ：文章
            comments                    ：评论
    """

    article = ArticlePost.objects.get(id=id)
    # 只能删除本人的文章
    if request.user != article.author:
        messages.error(request, "抱歉，你无权删除这篇文章")
        return redirect(article)
    # 调用.delete()方法删除问题
    comments = Comment.objects.filter(article_id=id)
    # if comments:
    if comments.count():
        for comment in comments:
            comment.delete()
    # comment_delete()
    article.delete()
    # messages.success(request,"成功删除！")
    # print('删除')
    # 完成后返回文章详情
    return redirect("/")


@login_required(login_url='/userprofile/login/')
def download_file(request,id):
    """ 下载文件

        用户可下载文章的附件

        属性：
            myuser                      ：用户
            article                     ：文章
            filename                    ：文件名
            filepath                    ：文件路径
            the_file_name               ：弹出对话框中的默认的下载文件名
    """

    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.view_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')

    article = ArticlePost.objects.get(id=id)
    #
    filename = article.attachment
    filepath = os.path.join(settings.MEDIA_ROOT, str(filename))

    the_file_name = str(filename).split("/")[-1]  # 显示在弹出对话框中的默认的下载文件名
    # print(the_file_name)
    # filename = '/usr/local/media/file/{}'.format(the_file_name)  # 要下载的文件路径
    fp = open(filepath, 'rb')
    # print("有有有")
    response = StreamingHttpResponse(fp)
    # print("可以看也")
    # response = StreamingHttpResponse(t)
    response['Content-Type'] = 'application/octet-stream'

    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(the_file_name.encode('utf8')))
    return response

