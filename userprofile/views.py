from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group

from doctor.models import Doctor
from patient.models import Patient
from .forms import UserLoginForm , UserRegisterForm, PatientForm, DoctorForm, UserPasswordForm

# 引入分页模块
from django.core.paginator import Paginator
# 引入权限检查模块
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from utils.utils import getUserGroup
from doctor.views import getDoctorInfo
from patient.views import getPatientInfo


def search_user(request):
    # 判断是否进行了搜索
    search = request.GET.get('search')
    # 如果进行了搜索
    if search:
        users = User.objects.filter(
            # 匹配用户名(不区分大小写)
            Q(username__icontains=search)
        )
        context = {'users': users, 'search_u': search}
    # 如果未进行搜索
    else:
        context = {'users': [], 'search_u': search}
    return render(request, 'search/search_user.html', context)

def user_login(request):
    # 用户进行数据POST
    if request.method == 'POST':
        # 得到用户的数据
        user_login_form = UserLoginForm(data=request.POST)
        # 判断数据是否有效
        if user_login_form.is_valid():
            # 清洗出合法数据
            data = user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                # 返回主页链接
                return redirect("/")
            else:
                # 创建用户表单类
                user_login_form = UserLoginForm()
                # 赋予上下文
                context = {'form': user_login_form}
                messages.success(request, "账号或密码输入不合法")
                return render(request, 'userprofile/login.html', context)
        else:
            # 创建用户表单类
            user_login_form = UserLoginForm()
            # 赋予上下文
            context = {'form': user_login_form}
            messages.success(request, "账号或密码输入不合法")
            return render(request, 'userprofile/login.html', context)
    # 用户获取视图
    elif request.method == 'GET':
        # 创建用户表单类
        user_login_form = UserLoginForm()
        # 赋予上下文
        context = { 'form': user_login_form }
        # 返回呈现给登录页面
        return render(request, 'userprofile/login.html', context)
    # 危险情况
    else:
        # 创建用户表单类
        user_login_form = UserLoginForm()
        # 赋予上下文
        context = {'form': user_login_form}
        messages.success(request, "请使用GET或POST请求数据")
        return render(request, 'userprofile/login.html', context)

def user_logout(request):
    # 用户登出
    logout(request)
    # 返回首页
    return redirect("/")

def user_register(request):
    # 用户进行数据POST
    if request.method == 'POST':
        # 得到注册表单数据
        user_register_form = UserRegisterForm(data=request.POST)
        # 检测数据是否有效
        if user_register_form.is_valid():
            # 保存表单到暂存区
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            # 保存用户名密码到数据库
            new_user.save()
            # 保存好数据后立即登录
            login(request, new_user)
            # 新用户分组（只能设置为病人）
            patients = Group.objects.get(name='patient') 
            patients.user_set.add(new_user)
            # 返回主界面
            return redirect("/")
        else:
            # 获取注册表格初始化
            user_register_form = UserRegisterForm()
            # 联系上下文
            context = {'form': user_register_form}
            messages.success(request, "注册表单有误，请重新输入~")
            # 传输到模板呈现给用户
            return render(request, 'userprofile/register.html', context)
    # 用户进行表格页面请求
    elif request.method == 'GET':
        # 获取注册表格初始化
        user_register_form = UserRegisterForm()
        # 联系上下文
        context = { 'form': user_register_form }
        # 传输到模板呈现给用户
        return render(request, 'userprofile/register.html', context)
    else:
        # 获取注册表格初始化
        user_register_form = UserRegisterForm()
        # 联系上下文
        context = {'form': user_register_form}
        messages.success(request, "请使用GET或POST请求数据")
        # 传输到模板呈现给用户
        return render(request, 'userprofile/register.html', context)

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    # 得到用户id
    user = User.objects.get(id=id)
    # 验证登录用户、待删除用户是否相同
    if request.user == user:
        # 退出登录
        logout(request)
        # 删除数据
        user.delete()
        # 返回主界面
        return redirect("/")
    else:
        return HttpResponse("你没有删除操作的权限。")


@login_required(login_url='/userprofile/login/')
def profile(request, id):
    group = getUserGroup(id)
    user = User.objects.get(id=id)

    # 医生用户
    if group == 'doctor':
        if Doctor.objects.filter(user__id=id).exists():
            profile = Doctor.objects.get(user__id = id)
        else:
            profile = Doctor.objects.create(user=user)

        context = getDoctorInfo(profile)
        context['user'] = user
        return render(request,'userprofile/doctorDetail.html',context)

    # 普通用户/病人
    if Patient.objects.filter(user__id=id).exists():
        profile = Patient.objects.get(user__id = id)
    else:
        profile = Patient.objects.create(user=user)

    context = getPatientInfo(profile)
    context['user'] = user
    return render(request, 'userprofile/patientDetail.html',context)


@login_required(login_url='/userprofile/login/')
def profile_update(request, id):
    user = User.objects.get(id=id)
    group = getUserGroup(id)

    if group == 'doctor':
        return profile_update_doctor(request,id)
    
    return profile_update_patient(request,id)

def profile_update_doctor(request, id):
    user = User.objects.get(id = id)
    if Doctor.objects.filter(user__id=id).exists():
        profile = Doctor.objects.get(user__id=id)
    else:
        profile = Doctor.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = DoctorForm(request.POST,request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.age = profile_cd['age']
            profile.gender = profile_cd['gender']
            profile.name = profile_cd['name']
            if 'avatar' in request.FILES:
                profile.avatar=profile_cd['avatar']
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:profile", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = DoctorForm(initial={"name":profile.name,"age":profile.age,"gender":profile.gender,"avatar":profile.avatar})
        context = {'profile_form': profile_form, 'user': user}
        return render(request, 'userprofile/profile.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

def profile_update_patient(request, id):
    user = User.objects.get(id = id)
    if Patient.objects.filter(user__id=id).exists():
        profile = Patient.objects.get(user__id=id)
    else:
        profile = Patient.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        profile_form = PatientForm(request.POST,request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.age = profile_cd['age']
            profile.gender = profile_cd['gender']
            profile.name = profile_cd['name']
            if 'avatar' in request.FILES:
                profile.avatar=profile_cd['avatar']
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:profile", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = PatientForm(initial={"name":profile.name,"age":profile.age,"gender":profile.gender,"avatar":profile.avatar})
        context = {'profile_form': profile_form, 'user': user}
        return render(request, 'userprofile/profile.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

@login_required(login_url='/userprofile/login/')
def password_update(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user_password_form = UserPasswordForm(request.POST)

        if user_password_form.is_valid():
            old_password = user_password_form.cleaned_data['old_password']
            new_password = user_password_form.cleaned_data['new_password']
            new_password2 = user_password_form.cleaned_data['new_password2']

            if not check_password(old_password, user.password):
                messages.error(request, "原始密码输入错误！")
                return render(request, 'userprofile/setting.html', {'user_password_form': user_password_form})

            if new_password != new_password2:
                messages.error(request, "两次新密码输入不同！")
                return render(request, 'userprofile/setting.html', {'user_password_form': user_password_form})

            user.set_password(new_password)
            user.save()
            logout(request)

            messages.success(request, "修改密码成功！")
            return redirect("/")
    else:
        user_password_form = UserPasswordForm()
        return render(request, 'userprofile/setting.html', {'user_password_form': user_password_form})

def get_profile(request):
    if(request.user.is_authenticated):
        group = getUserGroup(request.user.id)
        if group == 'doctor':
            if Patient.objects.filter(user__id=request.user.id).exists():
                profile = Patient.objects.get(user__id=request.user.id)
            else:
                profile = Patient.objects.create(user=request.user)
        else:
            if Patient.objects.filter(user__id=request.user.id).exists():
                profile = Patient.objects.get(user__id=request.user.id)
            else:
                profile = Patient.objects.create(user=request.user)

        context = {'globle_profile': profile}
        return  context
    return {'request1': request}

