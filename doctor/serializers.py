from rest_framework import serializers
from patient.models import Patient

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'