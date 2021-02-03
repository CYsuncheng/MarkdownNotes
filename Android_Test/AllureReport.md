# 记录一下，折腾 Allure Report 的过程

## 写这篇文章的目的
- 由于项目中有需要，所以在寻找一个方便展示的 report 框架
- 在网上看了好久，决定使用 Allure
- 但是搜索了一下，发现好多的文章的介绍都不是特别的完善，照着试了一下，遇到了一些问题
- 可能因为，好多的配置都是按照 1.x 的版本来的
- 后来经过自己的实验，ok 了，所以想着记录一下，方便日后。

## Allure Report 简介
> Allure 是一个轻量级的，灵活的，支持多语言，多平台的report框架。
可以方便的集成到各种框架中，例如，TestNG，Junit等。[GitHub 地址](https://github.com/allure-framework/)

## 报告展示
**OverView**
![OverView](https://ws4.sinaimg.cn/large/006tNc79ly1fl5yxuemd1j31kw15q490.jpg)
**Graphs**
![Graphs](https://ws3.sinaimg.cn/large/006tNc79ly1fl5z0e8tvcj31kw15qwn5.jpg)

## 如何集成
**我的项目是 Maven + TestNG 的，以下都是以这个为例子**

### Pom 文件

``` xml
<dependencies>
        <dependency>
            <groupId>io.qameta.allure</groupId>
            <artifactId>allure-testng</artifactId>
            <version>2.0-BETA19</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <artifactId>maven-compiler-plugin</artifactId>
                <configuration>
                    <source>1.8</source>
                    <target>1.8</target>
                    <encoding>UTF-8</encoding>
                </configuration>
                <version>3.5.1</version>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>2.20.1</version>
                <configuration>
                    <testFailureIgnore>true</testFailureIgnore>
                    <argLine>
                        -javaagent:"${settings.localRepository}/org/aspectj/aspectjweaver/${aspectj.version}/aspectjweaver-${aspectj.version}.jar"
                    </argLine>
                </configuration>
                <dependencies>
                    <dependency>
                        <groupId>org.aspectj</groupId>
                        <artifactId>aspectjweaver</artifactId>
                        <version>${aspectj.version}</version>
                    </dependency>
                </dependencies>
            </plugin>
        </plugins>
    </build>

    <properties>
        <aspectj.version>1.8.9</aspectj.version>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
    </properties>

    <reporting>
        <excludeDefaults>true</excludeDefaults>
        <plugins>
            <plugin>
                <groupId>io.qameta.allure</groupId>
                <artifactId>allure-maven</artifactId>
                <version>2.8</version>
            </plugin>
        </plugins>
    </reporting>
```

### 修改 Listener（可以实现失败的 case 自动截图并在报告中展示）

``` java
public class AllureReporterListener extends BaseTest implements IHookable {

    @Override
    public void run(IHookCallBack callBack, ITestResult testResult) {
        callBack.runTestMethod(testResult);
        if (testResult.getThrowable() != null) {
            try {
                takeScreenShot(testResult.getMethod().getMethodName());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @Attachment(value = "Failure in method {0}", type = "image/png")
    private byte[] takeScreenShot(String methodName) throws IOException {
        File screenshot = ((TakesScreenshot) getDriver()).getScreenshotAs(OutputType.FILE);
        return Files.toByteArray(screenshot);
    }
```

## 后续计划
目前只是继承了而已，看官方的介绍，allure 还提供了很多的 API 来实现更多的可以展示在报告中的东西，希望后续可以继续。。。

