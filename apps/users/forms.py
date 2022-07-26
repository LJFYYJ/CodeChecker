# _*_ coding:utf-8 _*_
from django import forms
from captcha.fields import CaptchaField
# 对用户提交的表单进行处理


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8)
    repassword = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetForm(forms.Form):
    password = forms.CharField(required=True)
    repassword = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})
