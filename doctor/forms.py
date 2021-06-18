# 引入表单类
from django import forms
from patient.models import Prescription, MedicalRecord
from django_select2 import forms as s2forms

class TreatmentWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class addPrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ('description','treatment','number','cost')
        widgets = {
            "treatment": TreatmentWidget,
        }
        

class addDescriptionForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('description','tag')