from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    # 病历详情
    path('medicalRecord/<int:id>/', views.medicalRecord, name='medicalRecord'),
    # 挂号
    path('registerPatient/', views.registerPatient, name='registerPatient'),
    # 账单结算
    path('payBill/', views.payBill, name='payBill'),
    # 申请出院
    path('applyCheckOut/', views.applyCheckOut, name='applyCheckOut'),
    # 结算成功
    path('paid/<str:paid>', views.paid, name="paid"),
]