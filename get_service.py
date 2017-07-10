#-*-coding:UTF-8-*-

#****************************************************************
# 获取关键词列表
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************
# 返回状态码说明
# 201 标示请求成功 未进入客服
# 200 表示请求成功 已进入客服
# 400 表示请求失败



import requests
import json
import sys
import json
reload(sys)
sys.setdefaultencoding("UTF-8")

def get_service(getvalue_dict):
    http = getvalue_dict['checkservice']
    para = {}
    para['app_key'] = getvalue_dict['app_key']
    para['token'] = getvalue_dict['token']
    para['openid'] = getvalue_dict['openid']
    para['uniqueid']=getvalue_dict['uniqueid']
    para['type']=getvalue_dict['type']
    para['content']=getvalue_dict['content']


    try:
        tmp_req = requests.get(http, para, timeout=5)
        # print tmp_req.url
        tmp_result=tmp_req.json()
        # print tmp_req.url
        # print tmp_result

        if tmp_result['code']==400:
            result='请求失败'
        elif tmp_result['code']==201:
            result='未进入客服'
        elif tmp_result['code']==200:
            result='进入客服'

        else:
            result='请求失败'

        return result,str(tmp_req.url)

    except Exception,e:
        result='请求失败'
        failurl = str(http)+'?app_key='+str(para['app_key'])+'&'+'token='+str(para['token'])+'&'+'openid='+str(para['openid'])+'&'+'uniqueid='+str(para['uniqueid'])+'&'+'type='+str(para['type'])+'&'+'content='+str(para['content'])
        print "判断客服状态失败，请检查接口参数或接口请求是否正常\n%s\n错误原因：%s"%(failurl,str(e))

        return result,'%s\n%s'%(failurl,str(e))





def exitservice(getvalue_dict):
    http = getvalue_dict['colseservice']
    para = {}
    para['app_key'] = getvalue_dict['app_key']
    para['token'] = getvalue_dict['token']
    para['openid'] = getvalue_dict['openid']
    para['uniqueid'] = getvalue_dict['uniqueid']
    try:
        tmp_req = requests.get(http, para, timeout=5)
        tmp_result = tmp_req.json()
        # print tmp_req.url
        # print tmp_result
        if tmp_result['code'] == 400:
            result = '请求失败'
        elif tmp_result['code'] == 201:
            result = '未进入客服'
        elif tmp_result['code'] == 200:
            result = '进入客服'

        else:
            result = '请求失败'

        return result, str(tmp_req.url)
    except Exception, e:
        result = '请求失败'
        failurl = http + '?' + 'app_key=' + str(para['app_key']) + '&' + 'token=' + str(para['token']) + '&' + 'openid=' + str(para['openid']) + '&' + 'uniqueid=' + str(para['uniqueid'])
        print "退出客服状态失败失败，请检查接口参数或接口请求是否正常\n%s\n错误原因：%s" % (failurl, str(e))

        return result, '%s\n%s' % (failurl, str(e))





if __name__ == '__main__':
    # getvalue_dict=({'app_key':'100018','token':'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL','openid':'onPq7jmg6sSzUOg77mwyCBjdXIzI','uniqueid':716,'checkservice':'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey',
    #                 'colseservice':'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom','type':'1','content':'test'})
    getvalue_dict={'openid': 'oBLDkjqjOR4bNIb3DLBqWIPtBQU0', 'authtype': '1', 'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get', 'http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords', 'colseservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/closecustom', 'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list', 'app_key': '100018', 'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view', 'uniqueid': '811', 'authtoken': 'LxclIRNR', 'reply_type': '4', 'content': '人头马哪里有卖', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wxbbf869c63e49ff10', 'type': 1, 'checkservice': 'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey'}



    get_service(getvalue_dict)
    exitservice(getvalue_dict)

    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxfecdf5deba3ddf79','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})
    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxc79c843b493be477','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})