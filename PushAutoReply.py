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
import Pushdata
import threading
import SubData
import get_material
import send_emails
import get_service
unix_time = time.mktime(datetime.now().timetuple())

def Auto_PushReply(getvalue_dict,pushper_dict,threadcount):
    appid = getvalue_dict['appid']
    authtype = getvalue_dict['authtype']

    # SubData.initData(appid)    ###初始化appid的统计,在Autoreply——Monior统一初始化
    try:
        reply_dict, get_keywords_url = get_keywords.get_keywords(getvalue_dict)

        if reply_dict=='NULL':
            print 'totalCount=0,无关键词配置!'
            writelog.errorlog(get_keywords_url,'查看该appid是否有关键词配置','totalCount=0,无关键词配置!')
            static_result = SubData.data
        elif reply_dict=='FAIL':
            send_failEmail('获取关键词失败，请检查接口参数或接口请求是否正常:\n%s'%get_keywords_url)
            writelog.errorlog(get_keywords_url,'获取该appid的关键词', '获取关键词失败，请检查接口参数或接口请求是否正常!')
            static_result=SubData.Key_static(appid, '500')

        else:
            threads=[]
            for key in reply_dict.keys():
                reply_relation = reply_dict[key]
                openid = getvalue_dict['openid']
                to_xml = MesType.runtext_reply(key, openid)
                MENUNAME = reply_relation['MENUNAME']
                inputword = '%s,\t菜单名称：%s' % (str(key),str(MENUNAME))
                getvalue_dict['type'] = 1
                getvalue_dict['content'] = key
                service_result, service_url = get_service.get_service(getvalue_dict)
                # print service_result
                if service_result == '进入客服':
                    close_result, close_url = get_service.exitservice(getvalue_dict)
                    print '\n%s\n该关键词触发了客服状态'%service_url
                    writelog.errorlog(appid, reply_relation['MENUNAME'], '此为人工客服独立功能，暂不校验')
                    while close_result == '进入客服':
                        close_result, close_url = get_service.exitservice(getvalue_dict)
                        break
                    if close_result == '请求失败':
                        close_result, close_url = get_service.exitservice(getvalue_dict)
                        MENUNAME = reply_relation['MENUNAME']
                        # print "key:%s" % str(key)
                        inputword = '%s,\t菜单名称：%s' % (str(key), str(MENUNAME))
                        print '\n该关键词判断客服状态失败,判断是否进入客服状态:%s\n判断是否退出成功：%s' % (close_url, close_result)
                        send_emails.send_failEmail('该关键词退出客服状态失败：\n%s' % close_url)
                        writelog.errorlog(str(service_url), '关键词名称：%s--该菜单退出客服状态失败，请检查该接口请求是否正常\n' % str(inputword),
                                          str(reply_relation['reply_content']))
                        SubData.Menu_static(appid, '500')
                    else:
                        SubData.Key_static(appid, '200')

                elif service_result == '请求失败':
                    MENUNAME = reply_relation['MENUNAME']
                    # print "key:%s" % str(key)
                    inputword = '%s,\t菜单名称：%s' % (str(key), str(MENUNAME))
                    print '\n%s\n该关键词判断客服状态失败' % (service_url)
                    send_emails.send_failEmail('该关键词判断是否进入客服状态:%s\n' % service_url)
                    writelog.errorlog(str(service_url), '关键词名称：%s--该菜单判断是否进入客服状态失败，请检查该接口请求是否正常' % str(inputword),
                                      str(reply_relation['reply_content']))
                    SubData.Key_static(appid, '500')

                else:

                    if reply_relation['reply_content_type'] in ['2', '3', '4']:
                        material_result, material_url = get_material.get_material(getvalue_dict,reply_relation['reply_content'])
                        if material_result == 'NULL':
                            SubData.Key_static(appid, '200')
                            print '该material_id获取不到对应的素材:%s' % str(material_url)

                            # sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), '该material_id获取不到对应的素材！\n%s' %str( material_url))
                            writelog.errorlog(str(material_url), '关键词名称：%s--该material_id获取不到对应的素材' % str(inputword),str(reply_relation['reply_content']))
                            continue
                        elif material_result == 'FAIL':
                            SubData.Key_static(appid, '500')
                            print '该material_id获取素材失败，请检查该接口请求是否正常:%s' % str(material_url)
                            print reply_relation
                            send_emails.send_failEmail('获取素材失败，请检查该接口请求是否正常%s\n' % str(material_url))
                            writelog.errorlog(str(material_url), '菜单名称：%s--获取素材失败，请检查该接口请求是否正常' % str(inputword),str(reply_relation['reply_content']))
                            continue
                        else:
                            pass
                    else:
                        pass

                    # print '\n授权方式', authtype
                    if authtype == '3':
                        pushper_dict['General'] = {}
                        pushper_dict['token']='irPNHoJN'
                    elif authtype == '1':
                        pushper_dict['token'] = getvalue_dict['authtoken']
                        General = {}
                        General['uniqueid'] = getvalue_dict['uniqueid']
                        General['appid'] = getvalue_dict['appid']
                        pushper_dict['General'] = General
                    # Pushdata.pushdata(pushper_dict, getvalue_dict, key, reply_relation, to_xml)
                    obj = Pushdata.pushdata
                    t=threading.Thread(target=obj,args=(pushper_dict, getvalue_dict, key,reply_relation, to_xml))
                    threads.append(t)

            for t in threads:
                t.setDaemon(True)
                t.start()
                while True:
                    if(threading.activeCount() < threadcount):
                        break
                # print 'threading.activeCount:',threading.activeCount()

            for t in threads:
                t.join()
                # time.sleep(0.02)

            static_result=SubData.data
            # print static_result

        return static_result


    except Exception, e:
        print Exception, ":", e
        static_result = SubData.data
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

    Auto_PushReply(getvalue_dict, pushper_dict, 10)









