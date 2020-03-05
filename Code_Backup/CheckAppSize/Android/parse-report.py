#-*- coding:utf-8 -*-

import json
import sys

previous_report_file = sys.argv[1]
current_report_file = sys.argv[2]

previous_tem_top_dict = {}
current_tem_top_dict = {}

with open(previous_report_file, 'r') as pre:
    previous_report_dict = json.load(pre)

previous_apk_total_size = previous_report_dict[0]["total-size"]
previous_top_list = previous_report_dict[0]["entries"]


with open(current_report_file, 'r') as cur:
    current_report_dict = json.load(cur)

current_apk_total_size = current_report_dict[0]["total-size"]
current_top_list = current_report_dict[0]["entries"]

for tl in previous_top_list:
    previous_tem_top_dict[tl['suffix']] = float('%.2f'%(tl['total-size']/(1024)))
    # print (f"format: {tl['suffix']}, total size: {tl['total-size']//(1024*1024)}M")

for tl in current_top_list:
    current_tem_top_dict[tl['suffix']] = float('%.2f'%(tl['total-size']/(1024)))

# print (f"previous apk total size: {previous_apk_total_size//(1024*1024)}M")
# print (f"current apk total size: {current_apk_total_size//(1024*1024)}M")

previous_tem_top_dict['total'] = float('%.2f'%(previous_apk_total_size/(1024)))
current_tem_top_dict['total'] = float('%.2f'%(current_apk_total_size/(1024)))

print ("%s" % "=".ljust(80, '='))
print ("%s" % "模块大小列表".center(84))
print ("%s" % "=".ljust(80, '='))
print ("%s%s%s%s" % ("文件类型".ljust(24), "上一版本".ljust(14), "当前版本".ljust(14), "是否新增".ljust(14)))

for key in previous_tem_top_dict.keys():
    if key not in current_tem_top_dict:
        print ("%s%s%s" % (key.ljust(28), str("%.2fK" % previous_tem_top_dict[key]).ljust(18),
                                str("%s" % "None").ljust(14)))

for key in current_tem_top_dict.keys():
    if key not in previous_tem_top_dict:
        print ("%s%s%s%s" % (key.ljust(28), str("%s" % "None").ljust(18),
                                str("%.2fK" % current_tem_top_dict[key]).ljust(14), "Y".center(18)))
        # print (f"new file: {key}, {current_tem_top_dict[key]}M")
    else:
        print ("%s%s%s" % (key.ljust(28), str("%.2fK" % previous_tem_top_dict[key]).ljust(18),
                                      str("%.2fK" % current_tem_top_dict[key]).ljust(18)))
        # print (f"file: {key}, {previous_tem_top_dict[key]}M, {current_tem_top_dict[key]}M")