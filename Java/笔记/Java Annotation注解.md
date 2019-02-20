# Annotation

## 定义注解
> 注解通过 `@interface` 关键字进行定义。

## 元注解
共5种，`@Retention、@Documented、@Target、@Inherited、@Repeatable`

### Retention
Retention 的英文意为保留期的意思。当 @Retention 应用到一个注解上的时候，它解释说明了这个注解的的存活时间。

它的取值如下：
`RetentionPolicy.SOURCE` 注解只在源码阶段保留，在编译器进行编译时它将被丢弃忽视。
`RetentionPolicy.CLASS` 注解只被保留到编译进行的时候，它并不会被加载到 JVM 中。
`RetentionPolicy.RUNTIME` 注解可以保留到程序运行的时候，它会被加载进入到 JVM 中，所以在程序运行时可以获取到它们。

### Documented
顾名思义，这个元注解肯定是和文档有关。它的作用是能够将注解中的元素包含到 Javadoc 中去。

### Target
Target 是目标的意思，@Target 指定了注解运用的地方。
你可以这样理解，当一个注解被 @Target 注解时，这个注解就被限定了运用的场景。

`ElementType.ANNOTATION_TYPE` 可以给一个注解进行注解
`ElementType.CONSTRUCTOR` 可以给构造方法进行注解
`ElementType.FIELD` 可以给属性进行注解
`ElementType.LOCAL_VARIABLE` 可以给局部变量进行注解
`ElementType.METHOD` 可以给方法进行注解
`ElementType.PACKAGE` 可以给一个包进行注解
`ElementType.PARAMETER` 可以给一个方法内的参数进行注解
`ElementType.TYPE` 可以给一个类型进行注解，比如类、接口、枚举

### Inherited
Inherited 是继承的意思，但是它并不是说注解本身可以继承，而是说如果一个超类被 @Inherited 注解过的注解进行注解的话，那么如果它的子类没有被任何注解应用的话，那么这个子类就继承了超类的注解。
说的比较抽象。代码来解释。

``` Java
@Inherited
@Retention(RetentionPolicy.RUNTIME)
@interface Test {}

@Test
public class A {}

public class B extends A {}
```
注解 Test 被 @Inherited 修饰，之后类 A 被 Test 注解，类 B 继承 A,类 B 也拥有 Test 这个注解。

### Repeatable
Repeatable 自然是可重复的意思。@Repeatable 是 Java 1.8 才加进来的，所以算是一个新的特性。
什么样的注解会多次应用呢？通常是注解的值可以同时取多个。
举个例子，一个人他既是程序员又是产品经理,同时他还是个画家。

``` Java
@interface Persons {
	Person[]  value();
}

@Repeatable(Persons.class)
@interface Person{
	String role default "";
}

@Person(role="artist")
@Person(role="coder")
@Person(role="PM")
public class SuperMan{
	
}
```
注意上面的代码，@Repeatable 注解了 Person。而 @Repeatable 后面括号中的类相当于一个容器注解。
什么是容器注解呢？就是用来存放其它注解的地方。它本身也是一个注解。

看第一段代码，它里面必须要有一个 value 的属性，属性类型是一个被 @Repeatable 注解过的注解数组，注意它是数组。

## 注解的属性
注解的属性也叫做成员变量。注解只有成员变量，没有方法。注解的成员变量在注解的定义中以“无形参的方法”形式来声明，其方法名定义了该成员变量的名字，其返回值定义了该成员变量的类型。

``` Java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface TestAnnotation {
	
	int id();
	String msg();
	
}
```

上面代码定义了 TestAnnotation 这个注解中拥有 id 和 msg 两个属性。在使用的时候，我们应该给它们进行赋值。
赋值的方式是在注解的括号内以 value="" 形式，多个属性之前用 ，隔开。

``` Java
@TestAnnotation(id=3,msg="hello annotation")
public class Test {

}
```
需要注意的是，在注解中定义属性时它的类型必须是 8 种基本数据类型外加 类、接口、注解及它们的数组。

注解中属性可以有默认值，默认值需要用 default 关键值指定。比如：

``` Java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
public @interface TestAnnotation {
	
	public int id() default -1;
	public String msg() default "Hi";

}
```
它可以这样应用。

``` Java
@TestAnnotation()
public class Test {}
```
因为有默认值，所以无需要再在 @TestAnnotation 后面的括号里面进行赋值了，这一步可以省略。

另外，还有一种情况。如果一个注解内仅仅只有一个名字为 value 的属性时，应用这个注解时可以直接接属性值填写到括号内。

``` Java
public @interface Check {
	String value();
}
```
上面代码中，Check 这个注解只有 value 这个属性。所以可以这样应用。

``` Java
@Check("hi")
int a;
```
这和下面的效果是一样的

``` Java
@Check(value="hi")
int a;
```
最后，还需要注意的一种情况是一个注解没有任何属性。那么在应用这个注解的时候，括号都可以省略。

## 注解的提取
注解通过反射获取。首先可以通过 Class 对象的 isAnnotationPresent() 方法判断它是否应用了某个注解

``` Java
public boolean isAnnotationPresent(Class<? extends Annotation> annotationClass) {}

public <A extends Annotation> A getAnnotation(Class<A> annotationClass) {}

public Annotation[] getAnnotations() {}
```
前一种方法返回指定类型的注解，后一种方法返回注解到这个元素上的所有注解。
如果获取到的 Annotation 如果不为 null，则就可以调用它们的属性方法了。比如

``` Java
@TestAnnotation()
public class Test {
	
	public static void main(String[] args) {
		
		boolean hasAnnotation = Test.class.isAnnotationPresent(TestAnnotation.class);
		
		if ( hasAnnotation ) {
			TestAnnotation testAnnotation = Test.class.getAnnotation(TestAnnotation.class);
			
			System.out.println("id:"+testAnnotation.id());
			System.out.println("msg:"+testAnnotation.msg());
		}
	}
}

结果：
id:-1
msg:
```

上面的例子中，只是检阅出了注解在类上的注解，其实属性、方法上的注解照样是可以的。同样还是要假手于反射。

``` Java
@TestAnnotation(msg="hello")
public class Test {
	
	@Check(value="hi")
	int a;
	
	
	@Perform
	public void testMethod(){}
	
	
	@SuppressWarnings("deprecation")
	public void test1(){
		Hero hero = new Hero();
		hero.say();
		hero.speak();
	}


	public static void main(String[] args) {
		
		boolean hasAnnotation = Test.class.isAnnotationPresent(TestAnnotation.class);
		
		if ( hasAnnotation ) {
			TestAnnotation testAnnotation = Test.class.getAnnotation(TestAnnotation.class);
			//获取类的注解
			System.out.println("id:"+testAnnotation.id());
			System.out.println("msg:"+testAnnotation.msg());
		}
		
		
		try {
			Field a = Test.class.getDeclaredField("a");
			a.setAccessible(true);
			//获取一个成员变量上的注解
			Check check = a.getAnnotation(Check.class);
			
			if ( check != null ) {
				System.out.println("check value:"+check.value());
			}
			
			Method testMethod = Test.class.getDeclaredMethod("testMethod");
			
			if ( testMethod != null ) {
				// 获取方法中的注解
				Annotation[] ans = testMethod.getAnnotations();
				for( int i = 0;i < ans.length;i++) {
					System.out.println("method testMethod annotation:"+ans[i].annotationType().getSimpleName());
				}
			}
		} catch (NoSuchFieldException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println(e.getMessage());
		} catch (SecurityException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println(e.getMessage());
		} catch (NoSuchMethodException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println(e.getMessage());
		}
	}
}

结果：
id:-1
msg:hello
check value:hi
method testMethod annotation:Perform
```
**需要注意的是，如果一个注解要在运行时被成功提取，那么 @Retention(RetentionPolicy.RUNTIME) 是必须的。**