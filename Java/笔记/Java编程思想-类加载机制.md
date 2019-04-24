# 类加载机制

ClassLoader一般是系统提供的，不需要自己实现，不过，通过创建自定义的 ClassLoader，可以实现一些强大灵活的功能，比如： 
1. 热部署。在不重启 Java程序的情况下，动态替换类的实现，比如 Java Web开发中的 JSP技术就利用自定义的 ClassLoader实现修改 JSP代码即生效， OSGI（ Open Service Gateway Initiative）框架使用自定义 ClassLoader实现动态更新。
2. 应用的模块化和相互隔离。不同的 ClassLoader可以加载相同的类但互相隔离、互不影响。 Web应用服务器如 Tomcat利用这一点在一个程序中管理多个 Web应用程序，每个 Web应用使用自己的 ClassLoader，这些 Web应用互不干扰。 OSGI和 Java 9利用这一点实现了一个动态模块化架构，每个模块有自己的 ClassLoader，不同模块可以互不干扰。
3. 从不同地方灵活加载。系统默认的 ClassLoader一般从本地的. class文件或 jar文件中加载字节码文件，通过自定义的 ClassLoader，我们可以从共享的 Web服务器、数据库、缓存服务器等其他地方加载字节码文件。

## 类加载的基本机制和过程
负责加载类的类就是类加载器，它的输入是完全限定的类名，输出是 Class对象。类加载器不是只有一个，一般程序运行时，都会有三个
1. 启动类加载器（Bootstrap ClassLoader）：这个加载器是 Java虚拟机实现的一部分，不是 Java语言实现的，一般是 C + +实现的，它负责加载 Java的基础类，主要是 <JAVA_ HOME>/lib/rt. jar，我们日常用的 Java类库比如 String、 ArrayList等都位于该包内。
2. 扩展类加载器（Extension ClassLoader）：这个加载器的实现类是 sun.misc.Laun-cher$ExtClassLoader，它负责加载 Java的一些扩展类，一般是 <JAVA_ HOME>/lib/ext目录中的 jar包。
3. 应用程序类加载器（Application ClassLoader）：这个加载器的实现类是 sun.misc.Launcher$AppClassLoader，它负责加载应用程序的类，包括自己写的和引入的第三方法类库，即所有在类路径中指定的类。

具体来说，在加载一个类时，基本过程是：
1. 判断是否已经加载过了，加载过了，直接返回 Class对象，一个类只会被一个 Class-Loader加载一次。
2. 如果没有被加载，先让父 ClassLoader去加载，如果加载成功，返回得到的 Class对象。
3. 在父 ClassLoader没有加载成功的前提下，自己尝试加载类。

这个过程一般被称为“双亲委派”模型，即优先让父 ClassLoader去加载。为什么要先让父 ClassLoader去加载呢？这样，可以避免 Java类库被覆盖的问题。比如，用户程序也定义了一个类 java.lang.String，通过双亲委派， java.lang.String只会被 Bootstrap ClassLoader加载，避免自定义的 String覆盖 Java类库的定义。

## 理解 ClassLoader
每个 Class对象都有一个方法，可以获取实际加载它的 ClassLoader，方法是：

``` Java
public ClassLoader getClassLoader()
```

ClassLoader有一个方法，可以获取它的父 ClassLoader： 

``` Java
public final ClassLoader getParent()
```

ClassLoader中有一个主要方法，用于加载类： 

``` Java
public Class <?> loadClass(String name) throws ClassNotFoundException
```

ClassLoader的 loadClass方法与 Class的 forName方法都可以加载类，它们有什么不同呢？基本是一样的，不过， ClassLoader的 loadClass不会执行类的初始化代码。

## 类加载的应用：可配置的策略
可以通过 ClassLoader的 loadClass或 Class. forName自己加载类，但什么情况需要自己加载类呢？很多应用使用面向接口的编程，接口具体的实现类可能有很多，适用于不同的场合，具体使用哪个实现类在配置文件中配置，通过更改配置，不用改变代码，就可以改变程序的行为，在设计模式中，这是一种策略模式。