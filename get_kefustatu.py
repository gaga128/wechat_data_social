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
reload(sys)
sys.setdefaultencoding("UTF-8")





def get_keywords(dict):
    http = dict['http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['openid'] = dict['openid']
    para['uniqueid']=dict['uniqueid']
    para['type']=dict['type']

    para['content']=dict['content']




    try:
        tmp_req = requests.get(http, para, timeout=5)
        print tmp_req.content


    except Exception,e:
        result='FAIL'
        failurl = http+'?'+'app_key='+str(para['app_key'])+'&'+'token='+str(para['token'])+'&'+'appid='+str(para['appid'])
        print "获取关键词失败，请检查接口参数或接口请求是否正常\n～%s\n%s"%(failurl,str(e))

        return result,'%s\n%s'%(failurl,str(e))







if __name__ == '__main__':
    dict=({'app_key':'100018','token':'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL','openid':'onPq7jmg6sSzUOg77mwyCBjdXIzI','uniqueid':716,'type':1,'content':'冬暖','http':'http://coreapi.biz.social-touch.com:8081/customeservice/1.0/interface/matchkey'})
    get_keywords(dict)

    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxfecdf5deba3ddf79','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})
    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxc79c843b493be477','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})