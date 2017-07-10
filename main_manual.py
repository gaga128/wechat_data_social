#-*- encoding:utf-8 -*-
#****************************************************************
# 主函数
# Author     : lujia
# Version    : 1.0
# Date       : 2017-01-19
# Description:
#****************************************************************


import time
from datetime import datetime
import os
import manual_Pushdata
import ConfigParser
import sys
import random
import get_authorinfo
import MesType




cur_time=str(int(time.mktime(datetime.now().timetuple())))
dict = ({'app_key': '100018', 'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL','authorinfo_http': 'http://coreapi.biz.social-touch.com:8081/usercenter/v1/wechat/get-wechat-info-by-appid'})


def fake(appid,MsgType,ToUserName,FromUserName,CreateTime,MsgId,args):
    try:
        dict['appid']=appid
        author_result,author_url=get_authorinfo.get_authorinfo(dict)
        conf = ConfigParser.ConfigParser()
        conf.read(os.getcwd() + '/config/Per.conf')
        Third_appid = conf.get('permission', 'Third_appid').strip("'")
        token = conf.get('permission', 'token').strip("'")
        encodingAESKey = conf.get('permission', 'encodingAESKey').strip("'")

        value_dict = {}
        if author_result == '2' or author_result == '1':
            if author_result == '2':
                token = conf.get('permission', 'token').strip("'")
                value_dict['authtype']='3'
                value_dict['General'] = {}
                Third_pushhttp = conf.get('permission', 'Third_pushhttp').strip("'")
                pushhttp = Third_pushhttp.replace('appid/', str('appid/%s?' % appid)).strip("'")
            elif author_result == '1':
                value_dict['authtype']='1'
                General = {}
                uniqueid,token = get_authorinfo.get_uniauth(appid, '/appid/appidlist.txt')
                if uniqueid == 'NULL':
                    print '未获取到该appid默认的uniqueid和token，请输入该appid的uniqueid和token'
                    print '该公众号为普通授权，请输入token：'
                    token = raw_input()
                    print '该公众号为普通授权，请输入uniqueid：'
                    uniqueid= raw_input()
                else:
                    pass
                General['uniqueid']=uniqueid
                General['appid'] = appid
                value_dict['General'] = General
                Third_pushhttp = conf.get('permission', 'General_pushhttp').strip("'")
                pushhttp = Third_pushhttp

            value_dict['appid'] = appid
            value_dict['ToUserName'] = ToUserName
            value_dict['FromUserName'] = FromUserName
            value_dict['MsgType'] = MsgType
            value_dict['CreateTime'] = CreateTime
            value_dict['MsgId'] = MsgId

            value_dict=MesType.manual_pushtype(value_dict, MsgType, args)

            Third_appid=Third_appid
            encodingAESKey=encodingAESKey

            manual_Pushdata.pushdata(token, pushhttp, Third_appid, encodingAESKey, value_dict)

            time.sleep(0.5)

        elif author_result=='FAIL':
            print '获取授权信息失败，请查看您的appid相关授权信息\n%s'%author_url

        else:
            print '非第三方授权appid，请查看您的appid相关授权信息\n%s'%author_url


    except Exception,e:
        print '\n支持类型及输入参数顺序如下，请检查您的数据是否正确!\n事件类型（MsgType）：-t (文本消息) -i (图片消息) -vo（语音消息）-vi (视频消息) -sv (小视频消息) -lo（地理位置消息）& -li（链接消息）& -e（事件消息）%s\n' % e
        print '普通文本消息 :\t\t\tappid, MsgType, Content'
        print '图片消息 :\t\t\tappid, MsgType, MediaId,PicUrl'
        print '语音消息 :\t\t\tappid, MsgType, MediaId,Format'
        print '视频\小视频消息 :\t\t\tappid, MsgType, MediaId,ThumbMediaId'
        print '地理位置消息 :\t\t\tappid, MsgType, Location_X,Location_Y,Scale,Label'
        print '链接消息 :\t\t\tappid, MsgType, Title,Description,Url'
        print '关注\取消关注事件(subscribe\unsubscribe) :\t\tappid, MsgType, Event'
        print '已关注事件(subscribe\SCAN) :\tappid, MsgType, Event, EventKey, TICKET'
        print '上报地理位置事件(LOCATION) :\tappid, MsgType, Event, Latitude, Longitude, Precision'
        print '自定义菜单事件(CLICK\VIEW) :\tappid, MsgType, Event, EventKey, TICKET\n'
        print '示例：sh push.sh wx15426e0b8f518593-t 测试文本消息\n'


if __name__ == '__main__':
    para=sys.argv
    appid=para[1]
    MsgType=para[2]
    if MsgType=='-t':
        MsgType='text'
    elif MsgType=='-e':
        MsgType='event'
    elif MsgType=='-i':
        MsgType='image'
    elif MsgType=='-vo':
        MsgType='voice'
    elif MsgType=='-vi':
        MsgType='video'
    elif MsgType=='-sv':
        MsgType='shortvideo'
    elif MsgType=='-lo':
        MsgType='location'
    elif MsgType=='-li':
        MsgType='link'
    else:
        print '类型信息类型输入错误，请输入：-t (文本) -i (图片) -vo（语音）-vi (视频) -sv (小视频) -lo（地理位置）& -li（链接）& -e（事件）'
    # print MsgType
    args = para[3:]
    ToUserName='test_b08ab3638b88'
    CreateTime=cur_time
    MsgId = str(random.randint(1000000000000000000, 9999999999999999999))+str(int(cur_time))
    FromUserName=get_authorinfo.get_opeind(appid, '/appid/appidlist.txt')
    if FromUserName=='NULL':
        print '未获取到该appid默认的openid，请输入该appid真实的openid'
        FromUserName=raw_input()
    else:
        pass
    fake(appid,MsgType,ToUserName,FromUserName,CreateTime,MsgId,args)