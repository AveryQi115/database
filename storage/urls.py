from django.urls import path
from . import views

app_name = 'storage'

urlpatterns = [
    # 仓储详情
    path('treatmentList', views.TreatmentList, name='treatmentList'),
    path('addTreatment', views.AddTreatMent, name='addTreatment'),
]