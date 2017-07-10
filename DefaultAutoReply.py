#-*-coding:UTF-8-*-
#****************************************************************
#推送关键词并对比返回结果是否与配置一致
# Author     : lujia
# Version    : 1.0
# Date       : 2017-03-13
# Description:
#****************************************************************
import get_autoreply
from datetime import datetime
import time
from send_emails import send_failEmail,sendEmail
import MesType
import writelog
import Pushdata
import get_material
import send_emails
import get_service
import SubData

cur_time = time.mktime(datetime.now().timetuple())

def default_PushReply(getvalue_dict,pushper_dict,reply_type):

    appid = getvalue_dict['appid']
    authtype = getvalue_dict['authtype']
    reply_dict, get_defautoreply_url=get_autoreply.get_defaultreply(getvalue_dict,reply_type)
    reply_dict['MENUNAME']='自动回复，非菜单'
    if authtype == '3':
        pushper_dict['General'] = {}
        pushper_dict['token'] = 'irPNHoJN'
    elif authtype == '1':
        pushper_dict['token'] = getvalue_dict['authtoken']
        General = {}
        General['uniqueid'] = getvalue_dict['uniqueid']
        General['appid'] = getvalue_dict['appid']
        pushper_dict['General'] = General
    # try:
    if reply_dict['reply_content'] =='NULL' or reply_dict['is_open']=='0':
        print '该appid未设置或已关闭自动回复!'
        writelog.errorlog(get_defautoreply_url,'查看该appid是否设置自动回复','该appid未设置自动回复!')
        static_result = SubData.data
    elif reply_dict['reply_content'] =='FAIL':
        send_failEmail('获取自动回复失败，请检查接口参数或接口请求是否正常:\n%s'%get_defautoreply_url)
        writelog.errorlog(get_defautoreply_url,'获取该appid的自动回复', '获取自动回复失败，请检查接口参数或接口请求是否正常!')
        SubData.subdef_static(appid, '500')
    else:
        openid = getvalue_dict['openid']
        if reply_type=='1':
            to_xml = MesType.runtext_reply(str(int(cur_time)), openid)
            inputword = str(int(cur_time))
            getvalue_dict['content'] = inputword
            getvalue_dict['type'] = 1
            service_result, service_url = get_service.get_service(getvalue_dict)
            # print service_result
            if service_result == '进入客服':
                close_result, close_url = get_service.exitservice(getvalue_dict)
                print '\n%s\n该词触发了客服状态' % service_url
                writelog.errorlog(appid, inputword, '此为人工客服独立功能，暂不校验')
                while close_result == '进入客服':
                    close_result, close_url = get_service.exitservice(getvalue_dict)
                    break
                if close_result == '请求失败':
                    close_result, close_url = get_service.exitservice(getvalue_dict)
                    SubData.subdef_static(appid, '500')
                    print '\n该词判断客服状态失败,判断是否进入客服状态:%s\n判断是否退出成功：%s' % (close_url, close_result)
                    send_emails.send_failEmail('该词退出客服状态失败：\n%s' % close_url)
                    writelog.errorlog(str(service_url), '名称：%s--该词退出客服状态失败，请检查该接口请求是否正常\n' % str(inputword),str(reply_dict['reply_content']))
                else:
                    SubData.subdef_static(appid, '200')
            elif service_result == '请求失败':
                print '\n%s\n该词判断客服状态失败' % (service_url)
                send_emails.send_failEmail('该词判断是否进入客服状态:%s\n' % service_url)
                writelog.errorlog(str(service_url), '名称：%s--该词判断是否进入客服状态失败，请检查该接口请求是否正常' % str(inputword),str(reply_dict['reply_content']))
                SubData.subdef_static(appid, '500')
            else:
                if reply_dict['reply_content_type'] in ['2', '3', '4']:
                    material_result, material_url = get_material.get_material(getvalue_dict, reply_dict['reply_content'])
                    if material_result == 'NULL':
                        print '该material_id获取不到对应的素材:%s' % str(material_url)
                        # sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), '该material_id获取不到对应的素材！\n%s' %str( material_url))
                        writelog.errorlog(str(material_url), '：%s--该material_id获取不到对应的素材' % str(inputword),str(reply_dict['reply_content']))
                        SubData.subdef_static(appid, '200')
                    elif material_result == 'FAIL':
                        SubData.subdef_static(appid, '500')
                        print '该material_id获取素材失败，请检查该接口请求是否正常:%s' % str(material_url)
                        send_emails.send_failEmail('获取素材失败，请检查该接口请求是否正常%s\n' % str(material_url))
                        writelog.errorlog(str(material_url), '菜单名称：%s--获取素材失败，请检查该接口请求是否正常' % str(inputword),str(reply_dict['reply_content']))
                    else:
                        Pushdata.pushdata(pushper_dict, getvalue_dict, inputword, reply_dict, to_xml)
                elif reply_dict['reply_content_type'] == '1':
                    Pushdata.pushdata(pushper_dict, getvalue_dict, inputword, reply_dict, to_xml)
                else:
                    print '该种reply_content_type暂不支持'
        elif reply_type=='3':
            evendict={}
            evendict['openid']=openid
            evendict['Event']='subscribe'
            to_xml=MesType.runevent_reply(evendict)
            inputword = 'subscribe'
            if reply_dict['reply_content_type'] in ['2', '3', '4']:
                material_result, material_url = get_material.get_material(getvalue_dict,reply_dict['reply_content'])
                if material_result == 'NULL':
                    SubData.subdef_static(appid, '200')
                    print '该material_id获取不到对应的素材:%s' % str(material_url)
                    # sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), '该material_id获取不到对应的素材！\n%s' %str( material_url))
                    writelog.errorlog(str(material_url), '：%s--该material_id获取不到对应的素材' % str(inputword),str(reply_dict['reply_content']))
                elif material_result == 'FAIL':
                    print '该material_id获取素材失败，请检查该接口请求是否正常:%s' % str(material_url)
                    SubData.subdef_static(appid, '500')
                    send_emails.send_failEmail('获取素材失败，请检查该接口请求是否正常%s\n' % str(material_url))
                    writelog.errorlog(str(material_url), '菜单名称：%s--获取素材失败，请检查该接口请求是否正常' % str(inputword),str(reply_dict['reply_content']))
                else:
                    Pushdata.pushdata(pushper_dict, getvalue_dict, inputword, reply_dict, to_xml)
            elif reply_dict['reply_content_type']=='1':
                Pushdata.pushdata(pushper_dict, getvalue_dict, inputword, reply_dict, to_xml)
            else:
                print '该种reply_content_type暂不支持'
        else:
            SubData.subdef_static(appid, '500')
            print '该种回复类型暂不支持！reply_type=%s'%reply_type
            return '该种回复类型暂不支持！reply_type=%s'%reply_type
            # print '\n授权方式', authtype
        static_result = SubData.data
    return static_result
    # except Exception,e:
    #     print Exception, ":", e
        #send_emails.send_failEmail('\n%s :%s' % (str(Exception), str(e)))


if __name__ == '__main__':

    pushper_dict = {'authtype': '3',
                'pushhttp': 'http://api.biz.social-touch.com/app-base/wechat/monitor/appid/wxfba8a23be3bb4304?',
                'Third_appid': 'wxfb798f3c38b79c85',
                'encodingAESKey': 'ed85e5ddefa3ade80d018178e34331ecsocialtouch',
                'General': {'appid': 'wxe92ee01c51105996', 'uniqueid': '523'}, 'token': 'irPNHoJN'}

    getvalue_dict = {'openid': 'onwbDt7RYVqWzkV-U1nq-vT89MVs', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL',
                 'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get',
                 'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords',
                 'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
                 'appid': 'wxfba8a23be3bb4304', 'reply_type': '4', 'authtype': '3', 'app_key': '100018',
                 'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list',
                 'checkservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/checkstatus',
                 'colseservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom',
                 'uniqueid': '347'
                 }
    list=['1','3']
    for i in range(0,len(list)):
        reply_type=list[i]
        default_PushReply(getvalue_dict,pushper_dict,reply_type)

