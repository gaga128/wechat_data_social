#-*-coding:UTF-8-*-
#****************************************************************
#log
# Author     : lujia
# Version    : 1.0
# Date       : 2017-02-14
# Description:
#****************************************************************


import time
import os




count=0
today = str(time.strftime("%Y-%m-%d %H.%M", time.localtime(time.time())))
def errorlog(request_url,erreason,acresult):
    # print request_url
    global count
    count=count+1
    filename = os.path.dirname(os.path.abspath(__file__)) + r'/log/errorlog/error_%s.htm'%today
    print filename
    f=file(filename,"a+")
    f.writelines('<meta charset=\"utf-8\">'+'<B>'+str(count)+'. '+'</B>'+ '<B>'+'<a href="'+request_url+'">'+request_url+'</a></br>'  + '<B>'+str(erreason)+'</B></br>' +  '<a href="'+acresult+'">'+acresult+'</a></br></br>')
    f.close()
    #备份只保留最近一次
    bkup = file(os.path.dirname(os.path.abspath(__file__)) + r'/log/failresult.html','a+')
    bkup.writelines('<meta charset=\"utf-8\">' + '<B>' + str(count) + '. ' + '</B>' + '<B>' + '<a href="' + request_url + '">' + request_url + '</a></br>' + '<B>' + erreason + '</B></br>' + '<a href="' + acresult + '">' + acresult + '</a></br></br>')
    bkup.close()



def static_log(appid,keyright,keyerr,keyfail,menuright,menuerr,menufail):
    staticname=os.path.dirname(os.path.abspath(__file__))+r'/log/static.txt'
    # print staticname
    f = open(staticname, 'a')
    f.write('appid:%s \n 关键词----校验成功：%s个\t未通过：%s个\t失败：%s个,\t自定义菜单----检验成功：%s个\t未通过：%s个\t失败：%s个\n'%(appid,keyright,keyerr,keyfail,menuright,menuerr,menufail))
    f.close()



if __name__ == '__main__':
    # errorlog('test','www.baidu.com','错误')
    for i in range(0,9):
        static_log(1,111,11,222,11,333,444)