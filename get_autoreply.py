#-*-coding:UTF-8-*-

#****************************************************************
# 获取素材列表
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-09
# Description:
#****************************************************************
import requests



def get_replyword(dict,menu_dict):
    http = dict['replywords_http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['appid'] = dict['appid']
    para['reply_type'] = dict['reply_type']
    para['id'] = menu_dict['reply_id']

    try:
        req = requests.get(http,para, timeout=5)
        # print req.url
        # print req.text
        result = req.json()
        data = result['data']
        if result['code']==200:
            if type(data)==type(dict) :
                if data=={}:
                    # print '该菜单的reply_id无对应回复信息',req.url
                    menu_dict['replyword']='NULL'
                else:
                    menu_dict['reply_content']=data['reply_content']

                    menu_dict['reply_content_type']=str(data['reply_content_type'])

            else:
                # print '该菜单的reply_id无对应回复信息',req.url
                menu_dict['replyword'] = 'NULL'
        else:
            menu_dict['replyword'] = 'FAIL'

        return menu_dict,req.url

    except Exception,e:
        failurl ='%s?app_key=%s&token=%s&appid=%s&reply_type=%s&id=%s'%(http,para['app_key'],para['token'] ,para['appid'],para['reply_type'],para['id'])
        print '根据reply_id获取菜单自动回复内容的接口请求失败',failurl
        menu_dict['replyword'] = 'FAIL'
        return menu_dict,failurl



def get_defaultreply(dict,reply_type):
    http = dict['replywords_http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['appid'] = dict['appid']
    para['reply_type'] = reply_type

    try:

        defauto_reply={}
        req = requests.get(http,para, timeout=5)
        print req.url
        # print req.text
        result = req.json()
        data = result['data']
        if result['code']==200:
            if type(data)==type(dict) :
                if data=={}:
                    # print '该菜单的reply_id无对应回复信息',req.url
                    defauto_reply['reply_content']='NULL'
                    defauto_reply['is_open'] ='0'
                else:
                    defauto_reply['reply_content']=str(data['reply_content'])
                    defauto_reply['reply_content_type']=str(data['reply_content_type'])
                    defauto_reply['is_open']=str(data['is_open'])

            else:
                # print '该菜单的reply_id无对应回复信息',req.url
                defauto_reply['reply_content'] = 'NULL'
                defauto_reply['is_open'] = '0'
        else:
            defauto_reply['reply_content'] = 'FAIL'
        # print defauto_reply
        return defauto_reply,req.url

    except Exception,e:
        failurl ='%s?app_key=%s&token=%s&appid=%s&reply_type=%s&id=%s'%(http,para['app_key'],para['token'] ,para['appid'],para['reply_type'],para['id'])
        print '根据reply_id获取菜单自动回复内容的接口请求失败',failurl
        defauto_reply['replyword'] = 'FAIL'
        return defauto_reply,failurl


if __name__ == '__main__':
    # dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wx15426e0b8f518593','replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view','reply_type':'4'})
    # menu_dict={'MenuId': '7988', 'reply_id': '373', 'Event': 'CLICK', 'EventKey': 'yu3FxPd8Ehzd14871467924875'}
    # menu_dict={'MenuId': '7992', 'reply_id': '3453', 'Event': 'CLICK', 'EventKey': 'iL4nqUZb3KJC14871521270646'}
    # get_replyword(dict,menu_dict)
    dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wx15426e0b8f518593',
             'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
             'reply_type': '1'})
    get_defaultreply(dict)



