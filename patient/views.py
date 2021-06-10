from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utils.utils import getUserGroup, getDepartment, getDoctorName, getGender, getTitle
from .models import Patient, MedicalRecord
from doctor.models import Doctor
from .forms import registerPatientForm

'''
    restful api相关
'''
from rest_framework.response import Response
from rest_framework import generics
from patient.models import Patient

@login_required(login_url='/userprofile/login')
def medicalRecord(request, id):
    # 权限检查
    if not user_authentication(request, id):
        messages.error(request, "抱歉，你无权查看该病人的病历")
        return redirect('')

    context = getRecordContext(request.user.id, id)
    # print(context)
    return render(request, 'patient/medicalRecord.html',context)
    
def update_medicalRecord(medicalRecord,doctorID):
    doctor = Doctor.objects.get(user__id=doctorID)
    if not medicalRecord.doctor:
        medicalRecord.doctor = doctor
        medicalRecord.save()

# 检查对当前id相关信息进行查询的用户是否有权限
def user_authentication(request, id):
    # 查询当前用户
    cur_user = User.objects.get(id=request.user.id)
    group = getUserGroup(request.user.id)
    
    if group == 'patient':
        # 检查查看病历的是否是本人
        if id != request.user.id:
            return False
        return True

    else:
        # 检查该医生是否是病人的责任医师
        patient = Patient.objects.get(user__id=id)
        if patient.doctor.user.id != request.user.id:
            return False
        return True

def getPatientInfo(p):
    return {'name':p.name,
            'age':p.age,
            'gender':getGender(p.gender),
            'department':getDepartment(p.department),
            'avatar':p.avatar,
            'doctor':getDoctorName(p.doctor)}

def getMRInfo(m):
    return {'tag':m.tag,
            'description':m.description
        }

def getRecordContext(doctorId,patientId):
    # 第一次登陆的user其实没有关联的病人账号
    if Patient.objects.filter(user__id=patientId).exists():
        patient = Patient.objects.get(user__patient=patientId)
    else:
        patient = Patient.objects.create(user=request.user)

    if MedicalRecord.objects.filter(patient__user__id=patientId).exists():
        medicalRecord = MedicalRecord.objects.get(patient__user__id=patientId)
    else:
        medicalRecord = MedicalRecord.objects.create(patient=patient)

    group = getUserGroup(doctorId)
    if group == 'doctor':
        # 检查病历信息中的医生一栏是否为空
        update_medicalRecord(medicalRecord, doctorId)

    if Prescription.objects.filter(patient__user__id=patientId).exists():
        prescriptionLists = Prescription.objects.filter(patient__user__id=patientId)
        context = {**getPatientInfo(patient),**getMRInfo(medicalRecord),"prescriptionLists":prescriptionLists}
        return context
    
    context = {**getPatientInfo(patient),**getMRInfo(medicalRecord)}
    return context

@login_required(login_url='/userprofile/login')
def registerPatient(request):
    if request.method == 'POST':
        form = registerPatientForm(request.POST,request.FILES)
        if form.is_valid():
            form_cd = form.cleaned_data
            if form_cd['doctor'].department != form_cd['department']:
                messages.error(request, "当前选择医生与挂号科室不符！")
                return render(request, 'patient/registerPatient.html', {'form':form})

            patient = Patient.objects.get(user__id=doctorId)
            patient.name = form_cd['name']
            patient.age = form_cd['age']
            patient.gender = form_cd['gender']
            patient.department = form_cd['department']
            patient.doctor = form_cd['doctor']
            if 'avatar' in request.FILES:
                patient.avatar = form_cd['avatar']
            patient.save()

            return redirect("patient:medicalRecord",id=request.user.id)
        else:
            return HttpResponse("挂号表单输入有误。请重新输入~")

    elif request.method == 'GET':
        # 检查：不能重复挂号
        if Patient.objects.filter(user__id=request.user.id).exists():
            return redirect("patient:medicalRecord",id = request.user.id)

        form = registerPatientForm()
        context = {'form':form}
        return render(request, 'patient/registerPatient.html',context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

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

