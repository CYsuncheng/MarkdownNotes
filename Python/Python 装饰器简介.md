# 装饰器
> 我的理解，就是写一个新的函数A，参数是另一个函数B，可以在B函数的基础上，加一些新的功能，从而让B拥有更多的能力，所以，装饰器装饰函数的时候，将函数作为变量传入装饰器内部，实际调用的是装饰器内部的函数（添加新功能之后的函数）

## 简单的释例

``` Python
#自定义装饰函数
def decorator(fn):
    def wrapper(*args):
        #这里装饰器的作用是在函数调用前增加一句话表示装饰成功
        print("this is decorator fo %s" % fn.__name__)
        fn(*args)
    return wrapper
    
def hello(name):
    print('hello,%s' %name)
    
    
if __name__=="__main__":
    #用赋值的形式进行装饰器
    hello=decorator(hello)
    hello("cool")
```

输出的结果：

``` Shell
this is decorator fo hello
hello,cool
```

一个函数可以返回另一个函数，`hello=decorator(hello)`这一句代码中，将hello函数作为变量传入decorator装饰器中，然后hello方法在decorator中的函数wrapper函数实现，同时包装新的功能，将新的函数wrapper作为变量返回 ，所以hello的新值是经过decorator装饰的wrapper新方法。

## 语法糖
Python 中装饰器语法并不用每次都用赋值语句。
在函数定义的时候就加上@+装饰器名字即可
再来我们刚才的例子吧：

``` Python
def decorator(fn):
    def wrapper(*args):
        print("this is decorator fo %s" % fn.__name__)
        fn(*args)
    return wrapper
    
@decorator
def hello(name):
    print('hello,%s' %name)
    
    
if __name__=="__main__":
    hello("cool")
```

### 多个装饰器

``` Python
@decorator_one
@decorator_two
def hello()
    pass
```
这句代码实际上类似于：

``` Python
hello=decorator_one(decorator_two(hello))
```

### 带参数的装饰器
例如：我们手写html的时候需要各种补全，但是，如果是在python中用字符串去表示html标签的时候，麻烦了，总不能每个标签我都写一个方法吧，最方便的方法，写一个带参数的装饰器！

``` Python
def makeHtmlTag(tag, *args, **kwargs):
    def real_decorator(fn):
        css_class = " class='{0}'".format(kwargs["css_class"]) \
                                     if "css_class" in kwargs else ""
        def wrapped(*args, **kwargs):
            return "<"+tag+css_class+">" + fn(*args, **kwargs) + "</"+tag+">"
        return wrapped
    return real_decorator

@makeHtmlTag(tag="b", css_class="bold_css")
@makeHtmlTag(tag="i", css_class="italic_css")
def hello():
    return "hello world"

print(hello())
print(hello())
```
结果：

``` HTML
<b class='bold_css'><i class='italic_css'>hello world</i></b>
<b class='bold_css'><i class='italic_css'>hello world</i></b>
```

### 用类的方式实现装饰器

``` Python
class makeHtmlTagClass(object):
 
    def __init__(self, tag, css_class=""):
        self._tag = tag
        self._css_class = " class='{0}'".format(css_class) \
                                       if css_class !="" else ""
 
    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            return "<" + self._tag + self._css_class+">"  \
                       + fn(*args, **kwargs) + "</" + self._tag + ">"
        return wrapped
 
@makeHtmlTagClass(tag="b", css_class="bold_css")
@makeHtmlTagClass(tag="i", css_class="italic_css")
def hello(name):
    return "Hello, {}".format(name)
 
print hello("Hao Chen")
```