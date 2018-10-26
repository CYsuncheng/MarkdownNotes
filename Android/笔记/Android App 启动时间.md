# Android App 启动时间
---

### 方法一：adb shell am start

命令行输入 **adb shell am start -W com.changba/.splash.Welcome**（*测试其他应用，更换包名和activity即可*）

其中：
* **WaitTime** 就是总的耗时，包括前一个应用Activity pause的时间和新应用启动的时间；
* **ThisTime** 表示一连串启动Activity的最后一个Activity的启动耗时；
* **TotalTime** 表示新应用启动的耗时，包括新进程的启动和Activity的启动，但不包括前一个应用Activity pause的耗时。
也就是说，开发者一般只要关心**TotalTime**即可，这个时间才是自己应用真正启动的耗时。

### 方法二：通过时间打点
##### 应用启动流程：

``` 
-> Application 构造函数
-> Application.attachBaseContext()
-> Application.onCreate()
-> Activity 构造函数
-> Activity.setTheme()
-> Activity.onCreate()
-> Activity.onStart
-> Activity.onResume
-> Activity.onAttachedToWindow
-> Activity.onWindowFocusChanged
```

根据上面的执行方法的顺序，可以在`Application.attachBaseContext()` 中打点作为起始时间，然后在`Activity.onWindowFocusChanged` 中打点作为结束的时间，时间差就是应用启动的耗时。

### 方法三：am 命令 高级用法

`adb shell am start -S -R 10 -W com.example.app/.MainActivity`
其中-S表示每次启动前先强行停止，-R表示重复测试次数。每一次的输出如下所示信息。

```
Stopping: com.example.app
Starting: Intent { act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] cmp=com.example.app/.MainActivity }
Status: ok
Activity: com.example.app/.MainActivity
ThisTime: 1059
TotalTime: 1059
WaitTime: 1073
Complete
```

***
[参考文档](http://www.jianshu.com/p/c967653a9468)
[知乎回答](https://www.zhihu.com/question/35487841)


