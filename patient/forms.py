# 引入表单类
from django import forms
from .models import Patient

class registerPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        # 用户自行选择挂号科室和责任医师
        fields = ('name','age','gender','avatar','department','doctor')
