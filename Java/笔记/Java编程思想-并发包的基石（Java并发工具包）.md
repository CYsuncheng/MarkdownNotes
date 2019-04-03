# 并发包的基石（Java并发工具包）
## 原子变量和 CAS

``` Java
public class Counter { 
	private int count; 
	public synchronized void incr(){ 
		count++; 
	} 
	public synchronized int getCount() { 
		return count; 
	} 
}
```

对于使用变量 count++ 这种操作来说，使用 synchronized 成本太高了，需要先获取锁，最后需要释放锁，获取不到锁的情况下需要等待，还会有线程的上下文切换，这些都需要成本。

对于这种情况，完全可以使用原子变量代替，Java并发包中的基本原子变量类型有以下几种。
* AtomicBoolean：原子 Boolean类型，常用来在程序中表示一个标志位。
* AtomicInteger：原子 Integer类型。
* AtomicLong：原子 Long类型，常用来在程序中生成唯一序列号。
* AtomicReference：原子引用类型，用来以原子方式更新复杂类型。

> 除了这 4个类，还有一些其他类，如针对数组类型的类 AtomicLongArray、 AtomicReferenceArray，以及用于以原子方式更新对象中的字段的类，如 AtomicIntegerFieldUpdater、 AtomicReferenceFieldUpdater等。 Java 8增加了几个类，在高并发统计汇总的场景中更为适合，包括 LongAdder、 LongAccumulator、 Double-Adder和 DoubleAccumulator 等。  

### AtomicInteger
#### 基本用法
AtomicInteger有两个构造方法： 

``` Java
public AtomicInteger(int initialValue) 
public AtomicInteger()
```

第一个构造方法给定了一个初始值，第二个构造方法的初始值为 0。

可以直接获取或设置 AtomicInteger中的值，方法是： 

``` Java
public final int get() 
public final void set(int newValue)
```

之所以称为原子变量，是因为它包含一些以原子方式实现组合操作的方法，部分方法如下：

``` Java
//以原子方式获取旧值并设置新值 
public final int getAndSet(int newValue) 
//以原子方式获取旧值并给当前值加 1 
public final int getAndIncrement() 
//以原子方式获取旧值并给当前值减 1 
public final int getAndDecrement() 
//以原子方式获取旧值并给当前值加 delta 
public final int getAndAdd(int delta) 
//以原子方式给当前值加 1并获取新值 
public final int incrementAndGet() 
//以原子方式给当前值减 1并获取新值 
public final int decrementAndGet() 
//以原子方式给当前值加 delta并获取新值 
public final int addAndGet(int delta)
```

这些方法的实现都依赖另一个 public方法： 

``` Java
public final boolean compareAndSet(int expect, int update)
```

**compareAndSet是一个非常重要的方法，比较并设置，我们以后将简称为 CAS。**该方法有两个参数 expect和 update，以原子方式实现了如下功能：如果当前值等于 expect，则更新为 update，否则不更新，如果更新成功，返回 true，否则返回 false。

#### 基本原理和思维
它的主要内部成员是：

``` Java
private volatile int value;
```

**它的声明带有 volatile，这是必需的，以保证内存可见性。**

它的大部分更新方法实现都类似，我们看一个方法 incrementAndGet，其代码为：

``` Java
public final int incrementAndGet() {
	for(;;) {
		int current = get(); 
		int next = current + 1; 
		if(compareAndSet(current, next)) 
			return next; 
		} 
	}
```

代码主体是个死循环，先获取当前值 current，计算期望的值 next，然后调用 CAS方法进行更新，如果更新没有成功，说明 value被别的线程改了，则再去取最新值并尝试更新直到成功为止。

与 synchronized锁相比，这种原子更新方式代表一种不同的思维方式。 synchronized是悲观的，它假定更新很可能冲突，所以先获取锁，得到锁后才更新。原子变量的更新逻辑是乐观的，它假定冲突比较少，但使用 CAS更新，也就是进行冲突检测，如果确实冲突了，那也没关系，继续尝试就好了。 synchronized代表一种阻塞式算法，得不到锁的时候，进入锁等待队列，等待其他线程唤醒，有上下文切换开销。原子变量的更新逻辑是非阻塞式的，更新冲突的时候，它就重试，不会阻塞，不会有上下文切换开销。对于大部分比较简单的操作，无论是在低并发还是高并发情况下，这种乐观非阻塞方式的性能都远高于悲观阻塞式方式。

#### ABA问题
使用 CAS方式更新有一个 ABA问题。该问题是指，假设当前值为 A，如果另一个线程先将 A修改成 B，再修改回成 A，当前线程的 CAS操作无法分辨当前值发生过变化。

解决方法是使用 AtomicStampedReference，在修改值的同时附加一个时间戳，只有值和时间戳都相同才进行修改。比较多，不详细写了。

## 显式锁
### 可重入锁 ReentrantLock
#### 基本用法
ReentrantLock有两个构造方法： 

``` Java
public ReentrantLock() 
public ReentrantLock(boolean fair)
```

参数 fair表示是否保证公平，不指定的情况下，默认为 false，表示不保证公平。所谓公平是指，等待时间最长的线程优先获得锁。保证公平会影响性能，一般也不需要，所以默认不保证， synchronized锁也是不保证公平的。

使用显式锁，一定要记得调用 unlock。一般而言，应该将 lock之后的代码包装到 try语句内，在 finally语句内释放锁。比如，使用 ReentrantLock实现 Counter，代码可以为：

``` Java
public class Counter { 
	private final Lock lock = new ReentrantLock(); 
	private volatile int count; 
	public void incr() { 
		lock.lock(); 
		try { 
			count++; 
		} 
		finally { 
			lock.unlock(); 
		}
	} 
	public int getCount() { 
		return count; 
	} 
}
```

**使用 tryLock（），可以避免死锁**。在持有一个锁获取另一个锁而获取不到的时候，可以释放已持有的锁，给其他线程获取锁的机会，然后重试获取所有锁。

Java提供了一个抽象类 AbstractQueued-Synchronizer，简称 AQS。

#### 对比 ReentrantLock和 synchronized
相比 synchronized， ReentrantLock可以实现与 synchronized相同的语义，而且支持以非阻塞方式获取锁，可以响应中断，可以限时，更为灵活。不过， synchronized的使用更为简单，写的代码更少，也更不容易出错。

synchronized代表一种声明式编程思维，程序员更多的是表达一种同步声明，由 Java系统负责具体实现，程序员不知道其实现细节；显式锁代表一种命令式编程思维，程序员实现所有细节。

声明式编程的好处除了简单，还在于性能，在较新版本的 JVM上， ReentrantLock和 synchronized的性能是接近的，但 Java编译器和虚拟机可以不断优化 synchronized的实现，比如自动分析 synchronized的使用，对于没有锁竞争的场景，自动省略对锁获取/释放的调用。

简单总结下，能用 synchronized就用 synchronized，不满足要求时再考虑 Reentrant-Lock。