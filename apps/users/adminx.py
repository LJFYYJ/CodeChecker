# -*- coding: utf-8 -*-
import xadmin
from xadmin import views
from .models import EmailVerifyRecord


# 修改主题
class BaseSetting(object):
    # 使用主题功能
    enable_themes = True
    use_bootswatch = True


# 修改页面左上角、底部、菜单栏
class GlobalSetting(object):
    site_title = 'CodeChecker后台管理系统'
    site_footer = 'CodeChecker'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    # 在后端表中显示特定几列
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 在后端对特定字段进行搜索
    search_fields = ['code', 'email', 'send_type']
    # 实现筛选功能
    list_filter = ['code', 'email', 'send_type', 'send_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)