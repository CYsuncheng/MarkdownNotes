# Python 多线程/多进程
## Python的GIL限制

全局解释器锁（global interpreter lock）如其名运行在解释器主循环中，在多线程环境下，任何一条线程想要执行代码的时候，都必须获取（acquire）到这个锁，运行一定数量字节码，然后释放（release）掉，然后再尝试获取。这样 GIL 就保证了同时只有一条线程在执行。

它是在实现Python解析器(CPython)时所引入的一个概念。同样一段Python代码可以通过CPython，PyPy等不同的Python执行环境来执行。像其中的JPython就没有GIL。然而因为CPython是大部分环境下默认的Python执行环境。GIL并不是Python的特性，Python完全可以不依赖于GIL。

官方解释如下：
> In CPython, the global interpreter lock, or GIL, is a mutex that prevents multiple native threads from executing Python bytecodes at once. This lock is necessary mainly because CPython’s memory management is not thread-safe. (However, since the GIL exists, other features have grown to depend on the guarantees that it enforces.)

接下来，我们找个例子来试一下：

## 实验多线程&多进程
``` python
list_num = [25000000, 25000000, 25000000, 25000000]

def test(n):
    while n > 0:
        n -= 1
        if n == 10000000:
            print "running",
        elif n == 0:
            print "stop"
```
上面的是一个测试的方法，很简单

### 普通方式

``` python
def single_thread():
    # 单线程
    start = time.time()
    for num in list_num:
        test(num)
    single_cost = time.time() - start
    print "single_cost: %s" % single_cost
    
single_cost: 7.60823106766
```

### 多线程：

``` python
def multi_thread():
    # thread方式
    t_list = []
    start = time.time()
    for num in list_num:
        t = Thread(target=test, args=[num])
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()
    spend = time.time() - start
    print "multi_thread_origin: %s" % spend
    
multi_thread_origin: 9.46964788437
```

从结果可以看到，时间居然花了更久，先不下结论，再看看多进程的方式：、

### 多进程

``` python
def multi_process():
    p_list = []
    start = time.time()
    for num in list_num:
        p = Process(target=test, args=[num])
        p_list.append(p)
        proc.start()
    for proc in p_list:
        proc.join()
    spend = time.time() - start
    print "multi_process_origin: %s" % spend
    
multi_process_origin: 1.95564603806
```

使用了多进程之后，我们终于看到了我们预先想要的结果，时间明显的缩短了。

那到底是为什么，多线程的方式，反而时间更久呢，这就和我们开头说的GIL有关了，我们例子里面写的test()方法，是个计算密集型的任务，而使用了多线程之后，线程的创建等反而增加了时间的消耗。

如何证明上面的结论呢，我们来换个test()试试看。

### IO 密集型任务

``` python
urls = [
    'http://tieba.baidu.com/',
    'http://zhidao.baidu.com/',
    'http://music.baidu.com/',
    'http://image.baidu.com/'
    ] # 实际测试的列表会更长，为了时间上有明显区别
    
def single_thread():
    # 单线程
    start = time.time()
    # for num in list_num:
    #     test(num)
    map(urllib2.urlopen, urls)
    single_cost = time.time() - start
    print "single_cost: %s" % single_cost

def ex():
    start = time.time()
    with futures.ThreadPoolExecutor(max_workers=4) as ex:
        # ex.map(test, list_num)
        ex.map(urllib2.urlopen, urls)
    print 'PoolExecutor:', time.time() - start
```

这次为了方便，直接使用了线程池，上面代码运行的结果是：

``` shell
single_cost: 3.52881193161
PoolExecutor: 0.769335985184
```

这次利用多线程，明显的缩短了任务的时长，这也证明了GIL的确对IO密集型的任务释放了锁。

### Thread 的 join and setDaemon 方法
`t.join()` 方法的意思是，主线程需要等待子线程运行结束后继续执行，不加这个方法，主线程会继续执行，例如上面的例子，改成这样：

``` python
def multi_thread():
    # thread方式
    t_list = []
    start = time.time()
    for num in list_num:
        t = Thread(target=test, args=[num])
        t_list.append(t)
        t.start()
    spend = time.time() - start
    print "multi_thread_origin: %s" % spend

# 结果：   
multi_thread_origin: 0.156303882599
running running running running stop
```
可以看到，主线程直接打印了时间，而此时子线程还在运行中。

`setDaemon()` 的意思是，如果主进程结束，则子进程也会跟着结束，调用需要在`start()`之前,可以自己改一下试试。还有 `apply` 和 `apply_async` 等方法，前者是阻塞的，后者非阻塞。


## 坑
1. Python 在 Mac 启动多进程，会导致 crash，解决办法是：环境变量添加：`export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`
2. TypeError: can't pickle cStringIO.StringO objects 看了些 stackoverflow 回复，貌似在python3.4解决了这类问题. 原因是，python 的 multiprocessing pool 进程池隐形的加入了一个任务队列，在你 apply_async 的时候，他会使用 pickle 序列化对象，但是 python 2.x 的pickle 应该是不支持这种模式的序列化。解决方法还不少，但是目前没看懂。。。最简单的就是直接使用Process，不用 ProcessPool。
