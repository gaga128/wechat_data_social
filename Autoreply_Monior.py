#-*-coding:UTF-8-*-
#****************************************************************
#推送关键词并对比返回结果是否与配置一致
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************

from PushAutoReply import Auto_PushReply
from MenuAutoReply import Menu_PushReply
import writelog
import get_authorinfo
import time
import SubData
import send_emails
import DefaultAutoReply


def Auto_Monior(getvalue_dict,pushper_dict,threadcount):
    try:
        app_openid_data = get_authorinfo.get_appidinfo(getvalue_dict)

        if app_openid_data=='NULL':
            print '无监测ID'
        else:
            start=time.time()

            for i in range(0, len(app_openid_data)):
                authtype = app_openid_data[i]['authtype']
                # print authtype
                getvalue_dict['appid']=app_openid_data[i]['appid']
                getvalue_dict['openid']=app_openid_data[i]['openid']
                getvalue_dict['authtype']=authtype
                appid=app_openid_data[i]['appid']
                SubData.initData(appid)
                # print getvalue_dict
                if authtype == '3':
                    getvalue_dict['uniqueid'] = app_openid_data[i]['uniqueid']
                    pushper_dict['pushhttp']='http://api.biz.social-touch.com/app-base/wechat/monitor/appid/%s?' % getvalue_dict['appid']
                elif authtype=='1':
                    getvalue_dict['uniqueid'] = app_openid_data[i]['uniqueid']
                    getvalue_dict['authtoken'] = app_openid_data[i]['authtoken']
                    pushper_dict['pushhttp']='http://api.biz.social-touch.com/app-base/wechat/monitor/?'


                # # list = ['1', '3']
                list=['1']
                for i in range(0, len(list)):   ###列表中1代表自动回复，3代表再次关注自动回复
                    DefaultAutoReply.default_PushReply(getvalue_dict, pushper_dict, list[i])
                result = Auto_PushReply(getvalue_dict, pushper_dict, threadcount)  ##关键词自定回复校验入口
                result = Menu_PushReply(getvalue_dict, pushper_dict, threadcount)  ##菜单自动回复校验入口

            total_keypass, total_keyerr, total_keyfail, total_menupass, total_menuerr, total_menufailr,total_subdefpass, total_subdeferr, total_subdeffailr=SubData.Total_static(result)

            writelog.static_log('总体', total_keypass, total_keyerr, total_keyfail,total_menupass,total_menufailr, total_menuerr)
            print 'total--关键词通过：%s,未通过：%s，失败：%s 菜单通过：%s，未通过：%s,失败：%s 自动回复通过：%s，未通过：%s,失败：%s'%(total_keypass, total_keyerr, total_keyfail, total_menupass, total_menuerr, total_menufailr,total_subdefpass,total_subdeferr,total_subdeffailr)

            if result!={} and result!=None:
                for key in result.keys():
                    tmp = result[key]
                    key_rightcount = tmp['Key_pass']
                    key_errcount = tmp['Key_err']
                    key_failcount = tmp['Key_fail']
                    menu_rightcount = tmp['Menu_pass']
                    menu_errcount = tmp['Menu_err']
                    menu_failcount = tmp['Menu_fail']
                    writelog.static_log(key, key_rightcount, key_errcount,key_failcount, menu_rightcount, menu_errcount,menu_failcount)
            else:
                print '全部结果为空'


            end = time.time()
            print end - start
            # send_emails.send_staticEmail()

    except Exception, e:
        print Exception, ":", e
        send_emails.send_failEmail( '%s :%s'%(Exception,e))



if __name__ == '__main__':
    getvalue_dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': '/appid/appidlist.txt',
                    'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords',
                      'material_http':'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get',
                      'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
                      'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list',
                      'checkservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey',
                      'colseservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom',
                      'reply_type': '4'})
    # getvalue_dict = ({'app_key': '100001', 'token': '6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR', 'appid': '/appid/appidlist.txt','http': 'http://coreapi.testbiz.social-touch.com:8081/autoreply/v1/auto-reply/keywords','material_http':'http://coreapi.testbiz.social-touch.com:8081/material/v1/manager/get','replywords_http': 'http://coreapi.testbiz.social-touch.com:8081/autoreply/v1/auto-reply/view','Menulist_http': 'http://coreapi.testbiz.social-touch.com:8081/menu/v1/manager/list','reply_type': '4'})
    # pushper_dict = {'token': 'Q5ymnlaH', 'Third_appid': 'wx76b8a7bc41157a1e','encodingAESKey': 'd403a0192fb864b90d32b806e449b0b0SocialTouch'}  ###线下
    threadcount=10
    pushper_dict = {'token': 'irPNHoJN', 'Third_appid': 'wxfb798f3c38b79c85',
                    'encodingAESKey': 'ed85e5ddefa3ade80d018178e34331ecsocialtouch'}
    Auto_Monior(getvalue_dict, pushper_dict,threadcount)












