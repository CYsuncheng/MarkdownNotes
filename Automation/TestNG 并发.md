# TestNG 并发

## 不同级别的并发
通常，在TestNG的执行中，测试的级别由上至下可以分为 **suite -> test -> class -> method**，箭头的左边元素跟右边元素的关系是一对多的包含关系。

**这里的 test 指的是 testng.xml 中的 test tag**，而不是测试类里的一个 `@Test`。测试类里的一个 `@Test` 实际上对应这里的method。所以我们在使用 `@BeforeSuite、@BeforeTest、@BeforeClass、@BeforeMethod` 这些标签的时候，它们的实际执行顺序也是按照这个级别来的。

### suite
一般情况下，一个testng.xml只包含一个suite。如果想起多个线程执行不同的suite，官方给出的方法是：通过命令行的方式来指定线程池的容量。
`java org.testng.TestNG -suitethreadpoolsize 3 testng1.xml testng2.xml testng3.xml`、
即可通过三个线程来分别执行testng1.xml、testng2.xml、testng3.xml。

### test，class，method
test，class，method级别的并发，可以通过在testng.xml中的suite tag下设置，如：
``` xml
<suite name="Testng Parallel Test" parallel="tests" thread-count="5">
<suite name="Testng Parallel Test" parallel="classes" thread-count="5">
<suite name="Testng Parallel Test" parallel="methods" thread-count="5">
```

它们的共同点都是最多起5个线程去同时执行不同的用例。
它们的区别如下：
* tests级别：不同test tag下的用例可以在不同的线程执行，相同test tag下的用例只能在同一个线程中执行。
* classs级别：不同class tag下的用例可以在不同的线程执行，相同class tag下的用例只能在同一个线程中执行。
* methods级别：所有用例都可以在不同的线程去执行。

搞清楚并发的级别非常重要，可以帮我们合理地组织用例，比如将非线程安全的测试类或group统一放到一个test中，这样在并发的同时又可以保证这些类里的用例是单线程执行。也可以根据需要设定class级别的并发，让同一个测试类里的用例在同一个线程中执行。

### 并发时的依赖
实践中，很多时候我们在测试类中通过dependOnMethods/dependOnGroups方式，给很多测试方法的执行添加了依赖，以达到期望的执行顺序。如果同时在运行testng时配置了methods级别并发执行，那么这些测试方法在不同线程中执行，还会遵循依赖的执行顺序吗？答案是——YES。牛逼的TestNG就是能在多线程情况下依然遵循既定的用例执行顺序去执行。

### 不同dataprovider的并发
在使用TestNG做自动化测试时，基本上大家都会使用dataprovider来管理一个用例的不同测试数据。而上述在testng.xml中修改suite标签的方法，并不适用于dataprovider多组测试数据之间的并发。执行时会发现，一个dp中的多组数据依然是顺序执行。

解决方式是：在**@DataProvider**中添加parallel=true。
如：
``` Java
import org.testng.annotations.DataProvider;
import testdata.ScenarioTestData;

public class ScenarioDataProvider {
    @DataProvider(name = "hadoopTest", parallel=true)
    public static Object [][] hadoopTest(){
        return new Object[][]{
            ScenarioTestData.hadoopMain,
            ScenarioTestData.hadoopRun,
            ScenarioTestData.hadoopDeliverProps
        };
    }

    @DataProvider(name = "sparkTest", parallel=true)
    public static Object [][] sparkTest(){
        return new Object[][]{
            ScenarioTestData.spark_java_version_default,
            ScenarioTestData.spark_java_version_162,
            ScenarioTestData.spark_java_version_200,
            ScenarioTestData.spark_python
        };
    }

    @DataProvider(name = "sqoopTest", parallel=true)
    public static Object [][] sqoopTest(){
        return new Object[][]{
            ScenarioTestData.sqoop_mysql2hive,
            ScenarioTestData.sqoop_mysql2hdfs
        };
    }
}
```

默认情况下，dp并行执行的线程池容量为10，如果要更改并发的数量，也可以在suite tag下指定参数 data-provider-thread-count：
`<suite name="Testng Parallel Test" parallel="methods" thread-count="5" data-provider-thread-count="20" >`

## 同一个方法的并发
有些时候，我们需要对一个测试用例，比如一个http接口，执行并发测试，即一个接口的反复调用。TestNG中也提供了优雅的支持方式，在@Test标签中指定threadPoolSize和invocationCount。
``` Java
@Test(enabled=true, dataProvider="testdp", threadPoolSize=5, invocationCount=10)
```
其中threadPoolSize表明用于调用该方法的线程池容量，该例就是同时起5个线程并行执行该方法；invocationCount表示该方法总计需要被执行的次数。该例子中5个线程同时执行，当总计执行次数达到10次时，停止。

**注意**，该线程池与dp的并发线程池是两个独立的线程池。这里的线程池是用于起多个method，而每个method的测试数据由dp提供，如果这边dp里有3组数据，那么实际上10次执行，每次都会调3次接口，这个接口被调用的总次数是10*3=30次。threadPoolSize指定的5个线程中，每个线程单独去调method时，用到的dp如果也是支持并发执行的话，会创建一个新的线程池（dpThreadPool）来并发执行测试数据。

示例代码：
``` Java
package testng.parallel.test;

import java.text.SimpleDateFormat;
import java.util.Date;

import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.DataProvider;
import org.testng.annotations.Test;

public class TestClass1 {
    private SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");//设置日期格式

    @BeforeClass
    public void beforeClass(){
        System.out.println("Start Time: " + df.format(new Date()));
    }

    @Test(enabled=true, dataProvider="testdp", threadPoolSize=2, invocationCount=5)
    public void test(String dpNumber) throws InterruptedException{
        System.out.println("Current Thread Id: " + Thread.currentThread().getId() + ". Dataprovider number: "+ dpNumber);
        Thread.sleep(5000);
    }

    @DataProvider(name = "testdp", parallel = true)
    public static Object[][]testdp(){
        return new Object[][]{
            {"1"},
            {"2"}
        };
    }

    @AfterClass
    public void afterClass(){
        System.out.println("End Time: " + df.format(new Date()));
    }
}
```

测试结果：
``` Java
Start Time: 2017-03-11 14:10:43
[ThreadUtil] Starting executor timeOut:0ms workers:5 threadPoolSize:2
Current Thread Id: 14. Dataprovider number: 2
Current Thread Id: 15. Dataprovider number: 2
Current Thread Id: 12. Dataprovider number: 1
Current Thread Id: 13. Dataprovider number: 1
Current Thread Id: 16. Dataprovider number: 1
Current Thread Id: 18. Dataprovider number: 1
Current Thread Id: 17. Dataprovider number: 2
Current Thread Id: 19. Dataprovider number: 2
Current Thread Id: 21. Dataprovider number: 2
Current Thread Id: 20. Dataprovider number: 1
End Time: 2017-03-11 14:10:58
```

## Other Tips
1. groups/dependsOnGroups/dependsOnMethods ——设置用例间依赖
2. dataProviderClass ——将dataprovider单独放到一个专用的类中，实现测试代码、dataprovider、测试数据分层。
3. timeout ——设置用例的超时时间（并发／非并发都可支持）
4. alwaysRun ——某些依赖的用例失败了，导致用例被跳过。对于一些为了保持环境干净而“扫尾”的测试类，如果我们想强制执行可以使用此标签。
5. priority ——设置优先级，让某些测试用例被更大概率优先执行。
6. singleThreaded ——强制一个class类里的用例在一个线程执行，忽视method级别并发
7. preserve-order ——指定是否按照testng.xml中的既定用例顺序执行用例