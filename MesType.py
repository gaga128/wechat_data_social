#-*-coding:UTF-8-*-

#****************************************************************
# 消息类型
# Author     : lujia
# Version    : 1.0
# Date       : 2017-01-19
# Description:
#****************************************************************



from datetime import datetime
import time
from lxml import etree
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')


tag='xml'

unix_time = time.mktime(datetime.now().timetuple())
inc = 0
def text_event(dict):
    MsgTypelist = ['text', 'image', 'voice', 'video', 'shortvideo', 'location','link']
    global inc
    inc=inc+1
    if dict['MsgType'] in MsgTypelist:
        runtext(dict)
        return runtext(dict)
    elif dict['MsgType'] == 'event':
        runevent(dict)
        return runevent(dict)
    else:
        print '该种消息类型或事件暂不支持，如需使用请告知相关人员进行添加～～'

def runtext(dict):
    try:
        to_xml=etree.Element(tag)
        if dict.has_key('ToUserName') and dict['ToUserName']!=str(''):
            # print dict['ToUserName']
            ToUserName_text=dict['ToUserName']
            ToUserName=etree.SubElement(to_xml,'ToUserName')
            ToUserName.text=etree.CDATA(ToUserName_text)
        else:
            ToUserName = etree.SubElement(to_xml, 'ToUserName')
            ToUserName.text = etree.CDATA('test_b08ab3638b88')

        if dict.has_key('FromUserName') and dict['FromUserName']!=str(''):
            FromUserName_text = dict['FromUserName']
            FromUserName = etree.SubElement(to_xml, 'FromUserName')
            FromUserName.text = etree.CDATA(FromUserName_text)
        else:
            FromUserName = etree.SubElement(to_xml, 'FromUserName')
            FromUserName.text = etree.CDATA('oCWncs00chDdcvYG4xCDnzz35tR4')

        if dict.has_key('CreateTime') and dict['CreateTime']!=str(''):
            CreateTime_text = dict['CreateTime']
            CreateTime = etree.SubElement(to_xml, 'CreateTime')
            CreateTime.text = str(int(CreateTime_text))
        else:
            CreateTime = etree.SubElement(to_xml, 'CreateTime')
            CreateTime.text =str(int(unix_time))

        if dict.has_key('MsgId') and dict['MsgId'] != str(''):
            MsgId_text = dict['MsgId']
            MsgId = etree.SubElement(to_xml, 'MsgId')
            MsgId.text = MsgId_text
        else:
            MsgId = etree.SubElement(to_xml, 'MsgId')
            MsgId.text = str(random.randint(1000000000000000000, 9999999999999999999))+str(int(unix_time))

        MsgType_text =dict['MsgType']
        MsgType = etree.SubElement(to_xml, 'MsgType')
        MsgType.text = etree.CDATA(MsgType_text)

        if dict['MsgType']=='text':
            Content_text = unicode(dict['Content'])
            Content = etree.SubElement(to_xml, 'Content')
            Content.text = etree.CDATA(Content_text)

        elif dict['MsgType'] == 'image':
            MediaId_text = dict['MediaId']  ####调取多媒体文件下载接口拉取数据
            MediaId = etree.SubElement(to_xml, 'MediaId')
            MediaId.text = etree.CDATA(MediaId_text)

            PicUrl_text = unicode(dict['PicUrl'])
            PicUrl = etree.SubElement(to_xml, 'PicUrl')
            PicUrl.text = etree.CDATA(PicUrl_text)

        elif dict['MsgType'] == 'voice':
            MediaId_text = dict['MediaId']  ####调取多媒体文件下载接口拉取数据
            MediaId = etree.SubElement(to_xml, 'MediaId')
            MediaId.text = etree.CDATA(MediaId_text)

            Format_text = unicode(dict['Format'])  ####语音格式，如amr，speex等
            Format = etree.SubElement(to_xml, 'Format')
            Format.text = etree.CDATA(Format_text)

        elif dict['MsgType'] == 'video' or dict['MsgType'] == 'shortvideo':
            MediaId_text = dict['MediaId']  ####调取多媒体文件下载接口拉取数据
            MediaId = etree.SubElement(to_xml, 'MediaId')
            MediaId.text = etree.CDATA(MediaId_text)

            ThumbMediaId_text =unicode(dict['ThumbMediaId'])  ####调取多媒体文件下载接口拉取数据
            ThumbMediaId = etree.SubElement(to_xml, 'ThumbMediaId')
            ThumbMediaId.text = etree.CDATA(ThumbMediaId_text)


        elif dict['MsgType'] == 'location':
            Location_X_text = dict['Location_X']  ####地理位置维度 浮点
            Location_X = etree.SubElement(to_xml, 'Location_X')
            Location_X.text = Location_X_text

            Location_Y_text = dict['Location_Y']  ####地理位置经度  浮点
            Location_Y = etree.SubElement(to_xml, 'Location_Y')
            Location_Y.text = Location_Y_text

            Scale_text = dict['Scale'] ####缩放大小，整型
            Scale = etree.SubElement(to_xml, 'Scale')
            Scale.text = Scale_text

            Label_text =unicode(dict['Label'])  ####地理位置信息
            Label = etree.SubElement(to_xml, 'Label')
            Label.text = etree.CDATA(Label_text)

        elif dict['MsgType'] == 'link':
            Title_text = unicode(dict['Title'])
            Title = etree.SubElement(to_xml, 'Title')
            Title.text = etree.CDATA(Title_text)

            Description_text =unicode(dict['Description'])
            Description = etree.SubElement(to_xml, 'Description')
            Description.text = etree.CDATA(Description_text)
            Url_text =unicode(dict['Url'])
            Url = etree.SubElement(to_xml, 'Url')
            Url.text = etree.CDATA(Url_text)

        FROM_text = 'QA-check'
        FROM = etree.SubElement(to_xml, 'FROM')
        FROM.text = etree.CDATA(FROM_text)


        # print 'Request_XML%s' % etree.tostring(to_xml)
        return to_xml
    except Exception, e:
        print '请检查您的初始数据填写是否正确%s---MesType'%e




def runevent(dict):
    # try:

        to_xml = etree.Element(tag)
        if dict.has_key('ToUserName') and dict['ToUserName'] != str(''):
            # print dict['ToUserName']
            ToUserName_text = dict['ToUserName']
            ToUserName = etree.SubElement(to_xml, 'ToUserName')
            ToUserName.text = etree.CDATA(ToUserName_text)
        else:
            ToUserName = etree.SubElement(to_xml, 'ToUserName')
            ToUserName.text = etree.CDATA('test_b08ab3638b77')

        if dict.has_key('FromUserName') and dict['FromUserName'] != str(''):
            FromUserName_text = dict['FromUserName']
            FromUserName = etree.SubElement(to_xml, 'FromUserName')
            FromUserName.text = etree.CDATA(FromUserName_text)
        else:
            FromUserName = etree.SubElement(to_xml, 'FromUserName')
            FromUserName.text = etree.CDATA('oCWncs00chDdcvYG4xCDnzz35tR4')

        if dict.has_key('CreateTime') and dict['CreateTime'] != str(''):
            CreateTime_text = dict['CreateTime']
            CreateTime = etree.SubElement(to_xml, 'CreateTime')
            CreateTime.text = str(int(CreateTime_text))
        else:
            CreateTime = etree.SubElement(to_xml, 'CreateTime')
            CreateTime.text = str(int(unix_time))

        MsgType_text = dict['MsgType']
        MsgType = etree.SubElement(to_xml, 'MsgType')
        MsgType.text = etree.CDATA(MsgType_text)

        Event_text = dict['Event']
        Event = etree.SubElement(to_xml, 'Event')
        Event.text = etree.CDATA(Event_text)

        if dict.has_key('EventKey') and dict['Event']=='subscribe':
            EventKey_text = dict['EventKey']
            EventKey = etree.SubElement(to_xml, 'EventKey')
            EventKey.text = etree.CDATA(EventKey_text)
            Ticket_text = dict['Ticket']
            Ticket = etree.SubElement(to_xml, 'Ticket')
            Ticket.text = etree.CDATA(Ticket_text)

        elif dict['Event'] == 'CLICK' or dict['Event'] =='VIEW':
            EventKey_text = dict['EventKey']
            EventKey = etree.SubElement(to_xml, 'EventKey')      ####事件KEY值，与自定义菜单接口中KEY值或者设置的跳转URL
            EventKey.text = etree.CDATA(EventKey_text)

        elif dict['Event'] == 'SCAN':                              ######扫描带参数的二维码
            EventKey_text = dict['EventKey']
            EventKey = etree.SubElement(to_xml, 'EventKey')
            EventKey.text = etree.CDATA(EventKey_text)

            Ticket_text = dict['Ticket']
            Ticket = etree.SubElement(to_xml, 'Ticket')
            Ticket.text = etree.CDATA(Ticket_text)

        elif dict['Event'] == 'LOCATION':
            Latitude_text = dict['Latitude']
            Latitude = etree.SubElement(to_xml, 'Latitude')         ####地理位置纬度
            Latitude.text = Latitude_text

            Longitude_text = dict['Longitude']
            Longitude = etree.SubElement(to_xml, 'Longitude')       ####地理位置经度
            Longitude.text = Longitude_text

            Precision_text = dict['Precision']
            Precision = etree.SubElement(to_xml, 'Precision')       ####地理位置精度
            Precision.text = Precision_text
        FROM_text = 'QA-check'
        FROM = etree.SubElement(to_xml, 'FROM')
        FROM.text = etree.CDATA(FROM_text)

        # print 'Request_XML%s'%etree.tostring(to_xml)
        return to_xml
    # except Exception,e:
    #     print '请检查您的初始数据填写是否正确%s---MesType'%e





def runtext_reply(keys,openid):
    try:
        to_xml = etree.Element('xml')
        ToUserName = etree.SubElement(to_xml, 'ToUserName')
        ToUserName.text = etree.CDATA('test_b08ab3638b88')
        FromUserName_text=openid
        FromUserName = etree.SubElement(to_xml, 'FromUserName')
        FromUserName.text = etree.CDATA(FromUserName_text)
        CreateTime = etree.SubElement(to_xml, 'CreateTime')
        CreateTime.text = str(int(unix_time))
        MsgId = etree.SubElement(to_xml, 'MsgId')
        MsgId.text = str(random.randint(1000000000000000000, 9999999999999999999))+str(int(unix_time))
        MsgType_text = 'text'
        MsgType = etree.SubElement(to_xml, 'MsgType')
        MsgType.text = etree.CDATA(MsgType_text)

        Content_text = unicode(keys, encoding='utf-8')
        Content = etree.SubElement(to_xml, 'Content')
        Content.text = etree.CDATA(Content_text)

        FROM_text = 'QA-check'
        FROM = etree.SubElement(to_xml, 'FROM')
        FROM.text = etree.CDATA(FROM_text)
        # print etree.tostring(to_xml)
        return to_xml
    except Exception, e:
        print '请检查您的初始数据填写是否正确%s---MesType'%e




def runevent_reply(Menu_reply):
    try:

        to_xml = etree.Element(tag)
        ToUserName = etree.SubElement(to_xml, 'ToUserName')
        ToUserName.text = etree.CDATA('test_b08ab3638b77')

        FromUserName = etree.SubElement(to_xml, 'FromUserName')
        if Menu_reply.has_key('openid'):
            FromUserName.text = etree.CDATA(Menu_reply['openid'])
        else:
            FromUserName.text = etree.CDATA('opB1Nt_Uzy3ahu_ODsHhZr3Z04fQ')

        CreateTime = etree.SubElement(to_xml, 'CreateTime')
        CreateTime.text = str(int(unix_time))

        MsgType = etree.SubElement(to_xml, 'MsgType')
        MsgType.text = etree.CDATA('event')

        Event_text = Menu_reply['Event']
        Event = etree.SubElement(to_xml, 'Event')
        Event.text = etree.CDATA(Event_text)
        if Menu_reply.has_key('EventKey'):
            EventKey_text = unicode(Menu_reply['EventKey'])
            EventKey = etree.SubElement(to_xml, 'EventKey')
            EventKey.text = etree.CDATA(EventKey_text)

        if Event_text=='VIEW':
            MenuId_text=Menu_reply['MenuId']
            MenuId=etree.SubElement(to_xml,'MenuId')
            MenuId.text=etree.CDATA(MenuId_text)

        FROM_text = 'QA-check'
        FROM = etree.SubElement(to_xml, 'FROM')
        FROM.text = etree.CDATA(FROM_text)

        # print etree.tostring(to_xml)
        return to_xml
    except Exception,e:
        print '请检查您的初始数据填写是否正确%s---MesType'%e




def manual_pushtype(value_dict,MsgType,args):
    if MsgType == 'text':
        value_dict['Content'] = args[0]
    elif MsgType == 'event':
        Event = args[0]
        value_dict['Event'] = args[0]
        if Event == 'subscribe' and len(args) == 1:
            pass
        elif Event == 'subscribe' and len(args) > 1:
            value_dict['EventKey'] = args[1]
            value_dict['Ticket'] = args[2]
        elif Event == 'CLICK' or Event == 'VIEW':
            value_dict['EventKey'] = args[1]

        elif Event == 'SCAN':
            value_dict['EventKey'] = args[1]
            value_dict['Ticket'] = args[2]

        elif Event == 'LOCATION':
            value_dict['Latitude'] = args[1]
            value_dict['Longitude'] = args[2]
            value_dict['Precision'] = args[3]
        else:
            print '该种事件类型暂不支持%s' % Event

    elif MsgType == 'image':
        value_dict['MediaId'] = args[0]
        value_dict['PicUrl'] = args[1]

    elif MsgType == 'voice':
        value_dict['MediaId'] = args[0]  ####调取多媒体文件下载接口拉取数据
        value_dict['Format'] = args[1]  ####语音格式，如amr，speex等

    elif MsgType == 'video' or MsgType == 'shortvideo':
        value_dict['MediaId'] = args[0]  ####调取多媒体文件下载接口拉取数据
        value_dict['ThumbMediaId'] = args[1]  ####调取多媒体文件下载接口拉取数据

    elif MsgType == 'location':
        value_dict['Location_X'] = args[0]  ####地理位置维度 浮点
        value_dict['Location_Y'] = args[1]  ####地理位置经度  浮点
        value_dict['Scale'] = args[2]  ####缩放大小，整型
        value_dict['Label'] = args[3]  ####地理位置信息

    elif MsgType == 'link':
        value_dict['Title'] = args[0]
        value_dict['Description'] = args[1]
        value_dict['Url'] = args[2]
    return value_dict


if __name__=='__main__':
    # reply='{"ewm": "我有活", "你好": "我有活", "ww": "我有", "ghg": "我有", "aas": "我有", "cds": "我有活", "ded": "我有活"}'
    # reply={'ewm': '\xe6\x88\x91\xe6\x9c\x89\xe6\xb4\xbb', '\xe4\xbd\xa0\xe5\xa5\xbd': '\xe6\x88\x91\xe6\x9c\x89\xe6\xb4\xbb', 'ww': '\xe6\x88\x91\xe6\x9c\x89', 'ghg': '\xe6\x88\x91\xe6\x9c\x89', 'aas': '\xe6\x88\x91\xe6\x9c\x89', 'cds': '\xe6\x88\x91\xe6\x9c\x89\xe6\xb4\xbb', 'ded': '\xe6\x88\x91\xe6\x9c\x89\xe6\xb4\xbb'}
    # dict={'app_key': '100001', 'token': '6d4UV3CZiiHhdeXunu1B4M4CyEfJYYhR', 'appid': 'wx15426e0b8f518593','http':'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/keywords'}
    # runtext_reply('e')

    # Menu_reply={'menu_id': '4563', 'MenuId': '4563', 'is_del': 'N', 'reply_id': '751', 'EventKey': 'http://app.biz.social-touch.com/svip/employee/index?`pf_uid`=2351_614&`pf_type`=3', 'Event': 'VIEW'}
    Menu_reply={'is_del': 'N', 'menu_id': '7988', 'reply_id': '3455', 'Event': 'CLICK', 'EventKey': 'uVu4jKQ0SdGN14869794365184'}
    runevent_reply(Menu_reply)
    # text_event({'ToUserName':'gh_b08ab3638b88','FromUserName':'oCWncs00chDdcvYG4xCDnzz35tR4','CreateTime':'','Content':u'你好','MsgId':'6376872974261926294','MsgType':'text'})
    # text_event({'appid':'wx15426e0b8f518593','ToUserName':'gh_b08ab3638b88','FromUserName':'oCWncs00chDdcvYG4xCDnzz35tR4','CreateTime':'1484731439','MsgType':'event','Event':'subscribe'})
    # text_event({'appid':'wx15426e0b8f518593','Content':u'你好','MsgType':'text'})
    # text_event({'appid':'wx15426e0b8f518593','MsgType':'event','Event':'subscribe'})













######最初想用excel的方式控制数据输入，用了字典转换xml的形式进行数据准备，现废弃#################################################
# def runtext():
#     # for i in range(0,int(1)):
#     # global inc,totalCount,errorCount
#     # mutex.acquire()
#     inc=0
#     para =collections.OrderedDict()
#     inc += 1
#     para['ToUserName'] ='<![CDATA[%s]]>'%('gh_b08ab3638b88')
#     para['FromUserName'] = '<![CDATA[%s]]>'%('oCWncs00chDdcvYG4xCDnzz35tR4')
#     para['CreateTime'] ='1484731439'
#     para['MsgType'] = '<![CDATA[%s]]>'%'text'
#     para['Content'] = '<![CDATA[%s]]>' % '123'
#     # para['MsgId'] = str(random.randint(9000000000000000000, 9999999999999999999))
#     para['MsgId']='6376872974261926294'
#     # print para
#     to_xml = etree.Element(tag)
#     for key, val in para.items():
#         child = etree.Element(key)
#         child.text = str(val)
#         to_xml.append(child)
#     print unescape(etree.tostring(to_xml,pretty_print=True))
#     return to_xml

#