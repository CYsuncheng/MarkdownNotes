# 堆与优先级队列
## 堆
完全二叉树，没完全理解就不记录了

## PriorityQueue
PriorityQueue内部是用堆实现的，内部元素不是完全有序的，不过，逐个出队会得到有序的输出。

``` Java
public interface Queue <E> extends Collection <E> { 
	boolean add(E e); //在尾部添加元素，队列满时抛异常 
	boolean offer(E e); //在尾部添加元素，队列满时返回 false 
	E remove(); //删除头部元素,队列空时抛异常 
	E poll(); //删除头部元素，队列空时返回 null 
	E element(); //查看头部元素,队列空时抛异常 
	E peek(); //查看头部元素，队列空时返回 null
}
```

堆的实现类 PriorityQueue，它实现了队列接口 Queue，但按优先级出队，内部是用堆实现的，有如下特点：
1. 实现了优先级队列，最先出队的总是优先级最高的，即排序中的第一个。 
2. 优先级可以有相同的，内部元素不是完全有序的，如果遍历输出，除了第一个，其他没有特定顺序。 
3. 查看头部元素的效率很高，为 O（1），入队、出队效率比较高，为 O（log2（N）），构建堆 heapify的效率为 O（N）。
4. 根据值查找和删除元素的效率比较低，为 O（N）。除了用作基本的优先级队列， PriorityQueue还可以作为一种比较通用的数据结构，用于解决一些其他问题。