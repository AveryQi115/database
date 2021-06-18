from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utils.utils import getUserGroup, getDepartment, getDoctorName, getGender, getTitle
from .models import Patient, MedicalRecord, Prescription, Bill
from doctor.models import Doctor
from .forms import registerPatientForm

from notifications.signals import notify


@login_required(login_url='/userprofile/login')
def medicalRecord(request, id):
    # 权限检查
    token, group = user_authentication(request, id)
    if not token:
        messages.error(request, "抱歉，你无权查看该病人的病历")
        return redirect('/')

    context = getRecordContext(request.user.id, id)
    context['group'] = group
    # print(context)
    return render(request, 'patient/medicalRecord.html',context)
    
@login_required(login_url='/userprofile/login')
def registerPatient(request):
    if request.method == 'POST':
        form = registerPatientForm(request.POST,request.FILES)
        if form.is_valid():
            form_cd = form.cleaned_data
            if form_cd['doctor'].department != form_cd['department']:
                messages.error(request, "当前选择医生与挂号科室不符！")
                return render(request, 'patient/registerPatient.html', {'form':form})

            patient = Patient.objects.get(user__id=request.user.id)
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

@login_required(login_url='/userprofile/login')
def applyCheckOut(request):
    if getUserGroup(request.user.id)!='patient':
        messages.error(request, '您无权进行此操作')
        return redirect('/')

    if Patient.objects.filter(user__id=request.user.id).exists():
        patient = Patient.objects.get(user__id=request.user.id)
        # 发送通知
        notify.send(
                    patient,
                    recipient=patient.doctor.user,
                    verb='申请出院',
                    target=request.user,
                )


        patient.isDischarged = True
        patient.save()

        messages.info(request,'已通知主治医生')
        return redirect('/')

    messages.error(request,'当前病人档案不存在')
    return redirect('/')

@login_required(login_url='/userprofile/login')
def payBill(request):
    if getUserGroup(request.user.id)!='patient':
        messages.error(request, '您无权进行此操作')
        return redirect('/')
    
    # 拉取当前病人所有诊断记录
    total_cost = 0
    prescriptionLists = None
    if Prescription.objects.filter(patient__user__id=request.user.id).exists():
        prescriptionLists = Prescription.objects.filter(patient__user__id=request.user.id)
        for pres in prescriptionLists:
            if pres.cost:
                total_cost += pres.cost
            if pres.treatment and pres.treatment.cost and pres.number:
                total_cost += pres.treatment.cost * pres.number

    paid = 0
    if Bill.objects.filter(patient__user__id=request.user.id).exists():
        paid = Bill.objects.get(patient__user__id=request.user.id).paid

    remain = total_cost - paid
    return render(request,'patient/payBill.html',{'prescriptionList':prescriptionLists,'total_cost':total_cost,'paid':paid,'remain':remain})        

@login_required(login_url='/userprofile/login')
def paid(request, paid):
    try:
        paid = float(paid)
        if paid<0:
            messages.error(request, '付款信息错误')
            return redirect('/') 
    except Exception as e:
        print(e)
        messages.error(request, '付款信息错误')
        return redirect('/')

    if getUserGroup(request.user.id)!='patient':
        messages.error(request, '您无权进行此操作')
        return redirect('/')

    if Bill.objects.filter(patient__user__id=request.user.id).exists():
        bill = Bill.objects.get(patient__user__id=request.user.id)
        bill.paid = paid
        bill.save()

    else:
        bill = Bill(patient=Patient.objects.get(user__id=request.user.id), paid=paid)
        bill.save()

    messages.success(request, '付款成功')
    return redirect('/')




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
            return (False,'patient')
        return (True,'patient')

    else:
        # 检查当前id是否是病人且该医生是否是病人的责任医师
        if not Patient.objects.filter(user__id=id).exists():
            return (False,'doctor')

        patient = Patient.objects.get(user__id=id)
        if patient.doctor.user.id != request.user.id:
            return (False,'doctor')
        return (True,'doctor')

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
    # 获取病人信息
    if Patient.objects.filter(user__id=patientId).exists():
        patient = Patient.objects.get(user__id=patientId)
    else:
        patient = Patient.objects.create(user=request.user)

    # 获取MRI信息
    if MedicalRecord.objects.filter(patient__user__id=patientId).exists():
        medicalRecord = MedicalRecord.objects.get(patient__user__id=patientId)
    else:
        medicalRecord = MedicalRecord.objects.create(patient=patient)

    group = getUserGroup(doctorId)
    if group == 'doctor':
        # 检查病历信息中的医生一栏是否为空
        update_medicalRecord(medicalRecord, doctorId)

    # 获取所有病人相关的诊断信息
    if Prescription.objects.filter(patient__user__id=patientId).exists():
        prescriptionLists = Prescription.objects.filter(patient__user__id=patientId)
        context = {**getPatientInfo(patient),**getMRInfo(medicalRecord),"prescriptionList":prescriptionLists}
        return context
    
    context = {**getPatientInfo(patient),**getMRInfo(medicalRecord)}
    return context

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

