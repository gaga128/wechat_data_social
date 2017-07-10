#-*-coding:UTF-8-*-

#****************************************************************
# 获取素材列表
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-09
# Description:
#****************************************************************
import requests
import map_function
import get_autoreply
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def get_Menulist(dict):
    http = dict['Menulist_http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['appid'] = dict['appid']

    try:
        req = requests.get(http, para, timeout=5)
        # print req.text
        tmp_result = req.json()
        data = tmp_result['data']
        if tmp_result['msg']=='GetList Menu List Succes!':
            if data==[]:
                result='NULL'
            else:
                Menu_dict = map_function.menu_dict(data)
                if Menu_dict=={}:
                    result = 'NULL'
                else:
                    # print req.text
                    for menukey in Menu_dict.keys():
                        tmp_dict=Menu_dict[menukey]
                        # print tmp_dict
                        if tmp_dict['reply_id']=='0':
                            # print tmp_dict['reply_id']
                            # print tmp_dict
                            pass
                        else:
                            reply_dict,get_replyword_url=get_autoreply.get_replyword(dict, tmp_dict)

                            reply_dict['get_replyword_url']=get_replyword_url
                            Menu_dict[menukey]=reply_dict
                            # print Menu_dict[menukey]
                    result=Menu_dict
                    print '\n获取菜单%s'%req.url
                    print '菜单个数：%d'%len(Menu_dict)
                    print '菜单列表',json.dumps(Menu_dict, ensure_ascii=False)
        else:

            result = 'FAIL'
        # print result
        return result,req.url

    except Exception, e:
        result='FAIL'
        failurl = http + '?' + 'app_key=' + str(para['app_key']) +'&'+ 'token=' +str(para['token']) +'&'+ 'appid=' + str(para['appid'])
        print "获取自定义菜单失败，请检查接口参数或接口请求是否正常\n～%s\n%s" % (failurl, str(e))
        return result, '%s\n%s'%(failurl,str(e))





if __name__ == '__main__':
    dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wx8d97e09f8f2c3323',
             'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list','replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
             'reply_type': '4'})

    get_Menulist(dict)

