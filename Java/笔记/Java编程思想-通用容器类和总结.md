# 通用容器类和总结
## 抽象容器类
有 Collection、 List、 Set、 Queue、 Deque和 Map。有 6个抽象容器类。

### AbstractCollection
AbstractCollection提供了 Collection接口的基础实现，具体来说，它实现了如下方法：

``` Java
public boolean addAll(Collection <? extends E> c) 
public boolean contains(Object o) 
public boolean containsAll(Collection <?> c) 
public boolean isEmpty() 
public boolean remove(Object o) 
public boolean removeAll(Collection <?> c) 
public boolean retainAll(Collection <?> c) 
public void clear() 
public Object[] toArray() 
public <T> T[] toArray(T[] a) 
public String toString()
```

### AbstractList
AbstractList提供了 List接口的基础实现，具体来说，它实现了如下方法：

``` Java
public boolean add(E e) 
public boolean addAll(int index, Collection <? extends E> c)
public void clear() 
public boolean equals(Object o) 
public int hashCode() 
public int indexOf(Object o) 
public Iterator <E> iterator() 
public int lastIndexOf(Object o) 
public ListIterator <E> listIterator() 
public ListIterator <E> listIterator(final int index) 
public List <E> subList(int fromIndex, int toIndex)
```

### AbstractSequentialList
AbstractSequentialList是 AbstractList的子类，也提供了 List接口的基础实现，具体来说，它实现了如下方法： 

``` Java
public void add(int index, E element) 
public boolean addAll(int index, Collection <? extends E> c)
public E get(int index) 
public Iterator <E> iterator() 
public E remove(int index) 
public E set(int index, E element)
```

注意与 AbstractList相区别，可以说，虽然 AbstractSequentialList是 AbstractList的子类，但实现逻辑和用法上，与 AbstractList正好相反。

- AbstractList需要具体子类重写根据索引操作的方法 get、 set、 add、 remove，它提供了迭代器，但迭代器是基于这些方法实现的。它假定子类可以高效地根据索引位置进行操作，适用于内部是随机访问类型的存储结构（如数组），比如 ArrayList就继承自 AbstractList。 
- AbstractSequentialList需要具体子类重写迭代器，它提供了根据索引操作的方法 get、 set、 add、 remove，但这些方法是基于迭代器实现的。它适用于内部是顺序访问类型的存储结构（如链表），比如 LinkedList就继承自 AbstractSequentialList。

### AbstractMap
AbstractMap提供了 Map接口的基础实现，具体来说，它实现了如下方法：

``` Java
public void clear() 
public boolean containsKey(Object key) 
public boolean containsValue(Object value) 
public boolean equals(Object o) 
public V get(Object key) 
public int hashCode() 
public boolean isEmpty() 
public Set <K> keySet() 
public void putAll(Map <? extends K, ? extends V> m) 
public V remove(Object key) 
public int size() 
public String toString() 
public Collection <V> values()
```

### AbstractSet
AbstractSet提供了 Set接口的基础实现，它继承自 AbstractCollection，增加了 equals和 hashCode方法的默认实现。 Set接口要求容器内不能包含重复元素， AbstractSet并没有实现该约束，子类需要自己实现。扩展 AbstractSet与 AbstractCollection是类似的，只是需要实现无重复元素的约束，比如， add方法内需要检查元素是否已经添加过了。

### AbstractQueue
AbstractQueue提供了 Queue接口的基础实现，它继承自 AbstractCollection，实现了如下方法： 

``` Java
public boolean add(E e) 
public boolean addAll(Collection <? extends E > c) 
public void clear() 
public E element() 
public E remove()
```

## Collections
类 Collections以静态方法的方式提供了很多通用算法和功能，这些功能大概可以分为两类。 
1. 对容器接口对象进行操作。
2. 返回一个容器接口对象。

对于第 1类，操作大概可以分为三组。
* 查找和替换。
* 排序和调整顺序。
* 添加和修改。

对于第 2类，大概可以分为两组。
* 适配器：将其他类型的数据转换为容器接口对象。
* 装饰器：修饰一个给定容器接口对象，增加某种性质。

### 查找和替换
查找和替换包含多组方法。查找包括二分查找、查找最大值/最小值、查找元素出现次数、查找子 List、查看两个集合是否有交集等。

#### 二分查找
Collections提供了针对 List接口的二分查找，如下所示： 

``` Java
public static <T> int binarySearch(List <? extends Comparable <? super T> > list, T key) 

public static <T> int binarySearch(List <? extends T> list, T key, Comparator <? super T> c)
```

从方法参数角度而言，一个要求 List的每个元素实现 Comparable接口，另一个不需要，但要求提供 Comparator。二分查找假定 List中的元素是从小到大排序的。如果是从大到小排序的，需要传递一个逆序 Comparator对象， Collections提供了返回逆序 Comparator的方法，之前我们也用过： 

``` Java
public static <T> Comparator <T> reverseOrder() 
public static <T> Comparator <T> reverseOrder(Comparator <T> cmp)
```

#### 其他方法
返回元素 o在容器 c中出现的次数， o可以为 null。含义很简单，实现思路也很简单，就是通过迭代器进行比较计数。

``` Java
public static int frequency(Collection <? > c, Object o)
```

Collections提供了如下方法，在 source List中查找 target List的位置： 

``` Java
public static int indexOfSubList(List <?> source, List <?> target) 
public static int lastIndexOfSubList(List <? > source, List <?> target) 
```

indexOfSubList从开头找， lastIndexOfSubList从结尾找，没找到返回-1，找到返回第一个匹配元素的索引位置。这两个方法的实现都是属于“暴力破解”型的，将 target列表与 source从第一个元素开始的列表逐个元素进行比较，如果不匹配，则与 source从第二个元素开始的列表比较，再不匹配，与 source从第三个元素开始的列表比较，以此类推。

查看两个集合是否有交集，方法为： 

``` Java
public static boolean disjoint(Collection <?> c1, Collection <?> c2)
```

如果 c1和 c2有交集，返回值为 false；没有交集，返回值为 true。实现原理是遍历其中一个容器，对每个元素，在另一个容器里通过 contains方法检查是否包含该元素，如果包含，返回 false，如果最后不包含任何元素返回 true。这个方法的代码会根据容器是否为 Set以及集合大小进行性能优化。

替换方法为：
``` Java
public static <T> boolean replaceAll(List <T> list, T oldVal, T newVal)
```
将 List中的所有 oldVal替换为 newVal，如果发生了替换，返回值为 true，否则为 false。

Arrays类有针对数组对象的排序方法， Collections提供了针对 List接口的排序方法，如下所示：

``` Java
public static <T extends Comparable <? super T> > void sort(List <T> list) 
public static <T> void sort(List <T> list, Comparator <? super T> c)
```

内部它是通过 Arrays. sort实现的，先将 List元素复制到一个数组中，然后使用 Arrays. sort，排序后，再复制回 List。

交换元素位置的方法为： 

``` Java
public static void swap(List <?> list, int i, int j)
```

交换 list中第 i个和第 j个元素的内容。

翻转列表顺序的方法为： 

``` Java
public static void reverse(List <? > list)
```

将 list中的元素顺序翻转过来。实现思路就是将第一个和最后一个交换，第二个和倒数第二个交换，以此类推，直到中间两个元素交换完毕。如果 list实现了 RandomAccess接口或列表比较小，根据索引位置，使用上面的 swap方法进行交换，否则，由于直接根据索引位置定位元素效率比较低，使用一前一后两个 listIterator定位待交换的元素。

Collections直接提供了对 List元素洗牌的方法： 

``` Java
public static void shuffle(List <? > list) public static void shuffle(List <? > list, Random rnd)
```

实现思路与随机一节介绍的是一样的：从后往前遍历列表，逐个给每个位置重新赋值，值从前面的未重新赋值的元素中随机挑选。如果列表实现了 RandomAccess接口，或者列表比较小，直接使用前面 swap方法进行交换，否则，先将列表内容复制到一个数组中，洗牌，再复制回列表。

我们解释下循环移位的概念，比如列表为：
 [8, 5, 3, 6, 2]循环右移 2位，会变为：[6, 2, 8, 5, 3]
如果是循环左移 2位，会变为：[3, 6, 2, 8, 5]
因为列表长度为 5，循环左移 3位和循环右移 2位的效果是一样的。
循环移位的方法是： 

``` Java
public static void rotate(List <?> list, int distance）
```

distance表示循环移位个数，一般正数表示向右移，负数表示向左移。
这个方法很有用的一点是：它也可以用于子列表，可以调整子列表内的顺序而不改变其他元素的位置。比如，将第 j个元素向前移动到 k（ k > j），可以这么写：

``` Java
Collections.rotate(list. subList(j, k + 1), -1);
```

再举个例子： 

``` Java
List <Integer> list = Arrays.asList(new Integer[]{ 8, 5, 3, 6, 2, 19, 21 }); 
Collections.rotate(list.subList(1, 5), 2); 
System.out.println(list);
```

输出为： [8, 6, 2, 5, 3, 19, 21]

批量添加，方法为： 

``` Java
public static <T> boolean addAll(Collection <? super T> c, T... elements)
```

批量填充固定值，方法为： 

``` Java
public static <T> void fill(List <? super T> list, T obj)
```

这个方法与 Arrays类中的 fill方法是类似的，给每个元素设置相同的值。

批量复制，方法为： 

``` Java
public static <T> void copy(List <? super T> dest, List <? extends T> src)
```

将列表 src中的每个元素复制到列表 dest的对应位置处，覆盖 dest中原来的值， dest的列表长度不能小于 src， dest中超过 src长度部分的元素不受影响。

### 适配器
1. 空容器方法：类似于将 null或“空”转换为一个标准的容器接口对象。
2. 单一对象方法：将一个单独的对象转换为一个标准的容器接口对象。
3. 其他适配方法：将 Map转换为 Set等。

Collections中有一组方法，返回一个不包含任何元素的容器接口对象，如下所示： 

``` Java
public static final <T> List <T> emptyList() 
public static final <T> Set <T> emptySet() 
public static final <K, V> Map <K, V> emptyMap() 
public static <T> Iterator <T> emptyIterator()
```

一个空容器对象有什么用呢？空容器对象经常用作方法返回值。

返回一个空的 List。也可以这样实现： `return new ArrayList < Integer >();`  这与 emptyList方法有什么区别呢？ emptyList方法返回的是一个静态不可变对象，它可以节省创建新对象的内存和时间开销。

Collections中还有一组方法，可以将一个单独的对象转换为一个标准的容器接口对象，比如： 

``` Java
public static <T> Set <T> singleton(T o) 
public static <T> List <T> singletonList(T o) 
public static <K, V> Map <K, V> singletonMap(K key, V value)

#举例
Collection <String> coll = Collections.singleton("编程"); 
Set <String> set = Collections.singleton("编程"); 
List <String> list = Collections.singletonList("老马"); 
Map <String, String> map = Collections.singletonMap("老马","编程");
```
**需要注意的是， singleton方法返回的也是不可变对象，只能用于读取，写入会抛出 UnsupportedOperationException异常。其他 singletonXXX方法的实现思路是类似的，返回值也都只能用于读取，不能写入。**

场景：
remove方法只会删除第一条匹配的记录， removeAll方法可以删除所有匹配的记录，但需要一个容器接口对象，如果需要从一个 List中删除所有匹配的某一对象呢？这时，就可以使用 Collections. singleton封装这个要删除的对象。比如，从 list中删除所有的" b"，代码如下所示： 

``` Java
List <String> list = new ArrayList <>(); 
Collections.addAll(list, "a", "b", "c", "d", "b"); 
list.removeAll(Collections.singleton("b")); 
System.out.println(list);
```

需要说明的是，在 Java 9中，可以使用 List、 Map和 Set的 of方法达到 singleton同样的功能，也就是说，如下两行代码的效果是相同的： 
1. Set <String> b = Collections.singleton("b"); 
2. Set < String> b = Set.of("b");

### 装饰器
写安全的主要方法有： 

``` Java
public static <T> Collection <T> unmodifiableCollection(Collection <? extends T> c) 
public static <T> List <T> unmodifiableList(List <? extends T> list) 
public static <K, V> Map <K, V> unmodifiableMap(Map <? extends K, ? extends V> m) 
public static <T> Set <T> unmodifiableSet(Set <? extends T> s)
```

Collections提供了一组方法，可以将一个容器对象变为线程安全的，比如：

``` Java
public static <T> Collection <T> synchronizedCollection(Collection <T> c) 
public static <T> List <T> synchronizedList(List <T> list) 
public static <K, V> Map <K, V> synchronizedMap(Map <K, V> m) 
public static <T> Set <T> synchronizedSet(Set <T> s)
```

需要说明的是，这些方法都是通过给所有容器方法加锁来实现的，这种实现并不是最优的。
