#-*- encoding:utf-8 -*-
#****************************************************************
# 请求接口
# Author     : lujia
# Version    : 1.0
# Date       : 2017-01-19
# Description:
#****************************************************************



from lxml import etree
import time
from xml.sax.saxutils import unescape
import collections
import random
import requests
import hashlib
import MesCrypt
import MesType
import send_emails


def pushdata(token, http, Third_appid, encodingAESKey,  value_dict):
    authtype = value_dict['authtype']
    General = value_dict['General']
    Unencrypt_xml = etree.tostring(MesType.text_event(value_dict), encoding="UTF-8")
    timestamp = etree.fromstring(Unencrypt_xml).find('CreateTime').text
    openid=etree.fromstring(Unencrypt_xml).find('FromUserName').text
    # print token
    if authtype == '1':
        msg_encrypt = Unencrypt_xml

    elif authtype == '3':
        msg_encrypt = MesCrypt.encrypt(encodingAESKey, Third_appid, Unencrypt_xml)  ######XML数据加密
    else:
        send_emails.send_failEmail('该种授权类型不属于已知类型%s,请联系相关人员进行添加' % str(authtype))
        return {'authtype': authtype, 'request_url': http, 'request_xml': Unencrypt_xml,'result_decrypt': '该种授权类型不属于已知类型%s,请联系相关人员进行添加' % str(authtype)}
    nonce = str(random.randint(1000000000, 9999999999))
    encrypt_type = 'aes'
    signstr = ''.join(sorted([token, timestamp, nonce]))      ####按照升序排列,拼成字符串
    signature = hashlib.sha1(signstr).hexdigest()
    Msg_signstr = ''.join(sorted([token, timestamp, nonce, msg_encrypt]))
    Msg_Signature = hashlib.sha1(Msg_signstr).hexdigest()
    # print 'signature:%s  &  Msg_Signature:%s'%(signature, Msg_Signature)
    data = collections.OrderedDict()
    ToUserName=etree.fromstring(Unencrypt_xml).find('ToUserName').text
    if authtype == '3':
        data['ToUserName'] = '<![CDATA[%s]]>' % ToUserName
        data['Encrypt'] = '<![CDATA[%s]]>' % msg_encrypt
        data['from'] = '<![CDATA[QA-check]]>'
        ele = etree.Element('xml')
        for ke, val in data.items():
            child = etree.Element(ke)
            child.text = str(val)
            ele.append(child)
        encrypt_xml = unescape(etree.tostring(ele))
        url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&encrypt_type=%s&msg_signature=%s' % (http, signature, timestamp, nonce, openid, encrypt_type, Msg_Signature)
    elif authtype == '1':
        encrypt_xml = Unencrypt_xml
        appid = General['appid']
        uniqueid = General['uniqueid']
        url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&uniqueid=%s&appid=%s' % (http, signature, timestamp, nonce, openid, uniqueid, appid)

    # print url
    # print encrypt_xml

    try:

        headers = {'Content-Type': 'text/xml'}
        starttime = time.time()
        req = requests.post(url=url, data=encrypt_xml, headers=headers, timeout=10)
        # print req.url
        # print encrypt_xml
        result = req.text
        nowtime=time.time()-starttime
        print '\n****Request_URL****: \n%s\n****Unencrypt_XML****: \n%s\n****Request_EncryptXML****: \n%s'%(url,Unencrypt_xml,encrypt_xml)
        if req.status_code==200:
            if result:
                if authtype == '3':
                    MesCrypt.decrypt(encodingAESKey, Third_appid, result)
                elif authtype == '1':
                    MesCrypt.nodecrypt(result)
                else:
                    result_statu = 'FAIL'
                    result_decrypt = result
            else:
                print '\nSTATUS=200,请求成功，无返回结果!'
                return {'NULL':'NULL','request_url':req.url,'request_xml':encrypt_xml,'result_decrypt':'STATUS=200,请求成功，无返回结果!'}
        print '\n*Request time: %s ms'%int(nowtime*1000)
        print '*Status_code: %s\n'%req.status_code
    except Exception,e :
        url = '%ssignature=%s&timestamp=%s&nonce=%s&openid=%s&encrypt_type=%s&msg_signature=%s' % (http, signature, timestamp, nonce, openid, encrypt_type, Msg_Signature)
        print '数据推送失败%s\n%s'%(url,str(e))
        return {'FAIL': 'FAIL', 'request_url': url, 'request_xml': encrypt_xml,'result_decrypt': str(e)}





if __name__ == '__main__':

    value_dict = {'appid': 'wxee4c032ab72c2faa', 'FromUserName': 'o98Aet4Q8Sxk1K1VgREd8-A29xHE', 'authtype': '3',
                  'uniqueid': '827', 'authtoken': 'XahjqbYe', 'ToUserName': 'test_b08ab3638b88',
                  'CreateTime': '1484731439', 'Content': u'会员中心', 'MsgId': '637687297426192629111', 'MsgType': 'text'}

    pushdata('irPNHoJN', 'http://api.biz.social-touch.com/app-base/wechat/monitor/appid/wxee4c032ab72c2faa?',
             'wxfb798f3c38b79c85', "ed85e5ddefa3ade80d018178e34331ecsocialtouch", '3',value_dict)



###MsgId需要唯一，如果已经存在，则无返回结果












