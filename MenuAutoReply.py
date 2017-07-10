#-*-coding:UTF-8-*-
#****************************************************************
#推送关键词并对比返回结果是否与配置一致
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************
import get_keywords
from datetime import datetime
import time
from send_emails import send_failEmail,sendEmail
import MesType
import writelog
import get_Menulist
import threading
import Pushdata
import SubData
import get_material
import send_emails
import get_service


unix_time = time.mktime(datetime.now().timetuple())

def Menu_PushReply(getvalue_dict,pushper_dict,threadcount):
    appid = getvalue_dict['appid']
    authtype = getvalue_dict['authtype']
    reply_dict, get_Menu_url=get_Menulist.get_Menulist(getvalue_dict)

    # SubData.initData(appid)  ###初始化appid的统计,在Autoreply——Monior统一初始化
    try:
        if reply_dict=='NULL':
            print '该appid无自定义菜单!'
            writelog.errorlog(get_Menu_url,'查看该appid是否有自定义菜单','该appid无自定义菜单!')
            static_result = SubData.data
            # print static_result
        elif reply_dict=='FAIL':
            send_failEmail('获取自定义菜单失败，请检查接口参数或接口请求是否正常:\n%s'%get_Menu_url)
            writelog.errorlog(get_Menu_url,'获取该appid的自定义菜单', '获取自定义菜单失败，请检查接口参数或接口请求是否正常!')
            static_result=SubData.Menu_static(appid,'500')
            print static_result
        else:
            threads = []
            for keyone in reply_dict.keys():
                tmp_reply_relation=reply_dict[keyone]
                tmp_reply_relation['openid'] = getvalue_dict['openid']

                MENUNAME = tmp_reply_relation['MENUNAME']
                getvalue_dict['type'] = 2
                getvalue_dict['content'] = MENUNAME
                service_result, service_url = get_service.get_service(getvalue_dict)

                if service_result == '进入客服':
                    close_result, close_url = get_service.exitservice(getvalue_dict)
                    print '\n%s\n该关键词触发了客服状态' % service_url
                    writelog.errorlog(appid, tmp_reply_relation['MENUNAME'], '此为人工客服独立功能，暂不校验')
                    while close_result == '进入客服':
                        close_result, close_url = get_service.exitservice(getvalue_dict)
                        break
                    if close_result == '请求失败':
                        close_result, close_url = get_service.exitservice(getvalue_dict)
                        MENUNAME = tmp_reply_relation['MENUNAME']
                        inputword = '%s,\t菜单名称：%s' % (str(keyone), str(MENUNAME))
                        print '\n该菜单判断客服状态失败,判断是否进入客服状态:%s\n判断是否退出成功：%s' % (close_url, close_result)
                        send_emails.send_failEmail('该菜单退出客服状态失败：\n%s' % close_url)
                        writelog.errorlog(str(service_url), '菜单名称：%s--该菜单退出客服状态失败，请检查该接口请求是否正常\n%s' % str(inputword),str(tmp_reply_relation['reply_content']))
                        SubData.Menu_static(appid, '500')
                    else:
                        SubData.Menu_static(appid, '200')
                    reply_dict.pop(keyone)

                elif service_result == '请求失败':
                    MENUNAME = tmp_reply_relation['MENUNAME']
                    # print "key:%s" % str(key)
                    inputword = '%s,\t菜单名称：%s' % (str(keyone), str(MENUNAME))
                    print '\n%s\n该菜单判断客服状态失败' % (service_url)
                    send_emails.send_failEmail('该菜单判断是否进入客服状态:%s\n' % service_url)
                    writelog.errorlog(str(service_url), '菜单名称：%s--该菜单判断是否进入客服状态失败，请检查该接口请求是否正常' % str(inputword),
                                      str(tmp_reply_relation['reply_content']))
                    SubData.Menu_static(appid, '500')
                    reply_dict.pop(keyone)
                else:
                    if tmp_reply_relation['Event']=='CLICK':
                        if  tmp_reply_relation.has_key('replyword') and tmp_reply_relation['replyword']=='NULL':
                            get_replyword_url = tmp_reply_relation['get_replyword_url']
                            menuname=tmp_reply_relation['MENUNAME']
                            SubData.Menu_static(appid, '200')
                            writelog.errorlog(get_replyword_url, '查看reply_id对应的回复内容', '"%s"菜单的reply_id无对应回复信息'%menuname)
                            print '\n点击某菜单，该菜单的reply_id无对应回复信息,菜单名称：%s\n%s'%(menuname,get_replyword_url)
                            reply_dict.pop(keyone)
                            continue
                            # send_failEmail('"%s"菜单的reply_id无对应回复信息%s' % (menuname,get_replyword_url))   ##暂时不发送邮件
                        elif tmp_reply_relation.has_key('replyword') and tmp_reply_relation['replyword']=='FAIL':
                            SubData.Menu_static(appid, '500')
                            get_replyword_url = tmp_reply_relation['get_replyword_url']
                            writelog.errorlog(get_replyword_url, '查看reply_id对应的回复内容', '根据reply_id获取菜单自动回复内容的接口请求失败')
                            send_failEmail('根据reply_id获取菜单自动回复内容的接口请求失败%s' % get_replyword_url)
                            reply_dict.pop(keyone)
                            continue

                        else:
                            pass
                    else:
                        pass
                    reply_relation=reply_dict[keyone]
                    reply_relation['openid'] = getvalue_dict['openid']
                    to_xml=MesType.runevent_reply(reply_relation)
                    MENUNAME = reply_relation['MENUNAME']
                    inputword = '%s,\t菜单名称：%s' % (str(keyone),str(MENUNAME))

                    if  reply_relation.has_key('replycontent_type') and reply_relation['reply_content_type'] in ['2', '3', '4']:
                        material_result, material_url = get_material.get_material(getvalue_dict, reply_relation['reply_content'])
                        if material_result == 'NULL':
                            SubData.Menu_static(appid, '200')
                            print '该material_id获取不到对应的素材:%s' % str(material_url)
                            # sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), '该material_id获取不到对应的素材！\n%s' %str( material_url))
                            writelog.errorlog(str(material_url), '菜单名称：%s--该material_id获取不到对应的素材' % str(inputword), str(reply_relation['reply_content']))
                            reply_dict.pop(keyone)
                            continue
                        elif material_result == 'FAIL':
                            SubData.Menu_static(appid,'500')
                            print '该material_id获取素材失败，请检查该接口请求是否正常:%s' % str(material_url)
                            send_emails.send_failEmail('获取素材失败，请检查该接口请求是否正常%s\n' % str(material_url))
                            writelog.errorlog(str(material_url), '菜单名称：%s--获取素材失败，请检查该接口请求是否正常' % str(inputword), str(reply_relation['reply_content']))
                            reply_dict.pop(keyone)
                            continue
                        else:
                            pass
                    pushper_dict['key'] = keyone
                    if authtype == '3':
                        pushper_dict['token'] = 'irPNHoJN'
                        pushper_dict['General']={}
                    elif authtype == '1':
                        pushper_dict['token'] = getvalue_dict['authtoken']
                        General = {}
                        General['uniqueid'] = getvalue_dict['uniqueid']
                        General['appid'] = getvalue_dict['appid']
                        pushper_dict['General'] = General
                    # Pushdata.pushdata(pushper_dict, getvalue_dict, key,reply_relation, to_xml)
                    obj = Pushdata.pushdata
                    t = threading.Thread(target=obj, args=(pushper_dict, getvalue_dict, keyone,reply_relation, to_xml))
                    threads.append(t)


            for t in threads:
                t.setDaemon(True)
                t.start()
                while True:
                    if (len(threading.enumerate()) < threadcount):
                        break
                # print 'threading.activeCount:', threading.activeCount()


            for t in threads:
                t.join()
                # time.sleep(0.05)

            static_result=SubData.data
            # print static_result
        return static_result


    except Exception, e:
        print Exception, ":", e
        static_result=SubData.data
        send_emails.send_failEmail('\n%s :%s' % (str(Exception), str(e)))
        return static_result








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

    Menu_PushReply(getvalue_dict,pushper_dict,10)

