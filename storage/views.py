from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.utils import getUserGroup
from .models import Treatment
from utils.utils import scraper


# Create your views here.
@login_required(login_url='/userprofile/login')
def TreatmentList(request):
    if not operatorAuthentication(request.user.id):
        messages.error(request, "您没有权限查看此页面。")
        return redirect('/')

    #TODO:split page
    treatmentList = Treatment.objects.all()
    context = {"treatmentList":treatmentList}
    return render(request,'storage/treatmentList.html',context)

@login_required(login_url='/userprofile/login')
def AddTreatment(request):
    if not operatorAuthentication(request.user.id):
        messages.error(request, "您没有权限进行此操作。")
        return redirect('/')

    newTreatmentList = scraper()
    if not len(newTreatmentList['names']):
        messages.error(request, "进货渠道发生故障，请稍后再试。")
        return redirect('/')
    
    try:
        for i in range(len(newTreatmentList["names"])):
            if Treatment.objects.filter(name=newTreatmentList["names"][i]).exists():
                tr = Treatment.objects.get(name=newTreatmentList["names"][i])
                tr.cost = newTreatmentList["costs"][i]
                tr.number = min(tr.number+100,10000)
                tr.save()
            else:
                tr = Treatment(name=newTreatmentList["names"][i], cost=newTreatmentList["costs"][i], number=200)
                tr.save()
    except Exception as e:
        print(e)
        messages.error(request, "写入仓库发生故障，请稍后再试。")
        return redirect('/')

    return redirect('storage:treatmentList')

def operatorAuthentication(id):
    group = getUserGroup(id)
    return group=="operator"