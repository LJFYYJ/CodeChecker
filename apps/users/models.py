# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    username = models.CharField(max_length=150, verbose_name=u'用户名')
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u'找回密码')), max_length=10, verbose_name=u'验证码类型')
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u'发送时间')
    # 如果链接已被使用过，或者超出了24小时，则已失效
    has_expired = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class UploadFile(models.Model):
    username = models.CharField(max_length=150, verbose_name=u'用户名')
    upload_time = models.DateTimeField(default=datetime.now, verbose_name=u'上传时间')
    title = models.CharField(max_length=200, verbose_name=u'文件名')

    class Meta:
        verbose_name = u"上传文件信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username + '_' + self.title


class CheckInfo(models.Model):
    username = models.CharField(max_length=150, verbose_name=u'用户名')
    check_time = models.CharField(max_length=100, verbose_name=u'查重时间')

    class Meta:
        verbose_name = u"查重信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username + '_' + self.check_time


class CheckInfoFile(models.Model):
    check_id = models.IntegerField(verbose_name=u'查重编号')
    filename = models.CharField(max_length=200, verbose_name=u'查重文件名')

    class Meta:
        verbose_name = u"查重文件"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.check_id) + '_' + self.filename


class CheckResult(models.Model):
    check_id = models.IntegerField(verbose_name=u'查重编号')
    file1 = models.CharField(max_length=200, verbose_name=u'文件1名')
    file2 = models.CharField(max_length=200, verbose_name=u'文件2名')
    filename1 = models.CharField(max_length=200, verbose_name=u'文件1简单名字', default="")
    filename2 = models.CharField(max_length=200, verbose_name=u'文件2简单名字', default="")
    sim1 = models.FloatField(verbose_name=u'第一级相似度', default=0)
    sim2 = models.FloatField(verbose_name=u'第二级相似度', default=0)
    sim3 = models.FloatField(verbose_name=u'第三级相似度', default=0)

    class Meta:
        verbose_name = u"查重结果"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.check_id) + '_' + self.file1 + '_' + self.file2


