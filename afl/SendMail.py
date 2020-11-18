import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# 负责将多个对象集合起来
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
# 发件人邮箱账号
my_sender = 'biao.hu@aifenlei.com'
# user登录邮箱的用户名，password登录邮箱的密码（授权码，即客户端密码，非网页版登录密码），但用腾讯邮箱的登录密码也能登录成功
my_pass = 'tFgwgJUHRp6vyk3c'
# 收件人邮箱账号
my_user = '15576100991@163.com'


# 2.定义：取最新测试报告
def new_file(reports):
    # 列举test_dir目录下的所有文件，结果以列表形式返回。
    lists = os.listdir(reports)
    # sort按key的关键字进行排序，lambda的入参fn为lists列表的元素，获取文件的最后修改时间
    # 最后对lists元素，按文件修改时间大小从小到大排序。
    lists.sort(key=lambda fn: os.path.getmtime(reports+'/'+fn))
    # 获取最新文件的绝对路径
    file_path=os.path.join(reports, lists[-1])
#    L=file_path.split('\\')
#    file_path='\\\\'.join(L)
    return file_path


def mail(file_path):
    ret = True
    try:
        # msg = MIMEText('填写邮件内容','plain','utf-8')  # 邮件内容，如果只有一个html超文本正文或者plain普通文本正文的话，一般msg的类型可以是MIMEText
        msg = MIMEMultipart()  # 如果是多个的话，就都添加到MIMEMultipart
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(("biao.hu@aifenlei.com", my_sender))
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(("15576100991@163.com", my_user))
        # 邮件的主题
        msg['Subject'] = "接口测试报告"
        # 构造附件
        atta = MIMEText(open(file_path, 'rb').read(), 'html', 'utf-8')
        # 设置附件信息
        # atta["Content-Disposition"] = 'attachment; filename="测试报告"'
        # 添加附件到邮件信息当中去
        msg.attach(atta)
        # SMTP服务器，腾讯企业邮箱端口是465，腾讯邮箱支持SSL(不强制)， 不支持TLS
        # qq邮箱smtp服务器地址:smtp.qq.com,端口号：456
        # 163邮箱smtp服务器地址：smtp.163.com，端口号：25
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        # 登录服务器，括号中对应的是发件人邮箱账号、邮箱密码
        server.login(my_sender, my_pass)
        # 发送邮件，括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender,[my_user,],msg.as_string())
        # 关闭连接
        server.quit()
    # 如果 try 中的语句没有执行，则会执行下面的 ret=False
    except Exception as e:
        print(e)
        ret = False
    return ret


new_report = new_file(reports='./reports')
print(new_report)
ret = mail(new_report)
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")