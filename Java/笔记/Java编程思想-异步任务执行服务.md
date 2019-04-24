# 异步任务执行服务
## 基本接口
* Runnable和 Callable：表示要执行的异步任务。
* Executor和 ExecutorService：表示执行服务。
* Future：表示异步任务的结果。

Runnable没有返回结果，而 Callable有， Runnable不会抛出异常，而 Callable会。

ExecutorService有两个关闭方法： shutdown和 shutdownNow。区别是， shutdown表示不再接受新任务，但已提交的任务会继续执行，即使任务还未开始执行； shutdownNow不仅不接受新任务，而且会终止已提交但尚未执行的任务，对于正在执行的任务，一般会调用线程的 interrupt方法尝试中断，不过，线程可能不响应中断， shutdownNow会返回已提交但尚未执行的任务列表。

ExecutorService有两组批量提交任务的方法： invokeAll和 invokeAny，它们都有两个版本，其中一个限定等待时间。 invokeAll等待所有任务完成，返回的 Future列表中，每个 Future的 isDone方法都返回 true，不过 isDone为 true不代表任务就执行成功了，可能是被取消了。 invokeAll可以指定等待时间，如果超时后有的任务没完成，就会被取消。而对于 invokeAny，只要有一个任务在限时内成功返回了，它就会返回该任务的结果，其他任务会被取消；如果没有任务能在限时内成功返回，抛出 TimeoutException；如果限时内所有任务都结束了，但都发生了异常，抛出 ExecutionException。

ExecutorService的主要实现类是 ThreadPoolExecutor

## 线程池
Java并发包中线程池的实现类是 ThreadPoolExecutor，它继承自 AbstractExecutor-Service，实现了 ExecutorService

### 线程池大小
线程池的大小主要与 4个参数有关： 
* corePoolSize：核心线程个数。
* maximumPoolSize：最大线程个数。
* keepAliveTime和 unit：空闲线程存活时间。

maximumPoolSize表示线程池中的最多线程数，线程的个数会动态变化，但这是最大值，不管有多少任务，都不会创建比这个值大的线程个数。 corePoolSize表示线程池中的核心线程个数，不过，并不是一开始就创建这么多线程，刚创建一个线程池后，实际上并不会创建任何线程。

有新任务到来的时候，如果当前线程个数小于 corePoolSiz，就会创建一个新线程来执行该任务，需要说明的是，即使其他线程现在也是空闲的，也会创建新线程。不过，如果线程个数大于等于 corePoolSiz，那就不会立即创建新线程了，它会先尝试排队，需要强调的是，它是“尝试”排队，而不是“阻塞等待”入队，如果队列满了或其他原因不能立即入队，它就不会排队，而是检查线程个数是否达到了 maximumPoolSize，如果没有，就会继续创建线程，直到线程数达到 maximumPoolSize。

ThreadPoolExecutor还可以查看关于线程和任务数的一些动态数字：

``` Java
//返回当前线程个数 
public int getPoolSize() 
//返回线程池曾经达到过的最大线程个数 
public int getLargestPoolSize() 
//返回线程池自创建以来所有已完成的任务数 
public long getCompletedTaskCount() 
//返回所有任务数，包括所有已完成的加上所有排队待执行的 
public long getTaskCount()
```

### 任务拒绝策略
拒绝策略是可以自定义的， ThreadPoolExecutor实现了 4种处理方式。 
1. ThreadPoolExecutor. AbortPolicy：这就是默认的方式，抛出异常。 
2. ThreadPoolExecutor. DiscardPolicy：静默处理，忽略新任务，不抛出异常，也不执行。
3. ThreadPoolExecutor. DiscardOldestPolicy：将等待时间最长的任务扔掉，然后自己排队。
4. ThreadPoolExecutor. CallerRunsPolicy：在任务提交者线程中执行任务，而不是交给线程池中的线程执行。

默认情况下，提交任务的方法（如 execute/ submit/ invokeAll等）会抛出异常，类型为 RejectedExecutionException。

### 关于核心线程的特殊配置
线程个数小于等于 corePoolSize时，我们称这些线程为核心线程，默认情况下
* 核心线程不会预先创建，只有当有任务时才会创建。
* 核心线程不会因为空闲而被终止， keepAliveTime参数不适用于它。

不过， ThreadPoolExecutor有如下方法，可以改变这个默认行为。

``` Java
//预先创建所有的核心线程 
public int prestartAllCoreThreads() 
//创建一个核心线程，如果所有核心线程都已创建，则返回 false 
public boolean prestartCoreThread() 
//如果参数为 true，则 keepAliveTime参数也适用于核心线程 
public void allowCoreThreadTimeOut(boolean value)
```

newSingleThreadExecutor，只使用一个线程，使用无界队列 LinkedBlockingQueue，线程创建后不会超时终止，该线程顺序执行所有任务。该线程池适用于需要确保所有任务被顺序执行的场合。

newFixedThreadPool，使用固定数目的 n个线程，使用无界队列 LinkedBlockingQueue，线程创建后不会超时终止。和 newSingleThreadExecutor一样，由于是无界队列，如果排队任务过多，可能会消耗过多的内存。

newCachedThreadPool，它的 corePoolSize为 0， maximumPoolSize为 Integer. MAX_ VALUE， keepAliveTime是 60秒，队列为 SynchronousQueue。它的含义是：当新任务到来时，如果正好有空闲线程在等待任务，则其中一个空闲线程接受该任务，否则就总是创建一个新线程，创建的总线程个数不受限制，对任一空闲线程，如果 60秒内没有新任务，就终止。

在系统负载很高的情况下， newFixedThreadPool可以通过队列对新任务排队，保证有足够的资源处理实际的任务，而 newCachedThreadPool会为每个任务创建一个线程，导致创建过多的线程竞争 CPU和内存资源，使得任何实际任务都难以完成，这时， newFixedThreadPool更为适用。

不过，如果系统负载不太高，单个任务的执行时间也比较短， newCachedThreadPool的效率可能更高，因为任务可以不经排队，直接交给某一个空闲线程。

在系统负载可能极高的情况下，两者都不是好的选择， newFixedThreadPool的问题是队列过长，而 newCachedThreadPool的问题是线程过多，这时，应根据具体情况自定义 ThreadPoolExecutor，传递合适的参数。

### 线程池的死锁
就是任务之间有依赖，这种情况可能会出现死锁。比如任务 A，在它的执行过程中，它给同样的任务执行服务提交了一个任务 B，但需要等待任务 B结束。如果任务 A是提交给了一个单线程线程池，一定会出现死锁， A在等待 B的结果，而 B在队列中等待被调度。如果是提交给了一个限定线程个数的线程池，也有可能因线程数限制出现死锁。

## 定时任务
在 Java中，主要有两种方式实现定时任务：
* 使用 java. util包中的 Timer和 TimerTask。
* 使用 Java并发包中的 ScheduledExecutorService。

### Timer和 TimerTask
TimerTask表示一个定时任务，它是一个抽象类，实现了 Runnable，具体的定时任务需要继承该类，实现 run方法。 Timer是一个具体类，它负责定时任务的调度和执行，方法如下

``` Java
//在指定绝对时间 time运行任务 task 
public void schedule(TimerTask task, Date time) 
//在当前时间延时 delay毫秒后运行任务 task 
public void schedule(TimerTask task, long delay) 
//固定延时重复执行，第一次计划执行时间为 firstTime，后一次的计划执行时间为前一次"实际"执行时间加上 period 
public void schedule(TimerTask task, Date firstTime, long period) 
//同样是固定延时重复执行，第一次执行时间为当前时间加上 delay 
public void schedule(TimerTask task, long delay, long period) 
//固定频率重复执行，第一次计划执行时间为 firstTime，后一次的计划执行时间为前一次"计划"执行时间加上 period 
public void scheduleAtFixedRate(TimerTask task, Date firstTime, long period) 
//同样是固定频率重复执行，第一次计划执行时间为当前时间加上 delay 
public void scheduleAtFixedRate(TimerTask task, long delay, long period)
```

需要注意固定延时（fixed-delay）与固定频率（fixed-rate）的区别，二者都是重复执行，但后一次任务执行相对的时间是不一样的，对于固定延时，它是基于上次任务的“实际”执行时间来算的，如果由于某种原因，上次任务延时了，则本次任务也会延时，而固定频率会尽量补够运行次数。

另外，需要注意的是，如果第一次计划执行的时间 firstTime是一个过去的时间，则任务会立即运行，对于固定延时的任务，下次任务会基于第一次执行时间计算，而对于固定频率的任务，则会从 firstTime开始算，有可能加上 period后还是一个过去时间，从而连续运行很多次，直到时间超过当前时间。

需要强调的是，一个 Timer对象只有一个 Timer线程

在执行任务之前， Timer线程判断任务是否为周期任务，如果是，就设置下次执行的时间并添加到优先级队列中，对于固定延时的任务，下次执行时间为当前时间加上 period，对于固定频率的任务，下次执行时间为上次计划执行时间加上 period。

关于 Timer线程，还需要强调非常重要的一点：在执行任何一个任务的 run方法时，一旦 run抛出异常， Timer线程就会退出，从而所有定时任务都会被取消。

## ScheduledExecutorService
ScheduledExecutorService是一个接口，其定义为：

``` Java
public interface ScheduledExecutorService extends ExecutorService { 
//单次执行，在指定延时 delay后运行 command 
public ScheduledFuture <?> schedule(Runnable command, long delay, TimeUnit unit); 
//单次执行，在指定延时 delay后运行 callable 
public <V> ScheduledFuture <V> schedule(Callable <V> callable, long delay, TimeUnit unit); 
//固定频率重复执行 
public ScheduledFuture <?> scheduleAtFixedRate(Runnable command, long initialDelay, long period, TimeUnit unit); 
//固定延时重复执行 
public ScheduledFuture <?> scheduleWithFixedDelay(Runnable command, long initialDelay, long delay, TimeUnit unit); 
}
```

ScheduledThreadPoolExecutor的实现思路与 Timer基本是类似的，都有一个基于堆的优先级队列，保存待执行的定时任务，它的主要不同是：
1. 它的背后是线程池，可以有多个线程执行任务。
2. 它在任务执行后再设置下次执行的时间，对于固定延时的任务更为合理。
3. 任务执行线程会捕获任务执行过程中的所有异常，一个定时任务的异常不会影响其他定时任务，不过，发生异常的任务（即使是一个重复任务）不会再被调度。