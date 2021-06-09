from django.shortcuts import render

'''
    restful api相关
'''
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PatientListSerializer
from patient.models import Patient

from utils.utils import getGender,getDepartment,getTitle
# Create your views here.

class PatientsListView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered = queryset.filter(doctor__user__username = request.user.username)
        serializer = PatientListSerializer(filtered,many=True) 
        return Response(serializer.data)


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
