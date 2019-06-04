# Python 静态方法和类方法
## 样板代码
假设我们需要一个类来处理和日期相关的信息：

``` Python
class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year
```

显然,这个类能够存储一些日期相关的信息,通过**init**方法,我们传入day，month和year能够实例化一个Date对象,其中**init**方法的第一个参数self就代表我们新建的Date实例。

## Class Method
通过@classmethod我们可以比较优雅的完成一些任务。如果仅仅通过**init**方法来完成Date类的实例化,就必须这样实现:x = Date(day,month,year)。如果现在想要将一个日期的字符串形式(‘dd-mm-yy’)转为Date对象，我们需要完成这两个步骤：
1. 将字符串转为day,month,year三个整型对象或者一个包含三个值的元组；
2. 通过**init**方法完成Date对象的实例化。
上边的两步实现过程就像这样：

``` Python
day, month, year = map(int, string_date.split('-'))
date1 = Date(day, month, year)
```
在其他编程语言中，以c++为例，它可以重构自己的构造函数来接受某个日期的字符串形式最终返回一个Date实例。但是python没有这样的特性，于是classmethod就在这里派上了用场：

``` Python
@classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1
date2 = Date.from_string('11-09-2012')
```

上边利用classmethod来完成将字符串转为Date实例主要有这些优势：
1. 将字符串转化的过程放在类中，并且能够重用；
2. 封装的较好,符合面向对象思想；
3. classmethod中的cls代表Date，它不是类的一个实例,就是类对象本身，如果我们派生了其他的子类，它们也都能继承from_string方法。

## Static Method
说完了classmethod，接着唠一唠staticmethod。它其实和classmethod十分相似，但是它不需要像类方法或者普通的实例方法一样需要必须的参数(cls或者self)。
再举个例子：
通过classmethod我们完成了将一个字符串转为Date实例的过程，现在给我们一个字符串，在使用Date.from_string(‘str’)生成实例之前，判断这个str是否满足要求。
很显然，这个方法和类Date有密切的联系，但仅仅判断一个字符串是否满足转换的要求，并不需要实例化一个Date对象，这时候staticmethod就可以派上用场：

``` Python
@staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999

# usage:
is_date = Date.is_date_valid('11-09-2012')
```

也就是说，staticmethod可以像一个普通的方法被调用，它与这个类有明确的相关性，但是不需要访问这个类内部的属性或者方法。

## 总结
1. @classmethod，由于其强制要求有cls参数存在，可以更多的用于当作一个类实例工厂，或者可以作为一个可以用于派生类中的构造函数；
2. @staticmethod，如果一个方法不需要使用类内部的属性和方法，但确实和类有明确的相关性，它就可以使用@staticmethod来修饰。