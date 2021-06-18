from django.shortcuts import render, redirect
from patient.models import Patient, Prescription, MedicalRecord
from patient.views import user_authentication, getRecordContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.utils import getGender,getDepartment,getTitle,getUserGroup
from .forms import addPrescriptionForm, addDescriptionForm
from storage.models import Treatment
# Create your views here.

@login_required(login_url='/userprofile/login')
def PatientsList(request):
    # 当前用户必须是医生
    group = getUserGroup(request.user.id)
    if group != "doctor":
        messages.error(request, "抱歉，您不是医生，请重新登陆")
        return redirect('userprofile/login/')
    
    # 调取当前用户全部病人
    patient_list = []
    patients = Patient.objects.filter(doctor__user__id=request.user.id,isDischarged=False)
    for patient in patients:
        mr = MedicalRecord.objects.get(patient__user__id=patient.user.id)
        patient_list.append({"patient":patient,"mr":mr})
    return render(request, 'doctor_mainPage.html',{"patient_list":patient_list})

@login_required(login_url='/userprofile/login')
def AddPrescription(request,id):
    # 当前用户必须是当前id的主治医生
    # 权限检查
    if not user_authentication(request, id):
        messages.error(request, "抱歉，你无权查看该病人的病历")
        return redirect('/')

    # 检查病人是否已出院
    patient = Patient.objects.get(user__id=id)
    if patient.isDischarged:
        messages.error(request,"当前病人已出院")
        return redirect('/')

    context = getRecordContext(request.user.id, id)
    if request.method == 'POST':
        form = addPrescriptionForm(request.POST)
        if form.is_valid():
            form_cd = form.cleaned_data
            pres = Prescription(patient=Patient.objects.get(user__id=id))
            pres.description = form_cd['description']
            pres.treatment = form_cd['treatment']
            if pres.treatment.number<=form_cd['number']:
                messages.error(request, "抱歉，当前药品库存不足")
                return redirect('/')
            pres.number = form_cd['number']
            pres.treatment.number -= pres.number
            pres.treatment.save()

            pres.cost = form_cd['cost']
            pres.save()
            return redirect("patient:medicalRecord",id=id)
        else:
            return HttpResponse("诊断表单输入有误。请重新输入~")

    elif request.method == 'GET':
        form = addPrescriptionForm()
        context = {'form':form,"id":id}
        return render(request, 'doctor/addPrescription.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

@login_required(login_url='/userprofile/login')
def AddDescription(request,id):
    # 当前用户必须是当前id的主治医生
    if not user_authentication(request, id):
        messages.error(request, "抱歉，你无权查看该病人的病历")
        return redirect('/')

    # 检查病人是否已出院
    patient = Patient.objects.get(user__id=id)
    if patient.isDischarged:
        messages.error(request,"当前病人已出院")
        return redirect('/')

    context = getRecordContext(request.user.id, id)
    if request.method == 'POST':
        form = addDescriptionForm(request.POST)
        if form.is_valid():
            form_cd = form.cleaned_data
            des = MedicalRecord.objects.get(patient__user__id=id)
            des.description = form_cd['description']
            des.tag = form_cd['tag']
            des.save()
            return redirect("patient:medicalRecord",id=id)
        else:
            return HttpResponse("病历表单输入有误。请重新输入~")

    elif request.method == 'GET':
        form = addDescriptionForm()
        context = {'form':form,"id":id}
        return render(request, 'doctor/addDescription.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

def getDoctorInfo(d):
    return {'name':d.name,
            'age':d.age,
            'gender':getGender(d.gender),
            'department':getDepartment(d.department),
            'avatar':d.avatar,
            'title':getTitle(d.title)}


