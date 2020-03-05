```
# 只可以遍历指定文件夹rootdir中的文件夹名和文件名
# 无法遍历出其中包含的子文件夹中的内容

import os

rootdir = './'   # 需要遍历的文件夹，这里设定为当前文件夹
list = os.listdir(rootdir)
for line in list:
    filepath = os.path.join(rootdir, line)
    if os.path.isdir(filepath):
        print "dir:" + filepath
    if os.path.isfile(filepath):
        print "file:" + filepath
```

```
# 遍历指定文件夹rootdir中的所有文件夹及文件，包括子文件夹

import os

rootdir = './'   # 需要遍历的文件夹，这里设定为当前文件夹

# 如果此循环在迭代第一次时break出，则其效果和上面的相同
for root, dirs, files in os.walk(rootdir):    # 当前路径、子文件夹名称、文件列表
    for filename in files:
        print filename
    for dirname in dirs:
        print dirname
```