# coding: utf8

import sys
import os

root_dir = "/Users/suncheng/Downloads/LinkMapParser-master/LuoJiFM-IOS_release_7.8.0_20200108154054/Payload/LuoJiFMIOS.app/"
test_path = "/Users/suncheng/Desktop/PPT/"

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


def get_file_size(filter="bundle"):
    total_size = 0
    file_list = os.listdir(root_dir)
    for file_name in file_list:
        if file_name.endswith(filter):
            print(file_name)
            filepath = os.path.join(root_dir, file_name)
            fsize = os.path.getsize(filepath)
            print(fsize)
            total_size += fsize
    # print (total_size)
    return formatSize(total_size)

if __name__ == "__main__":
    print(get_file_size())