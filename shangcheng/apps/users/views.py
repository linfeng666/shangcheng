import re

from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from users.models import User
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from utils import constants

from celery_task.tasks import send_active_email


class RegisterView(View):
    '''注册类视图'''
    def get(self,request):
        """对应get请求方式的逻辑, 返回注册的页面"""
        return render(request,'register.html')

    def post(self,request):
        '''对应的post请求方式的逻辑'''
        # 1,获取参数
        # 2,检验参数
        # 3,业务处理
        # 4,返回值


        # 获取参数
        user_name = request.POST.get('user_name')
        password = request.POST.get("pwd")
        password2 = request.POST.get("cpwd")
        email = request.POST.get("email")
        allow = request.POST.get("allow")


        # 检验参数
        # all()返回真或者假，数据为空为假，不为空为真
        if not all([user_name,password,password2,email,allow]):
            # 参数不完整
            url = reverse('users:register')
            return redirect(url)

        #判断再次密码是否一致
        if password != password2:
            errmsg = '两次密码不一致'
            return render(request,'register.html',errmsg)

        # 判断邮政格式是否正确
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}',email):
            # 不匹配
            errmsg = '邮箱格式不正确'
            return render(request,'register.html',errmsg)

        # 判断是否勾选了同意用户协议
        if allow != 'on':
            errmsg = '请勾选同意用户协议'
            return render(request, 'register.html', errmsg)


        # 业务处理

        #保存数据到数据库中
        # creat_user
        try:
            user = User.objects.create_user(user_name,email,password)
        except IntegrityError as e:
            # 用户名已注册
            errmsg = '用户名已注册，请重新输入'
            return render(request,'register.html',errmsg)

        # 更改用户的激活状态，将默认的已激活状态改为未激活
        user.is_active = False
        user.save()

        # 发送激活邮件
        # 生成用户激活的身份token（令牌）
        token = user.generate_active_token()
        active_url = 'http://127.0.0.1:8000/users/active/' + token

        # 同步发送激活邮件
        # send_mail(邮件标题，邮件内容，发件人，收件人，html_message=html格式的邮件内容)
        # html_message = '''
        # <h1>天天生鲜用户激活</h1>
        # <h2>尊敬的用户%s, 感谢您注册天天生鲜，请在24小时内点击如下链接激活用户</h2>
        # <a href=%s>%s</a>
        # ''' % (user_name, active_url, active_url)
        # send_mail('ttsx用户激活','',settings.EMAIL_FROM,[email],html_message=html_message)

        # 异步发送邮件  非阻塞
        send_active_email.delay(user_name, active_url, email)

        return HttpResponse('这是登陆页面')

class UserActiveView(View):
    '''用户激活视图'''
    def get(self,request,user_token):
        '''
        用户激活
        :param request:
        :param user_token: 用户激活令牌
        :return:
        '''
        # 创建序列化器（用于转换数据）
        s = Serializer(settings.SECRET_KEY,constants.USER_ACTIVE_EXPIRES)
        # 获取用户未转换数据
        try:
            data = s.loads(user_token)
        except SignatureExpired:
            # token已过期
            return HttpResponse('链接已过期')
        # 获取用户id
        user_id = data.get('user_id')
        # 获取用户
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            # 用户不存在
            return HttpResponse('用户不存在')

        # 更新用户的激活状态
        # User.objects.filter(id=user_id).update(is_active=True)
        user.is_active = True
        user.save()

        return HttpResponse('激活成功')




