#-*- encoding:utf-8 -*-
#****************************************************************
# 加密和解密数据
# Author     : lujia
# Version    : 1.0
# Date       : 2017-01-19
# Description:
#****************************************************************



from lxml import etree

import WXBizMsgCrypt as WX
import base64
import MesType




def encrypt(encodingAESKey,Third_appid,Unencrypt_xml):
    # try:
        AESKey = base64.b64decode(encodingAESKey + "=")
        encryp_test = WX.Prpcrypt(AESKey)

        # ret, msg_encrypt = encryp_test.encrypt(Unencrypt_xml, Third_appid)
        # print Unencrypt_xml
        if etree.fromstring(Unencrypt_xml).find('MsgType').text =='text':
            ret, msg_encrypt = encryp_test.encrypt(Unencrypt_xml, Third_appid)
            # ret, msg_encrypt = encryp_test.encrypt(etree.tostring(MesType.runtext(dict), encoding="UTF-8"), Third_appid)
        elif etree.fromstring(Unencrypt_xml).find('MsgType').text:
            ret, msg_encrypt = encryp_test.encrypt(Unencrypt_xml, Third_appid)
            # ret, msg_encrypt = encryp_test.encrypt(etree.tostring(MesType.runevent(dict),encoding="UTF-8"), Third_appid)
        else:
            print '该种消息类型或事件暂不支持，如需使用请联系相关人员进行添加～～'
        # print '加密后数据-------', msg_encrypt

        return msg_encrypt
    # except Exception,e:
    #     print '加密失败，请检查您的数据，如数据输入正确，请联系相关人员进行解决！%s'%e




def decrypt(encodingAESKey,Third_appid,result):
    # try:

        if result=='ok':
            print 'result:%s'%str(result)
            return 'FAIL',result
        else:
            AESKey = base64.b64decode(encodingAESKey + "=")
            decrypt_Encrypt= etree.fromstring(result).find('Encrypt').text
            decrypt_test = WX.Prpcrypt(AESKey)
            ret, result_decrypt = decrypt_test.decrypt(decrypt_Encrypt, Third_appid)
            if '<xml>' not in result_decrypt:
                result='FAIL'
                print '\n接口返回的加密数据不是xml格式，返回结果：\n%s'%result_decrypt
                return result, result_decrypt
            else:
                returnresult = etree.fromstring(result_decrypt)
                ToUserName = returnresult.find('ToUserName').text
                FromUserName = returnresult.find('FromUserName').text
                CreateTime = returnresult.find('CreateTime').text
                MsgType = returnresult.find('MsgType').text
                print '\n****解密后的返回结果****： '
                print '*ToUserName*:', ToUserName
                print '*FromUserName*:', FromUserName
                print '*CreateTime*:', CreateTime
                print '*MsgType*:', MsgType
                if MsgType == 'text':
                    Content = returnresult.find('Content').text
                    print 'Content:', Content
                    result='NOTNULL'
                elif  MsgType == 'image':
                    Image = returnresult.find('Image')
                    MediaId=Image.find('MediaId').text
                    print 'MediaId: ', MediaId
                    result = 'NOTNULL'
                elif MsgType == 'voice':
                    Voice = returnresult.find('Voice')
                    MediaId = Voice.find('MediaId').text
                    print 'MediaId: ', MediaId
                    result = 'NOTNULL'
                elif MsgType == 'video':
                    Video = returnresult.find('Video')
                    MediaId = Video.find('MediaId').text
                    Title = Video.find('Title').text
                    Description = Video.find('Description').text
                    print 'MediaId: ', MediaId
                    print 'Description: ',Description
                    print 'Title: ',Title
                    result = 'NOTNULL'
                elif MsgType == 'music':
                    Music = returnresult.find('Music')
                    Title = Music.find('Title').text
                    Description = Music.find('Description').text
                    MusicUrl = Music.find('MusicUrl').text
                    HQMusicUrl = Music.find('HQMusicUrl').text
                    ThumbMediaId = Music.find('ThumbMediaId').text
                    print 'Description: ', Description
                    print 'Title: ', Title
                    print 'MusicUrl: ', MusicUrl
                    print 'HQMusicUrl: ', HQMusicUrl
                    print 'ThumbMediaId: ', ThumbMediaId
                    result = 'NOTNULL'
                elif MsgType == 'news':
                    ArticleCount = returnresult.find('ArticleCount').text
                    Articles = returnresult.find('Articles')
                    for item in Articles.findall('item'):
                        Title = item.find('Title').text
                        Description = item.find('Description').text
                        PicUrl = item.find('PicUrl').text
                        Url = item.find('Url').text
                        print 'ArticleCount: ',ArticleCount
                        print 'Description: ', Description
                        print 'Title: ', Title
                        print 'PicUrl: ', PicUrl
                        print 'Url: ', Url
                        result = 'NOTNULL'
                else:
                    result = 'FAIL'
                    print '该种回复类型初次出现，请将请求URL和XML数据包发送给相关人员进行添加～～'
                return result,result_decrypt
    # except Exception,e:
    #     result='FAIL'
    #     print '解密失败，请检查您的数据，如数据正确，请联系相关人员进行解决！%s'%str(e)
    #     return result,str(e)




def nodecrypt(result_decrypt):
    # try:
    if result_decrypt == 'ok':
        print 'result_decrypt:%s'%str(result_decrypt)
        return 'FAIL', result_decrypt
    else:
        if '<xml>' not in result_decrypt:
            result='FAIL'
            print '\n接口返回的加密数据不是xml格式，返回结果：\n%s'%result_decrypt
            return result, result_decrypt
        else:
            returnresult = etree.fromstring(result_decrypt)
            ToUserName = returnresult.find('ToUserName').text
            FromUserName = returnresult.find('FromUserName').text
            CreateTime = returnresult.find('CreateTime').text
            MsgType = returnresult.find('MsgType').text
            print '\n****解密后的返回结果****： '
            print '*ToUserName*:', ToUserName
            print '*FromUserName*:', FromUserName
            print '*CreateTime*:', CreateTime
            print '*MsgType*:', MsgType
            if MsgType == 'text':
                Content = returnresult.find('Content').text
                print 'Content:', Content
                result = 'NOTNULL'
            elif  MsgType == 'image':
                Image = returnresult.find('Image')
                MediaId=Image.find('MediaId').text
                print 'MediaId: ', MediaId
                result = 'NOTNULL'
            elif MsgType == 'voice':
                Voice = returnresult.find('Voice')
                MediaId = Voice.find('MediaId').text
                print 'MediaId: ', MediaId
                result = 'NOTNULL'
            elif MsgType == 'video':
                Video = returnresult.find('Video')
                MediaId = Video.find('MediaId').text
                Title = Video.find('Title').text
                Description = Video.find('Description').text
                print 'MediaId: ', MediaId
                print 'Description: ',Description
                print 'Title: ',Title
                result = 'NOTNULL'
            elif MsgType == 'music':
                Music = returnresult.find('Music')
                Title = Music.find('Title').text
                Description = Music.find('Description').text
                MusicUrl = Music.find('MusicUrl').text
                HQMusicUrl = Music.find('HQMusicUrl').text
                ThumbMediaId = Music.find('ThumbMediaId').text
                print 'Description: ', Description
                print 'Title: ', Title
                print 'MusicUrl: ', MusicUrl
                print 'HQMusicUrl: ', HQMusicUrl
                print 'ThumbMediaId: ', ThumbMediaId
                result = 'NOTNULL'
            elif MsgType == 'news':
                ArticleCount = returnresult.find('ArticleCount').text
                Articles = returnresult.find('Articles')
                for item in Articles.findall('item'):
                    Title = item.find('Title').text
                    Description = item.find('Description').text
                    PicUrl = item.find('PicUrl').text
                    Url = item.find('Url').text
                    print 'ArticleCount: ',ArticleCount
                    print 'Description: ', Description
                    print 'Title: ', Title
                    print 'PicUrl: ', PicUrl
                    print 'Url: ', Url
                result='NOTNULL'
            else:
                result='FAIL'
                print '该种回复类型初次出现，请将请求URL和XML数据包发送给相关人员进行添加～～'
            # print result_decrypt
            return result,result_decrypt
    # except Exception,e:
    #     result='FAIL'
    #     print '请检查您的返回结果是否正确，如果正确，请联系相关人员进行解决！%s'%str(e)
    #     return result,str(e)

if __name__ == '__main__':
    Third_appid = 'wxfb798f3c38b79c85'
    encodingAESKey = "ed85e5ddefa3ade80d018178e34331ecsocialtouch"
    # data_dict={'ToUserName':'gh_b08ab3638b88','FromUserName':'oCWncs00chDdcvYG4xCDnzz35tR4','CreateTime':'1234567','Content':u'你好','MsgId':'str(random.randint(9000000000000000000, 9999999999999999999))','MsgType':'text'}
    # result=encrypt(encodingAESKey, Third_appid, data_dict)
    # result='<xml><ToUserName><![CDATA[test_b08ab3638b77]]></ToUserName><Encrypt><![CDATA[6W2SMfVmjXwoaMNTBEKfy2iSNRXf47trwr+Wv4iNepMQlA9EsFv0yUc3v/wdackPKuTe1MC6GYFOoLx0sMLUlR1l5JXiF8pXGEYwC1+h8aeEs2RoYXfBUEIjg+X8Sk/CumxyiGCEKRADHve/L59L2+kTPbezxYidmf1HK1IXEC1jG/npL0Uu/BD50F69VWgBceQnE27Zkpg9d7OPBYhgeumbUcXq2kn/xfS/tcfBI8072hVZsHMuwtBDKj3UphOe0sbIEzW6sbNNBMN9rY2lG+nGNWFhy5makZs0RXuJ17Sy75rX4DyqWNzZGcy/M6sFlzPbHHATBMZi0Ec3bTrnfjH9Kax+9lF6bk1g8rd7VBOvFlDEvpgNwXemmRfTKKp7nvBdeR3CGw3ARcXV5YwENuHzvZ2KbLuxye6OvUDwQHSyKSHWS6hbwELafBz75DRbZ8Ky31OYxUm0Vjz/zZXENIK7YnikhnYQqHUuvyfWgTioNeyHyZjpxFwlVD69AJoQQJkhlriRSlqmszmK27Maw6ipJHXsj5IarjtlaeQuY/WTmMc9FWZkwCEB+ZsVAvdRGhhyZS92tZzv4MdyDcixruZaqV/ZqPDgMpmfRcIcG6NZu/lHQjPEEL7a5384Dms0]]></Encrypt><from><![CDATA[QA-check]]></from></xml>'
    # result='<xml><ToUserName><![CDATA[test_b08ab3638b77]]></ToUserName><Encrypt><![CDATA[6W2SMfVmjXwoaMNTBEKfy2iSNRXf47trwr+Wv4iNepMQlA9EsFv0yUc3v/wdackPKuTe1MC6GYFOoLx0sMLUlR1l5JXiF8pXGEYwC1+h8aeEs2RoYXfBUEIjg+X8Sk/CumxyiGCEKRADHve/L59L2+kTPbezxYidmf1HK1IXEC1jG/npL0Uu/BD50F69VWgBceQnE27Zkpg9d7OPBYhgeumbUcXq2kn/xfS/tcfBI8072hVZsHMuwtBDKj3UphOe0sbIEzW6sbNNBMN9rY2lG+nGNWFhy5makZs0RXuJ17Sy75rX4DyqWNzZGcy/M6sFlzPbHHATBMZi0Ec3bTrnfjH9Kax+9lF6bk1g8rd7VBOvFlDEvpgNwXemmRfTKKp7nvBdeR3CGw3ARcXV5YwENuHzvZ2KbLuxye6OvUDwQHSyKSHWS6hbwELafBz75DRbZ8Ky31OYxUm0Vjz/zZXENIK7YnikhnYQqHUuvyfWgTioNeyHyZjpxFwlVD69AJoQQJkhlriRSlqmszmK27Maw6ipJHXsj5IarjtlaeQuY/WTmMc9FWZkwCEB+ZsVAvdRGhhyZS92tZzv4MdyDcixruZaqV/ZqPDgMpmfRcIcG6NZu/lHQjPEEL7a5384Dms0]]></Encrypt><from><![CDATA[QA-check]]></from></xml>'
    # result='<xml><Encrypt><![CDATA[V/WGnWgio23IdciSdQz0dnOoBRbHlpDIFYOyV3pIpOO1H7YSFOxqAJC7+guYcv2poklMObe47MDxqHLap4VA5GQe4xrwUlfR0GYiN/HzufUob6wtgEctl11MeCi3nJK10M1Dsd2Xvu+iqeQBF4OKUVAARFP+oVVT4fpB2tRKa4Tw4Si/eXoLriGA87+xaVHt7VzaXgefvNU1HCQkSqV7NGksAPOII+3lYRcnh2sjGEZNxzWw+yCQ07wOba2rbPoMly7eL6woApPkVGza9gneFsKcBB9LoL5qmMucF8VbJ5ASCt95yYc4uC09ButwGmHRcJIhpKejNheIAWsONsb1dw==]]></Encrypt><MsgSignature><![CDATA[c3b8d411de83f40ff211f9b89c7cd8a70c08fc6e]]></MsgSignature><TimeStamp>1484731439</TimeStamp><Nonce><![CDATA[951813469]]></Nonce></xml>'
    result='<xml><ToUserName><![CDATA[test_b08ab3638b88]]></ToUserName><Encrypt><![CDATA[mijCZ1Wttk73Ie32dVx0b4pXjIi4Y2mPAWyLUYwHY/NpxAJ6Pba9IR3LiOwbU1Ny4518P7WjDB05P3CW/YpYX/QVD7bEO4sqV9FGftqQM4wlO1S5TUSK/UtjOoJrGb2Ffncb6H5k9pANpqdnsZ1Qibg2Xo54f9vbY+IqopGg6iSXjeDfT2SPBqcE2LIQ5adIEs9uMxuotXZuSlufV2Ymks5AaeYHunN9aNdLajUTV/q8FnlFzL68/nzzddxO6DCqvngLoWcudesb1LniPMmlC69kLx3Rdm0A7Bw7zEhyP44ZOVu8XucNZ+f946s5vWYgwl9j154dVsOKXjt7qN11sc81MP1eyTx1VpfESq05sigxj85/UU1JUWj+3fDWWBujk0zK/O+miQpQMEWOpcqZh9zZp/FtIMhpK0yNQJw6h2k9PGEmeXqraYW0pAgBI8Tt87DxDZqcZi3QW2cSFEZLeQ==]]></Encrypt><from><![CDATA[QA-check]]></from></xml> '
    result=''
    decrypt(encodingAESKey, Third_appid, result)
