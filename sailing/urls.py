"""sailing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import path, include
from django.shortcuts import render, redirect
from django.conf import settings
from django.conf.urls.static import static

from utils.utils import getUserGroup
from patient.models import Patient

def mainPage(request):
    try:
        group = getUserGroup(request.user.id)
    except:
        group = 'patient'

    if group == 'doctor':
        return redirect('doctor:patientList')
    else:
        try:
            # 已有住院记录返回病历详情
            if Patient.objects.filter(user__id=request.user.id).exists():
                return redirect('patient:medicalRecord',id=request.user.id)
            # 无住院记录返回挂号页面
            else:
                return redirect('patient:registerPatient')
        # 未登录
        except Exception as e:
            print(e)
            return redirect('userprofile/login/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainPage, name='mainPage'),

    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    path('patient/', include('patient.urls', namespace='patient')),
    path('doctor/', include('doctor.urls', namespace='doctor')),

    # path('article/', include('article.urls', namespace='article')),
    # path('comment/', include('comment.urls', namespace='comment')),
    # path('collect/', include('collect.urls', namespace='collect')),
    
    # path('search_user/', user_views.search_user),
    
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # path('notice/', include('notice.urls', namespace='notice')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)