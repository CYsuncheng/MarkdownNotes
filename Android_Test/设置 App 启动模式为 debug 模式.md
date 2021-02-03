
## 启动 App 为 debug mode

> adb shell am set-debug-app -w com.changba

其中：

- set-debug-app 用来应用为debug模式
- -w 意思为wait，在进程启动的时候，等待debugger进行连接
- com.changba 代表应用的包名

如果需要多次调试：
> adb shell am set-debug-app -w --persistent  com.changba

- —persitent 意思是持久的，意思是一直设置这个应用为调试模式，即每次开启（进程创建）都会弹出对话框，即使卸载再安装或者更新应用

如果多次debug完成后，解决了问题，想要恢复正常的启动也很简单：
> adb shell am clear-debug-app

这个调试的方法很简单，但是可能会节省我们很多的宝贵时间。
