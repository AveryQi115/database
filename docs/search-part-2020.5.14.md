## 注意事项

* 后端接口未改变
* 做了两个搜索窗口，未进行排版，前端需注意时进行合理布局，还是合并到一起
* 按回车进行搜索，未制作搜索按钮
* 搜索内容展示未进行顺序相关处理
* 搜索根据标题和内容进行

## 前端改动

* hotContent.html增加

```html
<!-- 问题搜索栏 -->
<div class="row">
    <div class="col-auto mr-auto">
        <form class="form-inline" >
            <label class="sr-only">content</label>
            <input type="text" 
                class="form-control mb-2 mr-sm-2" 
                name="search_q" 
                placeholder="搜索问题..." 
                required
            >
        </form>
    </div>
</div>

<!-- 问题搜索提示语 -->
{% if search_q %}
    {% if questions %}
        <h4><span style="color: red">"{{ search_q }}"</span>的问题搜索结果如下：</h4>
        <hr>        
    {% else %}
        <h4>暂无<span style="color: red">"{{ search_q }}"</span>有关的问题。</h4>
        <hr>
    {% endif %}
{% endif %}
```

和

```html
<!-- 文章搜索栏 -->
<div class="row">
    <div class="col-auto mr-auto">
        <form class="form-inline" >
            <label class="sr-only">content</label>
            <input type="text" 
                class="form-control mb-2 mr-sm-2" 
                name="search_a" 
                placeholder="搜索文章..." 
                required
            >
        </form>
    </div>
</div>

<!-- 文章搜索提示语 -->
{% if search_a %}
    {% if articles %}
        <h4><span style="color: red">"{{ search_a }}"</span>的文章搜索结果如下：</h4>
        <hr>        
    {% else %}
        <h4>暂无<span style="color: red">"{{ search_a }}"</span>有关的文章。</h4>
        <hr>
    {% endif %}
{% endif %}
```



## 后端改动

* 更改article.views中hot_article_list()函数`注释部分是之前代码没搞清楚用处，所以没敢删`

```python 
# 热门文章
def hot_article_list(request):
    #判断是否进行了搜索
    search = request.GET.get('search')
    #如果进行了搜索
    if search:
        articles = ArticlePost.objects.filter(
            #匹配标题(不区分大小写)
            Q(title__icontains=search) |
            #匹配文章内容(不区分大小写)
            Q(body__icontains=search)
        )
    #如果未进行搜索
    else:
        articles = ArticlePost.objects.all()
    # 增加 search 到 context
    context = {'articles': articles,'search': search}
    return render(context)
    # return render(request, 'article/list.html', context)
    # # 取出所有博客文章
    # articles = list(ArticlePost.objects.all()[:5])
    # # 将博客文章标题构成list
    # # hot_titles = [article.title for article in articles]
    # # 如果list长度不足5，则用'...'补齐
    # # hot_titles += ['...' for i in range(5 - len(articles))]
    # # 将博客文章标题构成list
    # # hot_ids = [article.id for article in articles]
    # # 如果list长度不足5，则用'...'补齐
    # # hot_ids += [0 for i in range(5 - len(articles))]
    # # 将title list传递给模板（templates）

    # # 将整个article列表传递给前端页面，没有解决可能出现的列表不足默认内容补足5个的问题
    # context = {'articles': articles}
    # # render函数：载入模板，并返回context对象
    # return context
```

- 更改question.views中hot_question_list()函数`注释部分是之前代码没搞清楚用处，所以没敢删`

```python 
# 热门问题
def hot_question_list(request):
    #判断是否进行了搜索
    search = request.GET.get('search_q')
    #如果进行了搜索
    if search:
        questions = QuestionPost.objects.filter(
            #匹配标题(不区分大小写)
            Q(title__icontains=search) |
            #匹配问题描述(不区分大小写)
            Q(description__icontains=search)
        )
    #如果未进行搜索
    else:
        questions = QuestionPost.objects.all()
    # 增加 search 到 context
    context = {'questions': questions,'search_q': search}
    return context
    取出所有问题
    # questions = list(QuestionPost.objects.all()[:5])
    # # 将问题标题构成list
    # # hot_titles = [question.title for question in questions]
    # # 如果list长度不足5，则用'...'补齐
    # # hot_titles += ['...' for i in range(5 - len(questions))]
    # # 将问题id构成list
    # # hot_ids = [question.id for question in questions]
    # # 如果list长度不足5，则用'...'补齐
    # # hot_ids += [0 for i in range(5 - len(questions))]
    # # 将title list传递给模板（templates）
    # context = {'questions': questions}
    # # render函数：载入模板，并返回context对象
    # return context
```

