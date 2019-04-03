# 并发（基础知识）
## 基础知识
### 创建线程
在 Java中创建线程有两种方式：一种是继承 Thread；另外一种是实现 Runnable接口。

### 线程的基本属性和方法
daemon线程有什么用呢？它一般是其他线程的辅助线程，在它辅助的主线程退出的时候，它就没有存在的意义了。在我们运行一个即使最简单的"hello world"类型的程序时，实际上， Java也会创建多个线程，除了 main线程外，至少还有一个负责垃圾回收的线程，这个线程就是 daemon线程，在 main线程结束的时候，垃圾回收线程也会退出。

Thread.sleep()，睡眠期间，该线程会让出 CPU，但睡眠的时间不一定是确切的给定毫秒数，可能有一定的偏差，偏差与系统定时器和操作系统调度器的准确度和精度有关。

Thread还有一个让出 CPU的方法： `public static native void yield();` 这也是一个静态方法，调用该方法，是告诉操作系统的调度器：我现在不着急占用 CPU，你可以先让其他线程运行。不过，这对调度器也仅仅是建议，调度器如何处理是不一定的，它可能完全忽略该调用。

Thread有一个 join方法，可以让调用 join的线程等待该线程结束。

### 线程内存共享
所谓竞态条件（race condition）是指，当多个线程访问和操作同一个对象时，最终执行结果与执行时序有关，可能正确也可能不正确。

内存可见性，多个线程可以共享访问和操作相同的变量，但一个线程对一个共享变量的修改，另一个线程不一定马上就能看到，甚至永远也看不到。

这就是内存可见性问题。在计算机系统中，除了内存，数据还会被缓存在 CPU的寄存器以及各级缓存中，当访问一个变量时，可能直接从寄存器或 CPU缓存中获取，而不一定到内存中去取，当修改一个变量时，也可能是先写到缓存中，稍后才会同步更新到内存中。在单线程的程序中，这一般不是问题，但在多线程的程序中，尤其是在有多 CPU的情况下，这就是严重的问题。一个线程对内存的修改，另一个线程看不到，一是修改没有及时同步到内存，二是另一个线程根本就没从内存读。

### 成本
关于线程，我们需要知道，它是有成本的。创建线程需要消耗操作系统的资源，操作系统会为每个线程创建必要的数据结构、栈、程序计数器等，创建也需要一定的时间。

此外，线程调度和切换也是有成本的。一个线程被切换出去后，操作系统需要保存它的当前上下文状态到内存，上下文状态包括当前 CPU寄存器的值、程序计数器的值等，而一个线程被切换回来后，操作系统需要恢复它原来的上下文状态，整个过程称为上下文切换，这个切换不仅耗时，而且使 CPU中的很多缓存失效。

另外，如果执行的任务都是 CPU密集型的，即主要消耗的都是 CPU，那创建超过 CPU数量的线程就是没有必要的，并不会加快程序的执行。

## 理解 synchronized
### 用法和基本原理
synchronized可以用于修饰类的实例方法、静态方法和代码块，我们分别介绍。

#### 实例方法
synchronized使得同时只能有一个线程执行实例方法，但这个理解是不确切的。多个线程是可以同时执行同一个 synchronized实例方法的，只要它们访问的对象是不同的即可。

所以， synchronized实例方法实际保护的是同一个对象的方法调用，确保同时只能有一个线程执行。再具体来说， synchronized实例方法保护的是当前实例对象，即 this， this对象有一个锁和一个等待队列，锁只能被一个线程持有，其他试图获得同样锁的线程需要等待。

**synchronized保護的是對象而非代碼，只要訪問的是同一個對象的 synchronized方法，即使是不同的代碼，也會被同步順序訪問。**

需要说明的是， synchronized方法不能防止非 synchronized方法被同时执行。这通常会出现非期望的结果，所以，一般在保护变量时，需要在所有访问该变量的方法上加上 synchronized。

#### 静态方法
前面我们说， synchronized保护的是对象，对实例方法，保护的是当前实例对象 this，对静态方法，保护的是哪个对象呢？是类对象，实际上，每个对象都有一个锁和一个等待队列，类对象也不例外。 

synchronized静态方法和 synchronized实例方法保护的是不同的对象，不同的两个线程，可以一个执行 synchronized静态方法，另一个执行 synchronized实例方法。

#### 代码块
实例：synchronized(this){}

静态：synchronized(StaticXXX.class){}

synchronized同步的对象可以是任意对象，任意对象都有一个锁和等待队列，或者说，任何对象都可以作为锁对象。

使用单独对象作为锁：
``` Java
public class Counter { 
	private int count; 
	private Object lock = new Object(); 
	public void incr(){ 
		synchronized(lock){ 
			count + +; 
		} 
	} 
	public int getCount() { 
		synchronized(lock){ 
			return count;
		} 
	}
}
```

### 理解 synchronized
#### 可重入性
synchronized有一个重要的特征，它是可重入的，也就是说，对同一个执行线程，它在获得了锁之后，在调用其他需要同样锁的代码时，可以直接调用。

可重入是通过记录锁的持有线程和持有数量来实现的，当调用被 synchronized保护的代码时，检查对象是否已被锁，如果是，再检查是否被当前线程锁定，如果是，增加持有数量，如果不是被当前线程锁定，才加入等待队列，当释放锁时，减少持有数量，当数量变为 0时才释放整个锁。

#### 内存可见性
synchronized除了保证原子操作外，它还有一个重要的作用，就是保证内存可见性，在释放锁时，所有写入都会写回内存，而获得锁后，都会从内存中读最新数据。

不过，如果只是为了保证内存可见性，使用 synchronized的成本有点高，有一个更轻量级的方式，那就是给变量加修饰符 **volatile**。
``` Java
public class Switcher { 
	private volatile boolean on; 
	public boolean isOn() { 
		return on; 
	} 
	public void setOn(boolean on) { 
		this. on = on; 
	} 
}
```
加了 volatile之后， Java会在操作对应变量时插入特殊的指令，保证读写到内存最新值，而非缓存的值。

#### 死锁
使用 synchronized或者其他锁，要注意死锁。所谓死锁就是类似这种现象，比如，有 a、 b两个线程， a持有锁 A，在等待锁 B，而 b持有锁 B，在等待锁 A， a和 b陷入了互相等待，最后谁都执行不下去。

怎么解决呢？首先，应该尽量避免在持有一个锁的同时去申请另一个锁，如果确实需要多个锁，所有代码都应该按照相同的顺序去申请锁。比如，对于上面的例子，可以约定都先申请 lockA，再申请 lockB。

还有一种方法是使用后续章节介绍的显式锁接口 Lock，它支持尝试获取锁（tryLock）和带时间限制的获取锁方法，使用这些方法可以在获取不到锁的时候释放已经持有的锁，然后再次尝试获取锁或干脆放弃，以避免死锁。

#### 并发容器
Java中还有很多专为并发设计的容器类，比如：
* CopyOnWriteArrayList。
* ConcurrentHashMap。
* ConcurrentLinkedQueue。
* ConcurrentSkipListSet。

这些容器类都是线程安全的，但都没有使用 synchronized，没有迭代问题，直接支持一些复合操作，性能也高得多。

## 协作的场景
### wait/notify
Java的根父类是 Object， Java在 Object类而非 Thread类中定义了一些线程协作的基本方法，使得每个对象都可以调用这些方法，这些方法有两类，一类是 wait，另一类是 notify。

主要有两个 wait方法： 

``` Java
public final void wait() throws InterruptedException 
public final native void wait(long timeout) throws InterruptedException;
```

一个带时间参数，单位是毫秒，表示最多等待这么长时间，参数为 0表示无限期等待；一个不带时间参数，表示无限期等待，实际就是调用 wait（ 0）。在等待期间都可以被中断，如果被中断，会抛出 InterruptedException。

wait实际上做了什么呢？它在等待什么？上节我们说过，每个对象都有一把锁和等待队列，一个线程在进入 synchronized代码块时，会尝试获取锁，如果获取不到则会把当前线程加入等待队列中，**其实，除了用于锁的等待队列，每个对象还有另一个等待队列，表示条件队列，该队列用于线程间的协作。**调用 wait就会把当前线程放到条件队列上并阻塞，表示当前线程执行不下去了，它需要等待一个条件，这个条件它自己改变不了，需要其他线程改变。当其他线程改变了条件后，应该调用 Object的 notify方法：

``` Java
public final native void notify(); 
public final native void notifyAll();
```

notify做的事情就是从条件队列中选一个线程，将其从队列中移除并唤醒， notifyAll和 notify的区别是，它会移除条件队列中所有的线程并全部唤醒。

两个线程都要访问协作的变量 var，容易出现竞态条件，所以相关代码都需要被 synchronized保护。实际上， wait/notify方法只能在 synchronized代码块内被调用，如果调用 wait/notify方法时，当前线程没有持有对象锁，会抛出异常 java.lang.IllegalMonitor-StateException。

如果 wait必须被 synchronized保护，那一个线程在 wait时，另一个线程怎么可能调用同样被 synchronized保护的 notify方法呢？它不需要等待锁吗？我们需要进一步理解 wait的内部过程，虽然是在 synchronized方法内，但调用 wait时，线程会释放对象锁。 wait的具体过程是：
1. 把当前线程放入条件等待队列，释放对象锁，阻塞等待，线程状态变为 WAITING或 TIMED_ WAITING。
2. 等待时间到或被其他线程调用 notify/notifyAll从条件队列中移除，这时，要重新竞争对象锁：
	* 如果能够获得锁，线程状态变为 RUNNABLE，并从 wait调用中返回。
	* 否则，该线程加入对象锁等待队列，线程状态变为 BLOCKED，只有在获得锁后才会从 wait调用中返回。

调用 notify会把在条件队列中等待的线程唤醒并从队列中移除，但它不会释放对象锁，也就是说，只有在包含 notify的 synchronized代码块执行完后，等待的线程才会从 wait调用中返回。

简单总结一下， wait/notify方法看上去很简单，但往往难以理解 wait等的到底是什么，而 notify通知的又是什么，我们需要知道，它们被不同的线程调用，但共享相同的锁和条件等待队列（相同对象的 synchronized代码块内），它们围绕一个共享的条件变量进行协作，这个条件变量是程序自己维护的，当条件不成立时，线程调用 wait进入条件等待队列，另一个线程修改了条件变量后调用 notify，调用 wait的线程唤醒后需要重新检查条件变量。从多线程的角度看，它们围绕共享变量进行协作，从调用 wait的线程角度看，它阻塞等待一个条件的成立。我们在设计多线程协作时，需要想清楚协作的共享变量和条件是什么，这是协作的核心。

只能有一个条件等待队列，这是 Java wait/ notify机制的局限性。

Java提供了专门的阻塞队列实现，包括：
* 接口 BlockingQueue和 BlockingDeque。
* 基于数组的实现类 ArrayBlockingQueue。
* 基于链表的实现类 LinkedBlockingQueue和 LinkedBlockingDeque。
* 基于堆的实现类 PriorityBlockingQueue。

join实际上就是调用了 wait，其主要代码是： 
``` Java
while (isAlive()) {
	wait(0); 
}
```
只要线程是活着的， isAlive（）返回 true， join就一直等待。当线程运行结束的时候， Java系统调用 notifyAll来通知。

使用 join有时比较麻烦，需要主线程逐一等待每个子线程。这里，我们演示一种新的写法。主线程与各个子线程协作的共享变量是一个数，这个数表示未完成的线程个数，初始值为子线程个数，主线程等待该值变为 0，而每个子线程结束后都将该值减一，当减为 0时调用 notifyAll。

可以使用一个变量，比如子线程数量，来控制同时开始、等待结束、到达某个集合点，交换数据，再继续等场景。

## 线程的中断
### 取消/关闭的场景
1. 很多线程的运行模式是死循环，比如在生产者/消费者模式中，消费者主体就是一个死循环，它不停地从队列中接受任务，执行任务，在停止程序时，我们需要一种“优雅”的方法以关闭该线程。
2. 在一些图形用户界面程序中，线程是用户启动的，完成一些任务，比如从远程服务器上下载一个文件，在下载过程中，用户可能会希望取消该任务。
3. 在一些场景中，比如从第三方服务器查询一个结果，我们希望在限定的时间内得到结果，如果得不到，我们会希望取消该任务。
4. 有时，我们会启动多个线程做同一件事，比如类似抢火车票，我们可能会让多个好友帮忙从多个渠道买火车票，只要有一个渠道买到了，我们会通知取消其他渠道。

### 取消/关闭的机制
在 Java中，停止一个线程的主要机制是中断，中断并不是强迫终止一个线程，它是一种协作机制，是给线程传递一个取消信号，但是由线程来决定如何以及何时退出。

``` Java
public boolean isInterrupted() 
public void interrupt() 
public static boolean interrupted()
```
isInterrupted（）和 interrupt（）是实例方法，调用它们需要通过线程对象； interrupted（）是静态方法，实际会调用 Thread. currentThread（）操作当前线程。

每个线程都有一个标志位，表示该线程是否被中断了。
1. isInterrupted：返回对应线程的中断标志位是否为 true。
2. interrupted：返回当前线程的中断标志位是否为 true，**但它还有一个重要的副作用，就是清空中断标志位，也就是说，连续两次调用 interrupted（），第一次返回的结果为 true，第二次一般就是 false（除非同时又发生了一次中断）。**
3. interrupt：表示中断对应的线程。中断具体意味着什么呢？下面我们进一步来说明。

### 线程对中断的反应
- RUNNABLE：线程在运行或具备运行条件只是在等待操作系统调度。
- WAITING/TIMED_ WAITING：线程在等待某个条件或超时。
- BLOCKED：线程在等待锁，试图进入同步块。
- NEW/TERMINATED：线程还未启动或已结束。

interrupt（）对线程的影响与线程的状态和在进行的 IO操作有关。

1. RUNNABLE
如果线程在运行中，且没有执行 IO操作， interrupt（）只是会设置线程的中断标志位，没有任何其他作用。线程应该在运行过程中合适的位置检查中断标志位。
``` Java
while(!Thread.currentThread().isInterrupted()) { 
//…单次循环代码 
}
```

2. WAITING/TIMED_ WAITING
线程调用 join/ wait/ sleep方法会进入 WAITING或 TIMED_ WAITING状态，在这些状态时，对线程对象调用 interrupt（）会使得该线程抛出 InterruptedException。需要注意的是，抛出异常后，中断标志位会被清空，而不是被设置。

3. BLOCKED
如果线程在等待锁，对线程对象调用 interrupt（）只是会设置线程的中断标志位，线程依然会处于 BLOCKED状态，也就是说， interrupt（）并不能使一个在等待锁的线程真正“中断”。
在使用 synchronized关键字获取锁的过程中不响应中断请求，这是 synchronized的局限性。

3. NEW/TERMINATE
如果线程尚未启动（NEW），或者已经结束（TERMINATED），则调用 interrupt（）对它没有任何效果，中断标志位也不会被设置。

### 如何正确地取消/关闭线程
interrupt方法不一定会真正“中断”线程，它只是一种协作机制，如果不明白线程在做什么，不应该贸然地调用线程的 interrupt方法，以为这样就能取消线程。

对于以线程提供服务的程序模块而言，它应该封装取消/关闭操作，提供单独的取消/关闭方法给调用者，外部调用者应该调用这些方法而不是直接调用 interrupt。

比如：
Future接口提供了如下方法以取消任务： 

``` Java
boolean cancel(boolean mayInterruptIfRunning);
```

再如， ExecutorService提供了如下两个关闭方法： 

``` Java
void shutdown(); 
List <Runnable> shutdownNow();
```