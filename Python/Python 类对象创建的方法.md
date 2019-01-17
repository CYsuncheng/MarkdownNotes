# 类的 init，new，call 方法

## 结论

先来看看结论：
``` Python
class Test(object):

    def __new__(cls, *args, **kwargs):
        print("new")
        return super(Test,cls).__new__(cls,*args,**kwargs)

    def __init__(self, *args, **kwargs):
        print("init")
        super(Test,self).__init__(*args,**kwargs)

    def __call__(self, *args, **kwargs):
        print("call")

obj=Test()
obj()
```
输出：

``` Shell
new
init
call
```

`__new__` 在创建对象时调用，返回当前对象的一个实例。第一个参数是cls即class本身。
`__init__` 在创建完对象后调用，可以进行对象实例的初始化操作，无返回值。第一个参数是self，表示实例对象。
`__call__` 如果类实现了这个方法，则实例是可调用的，相当于重载了括号运算符。

### `__init__` 方法
`__init__` 负责对象的初始化，系统执行该方法前，其实该对象已经存在了，要不然初始化什么东西呢？先看例子：

``` Python
# class A(object): python2 必须显示地继承object
class A:
    def __init__(self):
        print("__init__ ")
        super(A, self).__init__()

    def __new__(cls):
        print("__new__ ")
        return super(A, cls).__new__(cls)

    def __call__(self):  # 可以定义任意参数
        print('__call__ ')

A()

输出：
__new__
__init__
```
从输出结果来看， `__new__`方法先被调用，返回一个实例对象，接着 `__init__` 被调用。 __call__方法并没有被调用，这个我们放到最后说，先来说说前面两个方法，稍微改写成：

``` Python 
def __init__(self):
    print("__init__ ")
    print(self)
    super(A, self).__init__()

def __new__(cls):
    print("__new__ ")
    self = super(A, cls).__new__(cls)
    print(self)
    return self
    
输出：
__new__ 
<__main__.A object at 0x1007a95f8>
__init__ 
<__main__.A object at 0x1007a95f8>
```
从输出结果来看，`__new__` 方法的返回值就是类的实例对象，这个实例对象会传递给 `__init__` 方法中定义的 self 参数，以便实例对象可以被正确地初始化。

如果 `__new__` 方法不返回值（或者说返回 None）那么 `__init__` 将不会得到调用，这个也说得通，因为实例对象都没创建出来，调用 init 也没什么意义，此外，Python 还规定，`__init__` 只能返回 None 值，否则报错。

**`__init__` 方法中除了self之外定义的参数，都将与 `__new__` 方法中除cls参数之外的参数是必须保持一致或者等效。**

### `__new__` 方法

``` Python
class BaseController(object):
    _singleton = None
    def __new__(cls, *a, **k):
        if not cls._singleton:
            cls._singleton = object.__new__(cls, *a, **k)
        return cls._singleton
```
这就是通过 `__new__` 方法是实现单例模式的的一种方式，如果实例对象存在了就直接返回该实例即可，如果还没有，那么就先创建一个实例，再返回。

参考：[Python 中的单例](https://foofish.net/python_singleton.html)

### `__call__` 方法

关于 `__call__` 方法，不得不先提到一个概念，就是可调用对象（callable），我们平时自定义的函数、内置函数和类都属于可调用对象，但凡是可以把一对括号()应用到某个对象身上都可称之为可调用对象，判断对象是否为可调用对象可以用函数 callable

如果在类中实现了 `__call__` 方法，那么实例对象也将成为一个可调用对象，我们回到最开始的那个例子：

`a = A()`
`print(callable(a))  # True`
a是实例对象，同时还是可调用对象，那么我就可以像函数一样调用它。试试：

`a()  # __call__`
实例对象也可以像函数一样作为可调用对象来用，那么，这个特点在什么场景用得上呢？这个要结合类的特性来说，类可以记录数据（属性），而函数不行（闭包某种意义上也可行），利用这种特性可以实现基于类的装饰器，在类里面记录状态，比如，下面这个例子用于记录函数被调用的次数：

``` Python
class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@Counter
def foo():
    pass

for i in range(10):
    foo()

print(foo.count)  # 10
```