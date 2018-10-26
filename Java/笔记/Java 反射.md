# Java 反射
---

## Java 内存模型
![Alt text](./image.jpg)

## 什么是JVM

- 假如你写了一段代码：Object o=new Object()，运行了起来！
- 首先JVM会启动，你的代码会编译成一个.class文件，然后被类加载器加载进jvm的内存中，你的类Object加载到方法区中，创建了Object类的class对象到堆中，注意这个不是new出来的对象，而是类的类型对象，每个类只有一个class对象，作为方法区类的数据结构的接口。
- jvm 创建对象前，会先检查类是否加载，寻找类对应的class对象，若加载好，则为你的对象分配内存，初始化也就是代码:new Object()。
- 上面的流程就是你自己写好的代码扔给jvm去跑，跑完就over了，jvm关闭，你的程序也停止了。

*为什么要讲这个呢？因为要理解反射必须知道它在什么场景下使用。*
*题主想想上面的程序对象是自己new的，程序相当于写死了给jvm去跑。假如一个服务器上突然遇到某个请求哦要用到某个类，哎呀但没加载进jvm，是不是要停下来自己写段代码，new一下？*
 
## 反射是什么呢？

- 当我们的程序在运行时，需要动态的加载一些类这些类可能之前用不到所以不用加载到jvm，而是在运行时根据需要才加载，这样的好处对于服务器来说不言而喻，
- 举个例子， 我们的项目底层有时是用mysql，有时用oracle，需要动态地根据实际情况加载驱动类，这个时候反射就有用了
- 假设 `com.java.dbtest.myqlConnection`，`com.java.dbtest.oracleConnection`这两个类我们要用，这时候我们的程序就写得比较动态化，通过`Class tc = Class.forName("com.java.dbtest.TestConnection");`通过类的全类名让jvm在服务器中找到并加载这个类。
- 这时候就可以看到反射的好处了，这个动态性就体现出java的特性了！
- 举多个例子，大家如果接触过spring，会发现当你配置各种各样的bean时，是以配置文件的形式配置的，你需要用到哪些bean就配哪些，spring容器就会根据你的需求去动态加载，你的程序就能健壮地运行。

[全方位解读Java反射](http://www.imooc.com/article/8581)
[学习java应该如何理解反射？](https://www.zhihu.com/question/24304289)



