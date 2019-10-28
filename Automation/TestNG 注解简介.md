# TestNG 注解简介

## Before&After
**BeforeSuite**
该方法会运行在该测试集所有其他测试前面
**AfterSuite**
该方法会运行在测试集里所有其他测试后面
**BeforeTest**
该方法会运行在本类内部test标注的方法前面
**AfterTest**
该方法会运行在本类内部test标注的方法后面
**BeforeGroups**
该方法会运行在测试组之前。这个方法会在这个组里的第一个方法被调用之前执行
**AfterGroups**
该方法会运行在测试组之后。这个方法会在这个组里的最后一个方法被调用之后执行
**BeforeClass**
该方法会当前类的第一个测试之前执行
**AfterClass**
该方法会在当前类的所有测试执行完之后执行
**BeforeMethod**
该方法在每一个测试方法执行之前都会调用
**AfterMethod**
该方法在每一个测试方法执行之后都会调用

**before test 中的 test 代表的是xml配置文件中的 test tag，可以配置多个test tag**
``` Java
----before suite---- 
----before test---- 
----before class---- 
----before method---- 
----in test1---- 
----after method---- 
----before method---- 
----in test2---- 
----after method---- 
----after class---- 
----after test---- 
----after suite---- 
```

## @Test 注解
* alwaysRun : 如果=true,表示即使该测试方法所依赖的前置测试有失败的情况，也要执行
* dataProvider : 选定传入参数的构造器。(@DataProvider注解将在后面章节介绍)
* dataProviderClass : 确定参数构造器的Class类。(参数构造器首先会在当前测试类里面查找，如果参数构造器不在当前测试类定义，那么必须使用该属性来执行它所在的Class类)
* dependsOnGroups : 确定依赖的前置测试组别。
* dependsOnMethods : 确定依赖的前置测试方法。
* description ： 测试方法描述信息。(建议为每个测试方法添加有意义的描述信息，这将会在最后的报告中展示出来)
* enabled : 默认为true，如果指定为false，表示不执行该测试方法。
* expectedExceptions ： 指定期待测试方法抛出的异常，多个异常以逗号(,)隔开。
* groups : 指定该测试方法所属的组，可以指定多个组，以逗号隔开。组测试的用法将在后面文章单独介绍。
* invocationCount ： 指定测试方法需要被调用的次数。
* invocationTimeOut： 每一次调用的超时时间，如果invocationCount没有指定，该参数会被忽略。应用场景可以为测试获取数据库连接，超时就认定为失败。单位是毫秒。
* priority ： 指定测试方法的优先级，数值越低，优先级越高，将会优先与其他数值高的测试方法被调用。(注意是针对一个测试类的优先级)
* timeout : 指定整个测试方法的超时时间。单位是毫秒。

## @Parameters 注解
@Parameters 注解用于为测试方法传递参数， 用法如下所示:
``` Java
package com.crazypig.testngdemo;

import org.testng.annotations.Parameters;
import org.testng.annotations.Test;

public class AnnotationParametersTest {
    @Parameters(value = {"param1", "param2"})
    @Test
    public void test(String arg1, String arg2) {
        System.out.println("use @Parameters to fill method arguments : arg 1 = " + arg1 + ", arg2 = " + arg2);
    }
}
```

testng.xml 配置
``` xml
<test name="testAnnotationParameters">
    <parameter name="param1" value="value1"></parameter>
    <parameter name="param2" value="value2"></parameter>
    <classes>
        <class name="com.crazypig.testngdemo.AnnotationParametersTest" />
    </classes>
</test>
```

## @DataProvider 注解
上面的小结提到@Parameters注解可以为测试方法传递参数，但是这种方式参数值需要配置在testng.xml里面，灵活性不高。而@DataProvider注解同样可以为测试方法传递参数值，并且，它是真正意义上的参数构造器，可以传入多组测试数据对测试方法进行测试。被@DataProvider注解的方法，方法返回值必须为Object[][]或者Iterator<Object[]>。例子如下所示:
``` Java
package com.crazypig.testngdemo;

import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class AnnotationDataProviderTest {
    @DataProvider(name="testMethodDataProvider")
    public Object[][] testMethodDataProvider() {
        return new Object[][]{
                {"value1-1", "value2-1"}, 
                {"value1-2", "value2-2"}, 
                {"value1-3", "value2-3"}
                };
    @Test(dataProvider="testMethodDataProvider")
    public void test(String arg1, String arg2) {
        System.out.println("use @DataProvider to fill method argument : arg1 = " + arg1 + " , arg2 = " + arg2);
    }
}
```

## @Listeners 注解
一般我们写测试类不会涉及到这种类型的注解，这个注解必须定义在类、接口或者枚举类级别。实用的Listener包括ISuiteListener、ITestListener和IInvokedMethodListener，他们可以在suite级别、test级别和test method一些执行点执行一些自定义操作，可以扩展。

## @Factory 注解
在一个方法上面打上@Factory注解，表示该方法将返回能够被TestNG测试的测试类。利用了设计模式中的工厂模式。例子如下所示:
``` Java
package com.crazypig.testngdemo;

import org.testng.annotations.Factory;

public class AnnotationFactoryTest {
    @Factory
    public Object[] getSimpleTest() {
        return new Object[]{ new SimpleTest("one"), new SimpleTest("two")};
    }
}

package com.crazypig.testngdemo;

import org.testng.annotations.Test;

public class SimpleTest {
    private String param;
    public SimpleTest(String param) {
        this.param = param;
    }

    @Test
    public void test() {
        System.out.println("SimpleTest.param = " + param);
    }
}
```
