#-*-coding:UTF-8-*-
#****************************************************************
#发送邮件预警
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-08
# Description:
#****************************************************************
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os



def sendEmail(request_url,request_xml,result_decrypt,keywords,exreply,acreply):
    # return 0
    sender = 'bdtest@social-touch.com'
    receivers = ['lujia@social-touch.com','tianlongzhe@social-touch.com','songlei@social-touch.com','liyang@social-touch.com']
    # receivers = ['lujia@social-touch.com']
    msg = MIMEText('关键词自动回复错误\n\n请求url：\n%s\nrequest_xml:\n%s\n\n返回结果：\n%s\n\n\n关键词或菜单key：%s，\n\n预期回复： %s，\n\n实际回复：  %s'%(str(request_url),str(request_xml),str(result_decrypt),keywords,str(exreply),str(acreply)), 'plain', 'utf-8')
    msg['From'] = Header("测试sender", 'utf-8')
    msg['To'] = Header("tianlongzhe,songlei,liyang,lujia", 'utf-8')
    msg['subject'] = Header("关键词自动监测预警", 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qiye.163.com', 25)
        smtp.starttls()
        smtp.login('bdtest@social-touch.com', 'bbaa11!!')
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.close()
        print "sendEmail--email sent"
    except smtplib.SMTPException:
        print "sendEmail--Error in sending"






def send_failEmail(url):
    # return 0
    sender = 'bdtest@social-touch.com'
    receivers = ['lujia@social-touch.com','tianlongzhe@social-touch.com','songlei@social-touch.com','liyang@social-touch.com']
    # receivers = ['lujia@social-touch.com']
    msg = MIMEText('接口异常：%s'%url, 'plain', 'utf-8')
    msg['From'] = Header("测试sender", 'utf-8')
    msg['To'] = Header("tianlongzhe,songlei,liyang,lujia", 'utf-8')
    msg['subject'] = Header("关键词自动监测预警", 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qiye.163.com', 25)
        smtp.starttls()
        smtp.login('bdtest@social-touch.com', 'bbaa11!!')
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.close()
        print "send_failEmail--email sent"
    except smtplib.SMTPException:
        print "send_failEmail--Error in sending"


def send_staticEmail():
    # return 0
    f = open(os.getcwd()+r'/log/static.txt')
    txt = f.read()
    # print txt
    sender = 'bdtest@social-touch.com'
    receivers = ['lujia@social-touch.com','tianlongzhe@social-touch.com','songlei@social-touch.com','liyang@social-touch.com']
    # receivers = ['lujia@social-touch.com']
    msg = MIMEText(txt, 'plain', 'utf-8')
    msg['From'] = Header("测试sender", 'utf-8')
    msg['To'] = Header("tianlongzhe,songlei,liyang,lujia", 'utf-8')
    msg['subject'] = Header("SCRM自动监测预警结果统计", 'utf-8')
    try:
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qiye.163.com', 25)
        smtp.starttls()
        smtp.login('bdtest@social-touch.com', 'bbaa11!!')
        smtp.sendmail(sender, receivers, msg.as_string())
        smtp.close()
        print "send_staticEmail--email sent"
    except smtplib.SMTPException:
        print "send_staticEmail--Error in sending"

if __name__ == '__main__':
    # sendEmail()
    send_staticEmail()