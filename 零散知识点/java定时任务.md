# java定时任务

## 简介
在 java中一个完整定时任务需要由Timer、TimerTask两个类来配合完成。 API中是这样定义他们的，Timer：一种工具，线程用其安排以后在后台线程中执行的任务。可安排任务执行一次，或者定期重复执行。由TimerTask：Timer 安排为一次执行或重复执行的任务。我们可以这样理解 **Timer是一种定时器工具，用来在一个后台线程计划执行指定任务，而TimerTask一个抽象类，它的子类代表一个可以被Timer计划的任务。**

### Timer类
在工具类Timer中，提供了四个构造方法，每个构造方法都启动了计时器线程，同时Timer类可以保证多个线程可以共享单个Timer对象而无需进行外部同步，所以Timer类是线程安全的。但是由于每一个Timer对象对应的是单个后台线程，用于顺序执行所有的计时器任务，一般情况下我们的线程任务执行所消耗的时间应该非常短，但是由于特殊情况导致某个定时器任务执行的时间太长，那么他就会“独占”计时器的任务执行线程，其后的所有线程都必须等待它执行完，这就会延迟后续任务的执行，使这些任务堆积在一起，具体情况我们后面分析。

当程序初始化完成Timer后，定时任务就会按照我们设定的时间去执行，Timer提供了schedule方法，该方法有多中重载方式来适应不同的情况，如下：
* schedule(TimerTask task, Date time)：安排在指定的时间执行指定的任务。
* schedule(TimerTask task, Date firstTime, long period) ：安排指定的任务在指定的时间开始进行重复的固定延迟执行。
* schedule(TimerTask task, long delay) ：安排在指定延迟后执行指定的任务。
* schedule(TimerTask task, long delay, long period) ：安排指定的任务从指定的延迟后开始进行重复的固定延迟执行。

同时也重载了scheduleAtFixedRate方法，scheduleAtFixedRate方法与schedule相同，只不过他们的侧重点不同，区别后面分析。
* scheduleAtFixedRate(TimerTask task, Date firstTime, long period)：安排指定的任务在指定的时间开始进行重复的固定速率执行。
* scheduleAtFixedRate(TimerTask task, long delay, long period)：安排指定的任务在指定的延迟后开始进行重复的固定速率执行。

### TimerTask
TimerTask类是一个抽象类，由Timer 安排为一次执行或重复执行的任务。它有一个抽象方法run()方法，该方法用于执行相应计时器任务要执行的操作。因此每一个具体的任务类都必须继承TimerTask，然后重写run()方法。

另外它还有两个非抽象的方法：
* boolean cancel()：取消此计时器任务。
* long scheduledExecutionTime()：返回此任务最近实际执行的安排执行时间。

## 实例
延迟指定时间，执行定时任务
``` Java
public class TimerTest01 {
    Timer timer;
    public TimerTest01(int time){
        timer = new Timer();
        timer.schedule(new TimerTaskTest01(), time * 1000);
    }
    
    public static void main(String[] args) {
        System.out.println("timer begin....");
        new TimerTest01(3);
    }
}

public class TimerTaskTest01 extends TimerTask{

    public void run() {
        System.out.println("Time's up!!!!");
    }
}
```

在延迟指定时间后以指定的间隔时间循环执行定时任务
``` Java
public class TimerTest03 {
    Timer timer;
    
    public TimerTest03(){
        timer = new Timer();
        timer.schedule(new TimerTaskTest03(), 1000, 2000);
    }
    
    public static void main(String[] args) {
        new TimerTest03();
    }
}

public class TimerTaskTest03 extends TimerTask{

    @Override
    public void run() {
        Date date = new Date(this.scheduledExecutionTime());
        System.out.println("本次执行该线程的时间为：" + date);
    }
}
```
对于这个线程任务,如果我们不将该任务停止,他会一直运行下去。

## Timer的缺陷
前面Timer在执行定时任务时只会创建一个线程任务，如果存在多个线程，若其中某个线程因为某种原因而导致线程任务执行时间过长，超过了两个任务的间隔时间，会发生一些缺陷：
1. 如果 task1 的执行时间过长，或导致 task2 的任务受影响，比如 task2 3秒后执行任务，但是 task1 4秒后才结束，导致 task2 也是 4秒后才能开始任务
2. 如果 task1 抛出了 exception，会导致 task2 无法运行

## ScheduledThreadPoolExecutor 
对于Timer的缺陷，我们可以考虑 ScheduledThreadPoolExecutor 来替代。Timer是基于绝对时间的，对系统时间比较敏感，而ScheduledThreadPoolExecutor 则是基于相对时间；Timer是内部是单一线程，而ScheduledThreadPoolExecutor内部是个线程池，所以可以支持多个任务并发执行。

[Java 定时任务详解](https://www.cnblogs.com/chenssy/p/3788407.html)