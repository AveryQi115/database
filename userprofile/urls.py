from django.urls import path
from . import views

app_name = 'userprofile'

urlpatterns = [
    # 用户登入
    path('login/', views.user_login, name='login'),
    # 用户退出
    path('logout/', views.user_logout, name='logout'),
    # 用户退出
    path('register/', views.user_register, name='register'),
    # 用户删除
    path('delete/<int:id>/', views.user_delete, name='delete'),
    # 用户查看信息
    path('profile/<int:id>/', views.profile, name='profile'),
    # 用户编辑信息
    path('profile-update/<int:id>/', views.profile_update, name='profile_update'),
    # 用户修改密码
    path('password-update/<int:id>/', views.password_update, name='password_update'),
]