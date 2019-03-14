# 容器类总结

## 用法总结
List是 Collection的子接口，表示有顺序或位置的数据集合，增加了根据索引位置进行操作的方法。它有两个主要的实现类： ArrayList和 LinkedList。 ArrayList基于数组实现， LinkedList基于链表实现； ArrayList的随机访问效率很高，但从中间插入和删除元素需要移动元素，效率比较低， LinkedList则正好相反，随机访问效率比较低，但增删元素只需要调整邻近节点的链接。

Set也是 Collection的子接口，它没有增加新的方法，但保证不含重复元素。它有两个主要的实现类： HashSet和 TreeSet。 HashSet基于哈希表实现，要求键重写 hashCode方法，效率更高，但元素间没有顺序； TreeSet基于排序二叉树实现，元素按比较有序，元素需要实现 Comparable接口，或者创建 TreeSet时提供一个 Comparator对象。 HashSet还有一个子类 LinkedHashSet可以按插入有序。

还有一个针对枚举类型的实现类 EnumSet，它基于位向量实现，效率很高。 

Queue是 Collection的子接口，表示先进先出的队列，在尾部添加，从头部查看或删除。 Deque是 Queue的子接口，表示更为通用的双端队列，有明确的在头或尾进行查看、添加和删除的方法。普通队列有两个主要的实现类： LinkedList和 ArrayDeque。 LinkedList基于链表实现， ArrayDeque基于循环数组实现。一般而言，如果只需要 Deque接口， Array-Deque的效率更高一些。 

Queue还有一个特殊的实现类 PriorityQueue，表示优先级队列，内部是用堆实现的。堆除了用于实现优先级队列，还可以高效方便地解决很多其他问题，比如求前 K个最大的元素、求中值等。 

Map接口表示键值对集合，经常根据键进行操作，它有两个主要的实现类： HashMap和 TreeMap。 HashMap基于哈希表实现，要求键重写 hashCode方法，操作效率很高，但元素没有顺序。 

TreeMap基于排序二叉树实现，要求键实现 Comparable接口，或提供一个 Comparator对象，操作效率稍低，但可以按键有序。 

HashMap还有一个子类 LinkedHashMap，它可以按插入或访问有序。之所以能有序，是因为每个元素还加入到了一个双向链表中。如果键本来就是有序的，使用 LinkedHashMap而非 TreeMap可以提高效率。按访问有序的特点可以方便地用于实现 LRU缓存。

如果键为枚举类型，可以使用专门的实现类 EnumMap，它使用效率更高的数组实现。

需要说明的是，除了 Hashtable、 Vector和 Stack，我们介绍的各种容器类都不是线程安全的，也就是说，如果多个线程同时读写同一个容器对象，是不安全的。

如果需要线程安全，可以使用 Collections提供的 synchronizedXXX方法对容器对象进行同步，或者使用线程安全的专门容器类。

此外，容器类提供的迭代器都有一个特点，都会在迭代中间进行结构性变化检测，如果容器发生了结构性变化，就会抛出 ConcurrentModificationException，所以不能在迭代中间直接调用容器类提供的 add/ remove方法，如需添加和删除，应调用迭代器的相关方法。

## 数据结构和算法
1. 动态数组： ArrayList内部就是动态数组， HashMap内部的链表数组也是动态扩展的， ArrayDeque和 PriorityQueue内部也都是动态扩展的数组。
2. 链表： LinkedList是用双向链表实现的， HashMap中映射到同一个链表数组的键值对是通过单向链表链接起来的， LinkedHashMap中每个元素还加入到了一个双向链表中以维护插入或访问顺序。
3. 哈希表： HashMap是用哈希表实现的， HashSet、 LinkedHashSet和 LinkedHashMap基于 HashMap，内部当然也是哈希表。
4. 排序二叉树： TreeMap是用红黑树（基于排序二叉树）实现的， TreeSet内部使用 TreeMap，当然也是红黑树，红黑树能保持元素的顺序且综合性能很高。
5. 堆： PriorityQueue是用堆实现的，堆逻辑上是树，物理上是动态数组，堆可以高效地解决一些其他数据结构难以解决的问题。
6. 循环数组： ArrayDeque是用循环数组实现的，通过对头尾变量的维护，实现了高效的队列操作。
7. 位向量： EnumSet和 BitSet是用位向量实现的，对于只有两种状态，且需要进行集合运算的数据，使用位向量进行表示、位运算进行处理，精简且高效。