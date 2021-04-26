# 引入表单类
from django import forms
# 引入django自带的User数据模型
from django.contrib.auth.models import User
from doctor.models import Doctor
from patient.models import Patient


# 登录需要用到的表单
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 注册需要用到的表单
class UserRegisterForm(forms.ModelForm):
    # 复写 User 的密码
    password = forms.CharField()
    password2 = forms.CharField()

    # 定义数据，使用django的user类
    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致,请重试。")

# 修改病人信息需要用的表单
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name','age','gender','avatar')

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('name','age','gender','avatar')

# 修改用户密码需要用到的表单
class UserPasswordForm(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()
    new_password2 = forms.CharField()
