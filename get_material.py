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



def get_material(dict,material_id):
    http = dict['material_http']
    para = {}
    para['app_key'] = dict['app_key']
    para['token'] = dict['token']
    para['app_id'] = dict['appid']
    para['material_id'] = material_id
    try:
        req = requests.get(http,para, timeout=10)
        # print req.url
        # print req.text
        result = req.json()
        data = result['data']
        # print data
        if result['msg']=='Get Material Info Succes!':
            if data==[]:
                result='NULL'

            else:
                material_dict = map_function.material_dict(data)
                if material_dict=={}:
                    result='NULL'

                else:
                    result=material_dict

        else:
            result='NULL'
        # print result
        return result,req.url


    except Exception, e:
        failurl = http + '?' + 'app_key=' + str(para['app_key']) +'&'+ 'token=' + str(para['token']) +'&'+ 'app_id=' + str(para['app_id'])+'&'+'material_id='+str(para['material_id'])
        result = 'FAIL'
        print "获取素材失败，请检查接口参数或接口请求是否正常\n～%s\n%s" % (failurl, str(e))
        return  result,'%s\n%s'%(failurl,str(e))




if __name__ == '__main__':
    # dict=({'app_key':'100018','token':'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL','appid':'wx15426e0b8f518593','material_http':'http://coreapi.biz.social-touch.com:8081/material/v1/manager/list'})
    # get_material(dict)

    dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL', 'appid': 'wx2e675e890f78682f',
             'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get'})
    get_material(dict,'56426')
