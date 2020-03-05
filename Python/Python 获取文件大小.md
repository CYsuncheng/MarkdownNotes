```
# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小
def getFileSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)


if __name__ == "__main__":
    print(getDocSize("../detailhtml/20161103112313.html"))
    # 1006.142578kb
    print(getFileSize("../data/"))
    # 111.856756M
```