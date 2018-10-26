## Android Memory 相关总结
---

[TOC]

#### 内存泄漏
**简单的说，就是new出来的Object 放在Heap上无法被GC回收。**

#### java中的内存分配：
- **静态储存区**：编译时就分配好，在程序整个运行期间都存在。它主要存放静态数据和常量；
- **栈区**：当方法执行时，会在栈区内存中创建方法体内部的局部变量，方法结束后自动释放内存；
- **堆区**：通常存放 new 出来的对象。由 Java 垃圾回收器回收。


#### 四种引用类型的介绍
- **强引用(StrongReference)**：JVM 宁可抛出 OOM ，也不会让 GC 回收具有强引用的对象；
- **软引用(SoftReference)**：只有在内存空间不足时，才会被回的对象；
- **弱引用(WeakReference)**：在 GC 时，一旦发现了只具有弱引用的对象，不管当前内存空间足够与否，都会回收它的内存；
- **虚引用(PhantomReference)**：任何时候都可以被GC回收，当垃圾回收器准备回收一个对象时，如果发现它还有虚引用，就会在回收对象的内存之前，把这个虚引用加入到与之关联的引用队列中。程序可以通过判断引用队列中是否存在该对象的虚引用，来了解这个对象是否将要被回收。可以用来作为GC回收Object的标志。
**我们常说的内存泄漏是指new出来的Object无法被GC回收，即为强引用。**

#### Java 的 GC（Garbage Collection）
**GC 是一种自动的存储管理机制。当一些被占用的内存不再需要时，就应该予以释放，以让出空间，这种存储资源管理，称为垃圾回收。**

##### 执行时机：
1. 当应用程序空闲时，即没有应用线程在运行时，GC会被调用。因为GC在优先级最低的线程中进行,所以当应用忙时，GC线程就不会被调用，但以下条件除外。
2.  Java堆内存不足时，GC会被调用。当应用线程在运行，并在运行过程中创建新对象，若这时内存空间不足，JVM就会强制地调用GC线程，以便回收内存用于新的分配。
3.  若GC一次之后仍不能满足内存分配的要求，JVM会再进行两次GC作进一步的尝试，若仍无法满足要求，则 JVM将报**“Out Of Memory”**的错误，引起App的**Crash**。


##### 影响：
当垃圾回收开始清理资源时，其余的所有线程都会被停止。所以，我们要做的就是尽可能的让它执行的时间变短。如果清理的时间过长，在我们的应用程序中就能感觉到明显的卡顿。

#### GC的类型
- **GC_FOR_MALLOC**：表示是在堆上分配对象时内存不足触发的GC。
- **GC_CONCURRENT**：当我们应用程序的堆内存达到一定量，或者可以理解为快要满的时候，系统会自动触发GC操作来释放内存。
- **GC_EXPLICIT**：表示是应用程序调用System.gc、VMRuntime.gc接口或者收到SIGUSR1信号时触发的GC。
- **GC_BEFORE_OOM**：表示是在准备抛OOM异常之前进行的最后努力而触发的GC。
- **并发和非并发GC**：并发有条件地挂起和唤醒非GC线程，而非并发在执行GC的过程中，一直都是挂起非GC线程的。并行GC就可以使得应用程序获得更好的响应性。但是并发GC也会占用更多的CPU资源。
- **ART and dalvik**：总的来看，art在gc上做的比dalvik好太多了，不光是gc的效率，减少pause时间，而且还在内存分配上对大内存的有单独的分配区域，同时还能有算法在后台做内存整理，减少内存碎片。对于开发者来说art下我们基本可以避免很多类似gc导致的卡顿问题了。另外根据谷歌自己的数据来看，Art相对Dalvik内存分配的效率提高了10倍，GC的效率提高了2-3倍。
**可以通过log查看GC的情况，也可根据log判断目前app的内存使用情况。**

#### 获取内存（Pss）
一、使用 android studio 提供的 monitors 工具查看；
此数据为**java**层的内存
![Alt text](./屏幕快照 2017-04-28 下午3.38.22.png)

##### 关注点：
- 退出某个页面后，内存是否回落。如果没有及时回落，也不一定就是问题，可能程序还没有自动GC，故一般情况下，需要手动GC，如果手动GC后，仍无法回落，此时可以确定有问题。
- 进行某个操作后，内存增长的过快，也可能存在风险，此时可反复操作进行确认。

二、使用 **dumpsys meminfo packagename/pid** 查看 Dalvik Heap;
![Alt text](./屏幕快照 2017-04-28 下午3.36.27.png)

##### 关注点：
- Native/Dalvik 的 Heap 信息中的alloc，具体在上面的第一行和第二行，它分别给出的是**JNI**层和**Java**层的内存分配情况，如果发现这个值一直增长，则代表程序可能出现了内存泄漏。
- Total 的 PSS 信息，这个值就是你的应用真正占据的内存大小。

三、上面提到了GC的log可以查看当前应用内存的使用情况，请看如下log，其中 **117MB/132MB** 就是当前已使用的内存和已分配内存。
`logI/art: Background sticky concurrent mark sweep GC freed 176032(11MB) AllocSpace objects, 25(3MB) LOS objects, 10% free, 117MB/132MB, paused 5.467ms total 68.455ms`
	 
#### 测试内存时的参考数据：
因为不同的设备，配置相差较大，所以在内存表现上也会相差很多，所以，通常在测试前，可以通过命令 **getprop | grep heap** 可以得到如下值：

```[dalvik.vm.heapgrowthlimit]: [256m]```
```[dalvik.vm.heapsize]: [512m]```
**heapgrowthlimit** 表示单个应用可分配的内存最大值，**heapsize** 表示单个虚拟机最大的内存，如果应用设置了largeHeap="true"，则理论上可以申请的最大内存就是 heapsize 的值，需要注意的是，**设置了largeHeap="true"，会导致GC频繁且耗时，影响性能**。
另外，**nativeheap** 的增长并不受 **heapsize** 的限制。

### 参考文档
[利用Android Studio、MAT对Android进行内存泄漏检测](https://joyrun.github.io/2016/08/08/AndroidMemoryLeak)
[Android 官方针对GC的说明](https://developer.android.com/studio/profile/investigate-ram.html?hl=zh-cn)
[Android GC 原理探究](https://mp.weixin.qq.com/s/CUU3Ml394H_fkabhNNX32Q)



