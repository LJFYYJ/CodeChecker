# _*_ coding:utf-8 _*_
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import FileResponse, HttpResponse
import datetime
import os
import zipfile
import shutil

from .models import User, EmailVerifyRecord, UploadFile, CheckInfo, CheckResult, CheckInfoFile
from .forms import LoginForm, RegisterForm, ForgetForm, ResetForm
from .checkcode import CheckCode, CheckDownload
from django.utils.encoding import escape_uri_path
from utils.email_send import send_register_email
from django.conf import settings


# 增加新的登录方式
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # get方法只获取一个值
            # 邮箱和用户名都可以登录
            user = User.objects.get(Q(username=username)|Q(email=username))
            # 对user进行验证
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm({'email': '', 'password': '', 'username': '', 'repassword': ''})
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            if User.objects.filter(username=username):
                return render(request, 'register.html', {'register_form': register_form, 'msg': u'错误：该用户名已存在'})
            user = User()
            user.username = username
            user.email = email
            user.is_active = False
            user.password = make_password(password)
            user.save()
            send_register_email(username, email, 'register')
            return render(request, 'register_success.html', {'username': username})
        else:
            print(1)
            return render(request, 'register.html', {'register_form': register_form, 'msg': u'错误：表单填写不规范'})


class LoginView(View):
    # 能够自动调用get或post方法
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # post里的内容即为字典，用form对齐验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'main.html')
                else:
                    return render(request, 'login.html', {'msg': u'错误：用户未激活'})
            else:
                return render(request, 'login.html', {'msg': u'错误：用户名或密码错误'})
        else:
            return render(request, 'login.html', {'msg': u'错误：表单填写不完整或密码长度过小'})


class ActiveUserView(View):
    def get(self, request, active_code, username):
        record = EmailVerifyRecord.objects.get(code=active_code, username=username)
        # 此处修改链接过期时间
        if datetime.datetime.now() > datetime.timedelta(minutes=120) + record.send_time:
            record.has_expired = True
            record.save()
        if not record.has_expired:
            email = record.email
            username = record.username
            user = User.objects.get(email=email, username=username)
            user.is_active = True
            user.save()
            record.has_expired = True
            record.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'active_access.html', {'username': username})


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm({'email': '', 'username': ''})
        return render(request, 'forget.html', {'forget_form': forget_form})

    def post(self, request):
        forget_from = ForgetForm(request.POST)
        if forget_from.is_valid():
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            if not User.objects.filter(username=username, email=email):
                msg = u'错误：输入的用户名或邮箱错误'
                return render(request, 'forget.html', {'msg': msg, 'forget_form': forget_from})
            send_register_email(username, email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forget.html', {'forget_form': forget_from, 'msg': u'错误：表单填写不完整'})


class ResetView(View):
    def get(self, request, active_code, username):
        reset_form = ResetForm({'password': '', 'repassword': ''})
        record = EmailVerifyRecord.objects.get(code=active_code, username=username)
        # 此处修改链接过期时间
        if datetime.datetime.now() > datetime.timedelta(minutes=120) + record.send_time:
            record.has_expired = True
            record.save()
        if not record.has_expired:
            email = record.email
            username = record.username
            record.has_expired = True
            record.save()
            return render(request, 'reset.html', {'email': email, 'username': username, 'reset_form': reset_form, 'active_code':active_code})
        else:
            return render(request, 'active_fail.html')


class ModifyView(View):
    def post(self, request):
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            password = request.POST.get('password', '')
            repassword = request.POST.get('repassword', '')
            email = request.POST.get('email', '')
            username = request.POST.get('username', '')
            if password != repassword:
                return render(request, 'reset.html', {'email': email, 'username': username, 'msg': '错误：密码输入不一致', 'reset_form': reset_form})
            user = User.objects.get(email=email, username=username)
            user.password = make_password(password)
            user.save()
            return render(request, 'reset_success.html', {'username': username})
        else:
            email = request.POST.get('email', '')
            username = request.POST.get('username', '')
            return render(request, 'reset.html', {'email': email, 'username': username, 'reset_form': reset_form, 'msg': '错误：表单填写不完整'})


class UploadFileView(View):
    def get(self, request):
        uploaded_files = UploadFile.objects.filter(username=request.user.username)
        check_info = CheckInfo.objects.filter(username=request.user.username).order_by('-id')
        return render(request, 'upload.html', {'uploaded_files': uploaded_files, 'check_info': check_info})

    def post(self, request):
        check_info = CheckInfo.objects.filter(username=request.user.username).order_by('-id')
        # 如果是上传文件
        if request.POST.get('type', '') == 'upload_form':
            for name, file in request.FILES.items():
                upload_file = UploadFile()
                upload_file.username = request.user.username
                upload_file.title = str(upload_file.upload_time).split('.')[0].replace(':', '-') + '_' + file.name
                path = '%s\%s\%s' % (settings.MEDIA_ROOT, upload_file.username, 'upload_file')
                if not os.path.exists(path):
                    os.makedirs(path)
                path = '%s\%s' % (path, upload_file.title)
                with open(path, 'wb') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                upload_file.save()
                if os.path.exists(path):
                    uploaded_files = UploadFile.objects.filter(username=request.user.username)
                    return render(request, 'upload.html', {'upload_msg': u'上传成功', 'uploaded_files': uploaded_files,
                                                           'check_info': check_info})
            uploaded_files = UploadFile.objects.filter(username=request.user.username)
            return render(request, 'upload.html', {'upload_msg': u'上传失败', 'uploaded_files': uploaded_files,
                                                   'check_info': check_info})
        # 如果是选择文件并查重
        if request.POST.get('type', '') == 'choose_form':
            chosen_files = []
            for key, item in request.POST.items():
                if item == 'on':
                    chosen_files.append(key)
            check_type = request.POST.get('file_scope', '')
            # 选择三种查重方式
            if check_type == 'rar':
                checkcode = CheckCode(request.user.username, chosen_files)
                checkcode.check()
            elif check_type == 'per_lib':
                pass
            elif check_type == 'database':
                pass
            # 未选择查重方式，仍返回当前页面
            uploaded_files = UploadFile.objects.filter(username=request.user.username)
            check_info = CheckInfo.objects.filter(username=request.user.username).order_by('-id')
            return render(request, 'upload.html', {'uploaded_files': uploaded_files, 'check_info': check_info})

        # 如果是删除历史记录
        if request.POST.get('type', '') == 'history_form':
            chosen_info = []
            for key, item in request.POST.items():
                if item == 'on':
                    chosen_info.append(key)
            for info in chosen_info:
                # 查重信息和查重结果一并删除
                check = CheckInfo.objects.get(username=request.user.username, check_time=info)
                CheckResult.objects.filter(check_id=check.id).delete()
                CheckInfo.objects.filter(username=request.user.username, check_time=info).delete()
                path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'check', check.check_time)
                if os.path.exists(path):
                    shutil.rmtree(path)
            uploaded_files = UploadFile.objects.filter(username=request.user.username)
            check_info = CheckInfo.objects.filter(username=request.user.username).order_by('-id')
            return render(request, 'upload.html', {'uploaded_files': uploaded_files, 'check_info': check_info})

        # 如果是删除下载个人库文件
        if request.POST.get('type', '') == 'perlib_form':
            chosen_files = []
            for key, item in request.POST.items():
                if item == 'on':
                    chosen_files.append(key)
            # 如果是删除
            if request.POST.get('delete'):
                for file in chosen_files:
                    # 删除数据库中记录、文件夹中文件
                    UploadFile.objects.filter(username=request.user.username, title=file).delete()
                    path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'upload_file', file)
                    if os.path.exists(path):
                        os.remove(path)
            # 如果是下载
            elif request.POST.get('download'):
                # 只有一个文件则直接下载
                if len(chosen_files) == 1:
                    file = chosen_files[0]
                    # 提供下载链接
                    path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'upload_file', file)
                    response = FileResponse(open(path, 'rb'))
                    response['Content-Type'] = 'application/octet-stream'
                    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(file))
                    return response
                # 多个文件下载需打包
                zipname = request.user.username + '_download' + '.zip'
                zippath = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'upload_file', zipname)
                zip = zipfile.ZipFile(zippath, 'w')
                for file in chosen_files:
                    path = '%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'upload_file', file)
                    zip.write(path, file)
                zip.close()
                response = HttpResponse(open(zippath, 'rb').read(), content_type='application/zip')
                response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(zipname))
                if os.path.exists(zippath):
                    os.remove(zippath)
                return response
            uploaded_files = UploadFile.objects.filter(username=request.user.username)
            return render(request, 'upload.html', {'uploaded_files': uploaded_files, 'check_info': check_info})


class CheckInfoView(View):
    def get(self, request, infoid):
        checkresults = CheckResult.objects.filter(check_id=int(infoid), sim3__gte=60).order_by('-sim3')
        checkinfofiles = CheckInfoFile.objects.filter(check_id=int(infoid))
        return render(request, 'checkinfo.html', {'checkresults': checkresults, 'checkinfofiles': checkinfofiles, 'infoid': infoid})

    def post(self, request, infoid):
        # 将所需文件存储到final_result中
        checkresults = []
        for key, item in request.POST.items():
            if item == 'on':
                checkresult = CheckResult.objects.get(id=key)
                checkresults.append(checkresult)
        check_download = CheckDownload()
        check_download.download(infoid, request.user.username, checkresults)
        checkresults = CheckResult.objects.filter(check_id=int(infoid), sim3__gte=60).order_by('-sim3')
        checkinfofiles = CheckInfoFile.objects.filter(check_id=int(infoid))
        # 下载查重结果压缩包
        checkinfo = CheckInfo.objects.get(id=infoid)
        zipname = checkinfo.check_time + '.zip'
        path = '%s\%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'check', checkinfo.check_time, zipname)
        response = FileResponse(open(path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(zipname))
        return response





class CheckResultView(View):
    def get(self, request, result_id):
        checkresult = CheckResult.objects.get(id=result_id)
        checkinfo = CheckInfo.objects.get(id=checkresult.check_id)
        path = '%s\%s\%s\%s\%s' % (settings.MEDIA_ROOT, request.user.username, 'check', checkinfo.check_time, 'check_result')
        filepath1 = '%s\%s' % (path, checkresult.file1.split('.')[0] + '_' + checkresult.file2.split('.')[0] + '__1.html')
        filepath2 = '%s\%s' % (path, checkresult.file1.split('.')[0] + '_' + checkresult.file2.split('.')[0] + '__2.html')
        f1 = open(filepath1, 'r').readlines()
        f2 = open(filepath2, 'r').readlines()
        s1 = ''
        s2 = ''
        for f in f1:
            f.replace('\n', '</br>')
            s1 = s1 + f
        for f in f2:
            f.replace('\n', '</br>')
            s2 = s2 + f
        return render(request, 'checkresult.html', {'checkresult': checkresult, 's1': s1, 's2': s2, 'Username': request.user.username})

class MainView(View):
    def get(self, request):
        return render(request, 'main.html')

# 全局404处理函数
def page_not_found(request, **kwargs):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response
