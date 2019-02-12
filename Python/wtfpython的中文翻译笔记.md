# wtfpython的中文翻译笔记

## 微妙的字符串

``` Python
# 例1
>>> a = "some_string"
>>> id(a)
140420665652016
>>> id("some" + "_" + "string") # 注意两个的id值是相同的.
140420665652016

# 例2
>>> a = "wtf"
>>> b = "wtf"
>>> a is b
True

>>> a = "wtf!"
>>> b = "wtf!"
>>> a is b
False

>>> a, b = "wtf!", "wtf!"
>>> a is b
True

# 例3
>>> 'a' * 20 is 'aaaaaaaaaaaaaaaaaaaa'
True
>>> 'a' * 21 is 'aaaaaaaaaaaaaaaaaaaaa'
False
```

### 说明
- 这些行为是由于 Cpython 在编译优化时, 某些情况下会尝试使用已经存在的不可变对象而不是每次都创建一个新对象. (这种行为被称作字符串的驻留[string interning])
- 发生驻留之后, 许多变量可能指向内存中的相同字符串对象. (从而节省内存)
- 在上面的代码中, 字符串是隐式驻留的. 何时发生隐式驻留则取决于具体的实现. 这里有一些方法可以用来猜测字符串是否会被驻留:
  - 所有长度为 0 和长度为 1 的字符串都被驻留.
  - 字符串在编译时被实现 (`'wtf'` 将被驻留, 但是 `''.join(['w', 't', 'f']` 将不会被驻留)
  - 字符串中只包含字母，数字或下划线时将会驻留. 所以 `'wtf!'` 由于包含 `!` 而未被驻留.
- 当在同一行将 `a` 和 `b` 的值设置为 `"wtf!"` 的时候, Python 解释器会创建一个新对象, 然后同时引用第二个变量. 如果你在不同的行上进行赋值操作, 它就不会“知道”已经有一个 `wtf！` 对象 (因为 `"wtf!"` 不是按照上面提到的方式被隐式驻留的). 它是一种编译器优化, 特别适用于交互式环境.
- 常量折叠(constant folding) 是 Python 中的一种 [窥孔优化(peephole optimization)](https://en.wikipedia.org/wiki/Peephole_optimization) 技术. 这意味着在编译时表达式 `'a'*20` 会被替换为 `'aaaaaaaaaaaaaaaaaaaa'` 以减少运行时的时钟周期. 只有长度小于 20 的字符串才会发生常量折叠.

## Time for some hash brownies!/是时候来点蛋糕了
* hash brownie指一种含有大麻成分的蛋糕, 所以这里是句双关

1\.
``` Python
some_dict = {}
some_dict[5.5] = "Ruby"
some_dict[5.0] = "JavaScript"
some_dict[5] = "Python"
```

**Output:**
``` Python
>>> some_dict[5.5]
"Ruby"
>>> some_dict[5.0]
"Python"
>>> some_dict[5]
"Python"
```

"Python" 消除了 "JavaScript" 的存在?

### 说明:

* Python 字典通过检查键值是否相等和比较哈希值来确定两个键是否相同.
* 具有相同值的不可变对象在Python中始终具有相同的哈希值.
  ``` Python
  >>> 5 == 5.0
  True
  >>> hash(5) == hash(5.0)
  True
  ```
  **注意:** 具有不同值的对象也可能具有相同的哈希值（哈希冲突）.
* 当执行 `some_dict[5] = "Python"` 语句时, 因为Python将 `5` 和 `5.0` 识别为 `some_dict` 的同一个键, 所以已有值 "JavaScript" 就被 "Python" 覆盖了.
* 这个 StackOverflow的 [回答](https://stackoverflow.com/a/32211042/4354153) 漂亮的解释了这背后的基本原理.

## Return return everywhere!/到处返回

``` Python
def some_func():
    try:
        return 'from_try'
    finally:
        return 'from_finally'
```

**Output:**
``` Python
>>> some_func()
'from_finally'
```

### 说明:

- 当在 "try...finally" 语句的 `try` 中执行 `return`, `break` 或 `continue` 后, `finally` 子句依然会执行.
- 函数的返回值由最后执行的 `return` 语句决定. 由于 `finally` 子句一定会执行, 所以 `finally` 子句中的 `return` 将始终是最后执行的语句.

## For what?/为什么?

``` Python
some_string = "wtf"
some_dict = {}
for i, some_dict[i] in enumerate(some_string):
    pass
```

**Output:**
``` Python
>>> some_dict # 创建了索引字典.
{0: 'w', 1: 't', 2: 'f'}
```

### 说明:
* [Python 语法](https://docs.python.org/3/reference/grammar.html) 中对 `for` 的定义是:
  ``` Python
  for_stmt: 'for' exprlist 'in' testlist ':' suite ['else' ':' suite]
  ```
  其中 `exprlist` 指分配目标. 这意味着对可迭代对象中的**每一项都会执行**类似 `{exprlist} = {next_value}` 的操作.

  一个有趣的例子说明了这一点:
  ``` Python
  for i in range(4):
      print(i)
      i = 10
  ```

  **Output:**
  ```
  0
  1
  2
  3
  ```

  你可曾觉得这个循环只会运行一次?

  **说明:**
  - 由于循环在Python中工作方式, 赋值语句 `i = 10` 并不会影响迭代循环, 在每次迭代开始之前, 迭代器(这里指 `range(4)`) 生成的下一个元素就被解包并赋值给目标列表的变量(这里指 `i`)了.

* 在每一次的迭代中, `enumerate(some_string)` 函数就生成一个新值 `i` (计数器增加) 并从 `some_string` 中获取一个字符. 然后将字典 `some_dict` 键 `i` (刚刚分配的) 的值设为该字符. 本例中循环的展开可以简化为:
  ``` Python
  >>> i, some_dict[i] = (0, 'w')
  >>> i, some_dict[i] = (1, 't')
  >>> i, some_dict[i] = (2, 'f')
  >>> some_dict
  ```

## `is` is not what it is!/出人意料的`is`!

下面是一个在互联网上非常有名的例子.

``` Python
>>> a = 256
>>> b = 256
>>> a is b
True

>>> a = 257
>>> b = 257
>>> a is b
False

>>> a = 257; b = 257
>>> a is b
True
```

### 说明:

**`is` 和 `==` 的区别**

* `is` 运算符检查两个运算对象是否引用自同一对象 (即, 它检查两个预算对象是否相同).
* `==` 运算符比较两个运算对象的值是否相等.
* 因此 `is` 代表引用相同, `==` 代表值相等. 下面的例子可以很好的说明这点
  ``` Python
  >>> [] == []
  True
  >>> [] is [] # 这两个空列表位于不同的内存地址.
  False
  ```

**`256` 是一个已经存在的对象, 而 `257` 不是**

当你启动Python 的时候, `-5` 到 `256` 的数值就已经被分配好了. 这些数字因为经常使用所以适合被提前准备好.

引用自 https://docs.python.org/3/c-api/long.html
> 当前的实现为-5到256之间的所有整数保留一个整数对象数组, 当你创建了一个该范围内的整数时, 你只需要返回现有对象的引用. 所以改变1的值是有可能的. 我怀疑这种行为在Python中是未定义行为. :-)

``` Python
>>> id(256)
10922528
>>> a = 256
>>> b = 256
>>> id(a)
10922528
>>> id(b)
10922528
>>> id(257)
140084850247312
>>> x = 257
>>> y = 257
>>> id(x)
140084850247440
>>> id(y)
140084850247344
```

这里解释器并没有智能到能在执行 `y = 257` 时意识到我们已经创建了一个整数 `257`, 所以它在内存中又新建了另一个对象.

**当 `a` 和 `b` 在同一行中使用相同的值初始化时，会指向同一个对象.**

``` Python
>>> a, b = 257, 257
>>> id(a)
140640774013296
>>> id(b)
140640774013296
>>> a = 257
>>> b = 257
>>> id(a)
140640774013392
>>> id(b)
140640774013488
```

* 当 a 和 b 在同一行中被设置为 `257` 时, Python 解释器会创建一个新对象, 然后同时引用第二个变量. 如果你在不同的行上进行, 它就不会 "知道" 已经存在一个 `257` 对象了.
* 这是一种特别为交互式环境做的编译器优化. 当你在实时解释器中输入两行的时候, 他们会单独编译, 因此也会单独进行优化. 如果你在 `.py` 文件中尝试这个例子, 则不会看到相同的行为, 因为文件是一次性编译的.

**运算符的优先级会影响表达式的求值顺序, 而在 Python 中 `==` 运算符的优先级要高于 `not` 运算符.**

## Half triple-quoted strings/三个引号

**Output:**
``` Python
>>> print('wtfpython''')
wtfpython
>>> print("wtfpython""")
wtfpython
>>> # 下面的语句会抛出 `SyntaxError` 异常
>>> # print('''wtfpython')
>>> # print("""wtfpython")
```

### 说明:
+ Python 提供隐式的[字符串链接](https://docs.python.org/2/reference/lexical_analysis.html#string-literal-concatenation)

  ``` Python
  >>> print("wtf" "python")
  wtfpython
  >>> print("wtf" "") # or "wtf"""
  wtf
  ```
+ `'''` 和 `"""` 在 Python中也是字符串定界符, Python 解释器在先遇到三个引号的的时候会尝试再寻找三个终止引号作为定界符, 如果不存在则会导致 `SyntaxError` 异常.

## What's wrong with booleans?/布尔你咋了?

1\.
``` Python
# 一个简单的例子, 统计下面可迭代对象中的布尔型值的个数和整型值的个数
mixed_list = [False, 1.0, "some_string", 3, True, [], False]
integers_found_so_far = 0
booleans_found_so_far = 0

for item in mixed_list:
    if isinstance(item, int):
        integers_found_so_far += 1
    elif isinstance(item, bool):
        booleans_found_so_far += 1
```

**Output:**
``` Python
>>> integers_found_so_far
4
>>> booleans_found_so_far
0
```

2\.
``` Python
another_dict = {}
another_dict[True] = "JavaScript"
another_dict[1] = "Ruby"
another_dict[1.0] = "Python"
```

**Output:**
``` Python
>>> another_dict[True]
"Python"
```

3\.
``` Python
>>> some_bool = True
>>> "wtf"*some_bool
'wtf'
>>> some_bool = False
>>> "wtf"*some_bool
''
```

### 说明:

* 布尔值是 `int` 的子类
  ``` Python
  >>> isinstance(True, int)
  True
  >>> isinstance(False, int)
  True
  ```

* 所以 `True` 的整数值是 `1`, 而 `False` 的整数值是 `0`.
  ``` Python
  >>> True == 1 == 1.0 and False == 0 == 0.0
  True
  ```
* 关于其背后的原理, 请看这个 StackOverflow 的[回答](https://stackoverflow.com/a/8169049/4354153).

## Class attributes and instance attributes/类属性和实例属性

1\.
``` Python
class A:
    x = 1

class B(A):
    pass

class C(A):
    pass
```

**Output:**
``` Python
>>> A.x, B.x, C.x
(1, 1, 1)
>>> B.x = 2
>>> A.x, B.x, C.x
(1, 2, 1)
>>> A.x = 3
>>> A.x, B.x, C.x
(3, 2, 3)
>>> a = A()
>>> a.x, A.x
(3, 3)
>>> a.x += 1
>>> a.x, A.x
(4, 3)
```

2\.
``` Python
class SomeClass:
    some_var = 15
    some_list = [5]
    another_list = [5]
    def __init__(self, x):
        self.some_var = x + 1
        self.some_list = self.some_list + [x]
        self.another_list += [x]
```

**Output:**

``` Python
>>> some_obj = SomeClass(420)
>>> some_obj.some_list
[5, 420]
>>> some_obj.another_list
[5, 420]
>>> another_obj = SomeClass(111)
>>> another_obj.some_list
[5, 111]
>>> another_obj.another_list
[5, 420, 111]
>>> another_obj.another_list is SomeClass.another_list
True
>>> another_obj.another_list is some_obj.another_list
True
```

### 说明:

* 类变量和实例变量在内部是通过类对象的字典来处理(译: 就是 `__dict__` 属性). 如果在当前类的字典中找不到的话就去它的父类中寻找.
* `+=` 运算符会在原地修改可变对象, 而不是创建新对象. 因此, 修改一个实例的属性会影响其他实例和类属性.

## Mutating the immutable!/强人所难

``` Python
some_tuple = ("A", "tuple", "with", "values")
another_tuple = ([1, 2], [3, 4], [5, 6])
```

**Output:**
``` Python
>>> some_tuple[2] = "change this"
TypeError: 'tuple' object does not support item assignment
>>> another_tuple[2].append(1000) # 这里不出现错误
>>> another_tuple
([1, 2], [3, 4], [5, 6, 1000])
>>> another_tuple[2] += [99, 999]
TypeError: 'tuple' object does not support item assignment
>>> another_tuple
([1, 2], [3, 4], [5, 6, 1000, 99, 999])
```

我还以为元组是不可变的呢...

### 说明:

* 引用 https://docs.python.org/2/reference/datamodel.html

    > 不可变序列
        不可变序列的对象一旦创建就不能再改变. (如果对象包含对其他对象的引用，则这些其他对象可能是可变的并且可能会被修改; 但是，由不可变对象直接引用的对象集合不能更改.)

* `+=` 操作符在原地修改了列表. 元素赋值操作并不工作, 但是当异常抛出时, 元素已经在原地被修改了.

(译: 对于不可变对象, 这里指tuple, `+=` 并不是原子操作, 而是 `extend` 和 `=` 两个动作, 这里 `=` 操作虽然会抛出异常, 但 `extend` 操作已经修改成功了. 详细解释可以看[这里](https://segmentfault.com/a/1190000010767068)）


## From filled to None in one instruction.../从有到无...

``` Python
some_list = [1, 2, 3]
some_dict = {
  "key_1": 1,
  "key_2": 2,
  "key_3": 3
}

some_list = some_list.append(4)
some_dict = some_dict.update({"key_4": 4})
```

**Output:**
``` Python
>>> print(some_list)
None
>>> print(some_dict)
None
```

### 说明:

大多数修改序列/映射对象的方法, 比如 `list.append`, `dict.update`, `list.sort` 等等. 都是原地修改对象并返回 `None`. 这样做的理由是, 如果操作可以原地完成, 就可以避免创建对象的副本来提高性能. (参考[这里](http://docs.python.org/2/faq/design.html#why-doesn-t-list-sort-return-the-sorted-list))


## Modifying a dictionary while iterating over it/迭代字典时的修改

``` Python
x = {0: None}

for i in x:
    del x[i]
    x[i+1] = None
    print(i)
```

**Output (Python 2.7- Python 3.5):**

```
0
1
2
3
4
5
6
7
```

是的, 它运行了**八次**然后才停下来.

### 说明:

* Python不支持对字典进行迭代的同时修改它.
* 它之所以运行8次, 是因为字典会自动扩容以容纳更多键值(我们有8次删除记录, 因此需要扩容). 这实际上是一个实现细节. (译: 应该是因为字典的初始最小值是8, 扩容会导致散列表地址发生变化而中断循环.)
* 在不同的Python实现中删除键的处理方式以及调整大小的时间可能会有所不同.(译: 就是说什么时候扩容在不同版本中可能是不同的, 在3.6及3.7的版本中到[5](https://github.com/python/cpython/blob/v3.6.1/Objects/dictobject.c#L103-L110)就会自动扩容了. 以后也有可能再次发生变化. 顺带一提,后面两次扩容会扩展为32和256. 8->32->256)
* 更多的信息, 你可以参考这个StackOverflow的[回答](https://stackoverflow.com/questions/44763802/bug-in-python-dict), 它详细的解释一个类似的例子.

## Stubborn `del` operator/坚强的 `del` *

``` Python
class SomeClass:
    def __del__(self):
        print("Deleted!")
```

**Output:**
1\.
``` Python
>>> x = SomeClass()
>>> y = x
>>> del x # 这里应该会输出 "Deleted!"
>>> del y
Deleted!
```

唷, 终于删除了. 你可能已经猜到了在我们第一次尝试删除 `x` 时是什么让 `__del__` 免于被调用的. 那让我们给这个例子增加点难度.

2\.
``` Python
>>> x = SomeClass()
>>> y = x
>>> del x
>>> y # 检查一下y是否存在
<__main__.SomeClass instance at 0x7f98a1a67fc8>
>>> del y # 像之前一样, 这里应该会输出 "Deleted!"
>>> globals() # 好吧, 并没有. 让我们看一下所有的全局变量
Deleted!
{'__builtins__': <module '__builtin__' (built-in)>, 'SomeClass': <class __main__.SomeClass at 0x7f98a1a5f668>, '__package__': None, '__name__': '__main__', '__doc__': None}
```

好了，现在它被删除了 :confused:

### 说明:
+ `del x` 并不会立刻调用 `x.__del__()`.
+ 每当遇到 `del x`, Python 会将 `x` 的引用数减1, 当 `x` 的引用数减到0时就会调用 `x.__del__()`.
+ 在第二个例子中, `y.__del__()` 之所以未被调用, 是因为前一条语句 (`>>> y`) 对同一对象创建了另一个引用, 从而防止在执行 `del y` 后对象的引用数变为0.
+ 调用 `globals` 导致引用被销毁, 因此我们可以看到 "Deleted!" 终于被输出了.
+ (译: 这其实是 Python 交互解释器的特性, 它会自动让 `_` 保存上一个表达式输出的值, 详细可以看[这里](https://www.cnblogs.com/leisurelylicht/p/diao-pi-de-kong-zhi-tai.html).)


## Deleting a list item while iterating/迭代列表时删除元素

``` Python
list_1 = [1, 2, 3, 4]
list_2 = [1, 2, 3, 4]
list_3 = [1, 2, 3, 4]
list_4 = [1, 2, 3, 4]

for idx, item in enumerate(list_1):
    del item

for idx, item in enumerate(list_2):
    list_2.remove(item)

for idx, item in enumerate(list_3[:]):
    list_3.remove(item)

for idx, item in enumerate(list_4):
    list_4.pop(idx)
```

**Output:**
``` Python
>>> list_1
[1, 2, 3, 4]
>>> list_2
[2, 4]
>>> list_3
[]
>>> list_4
[2, 4]
```

你能猜到为什么输出是 `[2, 4]` 吗?

### 说明:

* 在迭代时修改对象是一个很愚蠢的主意. 正确的做法是迭代对象的副本, `list_3[:]` 就是这么做的.

     ``` Python
     >>> some_list = [1, 2, 3, 4]
     >>> id(some_list)
     139798789457608
     >>> id(some_list[:]) # 注意python为切片列表创建了新对象.
     139798779601192
     ```

**`del`, `remove` 和 `pop` 的不同:**
* `del var_name` 只是从本地或全局命名空间中删除了 `var_name` (这就是为什么 `list_1` 没有受到影响).
* `remove` 会删除第一个匹配到的指定值, 而不是特定的索引, 如果找不到值则抛出 `ValueError` 异常.
* `pop` 则会删除指定索引处的元素并返回它, 如果指定了无效的索引则抛出 `IndexError` 异常.

**为什么输出是 `[2, 4]`?**
- 列表迭代是按索引进行的, 所以当我们从 `list_2` 或 `list_4` 中删除 `1` 时, 列表的内容就变成了 `[2, 3, 4]`. 剩余元素会依次位移, 也就是说, `2` 的索引会变为 0, `3` 会变为 1. 由于下一次迭代将获取索引为 1 的元素 (即 `3`), 因此 `2` 将被彻底的跳过. 类似的情况会交替发生在列表中的每个元素上.

* 参考这个StackOverflow的[回答](https://stackoverflow.com/questions/45946228/what-happens-when-you-try-to-delete-a-list-element-while-iterating-over-it)来解释这个例子
* 关于Python中字典的类似例子, 可以参考这个Stackoverflow的[回答](https://stackoverflow.com/questions/45877614/how-to-change-all-the-dictionary-keys-in-a-for-loop-with-d-items).


## Same operands, different story!/同人不同命!

1\.
``` Python
a = [1, 2, 3, 4]
b = a
a = a + [5, 6, 7, 8]
```

**Output:**
``` Python
>>> a
[1, 2, 3, 4, 5, 6, 7, 8]
>>> b
[1, 2, 3, 4]
```

2\.
``` Python
a = [1, 2, 3, 4]
b = a
a += [5, 6, 7, 8]
```

**Output:**
``` Python
>>> a
[1, 2, 3, 4, 5, 6, 7, 8]
>>> b
[1, 2, 3, 4, 5, 6, 7, 8]
```

### 说明:

*  `a += b` 并不总是与 `a = a + b` 表现相同. 类实现 *`op=`* 运算符的方式 *也许* 是不同的, 列表就是这样做的.
* 表达式 `a = a + [5,6,7,8]` 会生成一个新列表, 并让 `a` 引用这个新列表, 同时保持 `b` 不变.
* 表达式 `a += [5,6,7,8]` 实际上是使用的是 "extend" 函数, 所以 `a` 和 `b` 仍然指向已被修改的同一列表.

## Needle in a Haystack/大海捞针

1\.
``` Python
x, y = (0, 1) if True else None, None
```

**Output:**
``` Python
>>> x, y  # 期望的结果是 (0, 1)
((0, 1), None)
```

几乎每个 Python 程序员都遇到过类似的情况.

2\.
``` Python
t = ('one', 'two')
for i in t:
    print(i)

t = ('one')
for i in t:
    print(i)

t = ()
print(t)
```

**Output:**
``` Python
one
two
o
n
e
tuple()
```

### 说明:
* 对于 1, 正确的语句是 `x, y = (0, 1) if True else (None, None)`.
* 对于 2, 正确的语句是 `t = ('one',)` 或者 `t = 'one',` (缺少逗号) 否则解释器会认为 `t` 是一个字符串, 并逐个字符对其进行迭代.
* `()` 是一个特殊的标记，表示空元组.


## Yes, it exists!/是的, 它存在!

**循环的 `else`.** 一个典型的例子:

``` Python
  def does_exists_num(l, to_find):
      for num in l:
          if num == to_find:
              print("Exists!")
              break
      else:
          print("Does not exist")
```

**Output:**
``` Python
>>> some_list = [1, 2, 3, 4, 5]
>>> does_exists_num(some_list, 4)
Exists!
>>> does_exists_num(some_list, -1)
Does not exist
```

**异常的 `else` .** 例,

``` Python
try:
    pass
except:
    print("Exception occurred!!!")
else:
    print("Try block executed successfully...")
```

**Output:**
``` Python
Try block executed successfully...
```

### 说明:
- 循环后的 `else` 子句只会在循环没有触发 `break` 语句, 正常结束的情况下才会执行.
- try 之后的 `else` 子句也被称为 "完成子句", 因为在 `try` 语句中到达 `else` 子句意味着try块实际上已成功完成.


## `+=` is faster/更快的 `+=`

``` Python
# 用 "+" 连接三个字符串:
>>> timeit.timeit("s1 = s1 + s2 + s3", setup="s1 = ' ' * 100000; s2 = ' ' * 100000; s3 = ' ' * 100000", number=100)
0.25748300552368164
# 用 "+=" 连接三个字符串:
>>> timeit.timeit("s1 += s2 + s3", setup="s1 = ' ' * 100000; s2 = ' ' * 100000; s3 = ' ' * 100000", number=100)
0.012188911437988281
```

### 说明:
+ 连接两个以上的字符串时 `+=` 比 `+` 更快, 因为在计算过程中第一个字符串 (例如, `s1 += s2 + s3` 中的 `s1`) 不会被销毁.(译: 就是 `+=` 执行的是追加操作，少了一个销毁新建的动作.)


## Let's make a giant string!/来做个巨大的字符串吧！

``` Python
def add_string_with_plus(iters):
    s = ""
    for i in range(iters):
        s += "xyz"
    assert len(s) == 3*iters

def add_bytes_with_plus(iters):
    s = b""
    for i in range(iters):
        s += b"xyz"
    assert len(s) == 3*iters

def add_string_with_format(iters):
    fs = "{}"*iters
    s = fs.format(*(["xyz"]*iters))
    assert len(s) == 3*iters

def add_string_with_join(iters):
    l = []
    for i in range(iters):
        l.append("xyz")
    s = "".join(l)
    assert len(s) == 3*iters

def convert_list_to_string(l, iters):
    s = "".join(l)
    assert len(s) == 3*iters
```

**Output:**
``` Python
>>> timeit(add_string_with_plus(10000))
1000 loops, best of 3: 972 µs per loop
>>> timeit(add_bytes_with_plus(10000))
1000 loops, best of 3: 815 µs per loop
>>> timeit(add_string_with_format(10000))
1000 loops, best of 3: 508 µs per loop
>>> timeit(add_string_with_join(10000))
1000 loops, best of 3: 878 µs per loop
>>> l = ["xyz"]*10000
>>> timeit(convert_list_to_string(l, 10000))
10000 loops, best of 3: 80 µs per loop
```

让我们将迭代次数增加10倍.

``` Python
>>> timeit(add_string_with_plus(100000)) # 执行时间线性增加
100 loops, best of 3: 9.75 ms per loop
>>> timeit(add_bytes_with_plus(100000)) # 二次增加
1000 loops, best of 3: 974 ms per loop
>>> timeit(add_string_with_format(100000)) # 线性增加
100 loops, best of 3: 5.25 ms per loop
>>> timeit(add_string_with_join(100000)) # 线性增加
100 loops, best of 3: 9.85 ms per loop
>>> l = ["xyz"]*100000
>>> timeit(convert_list_to_string(l, 100000)) # 线性增加
1000 loops, best of 3: 723 µs per loop
```

#### 说明:
- 你可以在这获得更多 [timeit](https://docs.python.org/3/library/timeit.html) 的相关信息. 它通常用于衡量代码片段的执行时间.
- 不要用 `+` 去生成过长的字符串, 在 Python 中, `str` 是不可变得, 所以在每次连接中你都要把左右两个字符串复制到新的字符串中. 如果你连接四个长度为10的字符串, 你需要拷贝 (10+10) + ((10+10)+10) + (((10+10)+10)+10) = 90 个字符而不是 40 个字符. 随着字符串的数量和大小的增加, 情况会变得越发的糟糕 (就像`add_bytes_with_plus` 函数的执行时间一样)
- 因此, 更建议使用 `.format.` 或 `%` 语法 (但是, 对于短字符串, 它们比 `+` 稍慢一点).
- 又或者, 如果你所需的内容已经以可迭代对象的形式提供了, 使用 `''.join(可迭代对象)` 要快多了.
- `add_string_with_plus` 的执行时间没有像 `add_bytes_with_plus` 一样出现二次增加是因为解释器会如同上一个列子所讨论的一样优化 `+=`. 用 `s = s + "x" + "y" + "z"` 替代 `s += "xyz"` 的话, 执行时间就会二次增加了.

  ``` Python
  def add_string_with_plus(iters):
      s = ""
      for i in range(iters):
          s = s + "x" + "y" + "z"
      assert len(s) == 3*iters

  >>> timeit(add_string_with_plus(10000))
  100 loops, best of 3: 9.87 ms per loop
  >>> timeit(add_string_with_plus(100000)) # 执行时间二次增加
  1 loops, best of 3: 1.09 s per loop
  ```
  

## Explicit typecast of strings/字符串的显式类型转换

``` Python
a = float('inf')
b = float('nan')
c = float('-iNf')  # 这些字符串不区分大小写
d = float('nan')
```

**Output:**

``` Python
>>> a
inf
>>> b
nan
>>> c
-inf
>>> float('some_other_string')
ValueError: could not convert string to float: some_other_string
>>> a == -c #inf==inf
True
>>> None == None # None==None
True
>>> b == d #但是 nan!=nan
False
>>> 50/a
0.0
>>> a/a
nan
>>> 23 + b
nan
```

### 说明:

`'inf'` 和 `'nan'` 是特殊的字符串(不区分大小写), 当显示转换成 `float` 型时, 它们分别用于表示数学意义上的 "无穷大" 和 "非数字".


## Minor Ones/小知识点

* `join()` 是一个字符串操作而不是列表操作. (第一次接触会觉得有点违反直觉)

  **说明:**
  如果 `join()` 是字符串方法 那么它就可以处理任何可迭代的对象(列表，元组，迭代器). 如果它是列表方法, 则必须在每种类型中单独实现. 另外, 在 `list` 对象的通用API中实现一个专用于字符串的方法没有太大的意义.

* 看着奇怪但能正确运行的语句:
  + `[] = ()` 语句在语义上是正确的 (解包一个空的 `tuple` 并赋值给 `list`)
  + `'a'[0][0][0][0][0]` 在语义上也是正确的, 因为在 Python 中字符串同时也是[序列](https://docs.python.org/3/glossary.html#term-sequence)(可迭代对象支持使用整数索引访问元素).
  + `3 --0-- 5 == 8` 和 `--5 == 5` 在语义上都是正确的, 且结果等于 `True`.(译: 3减负0等于3，再减负5相当于加5等于8；负的负5等于5.)

* 鉴于 `a` 是一个数组, `++a` 和 `--a` 都是有效的 Python 语句, 但其效果与 C, C++ 或 Java 等不一样.
  ``` Python
  >>> a = 5
  >>> a
  5
  >>> ++a
  5
  >>> --a
  5
  ```

  **说明:**
  + python 里没有 `++` 操作符. 这其实是两个 `+` 操作符.
  + `++a` 被解析为 `+(+a)` 最后等于 `a`. `--a` 同理.
  + 这个 StackOverflow [回答](https://stackoverflow.com/questions/3654830/why-are-there-no-and-operators-in-python) 讨论了为什么 Python 中缺少增量和减量运算符.

* Python 使用 2个字节存储函数中的本地变量. 理论上, 这意味着函数中只能定义65536个变量. 但是，Python 内置了一个方便的解决方案，可用于存储超过2^16个变量名. 下面的代码演示了当定义了超过65536个局部变量时堆栈中发生的情况 (警告: 这段代码会打印大约2^18行文本, 请做好准备!):
     ``` Python
     import dis
     exec("""
     def f():
         """ + """
         """.join(["X"+str(x)+"=" + str(x) for x in range(65539)]))

     f()

     print(dis.dis(f))
     ```

* 你的 *Python 代码* 并不会多线程同时运行 (是的, 你没听错!). 虽然你觉得会产生多个线程并让它们同时执行你的代码, 但是, 由于 [全局解释锁](https://wiki.python.org/moin/GlobalInterpreterLock)的存在, 你所做的只是让你的线程依次在同一个核心上执行. Python 多线程适用于IO密集型的任务, 但如果想要并行处理CPU密集型的任务, 你应该会想使用 [multiprocessing](https://docs.python.org/2/library/multiprocessing.html) 模块.

* 列表切片超出索引边界而不引发任何错误
  ``` Python
  >>> some_list = [1, 2, 3, 4, 5]
  >>> some_list[111:]
  []
  ```

* `int('١٢٣٤٥٦٧٨٩')` 在 Python 3 中会返回 `123456789`. 在 Python 中, 十进制字符包括数字字符, 以及可用于形成十进制数字的所有字符, 例如: U+0660, ARABIC-INDIC DIGIT ZERO. 这有一个关于此的 [有趣故事](http://chris.improbable.org/2014/8/25/adventures-in-unicode-digits/).

* `'abc'.count('') == 4`. 这有一个 `count` 方法的相近实现, 能更好的说明问题
  ``` Python
  def count(s, sub):
      result = 0
      for i in range(len(s) + 1 - len(sub)):
          result += (s[i:i + len(sub)] == sub)
      return result
  ```
  这个行为是由于空子串(`''`)与原始字符串中长度为0的切片相匹配导致的.
