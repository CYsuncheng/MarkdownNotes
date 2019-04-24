# 并发容器
具体包括：
* 写时复制的 List和 Set； 
* ConcurrentHashMap；
* 基于 SkipList的 Map和 Set；
* 各种并发队列。

## 写时复制的 List和 Set
CopyOnWriteArrayList和 CopyOnWriteArraySet，Copy-On-Write即写时复制，或称写时拷贝，这是解决并发问题的一种重要思路。

### CopyOnWriteArrayList
CopyOnWriteArrayList实现了 List接口，它的用法与其他 List（如 ArrayList）基本是一样的。 CopyOnWriteArrayList的特点如下：
* 它是线程安全的，可以被多个线程并发访问；
* 它的迭代器不支持修改操作，但也不会抛出 ConcurrentModificationException；
* 它以原子方式支持一些复合操作。

> 基于 synchronized的同步容器的几个问题。迭代时，需要对整个列表对象加锁，否则会抛出 ConcurrentModificationException， CopyOnWriteArrayList没有这个问题，迭代时不需要加锁。  

基于 synchronized的同步容器的另一个问题是复合操作，比如先检查再更新，也需要调用方加锁，而 CopyOnWriteArrayList直接支持两个原子方法： 
``` Java
//不存在才添加，如果添加了，返回 true，否则返回 false 
public boolean addIfAbsent(E e) 
//批量添加 c中的非重复元素，不存在才添加，返回实际添加的个数 
public int addAllAbsent(Collection <? extends E> c) 
```

CopyOnWriteArrayList的内部也是一个数组，但这个数组是以原子方式被整体更新的。每次修改操作，都会新建一个数组，复制原数组的内容到新数组，在新数组上进行需要的修改，然后以原子方式设置内部的数组引用，这就是写时复制。

所有的读操作，都是先拿到当前引用的数组，然后直接访问该数组。在读的过程中，可能内部的数组引用已经被修改了，但不会影响读操作，它依旧访问原数组内容。
换句话说，数组内容是只读的，写操作都是通过新建数组，然后原子性地修改数组引用来实现的。

内部数组声明为： 
``` Java
private volatile transient Object[] array;
```

它声明为了 volatile，这是必需的，以保证内存可见性，即保证在写操作更改之后读操作能看到。

在 CopyOnWriteArrayList中，读不需要锁，可以并行，读和写也可以并行，但多个线程不能同时写，每个写操作都需要先获取锁。 CopyOnWriteArrayList内部使用 Reentrant-Lock。

add方法的代码为：
``` Java
public boolean add(E e) { 
	final ReentrantLock lock = this.lock; 
	lock.lock(); 
	try { 
		Object[] elements = getArray(); 
		int len = elements.length; 
		Object[] newElements = Arrays.copyOf(elements, len + 1); 
		newElements[len] = e; 
		setArray(newElements); 
		return true; 
	} 
	finally { 
		lock.unlock(); 
	} 
}
```

add方法是修改操作，整个过程需要被锁保护，先获取当前数组 elements，然后复制出一个长度加 1的新数组 newElements，在新数组中添加元素，最后调用 setArray原子性地修改内部数组引用。

每次修改都要创建一个新数组，然后复制所有内容，这听上去是一个难以令人接受的方案，如果数组比较大，修改操作又比较频繁，可以想象， CopyOnWriteArrayList的性能是很低的。事实确实如此， CopyOnWriteArrayList不适用于数组很大且修改频繁的场景。它是以优化读操作为目标的，读不需要同步，性能很高，但在优化读的同时牺牲了写的性能。

锁和循环 CAS都是控制对同一个资源的访问冲突，而写时复制通过复制资源减少冲突。对于绝大部分访问都是读，且有大量并发线程要求读，只有个别线程进行写，且只是偶尔写的场合，写时复制就是一种很好的解决方案。

### CopyOnWriteArraySet
CopyOnWriteArraySet实现了 Set接口，不包含重复元素，CopyOnWriteArraySet内部是通过 CopyOnWriteArrayList实现的，其成员声明为： 
``` Java
private final CopyOnWriteArrayList <E> al;
```

在构造方法中被初始化，如： 
``` Java
public CopyOnWriteArraySet() { 
	al = new CopyOnWriteArrayList <E>();
}
```

其 add方法代码为： 
``` Java
public boolean add(E e) { 
	return al.addIfAbsent(e); 
}
```

add方法就是调用了 CopyOnWriteArrayList的 addIfAbsent方法。

由于 CopyOnWriteArraySet是基于 CopyOnWriteArrayList实现的，所以与之前介绍过的 Set的实现类如 HashSet/ TreeSet相比，它的性能比较低，不适用于元素个数特别多的集合。如果元素个数比较多，可以考虑 ConcurrentHashMap或 ConcurrentSkipListSet这两个类。

简单总结下， CopyOnWriteArrayList和 CopyOnWriteArraySet适用于读远多于写、集合不太大的场合。

## ConcurrentHashMap
它是 HashMap的并发版本，与 HashMap相比，它有如下特点：
* 并发安全；
* 直接支持一些原子复合操作；
* 支持高并发，读操作完全并行，写操作支持一定程度的并行；
* 与同步容器 Collections.synchronizedMap相比，迭代不用加锁，不会抛出 ConcurrentModificationException；
* 弱一致性。

### 并发安全
HashMap不是并发安全的，在并发更新的情况下， HashMap可能出现死循环，占满 CPU。

ConcurrentHashMap没有这些问题，它同样实现了 Map接口，也是基于哈希表实现的。

### 高并发的基本机制
主要有两点：
* 分段锁；
* 读不需要锁。

同步容器使用 synchronized，所有方法竞争同一个锁；而 ConcurrentHashMap采用分段锁技术，将数据分为多个段，而每个段有一个独立的锁，每一个段相当于一个独立的哈希表，分段的依据也是哈希值，无论是保存键值对还是根据键查找，都先根据键的哈希值映射到段，再在段对应的哈希表上进行操作。

采用分段锁，可以大大提高并发度，多个段之间可以并行读写。
默认情况下，段是 16个，不过，这个数字可以通过构造方法进行设置，如下所示： 
``` Java
public ConcurrentHashMap( 
	int initialCapacity, 
	float loadFactor, 
	int concurrencyLevel)
```
concurrencyLevel表示估计的并行更新的线程个数， ConcurrentHashMap会将该数转换为 2的整数次幂，比如 14转换为 16， 25转换为 32。

ConcurrentHashMap也不是简单地使用锁进行同步，内部使用了 CAS。
实现的效果是，**对于写操作，需要获取锁，不能并行，但是读操作可以，多个读可以并行，写的同时也可以读，**这使得 ConcurrentHashMap的并行度远高于同步容器。

#### 弱一致性
ConcurrentHashMap的迭代器创建后，就会按照哈希表结构遍历每个元素，但在遍历过程中，内部元素可能会发生变化，如果变化发生在已遍历过的部分，迭代器就不会反映出来，而如果变化发生在未遍历过的部分，迭代器就会发现并反映出来，这就是弱一致性。

### 小结
本节介绍了 ConcurrentHashMap，它是并发版的 HashMap，通过降低锁的粒度和 CAS等实现了高并发，支持原子条件更新操作，不会抛出 ConcurrentModificationException，实现了弱一致性。

## 基于跳表的 Map和 Set
TreeSet是基于 TreeMap实现的，与此类似， ConcurrentSkipListSet也是基于 ConcurrentSkipListMap实现的。

### 基本概念
ConcurrentSkipListMap是基于 SkipList实现的， SkipList称为跳跃表或跳表，是一种数据结构，稍后我们会进一步介绍。并发版本为什么采用跳表而不是树呢？原因也很简单，因为跳表更易于实现高效并发算法。 ConcurrentSkipListMap有如下特点。

1. 没有使用锁，所有操作都是无阻塞的，所有操作都可以并行，包括写，多线程可以同时写。 
2. 与 ConcurrentHashMap类似，迭代器不会抛出 ConcurrentModificationException，是弱一致的，迭代可能反映最新修改也可能不反映，一些方法如 putAll、 clear不是原子的。
3. 与 ConcurrentHashMap类似，同样实现了 ConcurrentMap接口，支持一些原子复合操作。
4. 与 TreeMap一样，可排序，默认按键的自然顺序，也可以传递比较器自定义排序，实现了 SortedMap和 NavigableMap接口。

跳表是基于链表的，在链表的基础上加了多层索引结构。

## 并发队列
* 无锁非阻塞并发队列： ConcurrentLinkedQueue和 ConcurrentLinkedDeque。
* 普通阻塞队列：基于数组的 ArrayBlockingQueue，基于链表的 LinkedBlockingQueue和 LinkedBlockingDeque。
* 优先级阻塞队列： PriorityBlockingQueue。
* 延时阻塞队列： DelayQueue。
* 其他阻塞队列： SynchronousQueue和 LinkedTransferQueue。