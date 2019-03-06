# Java编程的逻辑-异常&常用基础类
1. try/ catch/ finally语法中， catch不是必需的，也就是可以只有 try/ finally，表示不捕获异常，异常自动向上传递，但 finally中的代码在异常发生后也执行。
2. finally语句有一个执行细节，如果在 try或者 catch语句内有 return语句，则 return语句在 finally语句执行结束后才执行，但 finally并不能改变返回值。
3. 如果在 finally中也有 return语句呢？ try和 catch内的 return会丢失，实际会返回 finally中的返回值。 finally中有 return不仅会覆盖 try和 catch内的返回值，还会掩盖 try和 catch内的异常，就像异常没有发生一样。
4. 所以，一般而言，为避免混淆，应该避免在 finally中使用 return语句或者抛出异常。

Java 7开始支持一种新的语法，称之为 try-with-resources，这种语法针对实现了 java. lang. AutoCloseable接口的对象。`try( AutoCloseable r = new FileInputStream(" hello"))` ，资源 r 的声明和初始化放在 try语句内，不用再调用 finally，在语句执行完 try语句后，会自动调用资源的 close() 方法。

## 包装类
1. 每种包装类都有一个静态方法 valueOf()，接受基本类型，返回引用类型，也都有一个实例方法 xxxValue()返回对应的基本类型。
2. 每个包装类都有一个静态的 valueOf(String)方法，根据字符串表示返回包装类对象，也都有一个静态的 parseXXX(String)方法，根据字符串表示返回基本类型值。
3. 包装类都是不可变类。所谓不可变是指实例对象一旦创建，就没有办法修改了。

### 装箱&拆箱
将基本类型转换为包装类的过程，一般称为“装箱”，而将包装类型转换为基本类型的过程，则称为“拆箱”。装箱/拆箱写起来比较烦琐， Java 5以后引入了自动装箱和拆箱技术。

### valueOf&new
一般建议使用 valueOf方法。 new每次都会创建一个新对象，而除了 Float和 Double外的其他包装类，都会缓存包装类对象（IntegerCache，Integer的内部类），减少需要创建对象的次数，节省空间，提升性能。实际上，从 Java 9开始，这些构造方法已经被标记为过时了，推荐使用静态的 valueOf方法。

### equals&hashCode
1. equals默认实现也是比较内存地址，所有的包装类都重写了，改成是对象间的逻辑相等关系。
2. hashCode返回一个对象的哈希值。哈希值是一个 int类型的数，由对象中一般不变的属性映射得来，用于快速对对象进行区分、分组等。
3. hashCode和 equals方法联系密切，对两个对象，如果 equals方法返回 true，则 hashCode也必须一样。反之不要求， equal方法返回 false时， hashCode可以一样，也可以不一样，但应该尽量不一样。 hashCode的默认实现一般是将对象的内存地址转换为整数，子类如果重写了 equals方法，也必须重写 hashCode。

### 字符串常量池
字符串常量池，它保存所有的常量字符串，每个常量只会保存一份，被所有使用者共享。当通过常量的形式使用一个字符串的时候，使用的就是常量池中的那个对应的 String类型的对象。

### 策略模式
**传递比较器 Comparator给 sort方法，体现了程序设计中一种重要的思维方式。将不变和变化相分离，排序的基本步骤和算法是不变的，但按什么排序是变化的， sort方法将不变的算法设计为主体逻辑，而将变化的排序方式设计为参数，允许调用者动态指定，这也是一种常见的设计模式，称为策略模式，不同的排序方式就是不同的策略。**