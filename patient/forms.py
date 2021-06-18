# 引入表单类
from django import forms
from .models import Patient
from django_select2 import forms as s2forms


class DoctorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
        "department__icontains",
    ]

class registerPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        # 用户自行选择挂号科室和责任医师
        fields = ('name','age','gender','avatar','department','doctor')
        widgets = {
            "doctor": DoctorWidget,
        }

