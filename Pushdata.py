#-*- encoding:utf-8 -*-
#****************************************************************
# 请求接口
# Author     : lujia
# Date       : 2017-03-03
# Description:
#****************************************************************



import threading
from lxml import etree
import time
from xml.sax.saxutils import unescape
import collections
import random
import requests
import hashlib
import MesCrypt
import MesType
import writelog
import send_emails
import Compare
import SubData



mutex = threading.Lock()
def pushdata(pushper_dict, getvalue_dict,key,reply_relation, to_xml):
    # print etree.tostring(to_xml)

    token=pushper_dict['token']
    appid = getvalue_dict['appid']
    http=pushper_dict['pushhttp']
    Third_appid=pushper_dict['Third_appid']
    encodingAESKey=pushper_dict['encodingAESKey']
    authtype=getvalue_dict['authtype']
    General=pushper_dict['General']
    global code

    Unencrypt_xml=etree.tostring(to_xml, encoding="UTF-8")

    timestamp = etree.fromstring(Unencrypt_xml).find('CreateTime').text
    openid = etree.fromstring(Unencrypt_xml).find('FromUserName').text
    if authtype=='1':
        msg_encrypt=Unencrypt_xml
    elif authtype=='3':
        msg_encrypt = MesCrypt.encrypt(encodingAESKey, Third_appid, Unencrypt_xml)  ######XML数据加密
    else:
        send_emails.send_failEmail('该种授权类型不属于已知类型%s,请联系相关人员进行添加'%str(authtype))
        return {'authtype': authtype, 'request_url': http, 'request_xml': Unencrypt_xml, 'result_decrypt': '该种授权类型不属于已知类型%s,请联系相关人员进行添加'%str(authtype)}
    nonce = str(random.randint(1000000000, 9999999999))
    encrypt_type = 'aes'
    # print  token ,timestamp,nonce
    signstr = ''.join(sorted([token, timestamp, nonce]))      ####按照升序排列,拼成字符串

    signature = hashlib.sha1(signstr).hexdigest()
    Msg_signstr = ''.join(sorted([token, timestamp, nonce, msg_encrypt]))
    Msg_Signature = hashlib.sha1(Msg_signstr).hexdigest()
    # print 'signature:%s  &  Msg_Signature:%s'%(signature, Msg_Signature)
    data = collections.OrderedDict()
    ToUserName=etree.fromstring(Unencrypt_xml).find('ToUserName').text
    if authtype=='3':
        data['ToUserName'] = '<![CDATA[%s]]>' % ToUserName
        data['Encrypt'] = '<![CDATA[%s]]>'%msg_encrypt
        data['from']='<![CDATA[QA-check]]>'
        ele = etree.Element('xml')
        for ke, val in data.items():
            child = etree.Element(ke)
            child.text = str(val)
            ele.append(child)
        encrypt_xml=unescape(etree.tostring(ele))
        url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&encrypt_type=%s&msg_signature=%s' % (
        http, signature, timestamp, nonce, openid, encrypt_type, Msg_Signature)
    elif authtype == '1':
        encrypt_xml=Unencrypt_xml
        appid=General['appid']
        uniqueid=General['uniqueid']
        url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&uniqueid=%s&appid=%s' % (http, signature, timestamp, nonce, openid, uniqueid, appid)
    headers = {'Content-Type': 'text/xml'}
    starttime = time.time()

    # try:
    req = requests.post(url=url, data=encrypt_xml, headers=headers, timeout=10)
    result = req.text

    mutex.acquire()
    taketime = time.time() - starttime
    # print pushper_dict
    # print getvalue_dict
    print '\n****Request_URL****: \n%s\n****Unencrypt_XML****: \n%s\n****Request_EncryptXML****: \n%s' % (url, Unencrypt_xml, encrypt_xml)
    print '*Request time: %s ms' % int(taketime * 1000)
    print '*Status_code: %s' % req.status_code
    if req.status_code==200:
        if result:
            if authtype=='3':
                result_statu,result_decrypt=MesCrypt.decrypt(encodingAESKey, Third_appid, result)
            elif authtype=='1':
                result_statu,result_decrypt=MesCrypt.nodecrypt(result)
            else:
                result_statu='FAIL'
                result_decrypt=result
        else:
            result_statu='NULL'
            print '\nSTATUS=200,请求成功，无返回结果!'
            result_decrypt='STATUS=200,请求成功，无返回结果!'
    else:
        result_statu='FAIL'
        result_decrypt=str(req.status_code)

    pushinfo_dict={'result_statu':result_statu,'request_url':str(req.url),'request_xml':encrypt_xml,'Unencrypt_xml':Unencrypt_xml,'result_decrypt':result_decrypt}

    if to_xml.find('MsgType').text=='text' or to_xml.find('Event').text == 'subscribe':
        request_url, request_xml, result_sign = Compare.Reply_Compare(reply_relation,key,getvalue_dict, pushinfo_dict)
        if result_sign == 'pass':
           code='200'
        elif result_sign == 'fail':
            code = '400'
        else:
            code = '400'
    elif to_xml.find('Event').text == 'VIEW':
        if pushinfo_dict['result_statu']=='NULL':
            print '\n 页面跳转类型，数据推送成功，无需验证!'
            code = '200'
        else:
            code = '500'
            writelog.errorlog(pushinfo_dict['request_url'], pushinfo_dict['request_xml'], pushinfo_dict['result_decrypt'])
            # send_emails.sendEmail(pushinfo_dict['request_url'], pushinfo_dict['request_xml'], result_decrypt, key, str(reply_relation['reply_content']), '接口推送数据失败！')
            # send_emails.send_failEmail('推送数据失败：%s' % str(pushinfo_dict))
    elif to_xml.find('Event').text == 'CLICK':
        if reply_relation['reply_id'] == '0':
            code = '200'
        else:
            request_url, request_xml, result_sign = Compare.Reply_Compare(reply_relation, key,getvalue_dict, pushinfo_dict)
            if result_sign == 'pass':
                code = '200'
            elif result_sign == 'fail':
                code = '400'
            else:
                code = '400'
    else:
        code = '400'
        writelog.errorlog(pushinfo_dict['request_url'], pushinfo_dict['request_xml'], pushinfo_dict['result_decrypt'])
        send_emails.send_failEmail('该种事件类型暂不支持，请联系相关人员进行添加：%s' % str(pushinfo_dict))
    print '\n compare-code:%s\n'%code
    if reply_relation['MENUNAME']== '关键词，非菜单':
        SubData.Key_static(appid, code)
    elif reply_relation['MENUNAME']=='自动回复，非菜单':
        SubData.subdef_static(appid,code)
    else:
        SubData.Menu_static(appid, code)
    mutex.release()
    # print SubData.data
    return

    # except Exception,e :
    #     url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&encrypt_type=%s&msg_signature=%s' % (http, signature, timestamp, nonce, openid, encrypt_type, Msg_Signature)
    #     print '数据推送失败%s\n%s'%(url,str(e))
    #     return
    #         # {'FAIL': 'FAIL', 'request_url': url, 'request_xml': encrypt_xml,'result_decrypt': str(e)}


if __name__ == '__main__':

        #  value_dict =  {"sqZnmJLVe6Wj14817116687582": {"MENUNAME": "我要咨询", "MenuId": "5510", "reply_content_type": "1",
        #                                 "reply_id": "596", "EventKey": "w47QDqJN76gi14773701362842",
        #                                 "get_replyword_url": "http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view?reply_type=4&token=mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL&id=596&app_key=100018&appid=wxfba8a23be3bb4304",
        #                                 "Event": "CLICK", "reply_content": "您好，您已进入人工客服！"}}
        # pushper_dict = {'pushhttp': 'http://api.biz.social-touch.com/app-base/wechat/monitor/appid/wxee4c032ab72c2faa?',
        #  'Third_appid': 'wxfb798f3c38b79c85', 'encodingAESKey': 'ed85e5ddefa3ade80d018178e34331ecsocialtouch',
        #  'General': {}, 'token': 'irPNHoJN', 'key': 'kUbn9su5aLeq14704030902593'}
        #
        # getvalue_dict = {'openid': 'o98Aet4Q8Sxk1K1VgREd8-A29xHE', 'authtype': '3', 'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get', 'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords', 'colseservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom', 'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list', 'app_key': '100018', 'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view', 'uniqueid': '827', 'reply_type': '4', 'content': '\xe5\xae\x8c\xe7\xbe\x8e\xe5\xba\x95\xe5\xa6\x86', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wxee4c032ab72c2faa', 'type': 2, 'checkservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey'}

        pushper_dict={'General': {}, 'token': 'irPNHoJN', 'encodingAESKey': 'ed85e5ddefa3ade80d018178e34331ecsocialtouch',
         'pushhttp': 'http://api.biz.social-touch.com/app-base/wechat/monitor/appid/wx8d97e09f8f2c3323?',
         'Third_appid': 'wxfb798f3c38b79c85'}

        getvalue_dict={'openid': 'okA7Sjua02GToyVHtQu-DNL9Xqmc', 'authtype': '3',
         'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get',
         'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords',
         'colseservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom',
         'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list', 'app_key': '100018',
         'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view', 'uniqueid': '369',
         'reply_type': '4', 'content': '\xe9\x9a\x90\xe4\xb8\x96', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL',
         'appid': 'wx8d97e09f8f2c3323', 'type': 1,
         'checkservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey'}
        value_dict={"甘南": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42565"}, "厦门": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42563"}, "有奖活动": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "83122"}, "游记": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "<a href=\"http://55782077.m.weimob.com/weisite/home?pid=55782077&bid=56772518&wechatid=fromUsername\">点击进入驴行者专栏</a>"}, "星座": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "43428"}, "新人福利": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "47653"}, "名单": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "212082"}, "精灵": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "84317"}, "神秘巴士": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "210908"}, "1元门票": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "50673"}, "2": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200044"}, "380优惠券": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "107145"}, "砍价": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200111"}, "手机上网": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42072"}, "td": {"reply_content_type": "2", "MENUNAME": "关键词，非菜单", "reply_content": "103392"}, "②": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200044"}, "免费": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "60456"}, "二": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200044"}, "cnn": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "104196"}, "台历": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "205710"}, "迪士尼": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "33105"}, "签证进度": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "<a href=\"http://m.lvmama.com/visa/progressQuery#1\">签证进度查询</a>"}, "审核": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "您好~亲登录官网http://dujia.lvmama.com/，点击上方【我的驴妈妈】→【金融中心】→【小驴白条】即可申请~小驴白条的具体事宜，请拨打驴妈妈热线10106060或者中银消费热线4008-295-195咨询哦~（上传照片建议使用电脑登录后进行提交）"}, "温泉": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "107293"}, "贷款": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "您好~亲登录官网http://dujia.lvmama.com/，点击上方【我的驴妈妈】→【金融中心】→【小驴白条】即可申请~小驴白条的具体事宜，请拨打驴妈妈热线10106060或者中银消费热线4008-295-195咨询哦~（上传照片建议使用电脑登录后进行提交）"}, "海岛": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "89169"}, "摩托": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "43422"}, "水果": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "48032"}, "天堂": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "106517"}, "名字": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "103351"}, "十一二": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "104194"}, "白条": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "您好~亲登录官网http://dujia.lvmama.com/，点击上方【我的驴妈妈】→【金融中心】→【小驴白条】即可申请~小驴白条的具体事宜，请拨打驴妈妈热线10106060或者中银消费热线4008-295-195咨询哦~（上传照片建议使用电脑登录后进行提交）"}, "秒杀": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200111"}, "签证": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "<a href=\"http://m.lvmama.com/visa/progressQuery#1\">签证进度查询</a>"}, "贰": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200044"}, "两": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "200044"}, "大闸蟹": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "102868"}, "1": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "107145"}, "3": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42072"}, "签证查询": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "<a href=\"http://m.lvmama.com/visa/progressQuery#1\">签证进度查询</a>"}, "三": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42072"}, "避暑": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "70390"}, "TD": {"reply_content_type": "2", "MENUNAME": "关键词，非菜单", "reply_content": "103392"}, "米其林": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "97658"}, "一": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "107145"}, "亲子": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "87331"}, "逆天": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "55819"}, "迪斯尼": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "33105"}, "秋色": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "102799"}, "绑定签到": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "42072"}, "出境签证": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "<a href=\"http://m.lvmama.com/visa/progressQuery#1\">签证进度查询</a>"}, "荷花": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "84315"}, "瞬间": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "50546"}, "21cake": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "使用规则：\n1.此优惠劵价值45元，包含小切块+咖啡1份；\n2.用户使用此优惠劵的必要条件为下单1磅蛋糕以上后方可使用；（可配送区域：北京、上海、杭州、广州、天津、苏州、无锡、深圳）\n3.领取优惠劵后，官网下单1磅蛋糕以上加入购物车，在自行添加一份小切块蛋糕与一份咖啡放入购物车后，在结算页面中使用优惠劵输入优惠劵码即可使用；\n4.订购方式：（1.官网下单2.APP下单3.微信端下单）\n5.兑换后的产品由廿一客负责随单配送，具体配送范围详见官网；\n6.使用期限为2017年4月30日；\n7.本劵码已全部测试均可使用，发放后不做任何退换；\n8.此劵码不可与其他优惠劵码同时使用，不可兑换现金；\n9.廿一客（上海）电子商务有限公司保留本劵码使用细则最终解释权；\n"}, "驴粉福利": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "83122"}, "小驴白条": {"reply_content_type": "1", "MENUNAME": "关键词，非菜单", "reply_content": "您好~亲登录官网http://dujia.lvmama.com/，点击上方【我的驴妈妈】→【金融中心】→【小驴白条】即可申请~小驴白条的具体事宜，请拨打驴妈妈热线10106060或者中银消费热线4008-295-195咨询哦~（上传照片建议使用电脑登录后进行提交）"}, "乡村": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "48030"}, "日本": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "58926"}, "消费": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "106687"}, "退订": {"reply_content_type": "2", "MENUNAME": "关键词，非菜单", "reply_content": "103392"}, "隐世": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "50547"}}
        # value_dict={"温泉": {"reply_content_type": "3", "MENUNAME": "关键词，非菜单", "reply_content": "107293"}}
        SubData.initData('wx8d97e09f8f2c3323')  ###初始化appid的统计,在Autoreply——Monior统一初始化
        for key in value_dict.keys():
            reply_relation = value_dict[key]
            to_xml = MesType.runtext_reply(key, getvalue_dict['openid'])
            pushdata(pushper_dict, getvalue_dict, key, reply_relation, to_xml)














