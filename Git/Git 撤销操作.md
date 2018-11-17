# Git 撤销操作

## 引入几个概念
### HEAD
可以理解为一个指向当前分支最近一次提交的指针

### Index
index 也被称为 staging area，即暂存区域。执行 add 之后，文件的修改就到了这个区域。

### Working Copy
工作区，未进行任何的 git 操作之前的区域。

### Repository
就是常说的 git 仓库，执行 commit 之后，文件的修改就到了这个区域。

### 远程仓库
执行 push 之后，将本地仓库的修改同步更新到远程仓库。

## checkout、reset、revert这三个指令
### checkout：清空工作区的修改
* 清空工作区的修改`git checkout changed_file`，清空所有工作区的修改`git checkout .`。
* 切换分支`git checkout branch_name`(在切换分支之前，需要清空工作区，提交到本地版本仓库或者移除工作区的东西)。
* 快速查看某个版本的代码`git checkout commit_id / HEAD~last_version_num`，切换到一个临时分支，内容就是指定的版本内容。

### reset：撤销某次提交(commit)，并把这次提交的所有修改放到工作区
* `git reset HEAD~last_version_num / commit_id`，注意：这个操作修改历史，所以push到
远程仓库会出现问题，可以通过-f参数，实现强制推送。

### revert：回到之前的某个版本的状态，并创建一个新的提交。
* `git revert HEAD~last_version_num / commit_id`，创建一个新的commit，该内容为指定的
版本的内容，注意：这个操作并不会重写历史，也就是原来的commit还是存在的。

### git reset 和git revert的区别：
* `git revert`是用一次新的commit来回滚之前的commit，`git reset`是直接删除指定的commit。
* `git reset`是把HEAD向后移动了一下，而`git revert`是HEAD继续前进。

## commit级别的操作
### reset

``` shell
$ git checkout hotfix
$ git reset HEAD~2
```

![](https://ws1.sinaimg.cn/large/006tNbRwly1fxb5h3y0noj30u017qtei.jpg)

git reset用于撤销未被提交到remote的改动，即撤销local的修改。除了移动当前分支的HEAD，还可以更改workspace和index：

* --soft：修改HEAD，不修改index和workspace。
* --mixed：修改HEAD和index，不修改workspace。默认行为。
* --hard：修改HEAD、index、workspace。

`git reset --mixed HEAD`把index的内容退回到workspace中。
`git reset --hard HEAD`把index和workspace的修改全部撤销。

### checkout
checkout作用于commit级别时，只是移动HEAD到不同的commit。如果有unstaged的文件，git会阻止操作并提示。

### revert

``` shell
$ git checkout hotfix
$ git revert HEAD^^
```

![](https://ws3.sinaimg.cn/large/006tNbRwly1fxb5nmygmvj30u01930ww.jpg)

revert通过新建一个commit来撤销一次commit所做的修改，是一种安全的方式，并没有修改commit history。
revert用于撤销committed changes，reset用于撤销uncommitted changes。

## file级别的操作
### reset
`git reset <commit> <filename>`只修改index去匹配某次commit。
`git reset HEAD filename`把文件从index退回workspace，并将更改保存在workspace中。

### checkout
`git checkout <commit> <filename>`只修改workspace去匹配某次commit。
`git checkout HEAD filename`抹掉文件在workspace的修改。
