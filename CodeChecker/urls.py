"""CodeChecker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetView, ResetView, UploadFileView, ModifyView, CheckInfoView, CheckResultView, MainView
from django.views.static import serve
import xadmin
from CodeChecker.settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='main.html')),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    path('forget/', ForgetView.as_view(), name='forget'),
    path('upload/', UploadFileView.as_view(), name='upload'),
    path('main/', MainView.as_view(), name='main'),
    re_path('checkinfo/id=(?P<infoid>.*)/', CheckInfoView.as_view(), name='checkinfo'),
    re_path('checkresult/id=(?P<result_id>.*)/', CheckResultView.as_view(), name='checkresult'),
    re_path('active/id=(?P<username>.*)&active=(?P<active_code>.*)/', ActiveUserView.as_view(), name='active'),
    re_path('reset/id=(?P<username>.*)&active=(?P<active_code>.*)/', ResetView.as_view(), name='reset'),
    path('modify/', ModifyView.as_view(), name='modify'),

]

handler404 = 'users.views.page_not_found'
