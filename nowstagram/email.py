#-*- encoding=UTF-8 -*-
from flask import Flask
from flask_mail import Mail,Message
import os

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.126.com',
    MAIL_PROT=25,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'zhuyuanshuo@126.com',
    MAIL_PASSWORD = 'JRESVYBZJQHW',
    MAIL_DEBUG = True
)


mail = Mail(app)

@app.route('/')
def index():
# sender 发送方，recipients 邮件接收方列表
    msg = Message("Hi!This is a test ",sender='zhuyuanshuo@126.com', recipients=['316417087@qq.com'])
# msg.body 邮件正文
    msg.body = "This is a first email"
# msg.attach 邮件附件添加
# msg.attach("文件名", "类型", 读取文件）
    with app.open_resource("F:\91d6680f-df8a-11ea-a055-7cb0c2b961a2.jpg") as fp:
        msg.attach("image.jpg", "image/jpg", fp.read())

    mail.send(msg)
    print "Mail sent"
    return "Sent"


if __name__ == '__main__':
    app.run()
