# 泛型与容器-列表和队列
## 列表和队列
### 迭代
只要对象实现了 Iterable接口，就可以使用 foreach语法，编译器会转换为调用 Iterable和 Iterator接口的方法。

1. Iterable表示对象可以被迭代，它有一个方法 iterator（），返回 Iterator对象，实际通过 Iterator接口的方法进行遍历；
2. 如果对象实现了 Iterable，就可以使用 foreach语法；
3. 类可以不实现 Iterable，也可以创建 Iterator对象。

### ArrayList
ArrayList还实现了三个主要的接口： Collection、 List和 Random-Access，Iterable接口

ArrayList还提供了两个返回 Iterator接口的方法：
``` Java
public ListIterator < E > listIterator() 
public ListIterator < E > listIterator( int index)
```
ListIterator扩展了 Iterator接口，增加了一些方法，向前遍历、添加元素、修改元素、返回索引位置等。

关于迭代器，有一种常见的误用，就是在迭代的中间调用容器的删除方法。

因为迭代器内部会维护一些索引位置相关的数据，要求在迭代过程中，容器不能发生结构性变化，否则这些索引位置就失效了。所谓结构性变化就是添加、插入和删除元素，只是修改元素内容不算结构性变化。如何避免异常呢？可以使用迭代器的 remove方法，例如:
``` Java
public static void remove(ArrayList <Integer> list){ 
	Iterator <Integer> it = list.iterator(); 
	while(it.hasNext()){
		it.next();
		it.remove(); 
	} 
}

# 错误的方式
for(Integer a : list){ 
	list.remove(a);
	}
```

Arrays中有一个静态方法 asList可以返回对应的 List，如下所示：
``` Java
Integer[] a = {1, 2, 3}; 
List <Integer> list = Arrays.asList(a);
```

需要注意的是，这个方法返回的 List，它的实现类并不是本节介绍的 ArrayList，而是 Arrays类的一个内部类，在这个内部类的实现中，内部用的数组就是传入的数组，没有拷贝，也不会动态改变大小，所以对数组的修改也会反映到 List中，对 List调用 add、 remove方法会抛出异常。

要使用 ArrayList完整的方法，应该新建一个 ArrayList，如下所示：
``` Java
List <Integer> list = new ArrayList <Integer>(Arrays.asList(a));
```

#### ArrayList特点分析
1. 可以随机访问，按照索引位置进行访问效率很高，用算法描述中的术语，效率是 O（ 1），简单说就是可以一步到位。 
2. 除非数组已排序，否则按照内容查找元素效率比较低，具体是 O（ N）， N为数组内容长度，也就是说，性能与数组长度成正比。 
3. 添加元素的效率还可以，重新分配和复制数组的开销被平摊了，具体来说，添加 N个元素的效率为 O（ N）。
4. 插入和删除元素的效率比较低，因为需要移动元素，具体为 O（ N）。

### LinkedList
除了实现了 List接口外， LinkedList还实现了 Deque和 Queue接口，可以按照队列、栈和双端队列的方式进行操作。

Queue，所谓队列就类似于日常生活中的各种排队，特点就是先进先出，在尾部添加元素，从头部删除元素。

栈和队列都是在两端进行操作，栈只操作头部，队列两端都操作，但尾部只添加、头部只查看和删除。有一个更为通用的操作两端的接口 Deque。 Deque扩展了 Queue，包括了栈的操作方法，此外还提供了一些方法，xxxFirst操作头部， xxxLast操作尾部。

Deque接口还有一个迭代器方法，可以从后往前遍历：
``` Java
Iterator < E > descendingIterator();
```

简单总结下： LinkedList的用法是比较简单的，与 ArrayList用法类似，支持 List接口，只是， LinkedList增加了一个接口 Deque，可以把它看作队列、栈、双端队列，方便地在两端进行操作。

1. 按需分配空间，不需要预先分配很多空间。
2. 不可以随机访问，按照索引位置访问效率比较低，必须从头或尾顺着链接找，效率为 O（ N/ 2）。
3. 不管列表是否已排序，只要是按照内容查找元素，效率都比较低，必须逐个比较，效率为 O（ N）。
4. 在两端添加、删除元素的效率很高，为 O（ 1）。
5. 在中间插入、删除元素，要先定位，效率比较低，为 O（ N），但修改本身的效率很高，效率为 O（ 1）。

### 区别
ArrayList内部是数组，元素在内存是连续存放的，但 LinkedList不是。 LinkedList直译就是链表，确切地说，它的内部实现是双向链表，每个元素在内存都是单独存放的，元素之间通过链接连在一起，类似于小朋友之间手拉手一样。

与 ArrayList不同， Linked-List的内存是按需分配的，不需要预先分配多余的内存，添加元素只需分配新元素的空间，然后调节几个链接即可。

在中间插入元素， LinkedList只需按需分配内存，修改前驱和后继节点的链接，而 ArrayList则可能需要分配很多额外空间，且移动所有后续元素。

**size>>1等于 size/2**

### ArrayDeque
ArrayDeque的高效来源于 head和 tail这两个变量，它们使得物理上简单的从头到尾的数组变为了一个逻辑上循环的数组，避免了在头尾操作时的移动。

ArrayDeque  不允许元素为 null。ArrayDeque 的主要成员是一个 elements 数组和 int 的 head 与 tail 索引，head 是队列的头部元素索引，而 tail 是队列下一个要添加的元素的索引，elements 的默认容量是 16 且默认容量必须是 2 的幂次，不足 2 的幂次会自动向上调整为 2 的幂次。

#### 特点
1. 在两端添加、删除元素的效率很高，动态扩展需要的内存分配以及数组复制开销可以被平摊，具体来说，添加 N个元素的效率为 O（ N）。
2. 根据元素内容查找和删除的效率比较低，为 O（ N）。
3. 与 ArrayList和 LinkedList不同，没有索引位置的概念，不能根据索引位置进行操作。

### 总结
**无论是 ArrayList、 LinkedList还是 Array-Deque，按内容查找元素的效率都很低，都需要逐个进行比较。**
