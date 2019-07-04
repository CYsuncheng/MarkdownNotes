# Python Unittest

## unittest核心工作原理
unittest中最核心的四个概念是：**test case, test suite, test runner, test fixture**。
![unittest](https://ws1.sinaimg.cn/large/006tNc79ly1g24ng07zonj30kj0hcjrw.jpg)

1. 一个TestCase的实例就是一个测试用例。什么是测试用例呢？就是一个完整的测试流程，包括测试前准备环境的搭建(setUp)，执行测试代码(run)，以及测试后环境的还原(tearDown)。
2. 元测试(unit test)的本质也就在这里，一个测试用例是一个完整的测试单元，通过运行这个测试单元，可以对某一个问题进行验证。
3. 而多个测试用例集合在一起，就是TestSuite，而且TestSuite也可以嵌套TestSuite。
4. TestLoader是用来加载TestCase到TestSuite中的，其中有几个loadTestsFrom()方法，就是从各个地方寻找TestCase，创建它们的实例，然后add到TestSuite中，再返回一个TestSuite实例。
5. TextTestRunner是来执行测试用例的，其中的run(test)会执行TestSuite/TestCase中的run(result)方法。 
6. 测试的结果会保存到TextTestResult实例中，包括运行了多少测试用例，成功了多少，失败了多少等信息。
7. 而对一个测试用例环境的搭建和销毁，是一个fixture。

一个class继承了unittest.TestCase，便是一个测试用例，但如果其中有多个以 test 开头的方法，那么每有一个这样的方法，在load的时候便会生成一个TestCase实例，如：一个class中有四个test_xxx方法，最后在load到suite中时也有四个测试用例。

到这里整个流程就清楚了：
写好TestCase，然后由TestLoader加载TestCase到TestSuite，然后由TextTestRunner来运行TestSuite，运行的结果保存在TextTestResult中，我们通过命令行或者unittest.main()执行时，main会调用TextTestRunner中的run来执行，或者我们可以直接通过TextTestRunner来执行用例。这里加个说明，在Runner执行时，默认将执行结果输出到控制台，我们可以设置其输出到文件，在文件中查看结果（你可能听说过HTMLTestRunner，是的，通过它可以将结果输出到HTML中，生成漂亮的报告，它跟TextTestRunner是一样的，从名字就能看出来，这个我们后面再说）。

## 跳过某个case
### skip装饰器

``` Python
class TestMathFunc(unittest.TestCase): 
	@unittest.skip("I don't want to run this case.") 
	def test_divide(self): 
		"""Test method divide(a, b)""" 
		self.assertEqual(2, divide(6, 3)) 
		self.assertEqual(2.5, divide(5, 2))
```

skip装饰器一共有三个 unittest.skip(reason)、unittest.skipIf(condition, reason)、unittest.skipUnless(condition, reason)，skip无条件跳过，skipIf当condition为True时跳过，skipUnless当condition为False时跳过。

### TestCase.skipTest()方法

``` Python
class TestMathFunc(unittest.TestCase): 
	def test_divide(self):
		self.skipTest('Do not run this.') 
		self.assertEqual(2, divide(6, 3)) 
		self.assertEqual(2.5, divide(5, 2))
```

效果跟上面的装饰器一样，跳过了divide方法。

## 总结一下：
1. Unittest是Python自带的单元测试框架，我们可以用其来作为我们自动化测试框架的用例组织执行框架。
2. unittest的流程：写好TestCase，然后由TestLoader加载TestCase到TestSuite，然后由TextTestRunner来运行TestSuite，运行的结果保存在TextTestResult中，我们通过命令行或者unittest.main()执行时，main会调用TextTestRunner中的run来执行，或者我们可以直接通过TextTestRunner来执行用例。
3. 一个class继承unittest.TestCase即是一个TestCase，其中以 test 开头的方法在load时被加载为一个真正的TestCase。
4. Verbosity参数可以控制执行结果的输出，0 是简单报告、1 是一般报告、2 是详细报告。
5. 可以通过addTest和addTests向suite中添加case或suite，可以用TestLoader的loadTestsFrom()方法。
6. 用 setUp()、tearDown()、setUpClass()以及 tearDownClass()可以在用例执行前布置环境，以及在用例执行后清理环境
7. 我们可以通过skip，skipIf，skipUnless装饰器跳过某个case，或者用TestCase.skipTest方法。
8. 参数中加stream，可以将报告输出到文件：可以用TextTestRunner输出txt报告，以及可以用HTMLTestRunner输出html报告。