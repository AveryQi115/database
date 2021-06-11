# 引入表单类
from django import forms
from patient.models import Prescription, MedicalRecord

class addPrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('description','treatment','cost')

class addDescriptionForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('description','tag')