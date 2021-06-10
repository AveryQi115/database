# 引入表单类
from django import forms
from patient.models import Prescription

class addPrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('description','treatment','cost')