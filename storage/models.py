from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.
# 药品模型
class Treatment(models.Model):
    '''
    属性：
        name                ：名称
        cost                ：单价
        number              ：数量
    '''
    name            = models.CharField(max_length=50,primary_key=True)
    cost            = models.FloatField(validators=[MinValueValidator(0)],blank=True,null=True)
    number          = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10000)],default=0)

    def __str__(self):
        return f'treatment_name:{self.name}'
