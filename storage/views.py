from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.utils import getUserGroup
from .models import Treatment


# Create your views here.
@login_required(login_url='/userprofile/login')
def TreatmentList(request):
    if not operatorAuthentication(request.user.id):
        message.error("您没有权限查看此页面。")
        return redirect('')

    #TODO:split page
    treatmentList = Treatment.objects.all()
    context = {"treatmentList":treatmentList}
    return render(request,'storage/treatmentList.html',context)

@login_required(login_url='/userprofile/login')
def AddTreatment(request):
    if not operatorAuthentication(request.user.id):
        message.error("您没有权限进行此操作。")
        return redirect('')

    newTreatmentList = scraper()
    #TODO:处理新加货物和老货物数量加
    return render(request,'storage/treatmentList.html',context)

def operatorAuthentication(id):
    group = getUserGroup(id)
    return group=="operator"