## 注意事项

* 增加用户封禁后，意味着增加了权限管理，权限的赋予在注册用户函数，所以除了管理员用户外，以前注册的用户没有任何权限。
* 如今后有功能涉及到用户权限，需要①在model中添加相应权限，进行数据迁移；②在功能函数中加入权限判断；③在注册函数中赋予权限部分加入相关权限
* 用户权限目前涉及到的功能：发布文章、更新文章、下载文章板块附件、下载问题板块附件、发布问题、更新问题、发布评论、发布回答、点赞、收藏
* 点赞、收藏按钮在封禁后将失效，因为该函数返回的不是一个链接，所以提示语在控制台；如需出现提示，需要相关后端同学进行更改
* 只有管理员（超级用户可以进行用户封禁），其余用户点击封禁按钮会提示没有权利
* 发现上传文件会出现错误，应该是一个后端相关板块出现的bug
* 发现删除回答会跳出404页面

## 前端改动（接口）

search_user.html加入封禁按钮，具体按钮在哪个页面，如何优化还要靠前端同学

```html
...
<a  href="{% url 'userprofile:user_forbidden' user.id %}" class="btn btn-primary">封禁用户</a>
...
```

## 后端改动

* 所有被更改文件引入

```python
#引入权限检查模块
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
```

* userprofile.views中user_register()函数增加代码：

```python 
...
            # 赋予新用户权限
            p1 = Permission.objects.get(codename = 'add_articlepost')
            p2 = Permission.objects.get(codename = 'change_articlepost')
            p3 = Permission.objects.get(codename = 'view_articlepost')
            p4 = Permission.objects.get(codename = 'add_questionpost')
            p5 = Permission.objects.get(codename = 'change_questionpost')
            p6 = Permission.objects.get(codename = 'view_questionpost')
            p7 = Permission.objects.get(codename = 'add_comment')
            p8 = Permission.objects.get(codename = 'change_comment')
            # 由于有重复字段，所以不能靠codename查询，用序号代替，所以如果新作数据迁移可能需要改这个地方
            # p9 = Permission.objects.get(codename = 'add_answer')
            p9 = Permission.objects.get(id = 41)
            # p10 = Permission.objects.get(codename = 'change_answer')
            p10 = Permission.objects.get(id = 42)
            p11 = Permission.objects.get(codename = 'change_collectcount')
            p12 = Permission.objects.get(codename = 'change_likecount')            
            new_user.user_permissions.set([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12])
...
```

- userprofile.views中增加函数user_forbidden()（相关url配置不再详述）：

```python 
# 用户封禁
def user_forbidden(request, id):
    nowuser = User.objects.get(id=request.user.id)
    if not nowuser.has_perm('userprofile.user_change'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
    # 取出对象用户
    myuser = User.objects.get(id=id)
    # 赋予新用户权限
    p1 = Permission.objects.get(codename = 'add_articlepost')
    p2 = Permission.objects.get(codename = 'change_articlepost')
    p3 = Permission.objects.get(codename = 'view_articlepost')
    p4 = Permission.objects.get(codename = 'add_questionpost')
    p5 = Permission.objects.get(codename = 'change_questionpost')
    p6 = Permission.objects.get(codename = 'view_questionpost')
    p7 = Permission.objects.get(codename = 'add_comment')
    p8 = Permission.objects.get(codename = 'change_comment')
    # 由于有重复字段，所以不能靠codename查询，用序号代替，所以如果新作数据迁移可能需要改这个地方
    # p9 = Permission.objects.get(codename = 'add_answer')
    p9 = Permission.objects.get(id = 41)
    # p10 = Permission.objects.get(codename = 'change_answer')
    p10 = Permission.objects.get(id = 42)
    p11 = Permission.objects.get(codename = 'change_collectcount')
    p12 = Permission.objects.get(codename = 'change_likecount')            
    myuser.user_permissions.remove(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12)
    return redirect("/")
```

* article.views中函数article_create(request)增加代码：

```python
...
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.add_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
...
```

* article.views中函数article_update(request, id)增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.change_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- article.views中函数download_file(request,id)增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('article.view_articlepost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- question.views中函数question_create(request)增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('question.add_questionpost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- question.views中函数question_update(request, id)增加代码：

```python
 # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('question.change_questionpost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- question.views中函数download_file(request,id)增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('question.view_questionpost'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- comment.views中函数post_comment()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('comment.add_comment'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- comment.views中函数update_comment()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('comment.change_comment'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- answer.views中函数answer_create()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('answer.add_answer'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- answer.views中函数answer_update()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('answer.change_answer'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- collect.views中函数collect_change()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('collect.change_collectcount'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

- like.views中函数like_change()增加代码：

```python
    # 判断该用户是否有相关权限
    myuser = User.objects.get(id=request.user.id)
    if not myuser.has_perm('like.change_likecount'):
        return HttpResponse('抱歉，您的相关权限已被管理员封禁；如有疑问，请联系管理员！！！')
```

