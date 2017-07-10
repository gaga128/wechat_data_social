#-*-coding:UTF-8-*-

#****************************************************************
# 获取关键词列表
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************




import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
import map_function





def get_keywords(dict):
    http = dict['http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['appid'] = dict['appid']


    try:
        tmp_req = requests.get(http, para, timeout=5)
        tmp_result = tmp_req.json()
        tmp_data = tmp_result['data']
        totalCount = tmp_data['totalCount']
        # totalCount=1
        # print totalCount

        if totalCount>'0':
            tmp = float(totalCount) / 50
            tmp_page = int(tmp)
            result_list=[]
            globals = {'true': 0,'null':0}
            if '0'<totalCount<='50':
                para['page_num'] = '50'
                para['page'] = '1'
                # print para
                req=requests.get(http,para,timeout=5)
                result = json.loads(req.content)
                # print result
                data = result['data']
                # AutoReply = data['AutoReply']
                AutoReply = json.dumps(data['AutoReply'], ensure_ascii=False)
                result_list = result_list + eval(AutoReply, globals)
                # print result_list
            elif totalCount>'50' and tmp==tmp_page:
                page = tmp_page + 1
                for i in  range(1,page):
                    # print i
                    para['page_num']='50'
                    para['page']=i
                    req = requests.get(http, para, timeout=5)
                    result = json.loads(req.content)
                    # print result
                    data = result['data']
                    # AutoReply = data['AutoReply']
                    AutoReply = json.dumps(data['AutoReply'], ensure_ascii=False)
                    result_list = result_list + eval(AutoReply, globals)
                    # print result_list
            elif totalCount > '50' and tmp != tmp_page:
                page=tmp_page+2
                for i in range(1, page):
                    # print i
                    para['page_num'] = '50'
                    para['page'] = i
                    req = requests.get(http, para, timeout=5)
                    result = json.loads(req.content)
                    # print req.url
                    data = result['data']
                    # AutoReply = data['AutoReply']
                    AutoReply = json.dumps(data['AutoReply'], ensure_ascii=False)
                    # print AutoReply
                    result_list = result_list + eval(AutoReply, globals)
                    # print "resylt_list",result_list
            keymap=map_function.key_dict(result_list)
            print '\n获取关键词：%s'%tmp_req.url
            print '关键词个数：%d'%len(keymap)
            print '关键词列表:',json.dumps(keymap,ensure_ascii=False)
            if keymap=={}:
                result='NULL'
            else:
                result=keymap
        else:
            print 'totalCount=0,无关键词配置!'
            result = 'NULL'
        return result, tmp_req.url
    except Exception,e:
        result='FAIL'
        failurl = http+'?'+'app_key='+str(para['app_key'])+'&'+'token='+str(para['token'])+'&'+'appid='+str(para['appid'])
        print "获取关键词失败，请检查接口参数或接口请求是否正常\n～%s\n%s"%(failurl,str(e))

        return result,'%s\n%s'%(failurl,str(e))







if __name__ == '__main__':
    dict=({'app_key':'100018','token':'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL','appid':'wxb0c46bde58a8bf34','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})
    get_keywords(dict)

    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxfecdf5deba3ddf79','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})
    # get_keywords({'app_key':'100001','token':'6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR','appid':'wxc79c843b493be477','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'})