from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    # 病历详情
    path('medicalRecord/<int:id>/', views.medicalRecord, name='medicalRecord'),
    # 挂号
    path('registerPatient/', views.registerPatient, name='registerPatient'),
]