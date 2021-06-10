from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator

from utils.utils import DEPARTMENTS,GENDERS,TITLES


# Create your models here.
# 医生模型
class Doctor(models.Model):
    '''
    属性：
        user                ：医生账号
        name                ：姓名
        age                 ：年龄
        gender              ：性别
        department          ：值班科室
        title               ：职称
    '''

    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_account')
    name            = models.CharField(max_length=20,blank=True)
    age             = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(150)],blank=True,null=True)
    gender          = models.CharField(max_length=1,blank=True,choices=GENDERS)
    department      = models.CharField(max_length=1,blank=True,choices=DEPARTMENTS)
    title           = models.CharField(max_length=2,blank=True,choices=TITLES)
    avatar          = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    def __str__(self):
        return f'doctor_name:{self.name},department:{self.department}'
