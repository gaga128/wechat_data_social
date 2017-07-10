#-*- encoding:utf-8 -*-
#****************************************************************
# 请求接口
# Author     : lujia
# Version    : 1.0
# Date       : 2017-01-19
# Description:
#****************************************************************




data = {}
def Key_static(appid,code):
    global data
    appid_static = data[appid]
    if code=='200':
        sucCount = appid_static['Key_pass']
        sucCount=sucCount+1
        appid_static['Key_pass']=sucCount
    elif code=='400':
        errcount = appid_static['Key_err']
        errcount = errcount + 1
        appid_static['Key_err'] = errcount
    elif code=='500':
        failcount=appid_static['Key_fail']
        failcount=failcount+1
        appid_static['Key_fail']=failcount
    data[appid] = appid_static


def Menu_static(appid,code):
    global data
    appid_static =data[appid]
    if code=='200':
        sucCount = appid_static['Menu_pass']
        sucCount=sucCount+1
        appid_static['Menu_pass']=sucCount
    elif code=='400':
        errcount = appid_static['Menu_err']
        errcount = errcount + 1
        appid_static['Menu_err'] = errcount
    elif code=='500':
        failcount = appid_static['Menu_fail']
        failcount = failcount + 1
        appid_static['Menu_fail'] = failcount
    data[appid] = appid_static



def subdef_static(appid,code):
    global data
    appid_static =data[appid]
    if code=='200':
        sucCount = appid_static['subdef_pass']
        sucCount=sucCount+1
        appid_static['subdef_pass']=sucCount
    elif code=='400':
        errcount = appid_static['subdef_err']
        errcount = errcount + 1
        appid_static['subdef_err'] = errcount
    elif code=='500':
        failcount = appid_static['subdef_fail']
        failcount = failcount + 1
        appid_static['subdef_fail'] = failcount
    data[appid] = appid_static



total_keypass=0
total_keyerr=0
total_keyfail=0
total_menupass=0
total_menuerr=0
total_menufail=0
total_subdefpass=0
total_subdeferr=0
total_subdeffail=0
def Total_static(dict):

    if dict=={} or dict==None:
        pass
    else:
        for key in dict.keys():
            global total_keypass,total_keyerr,total_menupass,total_menuerr,total_keyfail,total_menufail,total_subdefpass,total_subdeferr,total_subdeffail
            tmp=dict[key]
            total_keypass=total_keypass+tmp['Key_pass']
            total_keyerr = total_keyerr + tmp['Key_err']
            total_keyfail = total_keyfail + tmp['Key_fail']
            total_menupass = total_menupass + tmp['Menu_pass']
            total_menuerr = total_menuerr + tmp['Menu_err']
            total_menufail = total_menufail + tmp['Menu_fail']
            total_subdefpass = total_subdefpass + tmp['subdef_pass']
            total_subdeferr = total_subdeferr + tmp['subdef_err']
            total_subdeffail = total_subdeffail + tmp['subdef_fail']
    return total_keypass,total_keyerr,total_keyfail,total_menupass,total_menuerr,total_menufail,total_subdefpass,total_subdeferr,total_subdeffail



def initData(appid):
    global data
    init_data = {}
    init_data['Key_pass'] = 0
    init_data['Key_err'] = 0
    init_data['Key_fail']=0
    init_data['Menu_pass'] = 0
    init_data['Menu_err'] = 0
    init_data['Menu_fail']=0
    init_data['subdef_pass'] = 0
    init_data['subdef_err'] = 0
    init_data['subdef_fail'] = 0
    data[appid]=init_data
    return data
