from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

from doctor.models import Doctor
from utils.utils import DEPARTMENTS,GENDERS

# Create your models here.

# 病人模型
class Patient(models.Model):
    '''
    属性：
        user                ：病人账号
        name                ：姓名
        age                 ：年龄
        gender              ：性别
        department          ：住院科室
        doctor              ：责任医师
        medicalRecord       ：病历
        isDischarged        ：是否出院
    '''

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_account')
    name            = models.CharField(max_length=20,blank=True)
    age             = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(150)],blank=True,null=True)
    gender          = models.CharField(max_length=1,blank=True,choices=GENDERS)
    doctor          = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    department      = models.CharField(max_length=1,blank=True,choices=DEPARTMENTS)
    isDischarged    = models.BooleanField(blank=True,null=True)
    avatar          = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    def __str__(self):
        return f'userid:{self.user.username},username:{self.name}'


# 病历模型
class MedicalRecord(models.Model):
    '''
    属性：
        doctor              ：责任医师
        patient             ：病人
        department          ：科室
        description         ：病历描述
        tag                 ：基本病种分类
        prescription        ：诊断记录
    '''
    DEPARTMENTS = (
        ('A','Anaesthesiology and Adult Intensive Care Department'),
        ('C','Child Surgical Department'),
        ('G','General and Vascular Surgical Department'),
        ('D','Dermatology'),
        ('O','Obstetric and Maternity Ward'),
        ('I','Internal Department'),
        ('L','Laryngology'),
        ('N','Neurology'),
        ('F','First-Aid Department'),
    )

    doctor          = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True,blank=True)
    patient         = models.OneToOneField(Patient,on_delete=models.CASCADE,  related_name='prescription_patient')
    department      = models.CharField(max_length=1,blank=True,choices=DEPARTMENTS)
    description     = models.TextField(blank=True)
    tag             = models.CharField(max_length=40,blank=True)

    def __str__(self):
        return f'patient_name:{patient.name},doctor_name:{doctor.name},tag:{tag},description:{description}'


class Prescription(models.Model):
    '''
    属性：
        patient             ：病人
        description         ：诊断描述
        treatment           ：治疗手段
        cost                ：费用
    '''
    patient         = models.ForeignKey(Patient,on_delete=models.CASCADE,  related_name='prescribe_patient')
    description     = models.TextField(blank=True)
    treatment       = models.TextField(blank=True)
    cost            = models.FloatField(validators=[MinValueValidator(0)],blank=True,null=True)

    def __str__(self):
        return f'description:{description},treatment:{treatment},cost:{cost}'

