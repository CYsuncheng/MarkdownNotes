# python with as 用法

> 这个语法是用来代替传统的 `try...finally` 语法的。 

基本思想是 with 所求值的对象必须有一个`__enter__()`方法，一个`__exit__()`方法。

紧跟 with 后面的语句被求值后，返回对象的`__enter__()`方法被调用，这个方法的返回值将被赋值给 as 后面的变量。当 with 后面的代码块全部被执行完之后，将调用前面返回对象的`__exit__()`方法。

例如多线程的类 class ProcessPoolExecutor(_base.Executor) 继承自 Executor，查看源码：

``` python
class Executor(object):

    def submit(self, fn, *args, **kwargs):
        忽略

    def map(self, fn, *iterables, **kwargs):
        忽略

    def shutdown(self, wait=True):
        忽略

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False
```

其他方法的源码忽略了，可以看到，最后实现了 `__enter__()` and `__exit__()` 这两个方法。

在看一个例子，平时我们经常需要写入文件：
常用的写法：

``` python
file = open("/tmp/foo.txt")
try:
    data = file.read()
finally:
    file.close()
```

使用 with 方式：

``` python
with open("/tmp/foo.txt") as file:
    data = file.read()
```

大家可以看一下 file 类的源码，看看是不是也实现了 `__enter__()` and `__exit__()` 这两个方法。

接下来，我们可以自己写个类，实现 `__enter__()` and `__exit__()` 这两个方法。

``` python
class Sample:
    def __enter__(self):
        print "run __enter__()"
        return self

    def __exit__(self, type, value, trace):
        print "run __exit__()"

    def method(self):
        print "run only method"

if __name__ == '__main__':
    with Sample() as sample:
        sample.method()
```

结果：

``` shell
run __enter__()
run only method
run __exit__()
```

从结果也可以看出方法调用的结论了：
1. with 开始，enter()方法被执行
2. enter()方法返回的值 - self，返回了实例本身
3. 执行 method() 方法
4. exit()方法被调用

另外，`__exit__()` 方法还有个很强大的功能，就是可以处理异常，exit 方法有三个参数 val, type 和 trace。如果 with 语句执行政策，则三个参数都是 None。

我们可以把上面的例子修改一下：

``` python
class Sample:
    def __enter__(self):
        print "run __enter__()"
        return self

    def __exit__(self, type, value, trace):
        print "type:", type
        print "value:", value
        print "trace:", trace
        print "run __exit__()"

    def method(self):
        print "run only method"
        bar = 1 / 0
        return bar + 10

if __name__ == '__main__':
    with Sample() as sample:
        sample.method()
```

结果：

``` shell
run __enter__()
Traceback (most recent call last):
run only method
  File "/Users/suncheng/WorkSpace/sever-test/multi.py", line 155, in <module>
type: <type 'exceptions.ZeroDivisionError'>
    sample.method()
value: integer division or modulo by zero
trace: <traceback object at 0x105c7e0e0>
  File "/Users/suncheng/WorkSpace/sever-test/multi.py", line 150, in method
run __exit__()
    bar = 1 / 0
ZeroDivisionError: integer division or modulo by zero
```

可以看到，估计制造一个错误，现在这三个参数就不是 None 了。