from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    # 病人列表
    path('patientList', views.PatientsList, name='patientList'),
    path('add_prescription/<int:id>', views.AddPrescription, name='add_prescription'),
]