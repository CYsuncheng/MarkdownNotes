# 同步和协作工具类

Java并发包中有一些专门的同步和协作工具类，本章，我们就来探讨它们。具体工具类包括：
* 读写锁 ReentrantReadWriteLock。
* 信号量 Semaphore。
* 倒计时门栓 CountDownLatch。
* 循环栅栏 CyclicBarrier。
* 此外，有一个实现线程安全的特殊概念：线程本地变量 ThreadLocal

## 读写锁 ReentrantReadWriteLock
ReadWriteLock的定义为： 

``` Java
public interface ReadWriteLock { 
	Lock readLock(); 
	Lock writeLock(); 
}
```

通过一个 ReadWriteLock产生两个锁：一个读锁，一个写锁。读操作使用读锁，写操作使用写锁。需要注意的是，只有“读-读”操作是可以并行的，“读-写”和“写-写”都不可以。

## 信号量 Semaphore
之前介绍的锁都是限制只有一个线程可以同时访问一个资源。现实中，资源往往有多个，但每个同时只能被一个线程访问，比如，饭店的饭桌、火车上的卫生间。有的单个资源即使可以被并发访问，但并发访问数多了可能影响性能，所以希望限制并发访问的线程数。还有的情况，与软件的授权和计费有关，对不同等级的账户，限制不同的最大并发访问数。

信号量类 Semaphore就是用来解决这类问题的，它可以限制对资源的并发访问数，它有两个构造方法： 

``` Java
public Semaphore(int permits) 
public Semaphore(int permits, boolean fair) 
//fire表示公平，含义与之前介绍的是类似的， permits表示许可数量。
```

## 倒计时门栓 CountDownLatch
CountDownLatch。它相当于是一个门栓，一开始是关闭的，所有希望通过该门的线程都需要等待，然后开始倒计时，倒计时变为 0后，门栓打开，等待的所有线程都可以通过，它是一次性的，打开后就不能再关上了。

门栓的两种应用场景：一种是同时开始，另一种是主从协作。

## 循环栅栏 CyclicBarrier
CyclicBarrier。它相当于是一个栅栏，所有线程在到达该栅栏后都需要等待其他线程，等所有线程都到达后再一起通过，它是循环的，可以用作重复的同步。

CyclicBarrier特别适用于并行迭代计算，每个线程负责一部分计算，然后在栅栏处等待其他线程完成，所有线程到齐后，交换数据和计算结果，再进行下一次迭代。

## 理解 ThreadLocal
线程本地变量是说，每个线程都有同一个变量的独有拷贝。

ThreadLocal就是一个单一对象的容器，比如：

``` Java
public static void main(String[] args) { 
	ThreadLocal <Integer> local = new ThreadLocal <>(); 
	local.set(100); 
	System.out.println(local.get());
}
```

它们访问的虽然是同一个变量 local，但每个线程都有自己的独立的值，这就是线程本地变量的含义。

### 原理
每个线程都有一个 Map，对于每个 ThreadLocal对象，调用其 get/set实际上就是以 ThreadLocal对象为键读写当前线程的 Map，这样，就实现了每个线程都有自己的独立副本的效果。