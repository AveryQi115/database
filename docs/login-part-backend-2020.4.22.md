## 后端接口

- 已完成登入、登出、注册、删除

- 使用内置数据库，未结合mysql

- 登入url

  ```python
  href="{% url 'userprofile:login' %}"
  ```

- 登出url

  ```python
  href='{% url "userprofile:logout" %}'
  ```

- 注册url

  ```python
  href='{% url "userprofile:register" %}'
  ```

- 删除url

  ```python
  href='{% url "userprofile:delete" user.id %}'
  ```

- 安全删除url

  ```python
  href='{% url "userprofile:safe_delete" user.id %}'
  ```

- 传入Form：UserLoginForm

  | 接口名称 | 接口形容         |
  | -------- | ---------------- |
  | username | 登录输入的用户名 |
  | password | 登录输入的密码   |

- 传入Form：UserRegisterForm

  | 接口名称  | 接口形容       |
  | --------- | -------------- |
  | username  | 注册输入用户名 |
  | email     | 注册输入邮箱   |
  | password  | 注册输入密码   |
  | password2 | 注册确认密码   |

## 前端改动

- 增加

```txt
register.html -- 使用网站模板
```

- 更改header.html中

  ```html
  <a class="btn text-light" href="https://www.runoob.com/html/html-links.html">{用户名}</a>
  ```

  为：

  ```html
  {% if user.is_authenticated %}
      <!-- 如果用户已经登录，则显示用户名下拉框 -->
      <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            {{ user.username }}
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href='{% url "userprofile:logout" %}'>退出登录</a>
            <a class="dropdown-item" href='{% url "userprofile:delete" user.id %}'>删除用户</a>
          </div>
      </li>
  <!-- 如果用户未登录，则显示 “登录” -->
  {% else %}
      <li class="nav-item">
          <a class="nav-link" href="{% url 'userprofile:login' %}">登录</a>
      </li>                    
  <!-- if 语句在这里结束 -->
  {% endif %}
  ```


- 增加login.html

```html
<!-- 注册 -->
<div class="col-12">
    <br>
    <h5>点击<a href='{% url "userprofile:register" %}'>注册</a></h5>
    <br>
</div>
```

- 希望前端可以针对删除用户做一个弹窗，同时已写相应的安全删除链接

  ```python
  href='{% url "userprofile:delete" user.id %}'
  ```



## 后端注意事项

- profile的视图所有关于主页面的返回，全部用了**article.view**中的**hot_article_list**函数在总体url配置中的命名：**“hot_article_list”**
- 新增管理员：**userprofile**，密码：**aaa**