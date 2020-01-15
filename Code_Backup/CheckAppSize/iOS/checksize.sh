#!/bin/sh

base_root_path=$1
target_root_path=$2
echo "上一版本文件的目录：${base_root_path}";
echo "当前版本文件的目录：${target_root_path}";

root_path=$PWD

package_file='Package$'
assets_car='Assets.car'
bundle_file='bundle$'

# for path in $1 $2;
# do
# cd ${path}
# du -ch | grep ${package_file} | awk '{print "package file size = ", $1}'
# ls -lh | grep ${assets_car} | awk '{print "Assets.car size = ", $5}'

# bundle_size_kb=$(du -ck | grep ${bundle_file} | awk '{sum+=$1} END {print sum}')
# bundle_size_Mb=`expr ${bundle_size_kb} / 1024`
# echo "all .bundle file size = ${bundle_size_Mb} M"
# done

cd $1
echo "开始计算..."
package_size_1=$(du -ch | grep ${package_file} | awk '{print $1}')
assets_size_1=$(ls -lh | grep ${assets_car} | awk '{print $5}')
bundle_size_kb_1=$(du -ck | grep ${bundle_file} | awk '{sum+=$1} END {print sum}')
bundle_size_mb_1=`expr ${bundle_size_kb_1} / 1024`

# 解析出来文件名
bundle_file_1=${base_root_path#*LuoJiFM-IOS_release_}
bundle_file_1=${bundle_file_1%/Payload*}"-bundle.txt"
du -ch | grep 'bundle$' > $bundle_file_1
base_bundle_list_file_path=$PWD/$bundle_file_1
echo "生成 bundle 文件列表，目录：" ${base_bundle_list_file_path}


cd $2
package_size_2=$(du -ch | grep ${package_file} | awk '{print $1}')
assets_size_2=$(ls -lh | grep ${assets_car} | awk '{print $5}')
bundle_size_kb_2=$(du -ck | grep ${bundle_file} | awk '{sum+=$1} END {print sum}')
bundle_size_mb_2=`expr ${bundle_size_kb_2} / 1024`

bundle_file_2=${target_root_path#*LuoJiFM-IOS_release_}
bundle_file_2=${bundle_file_2%/Payload*}"-bundle.txt"
du -ch | grep 'bundle$' > $bundle_file_2
target_bundle_list_file_path=$PWD/$bundle_file_2
echo "生成 bundle 文件列表，目录：" ${target_bundle_list_file_path}
printf "\n\n\n"
echo "================================================================================"
echo "                                   主要文件大小变化对比                            "
echo "================================================================================"
printf "%-20s %-20s %-20s\n" FileName Pervious Current
printf "%-20s %-20s %-20s\n" Package ${package_size_1} ${package_size_2} 
printf "%-20s %-20s %-20s\n" Assets ${assets_size_1} ${assets_size_2} 
printf "%-20s %-20s %-20s\n" Bundle ${bundle_size_mb_1}M ${bundle_size_mb_2}M

cd ${root_path}
python3 diffbundle.py ${base_bundle_list_file_path} ${target_bundle_list_file_path}