# 启动celery的命令
# celery -A celery_task.tasks worker -l info

# 将django项目的配置文件信息保存到操作系统中
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "ttsx.settings"

# 在启动celery的时候需要，在启动django的时候不需要，需要注释掉
# 让django初始化一下，django读入配置文件的信息
# django.setup()会询问操作系统配置文件的位置，读入配置文件的信息
# import django
# django.setup()


from celery import Celery
from django.core.mail import send_mail
from django.conf import settings

# 创建celery的应用
app = Celery('ttsx',broker='redis://127.0.0.1:6379/0')

# 定义任务(以函数方式)
@app.task
def send_active_email(user_name,active_url,email):
    '''发送激活邮件'''
    # send_mail(邮件标题， 邮件内容，发件人， 收件人， html_message=html格式的邮件内容)
    html_message = """
                <h1>天天生鲜用户激活</h1>
                <h2>尊敬的用户%s, 感谢您注册天天生鲜，请在24小时内点击如下链接激活用户</h2>
                <a href=%s>%s</a>
                """ % (user_name, active_url, active_url)

    send_mail("天天生鲜用户激活", "", settings.EMAIL_FROM, [email], html_message=html_message)