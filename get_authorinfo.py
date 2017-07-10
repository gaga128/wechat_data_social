#-*-coding:UTF-8-*-
#****************************************************************
#获取配置文件中appid信息，返回字典
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************


import os
import FileOperation
import time
import send_emails
import requests



def get_appidinfo(getvalue_dict):
    today = str(time.strftime("%Y-%m-%d %H.%M", time.localtime(time.time())))
    a = FileOperation.FileExsit(os.getcwd() + r'/log/failresult.html')
    if a == True:
        FileOperation.Copy_file(os.getcwd() + r'/log/failresult.html',os.getcwd() + r'/log/failresult_history/failresult_%s.html'%today)
        FileOperation.DelFile(os.getcwd() + r'/log/failresult.html')
    b = FileOperation.FileExsit(os.getcwd() + r'/log/static.txt')
    if b == True:
            FileOperation.Copy_file(os.getcwd() + r'/log/static.txt',os.getcwd() + r'/log/staticlog/static_%s.txt' % today)
            FileOperation.DelFile(os.getcwd() + r'/log/static.txt')
    app_openid_data= []
    # print getvalue_dict
    path=getvalue_dict['appid']
    # print path
    a = FileOperation.FileExsit(os.getcwd() + path)
    if a == True:
        file = open(os.getcwd() + path, "r")
        for line in file.readlines():
            if line[0] == '#' or line[0] == '#' or len(line.strip()) == 0:
                pass
            else:
                app_openid = eval(line.decode(encoding='utf-8'))
                app_openid_data.append(app_openid)
                # appid = line.strip('\n').decode(encoding='utf-8')
                # appidlist.append(appid)
        file.close()
        # print app_openid_data
        return app_openid_data

    else:
        print '请检查/appid/appidlist.txt文件是否存在。'
        send_emails.send_failEmail('请检查/appid/appidlist.txt文件是否存在。')
        return 'NULL'



def get_opeind(appid,path):
    openid = 'NULL'
    a = FileOperation.FileExsit(os.getcwd() + path)
    if a == True:
        file = open(os.getcwd() + path, "r")
        for line in file.readlines():
            if line[0] == '#' or line[0] == '#' or len(line.strip()) == 0:
                pass
            else:
                app_openid = eval(line.decode(encoding='utf-8'))
                # print app_openid
                if app_openid['appid']!=appid:
                    continue
                else:
                    openid = app_openid['openid']
    else:
        print '请检查/appid/appidlist.txt文件是否存在。'
        send_emails.send_failEmail('请检查/appid/appidlist.txt文件是否存在。')

    return openid


def get_uniauth(appid,path):
    uniqueid='NULL'
    authtoken='NULL'

    a = FileOperation.FileExsit(os.getcwd() + path)
    if a == True:
        file = open(os.getcwd() + path, "r")
        for line in file.readlines():
            if line[0] == '#' or line[0] == '#' or len(line.strip()) == 0:
                pass
            else:
                app_openid = eval(line.decode(encoding='utf-8'))
                # print app_openid
                if app_openid['appid']!=appid:
                    continue
                else:
                    uniqueid=app_openid['uniqueid']
                    authtoken=app_openid['authtoken']

    else:
        print '请检查/appid/appidlist.txt文件是否存在。'
        send_emails.send_failEmail('请检查/appid/appidlist.txt文件是否存在。')

    return uniqueid,authtoken





def get_authorinfo(dict):
    http = dict['authorinfo_http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['wx_appid'] = dict['appid']

    try:
        req = requests.get(http,para, timeout=10)
        # print req.url
        tmp_result = req.json()
        # print tmp_result
        if tmp_result['msg']==u'成功':
            data = tmp_result['data']
            if data==[]:
                mode='FAIL'
            else:
                wechatInfo = data['wechatInfo']

                mode=wechatInfo['mode']

        else:
            mode='FAIL'
        # print mode
        return mode,req.url


    except Exception, e:
        failurl = http + '?' + 'app_key=' + str(para['app_key']) +'&'+ 'token=' + str(para['token']) +'&'+ 'wx_appid=' + str(para['wx_appid'])
        result = 'FAIL'
        print "获取素材失败，请检查接口参数或接口请求是否正常\n～%s\n%s" % (failurl, str(e))
        return  result,'%s\n%s'%(failurl,str(e))






if __name__ == '__main__':

    # getvalue_dict = ({'app_key': '100001', 'token': '6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR', 'appid': '/appid/appidlist.txt','http': 'http://coreapi.testbiz.social-touch.com:8081/autoreply/v1/auto-reply/keywords','material_http':'http://coreapi.testbiz.social-touch.com:8081/material/v1/manager/get','replywords_http': 'http://coreapi.testbiz.social-touch.com:8081/autoreply/v1/auto-reply/view','Menulist_http': 'http://coreapi.testbiz.social-touch.com:8081/menu/v1/manager/list','reply_type': '4'})
    # pushper_dict = {'token': 'Q5ymnlaH', 'Third_appid': 'wx76b8a7bc41157a1e','encodingAESKey': 'd403a0192fb864b90d32b806e449b0b0SocialTouch'}  ###线下
    getvalue_dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': '/appid/appidlist.txt',
                      'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords',
                      'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get',
                      'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
                      'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list',
                      'reply_type': '4'})
    pushper_dict = {'token': 'irPNHoJN', 'Third_appid': 'wxfb798f3c38b79c85',
                    'encodingAESKey': 'ed85e5ddefa3ade80d018178e34331ecsocialtouch'}
    get_appidinfo(getvalue_dict)

    dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wxe5826201582861fc',
             'authorinfo_http': 'http://coreapi.biz.social-touch.com:8081/usercenter/v1/wechat/get-wechat-info-by-appid'})
    get_authorinfo(dict)