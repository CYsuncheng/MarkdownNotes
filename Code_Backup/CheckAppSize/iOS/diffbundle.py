# coding: utf8

import sys
import os

def get_bundle_map_list(bundle_file):
    bundle_map = {}
    bundle_map_list = []
    with open(bundle_file) as f:
        for line in f.readlines():
            bundle_map = {"name": line.split("./")[1].strip(), "size": line.split("./")[0].strip()}
            bundle_map_list += [bundle_map]
    return bundle_map_list

def compare_increase(base_bundle_list, target_bundle_list):
    print ("%s" % "=".ljust(80, '='))
    print ("%s" % "bundle文件大小变化列表".center(84))
    print ("%s" % "=".ljust(80, '='))
    print ("%s%s%s" % ("FileName".ljust(40), "Previous".ljust(20), "Current".ljust(20)))
    for target_bundle_map in target_bundle_list:
        target_name = target_bundle_map["name"]
        target_size_value = target_bundle_map["size"]
        has_bundle_in_base = 0
        base_size_value = 0
        for base_bundle_map in base_bundle_list:
            base_name = base_bundle_map["name"]
            if base_name == target_name:
                base_size_value = base_bundle_map["size"]
                has_bundle_in_base = 1
                if base_size_value != target_size_value:
                    print ("%s%s%s" % (target_name.ljust(40), str(base_size_value).ljust(20),
                                      str(target_size_value).ljust(20)))
        if has_bundle_in_base == 0:
            print ("%s%s%s" % (target_name.ljust(40), str(base_size_value).ljust(20),
                                str(target_size_value).ljust(20)))


if __name__ == "__main__":
    base_file = sys.argv[1]
    target_fiel = sys.argv[2]
    base_bundle_list = get_bundle_map_list(base_file)
    target_bundle_list = get_bundle_map_list(target_fiel)
    compare_increase(base_bundle_list, target_bundle_list)
    