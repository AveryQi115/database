from django.urls import path
from . views import PatientsListView

app_name = 'doctor'

urlpatterns = [
    # 病人列表
    path('patientList', PatientsListView.as_view(), name='patientList'),
]