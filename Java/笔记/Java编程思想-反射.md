# 反射

> 反射是在运行时，而非编译时，动态获取类型的信息，比如接口信息、成员信息、方法信息、构造方法信息等，根据这些动态获取到的信息创建对象、访问/修改成员、调用方法等。  

## Class类
每个已加载的类在内存都有一份类信息，每个对象都有指向它所属类信息的引用。 Java中，类信息对应的类就是 java.lang.Class。所有类的根父类 Object有一个方法，可以获取对象的 Class对象：

``` Java
public final native Class <?> getClass()
```

Class是一个泛型类，有一个类型参数， getClass（）并不知道具体的类型，所以返回 Class <?>。

获取 Class对象不一定需要实例对象，如果在写程序时就知道类名，可以使用 <类名 >. class获取 Class对象，比如：

``` Java
Class <Date> cls = Date.class;
Class <Comparable> cls = Comparable.class;
```

Class有一个静态方法 forName，可以根据类名直接加载 Class，获取 Class对象，比如：

``` Java
try { 
	Class <?> cls = Class.forName("java.util.HashMap"); 
	System.out.println(cls.getName()); 
} 
catch (ClassNotFoundException e) { 
	e.printStackTrace(); 
}
```

### 名称信息
Class有如下方法，可以获取与名称有关的信息：

``` Java
public String getName() 
public String getSimpleName() 
public String getCanonicalName() 
public Package getPackage()
```

getSimpleName返回的名称不带包信息， getName返回的是 Java内部使用的真正的名称， getCanonicalName返回的名称更为友好， getPackage返回的是包信息。

### 字段信息
类中定义的静态和实例变量都被称为字段，用类 Field表示，位于包 java.lang.reflect下，Class有 4个获取字段信息的方法：

``` Java
//返回所有的 public字段，包括其父类的，如果没有字段，返回空数组 
public Field[] getFields() 
//返回本类声明的所有字段，包括非 public的，但不包括父类的 
public Field[] getDeclaredFields() 
//返回本类或父类中指定名称的 public字段，找不到抛出异常 NoSuchFieldException 
public Field getField(String name) 
//返回本类中声明的指定名称的字段，找不到抛出异常 NoSuchFieldException 
public Field getDeclaredField(String name)
```

Field也有很多方法，可以获取字段的信息，也可以通过 Field访问和操作指定对象中该字段的值，基本方法有：

``` Java
//获取字段的名称 
public String getName() 
//判断当前程序是否有该字段的访问权限 
public boolean isAccessible() 
//flag设为 true表示忽略 Java的访问检查机制，以允许读写非 public的字段 
public void setAccessible(boolean flag) 
//获取指定对象 obj中该字段的值 
public Object get(Object obj)
//将指定对象 obj中该字段的值设为 value 
public void set(Object obj, Object value)
```

在 get/ set方法中，对于静态变量， obj被忽略，可以为 null，如果字段值为基本类型， get/ set会自动在基本类型与对应的包装类型间进行转换；对于 private字段，直接调用 get/ set会抛出非法访问异常 IllegalAccessException，应该先调用 setAccessible（ true）以关闭 Java的检查机制。看段简单的示例代码：

``` Java
List <String> obj = Arrays.asList(new String[]{"老马","编程"}); 
Class <?> cls = obj.getClass(); 
for(Field f : cls.getDeclaredFields()){ 
	f.setAccessible(true); 
	System.out.println(f.getName() +"-"+ f.get(obj));
}
```

除了以上方法， Field还有很多其他方法，比如：

``` Java
//返回字段的修饰符 
public int getModifiers() 
//返回字段的类型 
public Class <?> getType() 
//以基本类型操作字段 
public void setBoolean(Object obj, boolean z) 
public boolean getBoolean( Object obj) 
public void setDouble(Object obj, double d) 
public double getDouble(Object obj)
//查询字段的注解信息，下一章介绍注解 
public <T extends Annotation> T getAnnotation(Class <T> annotationClass) 
public Annotation[] getDeclaredAnnotations()
```

### 方法信息
类中定义的静态和实例方法都被称为方法，用类 Method表示。 Class有如下相关方法：

``` Java
//返回所有的 public方法，包括其父类的，如果没有方法，返回空数组 
public Method[] getMethods() 
//返回本类声明的所有方法，包括非 public的，但不包括父类的 
public Method[] getDeclaredMethods() 
//返回本类或父类中指定名称和参数类型的 public方法，找不到抛出异常 NoSuchMethodException 
public Method getMethod(String name, Class <?>... parameterTypes) 
//返回本类中声明的指定名称和参数类型的方法，找不到抛出异常 NoSuchMethodException 
public Method getDeclaredMethod(String name, Class <?>... parameterTypes)
```

通过 Method可以获取方法的信息，也可以通过 Method调用对象的方法，基本方法有：

``` Java
//获取方法的名称 
public String getName() 
//flag设为 true表示忽略 Java的访问检查机制，以允许调用非 public的方法 
public void setAccessible(boolean flag)
//在指定对象 obj上调用 Method代表的方法，传递的参数列表为 args 
public Object invoke(Object obj, Object... args) throws IllegalAccessException, Illegal-ArgumentException, InvocationTargetException
```

对 invoke方法，如果 Method为静态方法， obj被忽略，可以为 null， args可以为 null，也可以为一个空的数组，方法调用的返回值被包装为 Object返回，如果实际方法调用抛出异常，异常被包装为 InvocationTargetException重新抛出，可以通过 getCause方法得到原异常。

### 创建对象和构造方法
Class有一个方法，可以用它来创建对象，它会调用类的默认构造方法（即无参 public构造方法），如果类没有该构造方法，会抛出异常 InstantiationException。看个简单示例：

``` Java
Map <String, Integer> map = HashMap.class.newInstance(); 
map.put("hello", 123);
```

newInstance只能使用默认构造方法。 Class还有一些方法，可以获取所有的构造方法：

``` Java
//获取所有的 public构造方法，返回值可能为长度为 0的空数组 
public Constructor <?>[] getConstructors() 
//获取所有的构造方法，包括非 public的 
public Constructor <?>[] getDeclaredConstructors() 
//获取指定参数类型的 public构造方法，没找到抛出异常 NoSuchMethodException 
public Constructor <T> getConstructor(Class <?>... parameterTypes) 
//获取指定参数类型的构造方法，包括非 public的，没找到抛出异常 NoSuchMethodException 
public Constructor <T> getDeclaredConstructor(Class <?>... parameterTypes)
```

类 Constructor表示构造方法，通过它可以创建对象，看个例子：

``` Java
Constructor <StringBuilder> contructor = StringBuilder.class.getConstructor(new Class[]{int.class});
StringBuilder sb = contructor.newInstance(100);
```

### 类型检查和转换

我们之前介绍过 instanceof关键字，它可以用来判断变量指向的实际对象类型。 instanceof后面的类型是在代码中确定的，如果要检查的类型是动态的，可以使用 Class类的如下方法：

``` Java
Class cls = Class.forName("java.util.ArrayList"); 
if(cls.isInstance(list)){ 
	System.out.println("array list"); 
}

//与下面代码相同
if(list instanceof ArrayList){ 
	System.out.println("array list"); 
}
```

除了判断类型，在程序中也往往需要进行强制类型转换，比如：

``` Java
List list = .. 
if(list instanceof ArrayList){ 
	ArrayList arrList = (ArrayList) list; 
}
```

在这段代码中，强制转换到的类型是在写代码时就知道的。如果是动态的，可以使用 Class的如下方法：

``` Java
public static <T> T toType(Object obj, Class <T> cls){ 
	return cls.cast(obj);
}
```

### Class的类型信息
Class代表的类型既可以是普通的类，也可以是内部类，还可以是基本类型、数组等，对于一个给定的 Class对象，它到底是什么类型呢？可以通过以下方法进行检查：

``` Java
public native boolean isArray() 
//是否是数组 
public native boolean isPrimitive() 
//是否是基本类型 
public native boolean isInterface() 
//是否是接口 
public boolean isEnum() 
//是否是枚举 
public boolean isAnnotation() 
//是否是注解 
public boolean isAnonymousClass() 
//是否是匿名内部类 
public boolean isMemberClass() 
//是否是成员类，成员类定义在方法外，不是匿名类 
public boolean isLocalClass() 
//是否是本地类，本地类定义在方法内，不是匿名类
```

### 类的声明信息
Class还有很多方法，可以获取类的声明信息，如修饰符、父类、接口、注解等，如下所示：

``` Java
//获取修饰符，返回值可通过 Modifier类进行解读 
public native int getModifiers() 
//获取父类，如果为 Object，父类为 null 
public native Class <? super T> getSuperclass() 
//对于类，为自己声明实现的所有接口，对于接口，为直接扩展的接口，不包括通过父类继承的 
public native Class <?>[] getInterfaces(); 
//自己声明的注解 
public Annotation[] getDeclaredAnnotations() 
//所有的注解，包括继承得到的 
public Annotation[] getAnnotations() 
//获取或检查指定类型的注解，包括继承得到的 
public <A extends Annotation > A getAnnotation(Class <A> annotationClass) 
public boolean isAnnotationPresent(Class <? extends Annotation> annotationClass)
```

### 类的加载
Class有两个静态方法，可以根据类名加载类：

``` Java
public static Class <?> forName(String className) 
public static Class <?> forName(String name, boolean initialize, ClassLoader loader)
```