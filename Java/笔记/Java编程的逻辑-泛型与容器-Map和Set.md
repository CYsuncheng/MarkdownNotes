# 泛型与容器-Map和Set
## Map 和 Set
Map中的键是没有重复的，所以 ketSet（）返回了一个 Set。 keySet（）、 values（）、 entrySet（）有一个共同的特点，它们返回的都是视图，不是复制的值，基于返回值的修改会直接修改 Map自身，比如： `map.keySet().clear();` 会删除所有键值对。

### HashMap
HashMap内部有如下几个主要的实例变量：
``` Java
transient Entry <K, V>[] table = (Entry <K, V>[]) EMPTY_ TABLE; 
transient int size; 
int threshold; 
final float loadFactor;
```

size表示实际键值对的个数。 table是一个 Entry类型的数组，称为哈希表或哈希桶，其中的每个元素指向一个单向链表，链表中的每个节点表示一个键值对。 Entry是一个内部类，它的实例变量和构造方法代码如下：
``` Java
static class Entry <K, V> implements Map.Entry <K, V> { 
	final K key; 
	V value; 
	Entry <K, V> next; 
	int hash; 
	Entry(int h, K k, V v, Entry <K, V> n) { 
		value = v; 
		next = n; 
		key = k; 
		hash = h; 
		}
}
```

其中， key和 value分别表示键和值， next指向下一个 Entry节点， hash是 key的 hash值，直接存储 hash值是为了在比较的时候加快计算。

当添加键值对后， table就不是空表了，它会随着键值对的添加进行扩展，扩展的策略类似于 ArrayList。添加第一个元素时，默认分配的大小为 16，threshold表示阈值，当键值对个数 size大于等于 threshold时考虑进行扩展。 threshold是怎么算出来的呢？一般而言， threshold等于 table. length乘以 loadFactor。比如，如果 table. length为 16， loadFactor为 0. 75，则 threshold为 12。 loadFactor是负载因子，表示整体上 table被占用的程度，是一个浮点数，默认为 0. 75，可以通过构造方法进行修改。

#### 原理小结
HashMap的基本实现原理，内部有一个哈希表，即数组 table，每个元素 table[ i]指向一个单向链表，根据键存取值，用键算出 hash值，取模得到数组中的索引位置 buketIndex，然后操作 table[ buketIndex]指向的单向链表。

1. 根据键保存和获取值的效率都很高，为 O（ 1），每个单向链表往往只有一个或少数几个节点，根据 hash值就可以直接快速定位； 
2. HashMap中的键值对没有顺序，因为 hash值是随机的。

**HashMap中， length为 2的幂次方， h&（ length-1）等同于求模运算 h% length。**

#### 保存过程
1. 计算键的哈希值； 
2. 根据哈希值得到保存位置（取模）； 
3. 插到对应位置的链表头部或更新已有值； 
4. 根据需要扩展 table大小。

### HashSet
`public HashSet(int initialCapacity, float loadFactor)` 
构造函数的 initialCapacity和 loadFactor的含义与 HashMap中的是一样的。

与 HashMap类似， HashSet要求元素重写 hashCode和 equals方法，且对于两个对象，如果 equals相同，则 hashCode也必须相同，如果元素是自定义的类，需要注意这一点。

#### 实现原理
HashSet内部是用 HashMap实现的，它内部有一个 HashMap实例变量，如下所示： 
`private transient HashMap <E, Object> map;`
我们知道， Map有键和值， HashSet相当于只有键，值都是相同的固定值，这个值的定义为： 
`private static final Object PRESENT = new Object();`

HashSet的构造方法，主要就是调用了对应的 HashMap的构造方法，比如： 

``` Java
public HashSet(int initialCapacity, float loadFactor) { 
	map = new HashMap <>(initialCapacity, loadFactor); 
}
```

1. 没有重复元素； 
2. 可以高效地添加、删除元素、判断元素是否存在，效率都为 O（1）；
3. 没有顺序。

### TreeMap
``` Java
public TreeMap() 
public TreeMap(Comparator <? super K> comparator)
```

第二个接受一个比较器对象 comparator，如果 comparator不为 null，在 TreeMap内部进行比较时会调用这个 comparator的 compare方法，而不再调用键的 compareTo方法，也不再要求键实现 Comparable接口。

**Collections类有一个静态方法 reverseOrder（）可以返回一个逆序比较器，String类有一个静态成员 CASE_ INSENSITIVE_ ORDER，它就是一个忽略大小写的 Comparator对象**

#### 特点
1. 按键有序， TreeMap同样实现了 SortedMap和 NavigableMap接口，可以方便地根据键的顺序进行查找，如第一个、最后一个、某一范围的键、邻近键等。
2. 为了按键有序， TreeMap要求键实现 Comparable接口或通过构造方法提供一个 Com-parator对象。
3. 根据键保存、查找、删除的效率比较高，为 O（ h）， h为树的高度，在树平衡的情况下， h为 log2（ N）， N为节点数。

### TreeSet
HashSet是基于 HashMap实现的，元素就是 HashMap中的键，值是一个固定的值， TreeSet是类似的，它是基于 TreeMap实现的。

#### 特点
1. 没有重复元素。
2. 添加、删除元素、判断元素是否存在，效率比较高，为 O（ log2（ N））， N为元素个数。
3. 有序， TreeSet同样实现了 SortedSet和 NavigatableSet接口，可以方便地根据顺序进行查找和操作，如第一个、最后一个、某一取值范围、某一值的邻近元素等。
4. 为了有序， TreeSet要求元素实现 Comparable接口或通过构造方法提供一个 Com-parator对象。

### LinkedHashMap
LinkedHashMap是 HashMap的子类，但内部还有一个双向链表维护键值对的顺序，每个键值对既位于哈希表中，也位于这个双向链表中。 LinkedHashMap支持两种顺序：一种是插入顺序；另外一种是访问顺序。

LinkedHashMap的基本实现原理，它是 HashMap的子类，它的节点类 LinkedHashMap. Entry是 HashMap. Entry的子类， LinkedHashMap内部维护了一个单独的双向链表，每个节点即位于哈希表中，也位于双向链表中，在链表中的顺序默认是插入顺序，也可以配置为访问顺序， LinkedHashMap及其节点类 LinkedHashMap. Entry重写了若干方法以维护这种关系。

所谓访问是指 get/ put操作，对一个键执行 get/ put操作后，其对应的键值对会移到链表末尾，所以，最末尾的是最近访问的，最开始的最久没被访问的，这种顺序就是访问顺序。

LinkedHashMap有 5个构造方法，其中 4个都是按插入顺序，只有一个构造方法可以指定按访问顺序，如下所示： 

``` Java
public LinkedHashMap(int initialCapacity, float loadFactor, boolean accessOrder)
```

其中参数 accessOrder就是用来指定是否按访问顺序，如果为 true，就是访问顺序。默认情况下， LinkedHashMap是按插入有序的。

#### 使用场景
LinkedHashMap可以用于缓存，比如缓存用户基本信息，键是用户 Id，值是用户信息，所有用户的信息可能保存在数据库中，部分活跃用户的信息可能保存在缓存中。
一般而言，缓存容量有限，不能无限存储所有数据，如果缓存满了，当需要存储新数据时，就需要一定的策略将一些老的数据清理出去，这个策略一般称为替换算法。 LRU是一种流行的替换算法，它的全称是 Least Recently Used，即最近最少使用。它的思路是，最近刚被使用的很快再次被用的可能性最高，而最久没被访问的很快再次被用的可能性最低，所以被优先清理。

使用 LinkedHashMap，可以非常容易地实现 LRU缓存，默认情况下， LinkedHashMap没有对容量做限制，但它可以容易地做到，它有一个 protected方法，如下所示：

``` Java
protected boolean removeEldestEntry(Map.Entry <K, V> eldest) { 
	return false; 
}
```

在添加元素到 LinkedHashMap后， LinkedHashMap会调用这个方法，传递的参数是最久没被访问的键值对，如果这个方法返回 true，则这个最久的键值对就会被删除。 Linked-HashMap的实现总是返回 false，所有容量没有限制，但子类可以重写该方法，在满足一定条件的情况，返回 true。

### LinkedHashSet
LinkedHashSet是 HashSet的子类，它内部的 Map的实现类是 LinkedHashMap，所以它也可以保持插入顺序。

### EnumMap
如果需要一个 Map的实现类，并且键的类型为枚举类型，可以使用 HashMap，但应该使用一个专门的实现类 EnumMap。
主要是因为枚举类型有两个特征：一是它可能的值是有限的且预先定义的；二是枚举值都有一个顺序，这两个特征使得可以更为高效地实现 Map接口。

构造方法
``` Java
Map <Size, Integer> map = new EnumMap <>(Size.class);
```

与 HashMap不同，它需要传递一个类型信息， Size. class表示枚举类 Size的运行时类型信息， Size. class也是一个对象，它的类型是 Class。为什么需要这个参数呢？没有这个， EnumMap就不知道具体的枚举类是什么，也无法初始化内部的数据结构。

需要说明的是，与 HashMap不同， EnumMap是保证顺序的，输出是按照键在枚举中的顺序的。

### EnumSet
它的实现与 EnumMap没有任何关系，而是用极为精简和高效的位向量实现的。
**位向量不太懂**

与 TreeSet/ HashSet不同， EnumSet是一个抽象类，不能直接通过 new新建，不过， EnumSet提供了若干静态工厂方法，可以创建 EnumSet类型的对象，比如：

``` Java
Set <Day> weekend = EnumSet.noneOf(Day.class); 
weekend.add(Day.SATURDAY); 
weekend.add(Day.SUNDAY); 
System.out.println(weekend);
```