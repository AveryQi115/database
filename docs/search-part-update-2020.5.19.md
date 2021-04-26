## 注意事项

* 直接搜索已经完成
* 板块内搜索已经做出相应的接口

```python
...
def search_in_column(request):
    c_questions = question_views.search_question_in_column(request)
    c_articles = article_views.search_article_in_column(request)
    context = {**c_questions, **c_articles}
    return render(request, '待添加', context)
...
    path('待添加', search_in_column, name='search_in_column'),
...
```



## 后端改动

* article.views增加函数search_article_in_column（）和 search_article()

```python
#栏目内搜索问题
def search_question_in_column(request):
    # 判断是否进行了搜索
    search = request.GET.get('search')
    column = request.GET.get('column')
    #先将栏目内问题过滤出来
    if column is not None and column.isdigit():
        questions = QuestionPost.objects.filter(column=column)
    else:
        questions = QuestionPost.objects.all()
    # 如果进行了搜索
    if search:
        questions = questions.filter(
            # 匹配标题(不区分大小写)
            Q(title__icontains=search) |
            # 匹配问题描述(不区分大小写)
            Q(description__icontains=search)
        ).order_by('-updated')
    #返回上下文
    context = {'questions': questions,'search_q': search,'column_q':column}
    return context

#搜索问题
def search_question(request):
    # 判断是否进行了搜索
    search = request.GET.get('search')
    # 如果进行了搜索
    if search:
        questions = QuestionPost.objects.filter(
            # 匹配标题(不区分大小写)
            Q(title__icontains=search) |
            # 匹配问题描述(不区分大小写)
            Q(description__icontains=search)
        ).order_by('-updated')
        context = {'questions': questions,'search_q': search}
    # 如果未进行搜索
    else:
        context = {'questions': [],'search_q': search}
    return render(request, 'search/search_question.html', context)
```

* quesiton.views增加函数search_question_in_column（）和 search_question()

```python
#栏目内搜索文章
def search_article_in_column(request):
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
        context = {'articles': [],'search_a': search}
    return render(request, 'search/search_article.html', context)
```



