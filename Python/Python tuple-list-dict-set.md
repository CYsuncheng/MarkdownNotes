# Python tuple-list-dict-set

## 元组
> 可以包含不同类型的对象，但是是不可变的，不可以在增减元素，用()来定义.

元组的操作: `tuple(obj),切片,in,for in,del,cmp,len,max,min`
``` python
#定义一个元组
tuple1 =()
tuple1 = tuple({1,2,3,4,5,'6'})
tuple1 = (1, 2, '3', 4, '5')
# 定义了一个元组之后就无法再添加或修改元组中的元素,但是可以重新赋值
print tuple1[0] # 元组的元素都有确定的顺序。元组的索引也是以0为基点的
print tuple1[-1] # 负的索引从元组的尾部开始计数
print tuple1[1:3] # 元组也可以进行切片操作。对元组切片可以得到新的元组。
# 可以使用 in 运算符检查某元素是否存在于元组中。
print 1 in tuple1 # True
#使用for in 进行遍历元组
for item in tuple1:
print item
# 如果需要获取item的序号 可以使用下面的遍历方法：
for index in range(len(tuple1)):
print tuple1[index]
# 还可以使用内置的enumerate函数
for index, item in enumerate(tuple1):
print '%i, %s' % (index, item)
print max(tuple1)
print min(tuple1)
print len(tuple1)
```

## 列表
> 列表是Python中最具灵活性的有序集合对象类型,与字符串不同的是,列表可以包含任何种类的对象:数字,字符串,甚至是其他列表.并且列表都是可变对象,它支持在原处修改的操作.也可以通过指定的索引和分片获取元素.列表就可元组的可变版本，用[]来定义.

列表的操作: `list(obj),切片,in,for in,del,cmp,len,max,min`
额外的操作:
`list.append(),list.insert(index,obj),list.extend(seq),list.remove(obj),list.pop(index=-1),list.count(obj),sorted(list),reversed(list),list.index(obj)`
``` python
#定义一个列表
listA = ['a', 'b', 'c', 1, 2]
list(obj)
#把对象转换成列表,obj可以是元组,字典,字符串等
print list((1,2,3,4,5,6,8,6))
#[1,2,3,4,5,6,8,6]
haloword = list('halo word')
print haloword
#['h', 'a', 'l', 'o', ' ', 'w', 'o', 'r', 'd']
#元素计数
print haloword.count('o')
#2
#元素查找(返回第一次出现索引,没有则报错)
print haloword.index('o')
#3
#haloword[3]='o'
#元素排序,倒置位置
numbers = [1,2,3,'4',5,'6']
print sorted(numbers)
#[1, 2, 3, 5, '4', '6']
print list(reversed(numbers))
#['6', 5, '4', 3, 2, 1]
# 向 list 中增加元素
# 1.使用append 向 list 的末尾追加单个元素。
listA.append(3)
# 2.使用 insert 将单个元素插入到 list 中。数值参数是插入点的索引
listA.insert(3, 'd') # 在下标为3处添加一个元素
# 3.使用 extend 用来连接 list
listA.extend([7, 8])
# extend 和 append 看起来类似，但实际上完全不同。
# extend 接受一个参数，这个参数总是一个 list，
# 并且把这个 list 中的每个元素添加到原 list 中。
# 另一方面，append 接受一个参数，这个参数可以是任何数据类型，并且简单地追加到 list 的尾部。
# 获取列表的长度
print len(listA) # 9
# 在 list 中搜索
listA.index(3) # index 在 list 中查找一个值的首次出现并返回索引值。
listA.index('100') # 如果在 list 中没有找到值，Python 会引发一个异常。
# 要测试一个值是否在 list 内，使用 in。如果值存在，它返回 True，否则返为 False 。
print 5 in listA
# 从 list 中删除元素
# remove 从 list 中 仅仅 删除一个值的首次出现。如果在 list 中没有找到值，Python 会引发一个异常
listA.remove(3)
# pop 它会做两件事：删除 list 的最后一个元素，然后返回删除元素的值。
print listA.pop()
# 遍历list
for item in listA:
print item
```

## 字典
> 字典(Dictionary) 是 Python 的内置数据类型之一，它定义了键和值之间一对一的关系,但它们是以无序的方式储存的。定义 Dictionary 使用一对大(花)括号” { } ”。

字典的操作: `dict(obj),in,for key in dict,del,cmp,len,max,min`
额外的操作:
`dict[key],dict.keys(),dict.fromkeys(seq,value),dict.has_key(key),dict.get(key,default),dict.items(),dict.values():,dict.update(dict2),dict.pop(key),dict.setdefault(key ,defaultvalue),dict.clear(),dict.copy()`
``` python
# 定义一个字典
# Dictionary 不只是用于存储字符串。Dictionary 的值可以是任意数据类型，
# 包括字符串、整数、对象，甚至其它的 dictionary。
# 在单个 dictionary 里，dictionary 的值并不需要全都是同一数据类型，可以根据需要混用和匹配。
dict1 = {'name' : 'LiuZhichao', 'age' : 24, 'sex' : 'Male'}
dict1['name'] = 'Liuzc' # 为一个已经存在的 dictionary key 赋值，将简单覆盖原有的值。
dict1['Age'] = 25 # 在 Python 中是区分大小写的 age和Age是完全不同的两个key
#使用dict()创建字典
dict_test = dict((['x',1],['y',2]))
#{'y': 2, 'x': 1}
#使用dict.fromkeys()创建字典
#创建并返回一个新字典，以序列seq中元素做字典的键，val为字典所有键对应的初始值(默认为None)
dict.fromkeys(seq,val=None)
#遍历数组 form key in dict_test (不可以更改字典长度,报错)
# 方法 1.报错
form key in dict_test:
if(key=='x'):
del dict_test[key]
# 方法 2.正常
from key in dict_test.keys()
if(key=='x'):
del dict_test[key]
#dict.has_key(key)判断key是否存在
dict_test.has_key('x')
#True
#dict.get(key,default) 返回键值key的值，若是key不存在，返回default的值
dict_test.get('x',0)
#1
#dict.update(dict2) 将dict2的键值对列表添加到字典dict中去
dict_test.update({
'name':'rming',
'age':100,
})
#{'y': 2, 'x': 1,'name':'rming','age':100}
#dict.pop(key)返回键值key的value ,删除原字典该减值
print dict_test.pop('name')
print dict_test
#rming
#{'y': 2, 'x': 1,'age':100}
#dict.setdefault(key ,defaultvalue) 类似get方法，能够获得给定key的value，此外setdefault还能在自动重不含有给定key的情况下设定相应的key-value
dict_test.setdefault('sex','male')
#male
#{'y': 2, 'x': 1,'age':100,'sex','male'}
#dict.copy():返回具有相同key-value的新字典，为浅复制(shallow copy)
new_dict = dict_test.copy()
#key in dict 是否有该键,同 dict.has_key(key)
'x' in new_dict
#True
# 从字典中删除元素
del dict1['sex'] # del 允许您使用 key 从一个 dictionary 中删除独立的元素
dict1.clear() # clear 从一个 dictionary 中清除所有元素
```

## 集合
> Python的集合(set)和其他语言类似, 是一个无序不重复元素集, 基本功能包括关系测试和消除重复元素. 集合对象还支持union(联合), intersection(交), difference(差)和sysmmetric difference(对称差集)等数学运算.由于集合是无序的,所以，sets 不支持 索引, 分片, 或其它类序列（sequence-like）的操作。

``` python
#定义一个集合
set1 = {1, 2, 3, 4, 5}
# 或者使用 set 函数
list1 = [6, 7, 7, 8, 8, 9]
set2 = set(list1)
set2.add(10) # 添加新元素
print set2 # set([8, 9, 6, 7]) 去掉重复内容,而且是无序的
set3 = frozenset(list1)
set3.add(10) # 固定集合不能添加元素
#方法（所有的集合方法）：
s.issubset(t) #如果s是t的子集,返回True，否则返回False
s.issuperset(t) #如果s是t的超集,返回True，否则返回False
s.union(t) #返回一个新集合, 该集合是s和t的并集
s.intersection(t) #返回一个新集合, 该集合是s和t的交集
s.difference(t) #返回一个新集合, 该集合是s的成员, 但不是t的成员, 即返回s不同于t的元素
s.symmetric_defference(t) #返回所有s和t独有的(非共同拥有)元素集合
s.copy() #返回一个s的浅拷贝, 效率比工厂要好
#方法（仅适用于可变集合）:以下方法参数必须是可哈希的
s.update(t) #用t中的元素 修改s，即s现在包含s或t的成员
s.intersection_update(t) #s中的成员是共同属于s和t的元素
s.difference_update(t) #s中的成员是属于s但不包含在t中的元素
s.symmetric_difference_update(t) #s中的成员更新为那些包含在s或t中，但不是s和t共有的元素
s.add(obj) #在集合s中添加对象obj
s.remove(obj) #从集合s中删除对象obj，如果obj不是集合s中的元素（obj not in s）,将引发keyError错误
s.discard(obj) #如果obj是集合s中的元素，从集合s中删除对象obj
s.pop() #删除集合s中得任意一个对象，并返回它
s.clear() #删除集合s中的所有元素
## 集合有并集，交集，求差操作
## 并集：intersection() 方法返回一个新集合，包含在两个集合中同时出现的所有元素。
## 交集：union() 方法返回一个新集合，包含在两个 集合中出现的元素。
## 差集：difference() 方法返回的新集合中，包含所有在 集合A出现但未在集合B中的元素。
## symmetric_difference() 方法返回一个新集合，包含所有只在其中一个集合中出现的元素。
# 删除元素
set2.discard(6) # 当元素不存在时,不会引发异常
set2.remove(6) # 与discard的区别在于，如果没有要删除的元素，remove会引发一个异常
set2.pop() # 因为set是无序的，所以pop会随机的从set中删除一个元素
```