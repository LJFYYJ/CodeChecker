# _*_ coding:utf-8 _*_
from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from CodeChecker.settings import EMAIL_FROM


# 生成字符串用于匹配
def random_str(randomlength=8):
    rand_str = ''
    chars = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        rand_str += chars[random.randint(0, length)]
    return rand_str


def send_register_email(username, email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str(8)
    email_record.username = username
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = u'CodeChecker注册激活链接'
        email_body = u'尊敬的用户{0}：\n    请点击下面的链接激活您的账号：\n    http://127.0.0.1:8000/active/id={0}&active={1}'\
            .format(username, code)
        # 在Setting里面配置发送者
        send_mail(email_title, email_body, EMAIL_FROM, [email])
    elif send_type == 'forget':
        email_title = u'CodeChecker密码重置链接'
        email_body = u'尊敬的用户{0}：\n    请点击下面的链接重置您的密码：\n    http://127.0.0.1:8000/reset/id={0}&active={1}'\
            .format(username, code)
        send_mail(email_title, email_body, EMAIL_FROM, [email])




