#-*-coding:UTF-8-*-
#****************************************************************
#推送关键词并对比返回结果是否与配置一致
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-07
# Description:
#****************************************************************

from send_emails import sendEmail
from lxml import etree
import get_material
import writelog




def Reply_Compare(reply_relation,key, getvalue_dict, pushinfo_dict):
    request_url = pushinfo_dict['request_url']
    request_xml = pushinfo_dict['request_xml']
    Unencrypt_xml=pushinfo_dict['Unencrypt_xml']
    request_xml=request_xml+'\n'+Unencrypt_xml
    result_decrypt = pushinfo_dict['result_decrypt']
    replycontent_type=reply_relation['reply_content_type']
    MENUNAME=reply_relation['MENUNAME']
    print "key:%s"%str(key)
    inputword = '%s,\t菜单名称：%s' % (str(key), str(MENUNAME))
    # try:
    if pushinfo_dict['result_statu']=='FAIl':
        print '接口推送数据失败！'
        sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']),'接口推送数据失败！')
        writelog.errorlog(request_url + request_xml, '接口推送数据失败！',result_decrypt)
        result_sign = 'fail'
    elif pushinfo_dict['result_statu'] == 'NULL':
        print '接口推送数据请求成功，无返回结果'
        # sendEmail(request_url, request_xml, result_decrypt, str(inputword),str(reply_relation['reply_content']),'接口推送数据请求成功，无返回结果')
        writelog.errorlog(request_url + request_xml, '接口推送数据请求成功，无返回结果', result_decrypt)
        result_sign = 'fail'

    elif pushinfo_dict['result_statu'] == 'NOTNULL':
        # print result_decrypt
        if replycontent_type == '1':
            returnresult = etree.fromstring(result_decrypt)

            if returnresult.find('MsgType').text == 'text':
                Content = returnresult.find('Content').text.replace('\r','').replace('\n','')
                ex_Content=reply_relation['reply_content'].replace('\r','').replace('\n','')
                # print '\n'
                # print '预期回复',ex_Content
                # print '实际回复',Content
                # print '\n'
                if Content==ex_Content:
                    # print reply_relation['reply_content']
                    print '\n关键词自动回复与配置一致！'
                    result_sign='pass'
                else:
                    print '文本类型消息校验不一致'
                    result_sign = 'fail'
                    sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), Content)
                    writelog.errorlog(request_url + request_xml,'关键词: %s----预期回复：%s\n' % (str(inputword), str(reply_relation['reply_content'])), Content)
            else:
                print '文本类型消息校验不一致，返回结果中MsgType不是text'
                result_sign = 'fail'
                sendEmail(request_url, request_xml, result_decrypt, str(inputword),str(reply_relation['reply_content']),returnresult )
                writelog.errorlog(request_url + request_xml,'关键词: %s----预期回复：%s' % (str(inputword), str(reply_relation['reply_content'])),str(returnresult))

        elif replycontent_type in ['2','3','4']:

            material_result, material_url = get_material.get_material(getvalue_dict, reply_relation['reply_content'])
            if material_result == 'FAIL':
                print '该material_id获取素材失败，请检查该接口请求是否正常:%s' % str(material_url)
                # send_emails.send_failEmail('获取素材失败，请检查该接口请求是否正常%s\n' % str(material_url))
                writelog.errorlog(str(material_url), '菜单名称：%s--获取素材失败，请检查该接口请求是否正常' % str(inputword),str(reply_relation['reply_content']))
                result_sign = 'fail'
            else:
                returnresult = etree.fromstring(result_decrypt)
                # print result_decrypt
                MsgType=returnresult.find('MsgType').text
                if MsgType=='image' or MsgType=='video' or  MsgType=='voice':
                    if returnresult.find('MsgType').text == 'image':
                        image = returnresult.find('Image')
                        MediaId = image.find('MediaId').text
                    elif returnresult.find('MsgType').text == 'video':
                        video = returnresult.find('video')
                        MediaId = video.find('MediaId').text
                    elif returnresult.find('MsgType').text == 'voice':
                        Voice = returnresult.find('Voice')
                        MediaId = Voice.find('MediaId').text
                    else:
                        print '该种类型暂不支持'
                    # print MediaId
                    if material_result.has_key(MediaId):
                        if reply_relation['reply_content'] == material_result[MediaId]:
                            # print reply_relation['reply_content']
                            print '\n关键词自动回复与配置一致！'
                            result_sign = 'pass'
                        else:
                            print '其他类型校验不一致'
                            result_sign = 'fail'
                            sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), material_result[MediaId])
                            writelog.errorlog(request_url + request_xml, '关键词：%s----预期回复的素材ID：%s' % (str(inputword), str(reply_relation['reply_content'])), material_result[MediaId])
                    else:
                        print '其他类型校验不一致，material_result中未发现MediaId'
                        result_sign = 'fail'
                        sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), result_decrypt)
                        writelog.errorlog(request_url + request_xml, '关键词：%s---预期回复：%s' % (str(inputword), str(reply_relation['reply_content'])), result_decrypt)
                elif returnresult.find('MsgType').text == 'news':
                    Articles = returnresult.find('Articles')
                    Titlelist = []
                    for item in Articles.findall('item'):
                        Title = item.find('Title').text
                        Titlelist.append(Title)
                    ex_reply=material_result[reply_relation['reply_content']]
                    if ex_reply in Titlelist:
                        print '\n关键词自动回复与配置一致！'
                        result_sign = 'pass'
                    else:
                        print '多图文校验不一致'
                        result_sign = 'fail'
                        Titles='TITLE'
                        for T in range(0,len(Titlelist)):
                            TitleN=Titlelist[T].encode('utf-8')
                            # tmp_Title = '第%s个Title：%s' % (T + 1, TitleN)
                            Titles=Titles+TitleN
                        sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), Titles)
                        writelog.errorlog(request_url + request_xml, '关键词：%s---预期回复"%s"的素材id：%s' % (str(inputword), ex_reply, str(reply_relation['reply_content'])), Titles)
                else:
                    print '多图文校验不一致，返回结果中MsgType不是news'
                    result_sign = 'fail'
                    sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), result_decrypt)
                    writelog.errorlog(request_url + request_xml, '关键词：%s---预期回复：%s' % (str(inputword), str(reply_relation['reply_content'])), 'STATUS=200,请求成功，无返回结果!')

    else:
        result_sign = 'fail'
        sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), result_decrypt)
        writelog.errorlog(request_url + request_xml, '关键词：%s---预期回复：%s' % (str(inputword), str(reply_relation['reply_content'])), result_decrypt)


    return request_url, request_xml,result_sign
    # except Exception,e:
    #     result_sign = 'fail'
    #     sendEmail(request_url, request_xml, result_decrypt, str(inputword), str(reply_relation['reply_content']), '结果校验失败，请联系相关人员检查Compare文件%s' % e)
    #     writelog.errorlog(request_url + request_xml, '关键词：%s---预期回复：%s' % (str(inputword), str(reply_relation['reply_content'])), result_decrypt)
    #     return request_url, request_xml,result_sign




if __name__ == '__main__':

    value_dict={'reply_content_type': '3',
     'MENUNAME': '\xe9\x9a\x94\xe5\xa3\x81\xe8\x80\x81\xe7\x8e\x8b\xe5\x80\x9f\xe9\x92\xb1\xe6\x9c\x89\xe9\x81\x93',
     'EventKey': 'UTWGB01jLfwu14809968398728', 'MenuId': '7869', 'reply_id': '626',
     'get_replyword_url': u'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view?reply_type=4&token=mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL&id=626&app_key=100018&appid=wx1a1ae93bd415474c',
     'Event': 'CLICK', 'reply_content': u'200312'}
    getvalue_dict={'token': 'mBcfiB3JnDaTJDKJIvyNMLw02PXnxByL',
     'material_http': 'http://coreapi.biz.social-touch.com:8081/material/v1/manager/get',
     'replywords_http': 'http://coreapi.biz.social-touch.com:8081/autoreply/v1/auto-reply/view',
     'appid': 'wx1a1ae93bd415474c', 'reply_type': '4', 'authtype': '3', 'app_key': '100018',
     'Menulist_http': 'http://coreapi.biz.social-touch.com:8081/menu/v1/manager/list'}
    pushinfo_dict={'result_statu': 'pass',
     'request_url': u'http://api.biz.social-touch.com/app-base/wechat/monitor/appid/wx1a1ae93bd415474c?signature=d90ecde88f9ed24f7e8c57218f9dde33aa7482a3&timestamp=1488032249&nonce=6684830722&openid=opB1Nt_Uzy3ahu_ODsHhZr3Z04fQ&encrypt_type=aes&msg_signature=a98d9b0869570f0497db2d80135e588d52cc2d7d',
     'result_decrypt': '<xml><ToUserName><![CDATA[opB1Nt_Uzy3ahu_ODsHhZr3Z04fQ]]></ToUserName><FromUserName><![CDATA[test_b08ab3638b77]]></FromUserName><CreateTime>1488032247</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>1</ArticleCount><Articles><item><Title><![CDATA[\xe5\x80\x9f\xe9\x92\xb1\xe6\x9c\x89\xe9\x81\x93\xef\xbd\x9c\xe5\xa5\xb3\xe9\x82\xbb\xe5\xb1\x85\xe6\x89\xbe\xe9\x9a\x94\xe5\xa3\x81\xe8\x80\x81\xe7\x8e\x8b\xe5\x80\x9f\xe9\x92\xb1\xef\xbc\x8c\xe4\xbb\x96\xe4\xb8\xba\xe5\x95\xa5\xe4\xb8\x8d\xe5\x80\x9f\xef\xbc\x9f]]></Title><Description><![CDATA[\xe6\x89\x93\xe5\xbc\x80\xe6\x9f\xa5\xe7\x9c\x8b\xe9\x9a\x94\xe5\xa3\x81\xe8\x80\x81\xe7\x8e\x8b\xe7\x9a\x84\xe5\x80\x9f\xe9\x92\xb1\xe5\xae\x9d\xe5\x85\xb8\xe2\x80\xa6\xe2\x80\xa6]]></Description><PicUrl><![CDATA[http://pinqu.qiniudn.com/449350533b10818cb0fa9e393d24d1b7]]></PicUrl><Url><![CDATA[http://mp.weixin.qq.com/s?__biz=MzA3NTI4NDM4OA==&mid=506038822&idx=1&sn=454b119594f3ddd9111c8f3b952c05a7&chksm=04afc0ed33d849fbb92b915b391208aead923507513a8f3edd25835c54cdf2969912d2f6ac81#rd]]></Url></item></Articles></xml>',
     'request_xml': '<xml><ToUserName><![CDATA[test_b08ab3638b77]]></ToUserName><Encrypt><![CDATA[2iXZqnKFVHAQDZYJnQ+L4zfvelEHv2GYhaRwmALVOII3V3VUYEYi1DXjdXDchZfdx13T1CpVOeW6BpJg5Grz9Z+ChMdsbzXCVhS+hqzuRIqY1MWQb7hnvs5nfjFvTLdHfp3AuChm9Bo6s16FsgsZnXcUwiQr31smc3Jt/Rkj1ZCO2GmhoNEPMhouz5BWiyoyHEQ+HHtuunRFPVfV9OuQUORREdfYi7Dsqz2vTOR5o0GMt6MllNMZLzKaDl39RTyjs/rFu2DKCwwDHFhkJCMqb7/HGPlLLXyATzUVl7GgEGtIX1U/cPtywRenCJofOtfeXsVFoU6Lemts8tZnymCYYyZp1zYp/L0vJugFGC+8X/JfP4tDSPj6IztarfSFj6qZVDNOV9uM5AIbwB/7owCQ1KTu9WDbcMP/N1MDiqmG7vO70yszHrSAurB1knb6LVwD24GT7oNZzVwPKOqSbEp9y+RgkX0CjSCbir1ArtrGWyqaUYcVWVYf0BFIkOzz8jTV]]></Encrypt><from><![CDATA[QA-check]]></from></xml>'}

    Reply_Compare(value_dict,getvalue_dict,pushinfo_dict)





