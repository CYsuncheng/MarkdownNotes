# python 常用 UI 自动化设计模式总结

## 工厂模式

### 简单工厂模式

``` Python
#encoding=utf-8
__author__ = 'kevinlu1010@qq.com'


class LeiFeng():
    def buy_rice(self):
        pass

    def sweep(self):
        pass


class Student(LeiFeng):
    def buy_rice(self):
        print '大学生帮你买米'

    def sweep(self):
        print '大学生帮你扫地'


class Volunteer(LeiFeng):
    def buy_rice(self):
        print '社区志愿者帮你买米'

    def sweep(self):
        print '社区志愿者帮你扫地'


class LeiFengFactory():
    def create_lei_feng(self, type):
        map_ = {
            '大学生': Student(),
            '社区志愿者': Volunteer()
        }
        return map_[type]


if __name__ == '__main__':
    leifeng1 = LeiFengFactory().create_lei_feng('大学生')
    leifeng2 = LeiFengFactory().create_lei_feng('大学生')
    leifeng3 = LeiFengFactory().create_lei_feng('大学生')
    leifeng1.buy_rice()
    leifeng1.sweep()
```

写一个雷锋类，定义买米和扫地两个方法，写一个学生类和社区志愿者类，继承雷锋类，写一个工厂类，根据输入的类型返回学生类或志愿者类。

### 工厂模式

``` Python
#encoding=utf-8
__author__ = 'kevinlu1010@qq.com'


class LeiFeng():
    def buy_rice(self):
        pass

    def sweep(self):
        pass


class Student(LeiFeng):
    def buy_rice(self):
        print '大学生帮你买米'

    def sweep(self):
        print '大学生帮你扫地'


class Volunteer(LeiFeng):
    def buy_rice(self):
        print '社区志愿者帮你买米'

    def sweep(self):
        print '社区志愿者帮你扫地'


class LeiFengFactory():
    def create_lei_feng(self):
        pass


class StudentFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Student()


class VolunteerFactory(LeiFengFactory):
    def create_lei_feng(self):
        return Volunteer()


if __name__ == '__main__':
    myFactory = StudentFactory()

    leifeng1 = myFactory.create_lei_feng()
    leifeng2 = myFactory.create_lei_feng()
    leifeng3 = myFactory.create_lei_feng()

    leifeng1.buy_rice()
    leifeng1.sweep()
```

雷锋类，大学生类，志愿者类和简单工厂一样，新写一个工厂方法基类，定义一个工厂方法接口（工厂方法模式的工厂方法应该就是指这个方法），然后写一个学生工厂类，志愿者工厂类，重新工厂方法，返回各自的类。

工厂方法相对于简单工厂的优点：

1.在简单工厂中，如果需要新增类，例如加一个中学生类（MiddleStudent），就需要新写一个类，同时要修改工厂类的map_，加入'中学生':MiddleStudent()。这样就违背了封闭开放原则中的一个类写好后，尽量不要修改里面的内容，这个原则。而在工厂方法中，需要增加一个中学生类和一个中学生工厂类（MiddleStudentFactory），虽然比较繁琐，但是符合封闭开放原则。在工厂方法中，将判断输入的类型，返回相应的类这个过程从工厂类中移到了客户端中实现，所以当需要新增类是，也是要修改代码的，不过是改客户端的代码而不是工厂类的代码。

2.对代码的修改会更加方便。例如在客户端中，需要将Student的实现改为Volunteer，如果在简单工厂中，就需要把
`leifeng1 = LeiFengFactory().create_lei_feng('大学生')`
中的大学生改成社区志愿者，这里就需要改三处地方，但是在工厂方法中，只需要把
`myFactory = StudentFactory()`
改成
`myFactory = VolunteerFactory()`
就可以了

### 单例模式
当我们实例化一个对象时，是先执行了类的new方法（我们没写时，默认调用object.new），实例化对象；然后再执行类的init方法，对这个对象进行初始化，所以我们可以基于这个，实现单例模式

``` Python
class Earth(object):    
    __instance=None #定义一个类属性做判断     
    def __new__(cls):         
        if cls.__instance==None:            
            #如果__instance为空证明是第一次创建实例            
            #通过父类的__new__(cls)创建实例                                             
            cls.__instance==object.__new__(cls)            
            return  cls.__instance        
        else:            
            #返回上一个对象的引用            
            return cls.__instance 
a = Earth()
print(id(a))
b = Earth()
print(id(b))
```

[资料](https://testerhome.com/topics/16892)