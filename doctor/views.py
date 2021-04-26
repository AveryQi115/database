from django.shortcuts import render
from patient.models import Patient
from utils.utils import getGender,getDepartment,getTitle
# Create your views here.


def getPatientList(doctorID,offset=0,limit=-1):
    res = Patient.objects.filter(doctor__user__username=doctorID)
    if limit < 0:
        return res
    #TODO:后续分页
    return res[offset:offset+limit]

def getDoctorInfo(d):
    return {'name':d.name,
            'age':d.age,
            'gender':getGender(d.gender),
            'department':getDepartment(d.department),
            'avatar':d.avatar,
            'title':getTitle(d.title)}
