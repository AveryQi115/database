from django.shortcuts import render

'''
    restful api相关
'''
from patient.models import Patient
from patient.views import user_authentication, getRecordContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utils.utils import getGender,getDepartment,getTitle,getUserGroup
# Create your views here.

def PatientsList(request):
    # 当前用户必须是医生
    group = getUserGroup(request.user.id)
    if group != "doctor":
        messages.error(request, "抱歉，您不是医生，请重新登陆")
        return redirect('userprofile/login/')
    
    # 调取当前用户全部病人
    patients = Patient.objects.filter(doctor__user__id=request.user.id)
    return render(request, 'doctor_mainPage.html',{"patient_list":patients})

@login_required(login_url='/userprofile/login')
def AddPrescription(request,id):
    # 当前用户必须是当前id的主治医生
        # 权限检查
    if not user_authentication(request, id):
        messages.error(request, "抱歉，你无权查看该病人的病历")
        return redirect('')

    context = getRecordContext(request.user.id, id)
    if request.method == 'POST':
        form = addPrescriptionForm(request.POST)
        if form.is_valid():
            #TODO
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


# def getPatientList(doctorID,offset=0,limit=-1):
#     res = Patient.objects.filter(doctor__user__username=doctorID)
#     if limit < 0:
#         return res
#     #TODO:后续分页
#     return res[offset:offset+limit]

def getDoctorInfo(d):
    return {'name':d.name,
            'age':d.age,
            'gender':getGender(d.gender),
            'department':getDepartment(d.department),
            'avatar':d.avatar,
            'title':getTitle(d.title)}
