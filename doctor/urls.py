from django.urls import path
from . import views

app_name = 'doctor'

urlpatterns = [
    # 病人列表
    path('patientList', views.PatientsList, name='patientList'),
    path('addPrescription/<int:id>', views.AddPrescription, name='addPrescription'),
    path('addDescription/<int:id>', views.AddDescription, name='addDescription'),
]