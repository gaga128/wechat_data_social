# -*- coding: utf-8 -*-
#****************************************************************
# FileOperation.py
# Author     : hsn
# Version    : 1.0
# Date       : 2016-5-12
# Description: 常用文件操作封装
#****************************************************************
import os
import shutil
"""
文件相关操作：文件/文件夹检查是否存在；文件/文件夹删除
"""
def FileExsit(path):
    """
    检测文件是否存在
    path    文件地址
    """
    if os.path.isfile(path):
        return True
    return False

def DirExsit(path):
    """
    判断文件夹是否存在
    path    文件夹地址
    """
    if os.path.isdir(path):
        return True
    return False

def DelFile(path):
    """
    删除文件
    path    文件地址
    """
    try:
        os.remove(path)
    except Exception as e:
        print 'Delete {0} failed.\n'.format('file'), e

def DelDir(path):
    """
    删除文件夹
    path    文件夹地址
    """
    try:
        shutil.rmtree(path)
    except Exception as e:
        print "Del {0} failed.\n".format('dir'), e

def Copy_file(myfilepath, tmpfilepath):
    """
    文件复制
    myfilepath  --- 从path1拷贝的文件路径
    tmpfilepath  --- 拷贝到path2
    """
    # try:
    #     os.remove(tmpfilepath)
    #     print "file del"
    # except Exception as e:
    #     print "Del {0} failed.\n".format('file'), e
    try:
        shutil.copy(myfilepath,tmpfilepath)
        print u"文件拷贝成功"
    except Exception as e:
        print "copy {0} failed.\n".format('file'), e

def DelDir_filelist(path):
    """
    清空文件夹
    path   文件夹目录
    """
    try:
        filelist=[]
        filelist=os.listdir(path)
        for f in filelist:
            filepath = os.path.join( path, f )
            if os.path.isfile(filepath):
                os.remove(filepath)
                print filepath+" removed!"
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath,True)
                print "dir "+filepath+" removed!"
    except Exception as e:
        print "DelDir_filelist {} failed.\n".format('dir'), e


if __name__ == '__main__':
    dirs = os.path.dirname(os.path.abspath(__file__)) + r'\log\failresult.html'
    print dirs
    print FileExsit(dirs)