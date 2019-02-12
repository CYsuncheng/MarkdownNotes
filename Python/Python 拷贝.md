# Python深拷贝和浅拷贝

## 对象赋值

``` Python
    will = ["Will", 28, ["Python", "C#", "JavaScript"]]
    wilber = will
    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]

    will[0] = "Wilber"
    will[2].append("CSS")
    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]
```

输出：

``` shell
will id: 4423542256
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4417298960, 140606798077296, 4423562736]
willer id: 4423542256
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4417298960, 140606798077296, 4423562736]
will id: 4423542256
['Wilber', 28, ['Python', 'C#', 'JavaScript', 'CSS']]
[4417299200, 140606798077296, 4423562736]
willer id: 4423542256
['Wilber', 28, ['Python', 'C#', 'JavaScript', 'CSS']]
[4417299200, 140606798077296, 4423562736]
```

### 分析一下这段代码：
![](https://ws4.sinaimg.cn/large/006tNc79ly1g03scf99avj30cy0c4dh3.jpg)

- 首先，创建了一个名为will的变量，这个变量指向一个list对象，从第一张图中可以看到所有对象的地址（每次运行，结果可能不同）
- 然后，通过will变量对wilber变量进行赋值，那么wilber变量将指向will变量对应的对象（内存地址），也就是说"wilber is will"，"wilber[i] is will[i]"
    - 可以理解为，Python中，对象的赋值都是进行对象引用（内存地址）传递
- 第三张图中，由于will和wilber指向同一个对象，所以对will的任何修改都会体现在wilber上
    - 这里需要注意的一点是，str是不可变类型，所以当修改的时候会替换旧的对象，产生一个新的地址39758496
---

## 浅拷贝


``` Python
    will = ["Will", 28, ["Python", "C#", "JavaScript"]]
    wilber = copy.copy(will)

    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]

    will[0] = "Wilber"
    will[2].append("CSS")
    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]
```

输出：

``` shell
will id: 4474218688
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4467974672, 140240056525696, 4474217968]
willer id: 4474879728
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4467974672, 140240056525696, 4474217968]
will id: 4474218688
['Wilber', 28, ['Python', 'C#', 'JavaScript', 'CSS']]
[4467974912, 140240056525696, 4474217968]
willer id: 4474879728
['Will', 28, ['Python', 'C#', 'JavaScript', 'CSS']]
[4467974672, 140240056525696, 4474217968]
```

### 分析一下这段代码：
![](https://ws1.sinaimg.cn/large/006tNc79ly1g03sgyxertj30dq0ehtac.jpg)

* 首先，依然使用一个will变量，指向一个list类型的对象
* 然后，通过copy模块里面的浅拷贝函数copy()，对will指向的对象进行浅拷贝，然后浅拷贝生成的新对象赋值给wilber变量
    * 浅拷贝会创建一个新的对象，这个例子中"wilber is not will"
    * 但是，对于对象中的元素，浅拷贝就只会使用原始元素的引用（内存地址），也就是说"wilber[i] is will[i]"
* 当对will进行修改的时候
    * 由于list的第一个元素是不可变类型，所以will对应的list的第一个元素会使用一个新的对象39758496
    * 但是list的第三个元素是一个可不类型，修改操作不会产生新的对象，所以will的修改结果会相应的反应到wilber上

#### 总结一下
当我们使用下面的操作的时候，会产生浅拷贝的效果：
1. 使用切片[:]操作
2. 使用工厂函数（如list/dir/set）
3. 使用copy模块中的copy()函数
---

## 深拷贝

``` Python
    import copy

    will = ["Will", 28, ["Python", "C#", "JavaScript"]]
    wilber = copy.deepcopy(will)

    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]

    will[0] = "Wilber"
    will[2].append("CSS")
    print "will id: %d" %id(will)
    print will
    print [id(ele) for ele in will]
    print "willer id: %d" %id(wilber)
    print wilber
    print [id(ele) for ele in wilber]
```

输出：

``` shell
will id: 4566206656
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4559962640, 140478066500480, 4566205936]
willer id: 4566234608
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4559962640, 140478066500480, 4566234824]
will id: 4566206656
['Wilber', 28, ['Python', 'C#', 'JavaScript', 'CSS']]
[4559962928, 140478066500480, 4566205936]
willer id: 4566234608
['Will', 28, ['Python', 'C#', 'JavaScript']]
[4559962640, 140478066500480, 4566234824]
```

### 分析一下这段代码：
![](https://ws3.sinaimg.cn/large/006tNc79ly1g03so2nb40j30dq0eh766.jpg)

* 首先，同样使用一个will变量，指向一个list类型的对象
* 然后，通过copy模块里面的深拷贝函数deepcopy()，对will指向的对象进行深拷贝，然后深拷贝生成的新对象赋值给wilber变量
    * 跟浅拷贝类似，深拷贝也会创建一个新的对象，这个例子中"wilber is not will"
    * 但是，对于对象中的元素，深拷贝都会重新生成一份（有特殊情况，下面会说明），而不是简单的使用原始元素的引用（内存地址）
    * 例子中will的第三个元素指向39737304，而wilber的第三个元素是一个全新的对象39773088，也就是说，"wilber[2] is not will[2]"
* 当对will进行修改的时候
    * 由于list的第一个元素是不可变类型，所以will对应的list的第一个元素会使用一个新的对象39758496
    * 但是list的第三个元素是一个可不类型，修改操作不会产生新的对象，但是由于"wilber[2] is not will[2]"，所以will的修改不会影响wilber
---
    
## 总结
* Python中对象的赋值都是进行对象引用（内存地址）传递
* 使用copy.copy()，可以进行对象的浅拷贝，它复制了对象，但对于对象中的元素，依然使用原始的引用.
* 如果需要复制一个容器对象，以及它里面的所有元素（包含元素的子元素），可以使用copy.deepcopy()进行深拷贝
* 对于非容器类型（如数字、字符串、和其他'原子'类型的对象）没有被拷贝一说
* 如果元祖变量只包含原子类型对象，则不能深拷贝，看下面的例子
    