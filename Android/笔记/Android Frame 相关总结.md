## Android Frame 相关总结

### **ANR**
#### 原因：
在Android系统里，应用程序的响应性是由ActivityManager和WindowManager系统服务监视的。当它监测到以下情况中的一个时，Android就会针对特定的应用程序显示ANR：

1. KeyDispatchTimeout(5 seconds) -- 主要类型按键或触摸事件在特定时间内无响应
2. BroadcastTimeout(10 seconds) -- BroadcastReceiver在特定时间内无法处理完成
3. ServiceTimeout(20 seconds) -- 小概率类型 Service在特定的时间内无法处理完成


### **页面卡顿**

#### 页面渲染：
- 时间：Android系统每隔16ms发出VSYNC信号，触发对UI进行渲染，那么整个过程如果保证在16ms以内，用户看到的就是一个流畅的画面。
- 流程：每一个View的绘制过程都必须经历三个最主要的过程，也就是 measure（计算）、layout（布局）和 draw（绘制）。所以上面提到的时间，就是这三个步骤所用的耗时。
#### 卡顿原因：

##### OverDraw：
- 设置 -> 开发者选项 -> 调试GPU过度绘制 -> 显示GPU过度绘制
- 蓝色，淡绿，淡红，深红代表了4种不同程度的Overdraw情况，我们的目标就是尽量减少红色Overdraw，看到更多的蓝色区域。
![Alt text](./overdraw.png)

**如果发现某个页面过度绘制严重，可查看此页面对应的 layout.xml 文件，看看是否有不必要的布局嵌套等，如果发现疑问，可以和开发沟通，或者自己试着修改布局，打包并查看是否有影响。**
*例子：LocalSongFragment*

##### 丢帧
- **丢帧** 就是某一帧的渲染在16ms没有完成，导致下一帧的绘制请求（VSYNC信号）无法进行正常渲染，这样就发生了丢帧现象。
- **检测丢帧**：Choreographer 这个类来控制同步处理输入(Input)、动画(Animation)、绘制(Draw)三个UI操作。其实UI显示的时候每一帧要完成的事情只有这三种。
- 这个类里面会有一个 looper 函数，来处理 VSync 信号，所以，根据这个类，我们就可以获取到我们需要的 UI 更新每一个 Frame 的时间。


##### 测试方法：
1. 新建类并实现 Choreographer.FrameCallback 接口，代码如下：

``` java 
Override
    public void doFrame(long frameTimeNanos) {
        // Todo 开始执行doFrame的时间
        long startNanos = System.nanoTime();
        if (mLastFrameTimeNanos == 0) {
            mLastFrameTimeNanos = frameTimeNanos;
        }
        // Todo 接收VSYNC任务和实际开始执行的时间差
        final long jitterNanos = startNanos - frameTimeNanos;
        // Todo 时间差大于16ms，计算一下到底丢了多少帧
        if (jitterNanos > mFrameIntervalNanos) {
            Log.d(TAG, "The jitterNanos is " + jitterNanos * 0.000001f + "ms");
        }
        mLastFrameTimeNanos = frameTimeNanos;
        mLastStartNanos = startNanos;
        //Todo 注册下一帧的回调
        Choreographer.getInstance().postFrameCallback(this);
```

2. 在 Application 类注册，如下：

``` java 
	Choreographer.getInstance().postFrameCallback(new FPSFrameCallback(System.nanoTime()));
```

3. 打包并安装，之后就可以在 logcat 中查看 FPS 的时间信息，如下：

`04-29 22:10:14.046 16868-16868/com.changba E/Choreographer: The real time this jitterNanos cost is 21.389572ms`

**adb shell dumpsys gfxinfo framestats 获取每一帧绘制过程中每个关键节点的耗时情况，但是只是最近的128帧的信息。**

***
### 参考文档
[Android UI性能优化](http://blog.csdn.net/lmj623565791/article/details/45556391/)
[Android view 的绘制流程解析](http://blog.csdn.net/guolin_blog/article/details/16330267)
[从FrameCallback理解Choreographer原理及简单帧率监控应用](http://blog.adisonhyh.com/2017/03/15/%E4%BB%8EFrameCallback%E7%90%86%E8%A7%A3Choreographer%E5%8E%9F%E7%90%86%E5%8F%8A%E7%AE%80%E5%8D%95%E5%B8%A7%E7%8E%87%E7%9B%91%E6%8E%A7%E5%BA%94%E7%94%A8/)



