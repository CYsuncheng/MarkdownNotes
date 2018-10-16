# Android 专项测试
@(Android 性能)[整理]

---

## 背景

> Android 性能测试一般包含，响应时间、内存、CPU、流畅度、流量、电量等几个主要方向。

- 性能表现越来越受到用户的重视，用户对耗电，发热，卡顿等体验问题的反馈明显增多。
- 应用在需求不断增加的过程中，为了达到更好的交互效果，往往会忽略性能开销的增加，实际上也反过来会影响功能的体验。
- 我们之前的专项测试并不系统，且基本上依赖手工操作，覆盖场景不足，效率较低。
- 自动化 case 已经有了一定的积累，基本覆盖主要场景，可以在跑自动化测试时，获取专项测试数据，提高效率。
- 接下详细说一下，如何实现。

## 如何获取数据
### 内存
#### 单个应用可申请的内存最大值
针对不同的 Android 设备，可以通过命令 `getprop | grep heap` 得到如下值：
`[dalvik.vm.heapgrowthlimit]: [256m] `
`[dalvik.vm.heapsize]: [512m]`

1. **heapgrowthlimit** 表示单个应用可分配的内存最大值。
2. **heapsize** 表示单个虚拟机最大的内存。
3. 如果应用设置了**largeHeap="true"**，则理论上可以申请的最大内存就是 **heapsize** 的值。

#### 内存高引发的主要问题
当应用所占内存过高时，会有以下主要的风险：

1. 应用的内存如果超过 heapgrowthlimit 的值，就可能发生 OOM。
2. 如果接近 heapgrowthlimit 的值，则会触发更多的 GC，导致应用的卡顿。
3. 如果持续升高，则可能发生了内存泄露。
4. 内存高，后台被系统 kill 的优先级也更高（LowMemoryKiller）。

#### 取值方法
一般有以下几个方法：

1. 通过 Android Studio 提供的 Profiler 工具，需要 debug 版本。如下：
![@AS Profiler](https://i.loli.net/2017/12/26/5a4219f60aef6.png)

2. 修改应用的源码，借助 ActivityManager 和 Debug 类，可以获取系统 or 当前进程的内存使用情况。本着尽量不对 APP 源码有过多改动的前提，没有选择这个方式。
3. 使用命令，例如 top，dumpsys meminfo，相对来说，PSS 的值来反映内存更准确，所以使用 `adb shell dumpsys meminfo packagename` ，命令输出如下：
![@adb shell dumpsys meminfo 输出内容|Meminfo](https://i.loli.net/2017/12/26/5a4218ce4ebd4.png)

上图中，TOTAL 就是总的 PSS 内存值，这个值包含了 swap（虚拟内存）的值，其实已分配的堆内存应该是 TOTAL 的 HeapSize 列，但是考虑到图片缓存等也应该考虑在内，所以直接取的是 TOTAL 的值。
代码中我们还分别获取了 Java heap 和 Native heap。

### CPU
#### CPU 过高可能引发的主要问题
1. 功耗高，直观感受就是耗电，手机发热严重等。
2. 卡顿， CPU 资源不足，无法及时执行任务，出现卡顿甚至 ANR。

#### 取值方法
1. 同样可以通过 AS Profiler 查看，这个不再多说。
2. 命令，如 top，dumpsys cpuinfo（拿到的值需要在计算一次），或者 cat /proc/stat（需要自行计算 jiffies 值），我们这里直接使用的 top 命令，输出如下：
![@top 命令输出|top](https://i.loli.net/2017/12/26/5a421f2b5cff7.png)

上图中，10% 就是应用主进程的 CPU 的值，现在应用都不会只有一个进程，同时需要关注其他进程的 CPU 开销。

上面分别介绍了 CPU 和内存的取值方法，接下来看一下如果处理这些值。

### 代码实现
以 Total Memory 为例子，代码实现如下：
CPU 相对来说简单的多，就不贴代码了。

创建类

```java
public class GetPerformance {
	private ExecutorService threadPool; //线程池
	private CompletionService<ArrayList<Performance>> CS;
	private Performance performance; // 创建的实体类
	private Exec exec = new Exec(); // 用于执行 shell 命令的类
	private boolean start = true; // 用于控制线程的开始和结束
```

需要写成单例模式

```java
    private static GetPerformance instance = new GetPerformance();

    private GetPerformance() {
        performance = new Performance();
    }

    public static GetPerformance getInstance() {
        if (instance == null) {
            instance = new GetPerformance();
        }
        return instance;
    }
```


线程的初始化

```java
	public void initThreadPool() {
        threadPool = Executors.newCachedThreadPool();
	    CS = new ExecutorCompletionService<>(threadPool);
    }
```

获取 Total 值

```java
	public void callable(int interval) {
        CS.submit(new Callable<ArrayList<Performance>>() {
            ArrayList<Performance> heapArrayList = new ArrayList<>();
            public ArrayList<Performance> call() throws Exception {
                while (getStart()) {
                    String totalMemory = exec.exec("adb shell dumpsys meminfo com.changba | grep TOTAL | awk \'{print $2}\' | sed -n \'1p\'").toString().trim();
                    Performance heap = new Performance();
                    heap.setTotalMemory(Integer.parseInt(totalMemory));
                    heapArrayList.add(heap);
                }
                return heapArrayList;
            }
        });
    }
```

获取上一步 return 的数据

```java
	public ArrayList<Performance> future() {
        ArrayList<Performance> perList = new ArrayList<>();
        try {
            perList = CS.take().get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        return perList;
    }
```

用于控制线程开始和结束

```java
	public boolean getStart() {
        return start;
    }

    public void setStart(boolean start) {
        this.start = start;
    }
}
```

拿到数据后，利用 jFreechart 生成图表，以附件形式展示在附件中。

#### 报告展示
取值间隔可以自定义，个人觉得太频繁没有必要。

![@CPU & Total MEM](https://i.loli.net/2018/01/17/5a5f11151f6e9.png)

如果数据较多，小图可能看不清，也可以放大查看

![@点击可以放大查看](https://i.loli.net/2018/01/17/5a5f11152ace2.png)


### 流畅度
#### Android View 的绘制
* Android 系统每隔 16ms 发出 VSYNC 信号，触发对 UI 进行渲染，如果每次绘制过程如果保证在16ms 以内，用户看到的就是一个流畅的画面。16ms = 1000ms/60，意思就是 1 秒 60 帧。
* 每一个 View 的绘制过程都必须经历三个最主要的过程，也就是 measure（计算）、layout（布局）和 draw（绘制）。所以上面提到的 16ms，也是这三个步骤所用的耗时。
* 如果1秒内没有绘制60帧，就发生了掉帧，而掉帧越多，用户看到的画面就越是不连贯。也就是越卡顿。

#### 取值
根据上面的描述，如果可以拿到每一秒的掉帧数据，然后就可以知道每一秒实际绘制了多少帧，这样就可以知道应用整体的 FPS 情况，也基本能表示应用整体的流畅度如何。那如何取得掉帧情况呢？

1. 首先需要了解一下 Choreographer 这个类，简单理解，这个类里面会有一个 looper，来处理 VSYNC 信号，然后执行 doFrame 方法，来刷新 UI。
2. 其实丢帧的数据，系统默认是一直有日志输出的，可以使用命令`adb shell logcat -v time -d Choreographer:I *:S`，但是因为SKIPPED_FRAME_WARNING_LIMIT 值默认设置为 30。导致UI线程 doFrame 时，只要丢帧不高于 30 帧，就不会通过 log 输出警告。
3. 所以获得我们想要的数据，只需要新建一个类，通过反射的方式来修改默认值。

代码如下：

```java
public class FPSFrameCallback implements Choreographer.FrameCallback {
	private static final int SKIPPED_FRAME_WARNING_LIMIT = 1;
	public void setWarningLimit(){
        if (Integer.parseInt(android.os.Build.VERSION.SDK)<16){
            return;
        }
        try {
            Class<?> onwChoreographer =Class.forName("android.view.Choreographer");
            Field mSkipped = onwChoreographer.getDeclaredField("SKIPPED_FRAME_WARNING_LIMIT");
            mSkipped.setAccessible(true);
            mSkipped.set(null,SKIPPED_FRAME_WARNING_LIMIT);
        }catch (Exception e){
            e.printStackTrace();
        }
    }
}
```

之后需要再 Mainactivity 的 onCreate 方法中，加一行代码

```java
FPSFrameCallback.setWarningLimit();
```

可以看到输出的 log 如下：
![@Jank frame per second|每秒掉帧数据](https://i.loli.net/2017/12/27/5a43400db7578.png)

由上图可以看出，会有几种情况需要处理，解决思路如下：
(1) 将属于同一秒的内的掉帧数据相加，得到每秒内的掉帧总数。
(2) 也会有未掉帧的秒数，即掉帧为 0，需要对未掉帧的秒数，进行补充数据。
(3) 某一秒掉帧总数大于 60，这种情况比较特殊，目前采取的校正方式是掉帧总数除以 60，取余。
(4) 用 60 减去某一秒的掉帧数据，得出的值就是这一秒内显示的总帧数。用这个值来体现流畅程度。

以上的步骤，都是准备工作，下面是涉及流畅度计算部分的代码：

开启线程

```java
public void callableForSM() {

        fpsCS.submit(new Callable<ArrayList<Integer>>() {

            ArrayList<Integer> jankArrayList = new ArrayList<>();

            public ArrayList<Integer> call() throws Exception {
                int interval = 5; //取值间隔
                long last_time = System.currentTimeMillis();
                String jankString; //存储logcat输出的内容
                String janknum = null; //存储掉帧数
                String lastTime; //上一行时间
                String currentTime = null; //当前行时间
                String pid = exec.exec("adb shell ps | grep com.changba | awk \'{print $2}\' | sed -n \'2p\'").toString();
```

循环取初始值

```java
       while (startSM) {
           long current_time = System.currentTimeMillis();
           if (current_time - last_time > interval * 1000) { //循环取值间隔
               last_time = current_time;
               jankString = exec.exec("adb shell logcat -v time -d  Choreographer:I *:S|grep \'Choreographer\'|awk \'{print $2,$"+p+"}\'").toString();
               if (jankString.length() > 0) {
                   logger.debug("fps start get value");
                   lastTime = jankString.substring(0, 8);
               } else {
                   logger.debug("!!! jankString.length() > 0");
                   continue;
               }
```

根据掉帧数分别处理

```java
       Integer sum = 0;

       while (jankString.length() > 14) {
           currentTime = jankString.substring(0, 8);

           if (jankString.charAt(14) == '\n') {//掉帧为个位数
               janknum = jankString.substring(13, 14);
               logger.debug("fps frame jank ========= " + janknum);
               if (jankString.length() == 15) {
                   jankString = " ";
               } else {
                   jankString = jankString.substring(15);
               }
           } else if (jankString.charAt(15) == '\n') {//掉帧为十位数
               janknum = jankString.substring(13, 15);
               logger.debug("fps frame jank ========= " + janknum);
               if (jankString.length() == 16) {
                   jankString = " ";
               } else {
                   jankString = jankString.substring(16);
               }
           }
```

计算相同秒数内的掉帧总数

```java
       if (lastTime.equals(currentTime)) {
           sum = sum + Integer.parseInt(janknum);//同一秒内掉帧之和
       } else {
           if (sum < 60) {
               jankArrayList.add(60 - sum);//当丢帧<60时，流畅度SM =60-丢帧数
           } else {
               int num = sum/60;
               jankArrayList.add(60 - sum % 60);//当丢帧frame>60时，流畅度SM = 60-丢帧数%60
               for (int i = 0; i < num; i++) {
                   jankArrayList.add(0);
               }

           }
           sum = Integer.parseInt(janknum);
           lastTime = currentTime;
       }
   }
```

处理同一秒内掉帧总数大于60的情况

```java
       if (sum != 0) {
           if (sum < 60)
               jankArrayList.add(60 - sum);
           else {
               int num = sum/60;
               jankArrayList.add(60 - sum % 60);
               for (int i = 0; i < num; i++) {
                   jankArrayList.add(0);
               }

```

填充没有掉帧的秒数的数据

```java
       int SM_60_Seconds = interval - jankArrayList.size();
       logger.debug("不掉帧的秒数为：" + SM_60_Seconds);
       for (int i = 0; i < SM_60_Seconds; i++) {
           jankArrayList.add(60);
       }
```

拿到处理好的数据之后，分别计算每一秒的 FPS 值，再将所有的 FPS 值， 根据区间（例如 50~60，40~50）计算出各自百分比，在报告中展示。

Choreographer.FrameCallback  这个接口，还可以做更多的事情，例如：我们可以重写 doFrame 函数，来输出跳帧所耗费的时间：

```java
    @Override
    public void doFrame(long frameTimeNanos) {
	    if (mLastFrameTimeNanos == 0) {
            mLastFrameTimeNanos = frameTimeNanos;
        }
        // 开始执行doFrame的时间
        long startNanos = System.nanoTime();
        // 接收VSYNC任务和实际开始执行的时间差
        final long jitterNanos = startNanos - frameTimeNanos;
        // 时间差大于16ms
        if (jitterNanos > mFrameIntervalNanos) {
            Log.d(TAG, "The jitterNanos is " + jitterNanos * 0.000001f + "ms");
        }
        mLastFrameTimeNanos = frameTimeNanos;
        mLastStartNanos = startNanos;
        // 注册下一帧的回调
        Choreographer.getInstance().postFrameCallback(this);
    }
```

其他用法，各位同学可以深入研究，根据自己的需要定制。

#### 报告展示
![@在 report 的 environment 部分展示整体的流畅度](https://i.loli.net/2018/01/04/5a4df5e89cb0b.png)


### 流量
#### 取值
通过命令`adb shell cat /proc/net/xt_qtaguid/stats`，可以分别获取到应用发送和接收流量的值，如下：
![@命令输出结果](https://i.loli.net/2018/01/04/5a4da09f6da3b.png)

上图可以看出，"rx\_bytes" & "tx\_bytes" 两列，分别是代表接收和发送的流量。
接下来，可以通过 uid 过滤应用的流量消耗。如下：
![@过滤uid之后](https://i.loli.net/2018/01/04/5a4da09e373a5.png)

根据上面，我们知道第 6 列和第 8 列，就是我们需要的原始的值，通过计算，就可以知道总的流量消耗。

这个实现起来要简单的多，代码实现如下：

接收 & 发送流量的值

```java
private int RxBytes(String PackageName) {
        String uid = UID(PackageName);
        int rxBytes = 0;
        String allRx = exec.exec("adb shell cat /proc/net/xt_qtaguid/stats
        | grep \'" + uid + "\' | awk \'{print $6}\'").toString();
        List<String> allRxList = Arrays.asList(allRx.split("\n"));
        for (String s : allRxList) {
            if (!s.equals("")) {
                rxBytes = rxBytes + Integer.parseInt(s);
            }
        }
        return rxBytes;
    }

private int TxBytes(String PackageName) {
        String uid = UID(PackageName);
        int txBytes = 0;
        String allTx = exec.exec("adb shell cat /proc/net/xt_qtaguid/stats
        | grep \'" + uid + "\' | awk \'{print $8}\'").toString();
        List<String> allTxList = Arrays.asList(allTx.split("\n"));
        for (String s : allTxList) {
            if (!s.equals("")) {
                txBytes = txBytes + Integer.parseInt(s);
            }
        }
        return txBytes;
    }
```

获取初始的流量值

```java
 private int getOriginalData(int x) {
        String packageName = "com.changba";
        int data = 0;
        switch (x) {
            case 0:
                data = GetPerformance.getInstance().RxBytes(packageName);
                break;
            case 1:
                data = GetPerformance.getInstance().TxBytes(packageName);
                break;
        }
        return data;
    }
```

计算每条用例消耗的流量

```java
public String dataForMethod(String methodName) {
        if (getOriginalData(0) > getPerf().getRxData()
        && getOriginalData(1) > getPerf().getTxData()) {
            rxResult = getOriginalData(0) - getPerf().getRxData();
            txResult = getOriginalData(1) - getPerf().getTxData();
            dataUsageSet();
        }
        int methodData = rxResult + txResult;
        totalData = totalData + methodData;
        performance.setTotalData(totalData);
        return methodName + " data usage is: " + methodData + " bytes"
        + "\n" + "Total data usage is: " + totalData + " bytes";
    }
```

上面的 totalData 用来记录自动化过程中总的流量消耗，最后会在报告中体现。

#### 报告展示
![@在每条用例的附件部分，展示当前用例的流量，以及累计流量](https://i.loli.net/2018/01/04/5a4dfc5f8b947.png)

## 与自动化的结合
我们使用了 TestNG 来组织测试用例，所以可以很方便的实现 IHookable, ITestListener 等接口，就可以在一些时间点来调用我们的性能测试代码，大概需要做的有：

针对内存和 CPU，根据 MethodName 过滤哪些需要收集性能数据

```java
	@Override
    public void onTestStart(ITestResult result) {
        if (result.getMethod().getMethodName().endsWith("_Per")) {
            if (getPerformance.getThreadPool() != null) {
                getPerformance.initThread("cpu");
                getPerformance.setStart(true);
                getPerformance.callable(1);
            }
        }
    }

	@Override
    public void run(IHookCallBack callBack, ITestResult testResult) {
        callBack.runTestMethod(testResult);
        if (testResult.getMethod().getMethodName().endsWith("_Per")) {
            try {
                getPerfPNG(testResult.getMethod().getMethodName());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
        dataForMethod(testResult.getMethod().getMethodName());
    }
```

针对流畅度测试，只需要在 onStart 和 onFinish 的方法内调用对应方法就可以了

```java
	@Override
    public void onStart(ITestContext context) {
        getPerformance.initThread("fps");
        if (getPerformance.getFpsCS() != null) {
            getPerformance.setStartSM(true);
            getPerformance.callableForSM();
        }
    }

    @Override
    public void onFinish(ITestContext context) {
        getPerformance.setStartSM(false);
        ArrayList<Integer> jankList = getPerformance.futureForSM();
        performance.setSMPercentage(getPerformance.getSMPercentage(jankList));
        if (getPerformance.getThreadPool() != null) {
            getPerformance.shutdown();
        }
    }

```

至于流量，从取值到计算都没有什么特别的地方，相对简单的多，就不再赘述。

## 后续

- FPS 这块有个坑，比如掉了10帧，fps 是50，这么看结果已经很不错了，但是如果是连续掉帧，那用户肯定还是可以感受到卡顿的，这个并没有能够体现出来。
- 镇对内存，计划在报告中加上不同机型的内存 limit 值，其次，也可以考虑，加上引起了多少次的 GC，Pause 了多久。
- 页面响应时间也是目前欠缺的，但是这个还需要好好研究，怎么保证，取到的值足够准确。
- 另外，启动时间和电量，目前觉得不适合接入。
