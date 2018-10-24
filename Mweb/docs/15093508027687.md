# Java 基础 for Android 开发

## Java 基础

### 运算符
- 按位与：两位同时为1，结果才为1，否则为0
- 按位或：两位同时为0，结果才为0，否则为1
- 按位异或：两位相同时为1，不同时为0
- 参考：[Java运算符](http://www.jianshu.com/p/acf982146311)

### 方法的重载，重写，构造方法
- 重写：重写只能出现在继承关系之中。当一个类继承它的父类方法时，都有机会重写该父类的方法。一个特例是父类的方法被标识为final。重写的主要优点是能够定义某个子类型特有的行为
- 重载：简单理解为同一个方法名，但是参数不同
- 构造方法：比如一些初始化操作
	1. 构造方法的名称必须与类名相同
	2. 构造方法不能有返回类型
	3. 如果不在类中创建自己的构造方法，编译器会自动生成默认的不带参数的构造函数
	4. 构造方法能使用任何访问修饰符

### super，this
- this
	1. 具体的说是指向对象本身的一个指针，当一个对象创建的时候，JVM 会给这个对象分配一个引用本身的指针，这个指针的名字就是 this
	2. 当局部变量和成员变量同名时，局部变量的优先级高，我们不能够通过变量名引用到成员变量，这时候就需要使用 this 来引用成员变量
- super：super用在子类中，引用的是直接父类的成员

### 循环，分支语句
- 这个就是 if else，while，switch 之类的，不细说了，给大家推荐两篇文章
- [Java循环结构](http://www.jianshu.com/p/c85bdec8036c)
- [Java分支结构](http://www.jianshu.com/p/24781a03c4e1)

### 单例模式
- java 单例模式指整个程序中只有一个某个类的实例，通常被用来代表那些本质上唯一的系统组件
- 文档有很多，比如这篇 [单例模式](http://www.jianshu.com/p/26cc87fe0d0c)

### synchronized 
- 由于同一进程的多个线程共享同一片存储空间，带来了访问冲突这个严重的问题
- 某个对象实例内，synchronized aMethod(){} 可以防止多个线程同时访问这个对象的 synchronized 方法，这时，不同的对象实例的 synchronized 方法是不相干扰的。也就是说，其它线程照样可以同时访问相同类的另一个对象实例中的 synchronized 方法
- 某个类的范围，synchronized static aStaticMethod{} 防止多个线程同时访问这个类中的 synchronized static 方法。它可以对类的所有对象实例起作用

> 如果一个对象有多个synchronized方法，只要一个线程访问了其中的一个synchronized方法，其它线程不能同时访问这个对象中任何一个synchronized方法

### Java 关键字
#### Static 
- static 关键字可以用来修饰类的变量，方法和内部类
- static 是静态的意思，**static强调只有一份**，也是全局的意思它定义的东西，属于全局与类相关，不与具体实例相关

>  就是说它调用的时候，只是 ClassName.method() 而不是 new ClassName().method()。不与具体实例相关

#### Final 
- final 关键字有三个东西可以修饰的。修饰类，方法，变量
1. 在类的声明中使用 final
	- 使用了 final 的类不能再派生子类，就是说不可以被继承了
2. 在方法声明中使用 final
	- 被定义为 final 的方法不能被重写了，如果定义类为 final 的话，是所有的方法都不能重写。而我们只需要类中的某几个方法，不可以被重写，就在方法前加 final 了。而且定义为 final 的方法执行效率要高的啊
3. 在变量声明中使用 final
	- 这样的变量就是常量了，在程序中这样的变量不可以被修改的。修改的话编译器会抱错的。而且执行效率也是比普通的变量要高
	- final 的变量如果没有赋予初值的话，其他方法就必需给他赋值，但只能赋值一次

> 注意：子类不能重写父类的静态方法哦，也不能把父类不是静态的重写成静态的方法。想隐藏父类的静态方法的话，在子类中声明和父类相同的方法就行了

> **其他关键字不再举例说明，留给大家自己去学习**

### Java 字符串
#### String（字符串常量）
- Stirng 是对象不是基本数据类型 
- String 是 final 类，不能被继承。是不可变对象，一旦创建，就不能修改它的值

#### StringBuffer（字符串变量）
- 一个类似于 String 的字符串缓冲区，对它的修改的不会像 String 那样重创建对象
- 使用 append() 方法修改 Stringbuffer 的值，使用 toString() 方法转换为字符串
- 线程安全的，建议多线程使用
- **注意**：不能通过赋值符号对他进行赋值

#### StringBuilder（字符串变量）
- StringBuild 是 jdk1.5 后用来替换 stringBuffer 的一个类，大多数时候可以替换 StringBuffer。和 StringBuffer 的区别在于Stringbuild 是一个单线程使用的类，不执行线程同步所以比 StringBuffer 的速度快，效率高
- 线程非安全的，建议单线程使用
- **注意**：不能通过赋值符号对他进行赋值

> 线程安全就是多线程访问时，采用了加锁机制，当一个线程访问该类的某个数据时，进行保护，其他线程不能进行访问直到该线程读取完，其他线程才可使用。不然会出现数据不一致或者数据污染

### Java 反射
#### 定义
- Java反射机制是指在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为java语言的反射机制
- 用一句话总结就是反射可以实现在运行时可以知道任意一个类的属性和方法

#### 方法

``` java
Code code1 = new Code();
Class c1 = Code.class;
//这说明任何一个类都有一个隐含的静态成员变量 class，这种方式是通过获取类的静态成员变量 class 得到的
Class c2 = code1.getClass();
//code1 是 Code 的一个对象，这种方式是通过一个类的对象的 getClass() 方法获得的
Class c3 = Class.forName("com.trigl.reflect.Code");
//这种方法是 Class 类调用 forName 方法，通过一个类的全量限定名获得
```

#### 举例

``` java
Class c = Class.forName("com.tengj.reflect.Person");
Method[] methods = c.getDeclaredMethods(); 
// 得到该类所有的方法，不包括父类的
Method[] methods = c.getMethods();
// 得到该类所有的public方法，包括父类的
```

**参考文章：** [java 反射](http://www.jianshu.com/p/f67182a482eb?utm_campaign=hugo&utm_medium=reader_share&utm_content=note)

### Java 接口，抽象类
#### 接口（Interface）
- 首先，理解多继承 ── 多继承就是可以继承多个父类，但是 Java 不能实现多继承，所以就要用到接口

> 接口是一种规范，是一种规则，它只定义了方法的名字，规定你要实现哪些方法，而没有实现具体的方法，接口的实现类需要去实现这些方法，但是对于不同的实现类来说，对方法的实现可以完全不同

- 实现接口的非抽象类必须实现接口的所有方法
- 接口的所有方法自动被声明为 public，而且只能为 public
- 所有方法都是抽象方法，不能包含实现的方法，也不能包含静态方法
- 可以使用 instanceOf 来判断一个类是否实现了某个接口，如 `if (object instanceOf ClassName){doSth()}`
- 接口可以定义"成员变量"，而且会自动转为 public final static，即常量

#### 抽象类（Abstract）
> 如果在两个类当中有同名的方法，按照正常道理来说，应该提取到父类里，但是这个两个方法又有明显的实现上的不同，那么在父类里的方法，就应该定义成为抽象方法，只给出了方法的样子，而不给出方法的具体实现，具体实现由继承这个类的具体的子类去实现

- 抽象类中可以包含抽象方法与非抽象方法
- 含有抽象方法的类一定是抽象类，但是抽象类不一定含有抽象方法
- 没有抽象方法的抽象类的存在也是有意义的。这决定了这个类是不能被直接实例化的
- 子类必须重写父类的所有抽象方法

#### 区别
- 接口一般处于代码的最底层，作出一些规定，而接口之上一层抽象类层，对接口进行第一次的实现，把不可能一次完成的方法，交由自己的子类来实现
- 抽象类可以提供某些方法的部分实现，而接口不可以。如果向一个抽象类里加入一个新的具体方法时，那么它所有的子类都一下子都得到了这个新方法，而接口做不到这一点，如果向一个接口里加入一个新方法，所有实现这个接口的类就无法成功通过编译了，因为你必须让每一个类都再实现这个方法才行

### Java 泛型
> 泛型的定义：参数化类型。具体点说就是处理的数据类型不是固定的，而是可以作为参数传入。这样，同一套代码，可以用于多种数据类型

#### 举例

``` java
// 定义泛型类
public class Som<T> {
    private T value;
    public T getValue() {
        return value;
    }
    public void setValue(T value) {
        this.value = value;
    }
}

// 使用泛型类
Som<String> som = new Som<>();
som.setValue("Hi");
String str = som.getValue();
```

> Som就是一个泛型类，value的类型是T，而T是参数化的。如果有多个类型参数，使用分号隔开,如 U,V


### Java 集合
#### List
> List表示一种有序的集合，而且其中元素可以重复，实现 List 接口的常用类有 ArrayList，LinkedList，Vector
> ArrayList是一个实现了List接口的可变大小的“数组”类，ArrayList类的对象会随着其中元素的增加而自动扩大。它是List的三个实现类中最常用、正常情况下效率最高的一个

##### 举例

``` java
public static void main(String[] args) {
    List<String> list = new ArrayList<>();
    list.add("a");
    list.add("b");
    list.add("c");
    list.add("d");
    String listString = list.toString();
    System.out.println(listString);

    Integer size = list.size();
    for (int i = 0; i < size; i++) {
        String value1 = list.get(i);
        System.out.println(value1);
    }
    System.out.println("==========================");

    Iterator<String> iterator = list.iterator();
    while (iterator.hasNext()) {
        String value2 = iterator.next();
        System.out.println(value2);
    }
    System.out.println("==========================");

    for (String string : list) {
        System.out.println(string);
    }
}}
```

#### Set
> Set 是最简单的一种集合。集合中的对象不按特定的方式排序，并且没有重复对象

##### 举例

``` java
Set set=new HashSet();  
String s1=new String("hello");  
String s2=s1;  
String s3=new String("world");  
set.add(s1);  
set.add(s2);  
set.add(s3);  
System.out.println(set.size());
// 打印集合中对象的数目为2
```

#### Map
> Map 是存储键和值这样的双列数据的集合，Map 中存储的数据是没有顺序的，其键是不能重复的，它的值是可以有重复的

##### 举例

``` java
public static void main(String[] args) {
    Map<String, Integer> map = new HashMap<>();
    map.put("a", 1);
    map.put("b", 2);
    map.put("c", 3);
    map.put("d", 4);

    Set<String> keySet = map.keySet();
    for (String key : keySet) {
        Integer value = map.get(key);
        System.out.println("键："+ key + "值："+ value);
    }

    Set<Entry<String, Integer>> set = map.entrySet();
    for (Entry<String, Integer> entry : set) {
        String key = entry.getKey();
        Integer value = entry.getValue();
        System.out.println("键："+ key + "值"+value);
    }
    
    Iterator<Entry<String, Integer>> entrySet = map.entrySet().iterator();
    while (entrySet.hasNext()) {
        Entry<String, Integer> entry = entrySet.next();
        String key = entry.getKey();
        Integer value = entry.getValue();
        System.out.println("键：" + key + " " + "值：" + value);
    }
}
```

### Java 多线程
#### 继承 Thread 类

``` java
class MyThread extends Thread {
    @Override 
    public void run() {
    }
}
new MyThread().start();
```

#### 实现 Runnable 接口

``` java
class MyThread implements Runnable {
    @Override
    public void run() {
    }
}
MyThread myThread = new MyThread();
new Thread (myThread).start();
```

#### 匿名类

``` java
new Thread (new Runnable()) {
    @Override
    Public Void run () {
    }
}).start();
```

### Java 虚拟机
**虚拟机内存**

![虚拟机](http://wiki.jikexueyuan.com/project/java-vm/images/jvmdata.png)

> 栈 Stack 主要存放 reference 引用
> 堆 Heap 主要存放实例 instance

#### 栈内存
##### Java 虚拟机栈
> 该区域也是线程私有的，它的生命周期也与线程相同。虚拟机栈描述的是 Java 方法执行的内存模型：每个方法被执行的时候都会同时创建一个栈帧，栈是用于支持续虚拟机进行方法调用和方法执行的数据结构。

- 在单线程的操作中，无论是由于栈帧太大，还是虚拟机栈空间太小，当栈空间无法分配时，虚拟机抛出的都是 StackOverflowError 异常。而在多线程环境下，则会抛出 OutOfMemoryError 异常

##### 本地方法栈
- 该区域与虚拟机栈所发挥的作用非常相似，只是虚拟机栈为虚拟机执行 Java 方法服务，而本地方法栈则为使用到的本地操作系统（Native）方法服务

#### 堆内存
- Java Heap 是 Java 虚拟机所管理的内存中最大的一块，它是所有线程共享的一块内存区域。几乎所有的对象实例都在这分配内存。Java Heap 是垃圾收集器管理的主要区域，因此很多时候也被称为“GC堆”
- 如果在堆中没有内存可分配时，并且堆也无法扩展时，将会抛出 OutOfMemoryError 异常

#### 方法区
- 方法区也是各个线程共享的内存区域，它用于存储已经被虚拟机加载的类信息、常量、静态变量、即时编译器编译后的代码等数据
- 垃圾收集行为在这个区域比较少出现，该区域的内存回收目标主要针是对废弃常量的和无用类的回收
- 运行时常量池是方法区的一部分

#### 垃圾回收
> GC 是一种自动的存储管理机制。当一些被占用的内存不再需要时，就应该予以释放，以让出空间，这种存储资源管理，称为垃圾回收

##### 执行时机
- 当应用程序空闲时，即没有应用线程在运行时，GC会被调用。因为GC在优先级最低的线程中进行,所以当应用忙时，GC线程就不会被调用，但以下条件除外
- Java堆内存不足时，GC会被调用。当应用线程在运行，并在运行过程中创建新对象，若这时内存空间不足，JVM就会强制地调用GC线程，以便回收内存用于新的分配
- 若GC一次之后仍不能满足内存分配的要求，JVM会再进行两次GC作进一步的尝试，若仍无法满足要求，则 JVM将报**“Out Of Memory”**的错误，引起App的**Crash**

##### 对程序的影响
- 当垃圾回收开始清理资源时，其余的所有线程都会被停止。所以，我们要做的就是尽可能的让它执行的时间变短。如果清理的时间过长，在我们的应用程序中就能感觉到明显的卡顿

> **虚拟机这块知识，内容很多，上面是我提取了其中的一部分，如果想深入了解，可以自行 Google，有很多资料都有介绍，下面是一些知识点**
*链接只是推荐，建议自行搜索，找适合自己，能看明白的文章*
1. [虚拟机](http://www.jianshu.com/p/e00971e07e14)
2. [class与dex文件](http://www.jianshu.com/p/2eb518941681)
3. [Class加载](http://www.jianshu.com/p/37cad7a901b1)

### 其余一些
- break 跳出，中断
- continue 继续
- return 返回
- instanceof 实例
- try ... catch
- 等等。。。

### 访问控制：

![访问限制](https://ws3.sinaimg.cn/large/006tKfTcly1fp40zn5tjqj30i8094425.jpg)




