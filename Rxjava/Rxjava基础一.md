# RxJava 入门教程一

### 1\. 什么是函数式编程

*   函数式编程是一种编程范式，是面向数学的抽象，将计算描述为一种表达式求值，函数可以在任何地方定义，并且可以对函数进行组合。体现在 RxJava 上很明显的就是链式操作、操作符的应用。

### 2\. 什么是响应式编程

*   响应式编程是一种面向数据流和变化传播的编程范式，数据更新是相关联的。举一个简单的例子：A = B + C ,A 被赋值为 B 和 C 的值, 紧接着 B 发生了变化，但是 A 却不会发生变化。但如果是响应式编程，当 B 发生变化以后，A 就会随之发生改变。体现在 RxJava 上很明显的就是我们对数据流的操作以及当被观察者发生变化的时候，观察者随之发生变化。

### 3\. 什么是函数响应式编程

*   把函数式编程里面的一套思路和响应式编程合起来就是函数响应式编程。它可以极大地简化项目，特别是处理嵌套回调的异步事件、复杂的列表过滤和变换或者时间相关问题。

### 4\. RxJava 概述

*   RxJava 是一个函数库，让开发者可以利用可观察序列和 LINQ 风格查询操作符来编写异步和基于事件的程序。
*   开发者可以用 Observables 表示异步数据流，用 LINQ 操作符查询异步数据流，用 Schedulers 参数化异步数据流的并发处理。
*   Rx 可以这样定义：Rx = Observables + LINQ + Schedulers.

### 5\. 为何要用 RxJava

*   代码简洁：异步操作有 Handler、AsyncTask 等，但是使用 RxJava，就算再多的异步操作，代码逻辑越来越复杂，RxJava 依然可以保持清晰的逻辑。

*   举例：假设有这样一个需求：界面上有一个自定义的视图 imageCollectorView ，它的作用是显示多张图片，并能使用 addImage(Bitmap) 方法来任意增加显示的图片。现在需要程序将一个给出的目录数组 File[] folders 中每个目录下的 png 图片都加载出来并显示在 imageCollectorView 中。需要注意的是，由于读取图片的这一过程较为耗时，需要放在后台执行，而图片的显示则必须在 UI 线程执行。我们分别展示非 RxJava 的操作和 RxJava 的操作。

```java
非RxJava：

new Thread() {
    @Override
    public void run() {
        super.run();
        for (File folder : folders) {
            File[] files = folder.listFiles();
            for (File file : files) {
                if (file.getName().endsWith(".png")) {
                    final Bitmap bitmap = getBitmapFromFile(file);
                    getActivity().runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            imageCollectorView.addImage(bitmap);
                        }
                    });
                }
            }
        }
    }
}.start();
```

```java
RxJava：

Observable.from(folders)
    .flatMap(new Func1<File, Observable<File>>() {
        @Override
        public Observable<File> call(File file) {
            return Observable.from(file.listFiles());
        }
    })
    .filter(new Func1<File, Boolean>() {
        @Override
        public Boolean call(File file) {
            return file.getName().endsWith(".png");
        }
    })
    .map(new Func1<File, Bitmap>() {
        @Override
        public Bitmap call(File file) {
            return getBitmapFromFile(file);
        }
    })
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(new Action1<Bitmap>() {
        @Override
        public void call(Bitmap bitmap) {
            imageCollectorView.addImage(bitmap);
        }
    });
```

不难发现：RxJava 好就好在什么复杂逻辑都能穿成一条线的简洁。

### 6\. RxJava 的原理

*   RxJava 的原理就是创建一个 Observable 对象来干活，然后使用各种操作符建立起来的链式操作，就如同流水线一样，把你想要处理的数据一步一步地加工成你想要的成品，然后发射给 Subscriber 处理。
*   看代码：

```java
Observable observable = Observable.create(new Observable.OnSubscribe<String>() {
    @Override
    public void call(Subscriber<? super String> subscriber) {
        subscriber.onNext("Hello");
        subscriber.onNext("Hi");
        subscriber.onNext("Aloha");
        subscriber.onCompleted();
    }
});
```

这里传入了一个 OnSubscribe 对象作为参数。OnSubscribe 存储在返回的 Observable 对象中，它的作用相当于一个计划表，当 Observable 被订阅的时候，OnSubscribe 对象中的 call 方法就会被自动调用，事件序列就会依照设定依次触发，这样，由被观察者调用了观察者的回调方法，就实现了由被观察者向观察者的事件传递，即观察者模式。

### 7\. 观察者模式（简单说）

7.1 观察者模式需要解决的问题

*   A 对象（观察者）对 B 对象（被观察者）的变化高度敏感，需要在 B 对象变化的一瞬间做出反应。

7.2 现实生活中的观察与程序观察者模式的区别

*   生活中警察（观察者）抓小偷（被观察者），警察需要时时刻刻盯着小偷作案，当小偷偷东西的那一刻，上前抓住。
*   程序中的观察者模式：观察者不用时时刻刻盯着被观察者，而是采用订阅的方式，观察者告诉被观察者你发生变化通知我。

7.3 很常见的观察者模式

*   Button（被观察者）与 OnClickListener（观察者），通过 setOnClickListener() 方法达成订阅关系。
*   采取这样被动的观察方式，既省去了反复检索状态的资源消耗，也能够得到最高的反馈速度。
*   通过 setOnClickListener（）方法，Button 持有 OnClickListener 的引用，当用户点击时，Button 会调用 OnClickListener 中的 onClick 方法。抽象出来就是 Button -> 被观察者、OnClickListener -> 观察者、setOnClickListener() -> 订阅，onClick() -> 事件。

### 8\. RxJava 与观察者模式

*   RxJava 有四个基本概念：Observable (可观察者，即被观察者)、 Observer (观察者)、 subscribe (订阅)、事件（被观察者的行为）。Observable 和 Observer 通过 subscribe() 方法实现订阅关系，从而 Observable 可以在需要的时候发出事件来通知 Observer。
*   RxJava 是通过扩展的观察者模式来实现的：与传统观察者模式不同， RxJava 的事件回调方法除了普通事件 onNext() （相当于 onClick() / onEvent()）之外，还定义了两个特殊的事件：onCompleted() 和 onError()。

### 9\. RxJava 基本实现

*   添加依赖

```groovy
    compile 'io.reactivex:rxjava:1.3.2'
    compile 'io.reactivex:rxandroid:1.2.1'
```

*   创建 Observer（观察者）：它决定事件触发的时候将有怎样的行为

```Java
    /**
     * 创建观察者：
     * Observer是一个接口，Subscriber是在Observer的基础上进行了扩展。
     */
    Subscriber mSubscriber = new Subscriber<String>() {

        @Override
        public void onCompleted() {
            Log.d(TAG, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.d(TAG, "onError");
        }

        @Override
        public void onNext(String s) {
            Log.d(TAG, "onNext:" + s);
        }

        @Override
        public void onStart() {
            Log.d(TAG, "onStart");
        }
    };

    Observer<String> mObserver = new Observer<String>() {
        @Override
        public void onCompleted() {
            Log.d(TAG, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.d(TAG, "onError");
        }

        @Override
        public void onNext(String s) {
            Log.d(TAG, "onNext:" + s);
        }
    };
```

*   创建 Obsevable（被观察者）：它决定什么时候触发事件以及触发怎样的事件

```java
    /**
     * 创建被观察者
     */
    Observable observable = Observable.create(new Observable.OnSubscribe<String>() {

        @Override
        public void call(Subscriber<? super String> subscriber) {
            subscriber.onNext("Mr.Li");
            subscriber.onNext("Mr.Fu");
            subscriber.onNext("Mr.Zhao");
            subscriber.onCompleted();
        }
    });
```

*   被观察者订阅观察者

```Java
observable.subscribe(mSubscriber);
```

*   链式调用

```java
Observable.create(new Observable.OnSubscribe<String>() {
    @Override
    public void call(Subscriber<? super String> subscriber) {
        subscriber.onNext("Mr.Li");
        subscriber.onNext("Mr.Fu");
        subscriber.onNext("Mr.Zhao");
    }
}).subscribe(new Subscriber<String>() {
    @Override
    public void onCompleted() {
        Log.d(TAG, "onCompleted");
    }

    @Override
    public void onError(Throwable e) {
        Log.d(TAG, "onError");
    }

    @Override
    public void onNext(String s) {
        Log.d(TAG, "onNext:" + s);
    }
});

```

*   Log

```shell
10-14 20:16:47.065 25587-25587/com.best.rxjava D/MainActivity: onStart
10-14 20:16:47.065 25587-25587/com.best.rxjava D/MainActivity: onNext:Mr.Li
10-14 20:16:47.065 25587-25587/com.best.rxjava D/MainActivity: onNext:Mr.Fu
10-14 20:16:47.065 25587-25587/com.best.rxjava D/MainActivity: onNext:Mr.Zhao
10-14 20:16:47.065 25587-25587/com.best.rxjava D/MainActivity: onCompleted
```

说明：先调用 onStart 方法，接着调用两个 onNext 方法，最后调用 onCompleted 方法。

### 10\. Observer 和 Subscriber 的关系

10.1 相同点

*   基本使用方式是完全一样：

```Java
Observer<String> observer = new Observer<String>() {
    @Override
    public void onNext(String s) {
        Log.d(tag, "Item: " + s);
    }

    @Override
    public void onCompleted() {
        Log.d(tag, "Completed!");
    }

    @Override
    public void onError(Throwable e) {
        Log.d(tag, "Error!");
    }
};
```

```java
Subscriber<String> subscriber = new Subscriber<String>() {
    @Override
    public void onNext(String s) {
        Log.d(tag, "Item: " + s);
    }

    @Override
    public void onCompleted() {
        Log.d(tag, "Completed!");
    }

    @Override
    public void onError(Throwable e) {
        Log.d(tag, "Error!");
    }
};
```

说明：Subscriber 是 Observer 的抽象类，Subscriber 对 Observer 接口进行了一些扩展，但实质上，在 RxJava 的 subscribe 过程中，Observer 也总是会先被转换成一个 Subscribe 再使用。

10.2 不同点

*   onStart(): 这是 Subscriber 增加的方法。它会在 subscribe 刚开始，而事件还未发送之前被调用，可以用于做一些准备工作，例如数据的清零或重置。这是一个可选方法，默认情况下它的实现为空。需要注意的是，如果对准备工作的线程有要求（例如弹出一个显示进度的对话框，这必须在主线程执行）， onStart() 就不适用了，因为它总是在 subscribe 所发生的线程被调用，而不能指定线程。要在指定的线程来做准备工作，可以使用 doOnSubscribe() 方法。

*   unsubscribe(): 这是 Subscriber 所实现的另一个接口 Subscription 的方法，用于取消订阅。在这个方法被调用后，Subscriber 将不再接收事件。一般在这个方法调用前，可以使用 isUnsubscribed() 先判断一下状态。 unsubscribe() 这个方法很重要，因为在 subscribe() 之后， Observable 会持有 Subscriber 的引用，这个引用如果不能及时被释放，将有内存泄露的风险。所以最好保持一个原则：要在不再使用的时候尽快在合适的地方（例如 onPause() onStop() 等方法中）调用 unsubscribe() 来解除引用关系，以避免内存泄露的发生。

### 11\. 操作符分类

Rx 操作符的类型分为创建操作符、变换操作符、过滤操作符、组合操作符、错误处理操作符、辅助操作符、条件和布尔操作符、算术和聚合操作符及连接操作符等，而这些操作符类型下又有很多操作符，每个操作符可能还有很多变体。

### 12\. 创建操作符

创建操作符, 顾名思义，它的作用就是创建 Observable. 这里讲解 create、just 和 from 以及 interval、range、repeat、deffer 操作符。

*   create：用来创建被观察者

```Java
Observable observable = Observable.create(new Observable.OnSubscribe<String>() {
    @Override
    public void call(Subscriber<? super String> subscriber) {
        subscriber.onNext("Mr.Li");
        subscriber.onNext("Mr.Fu");
        subscriber.onNext("Mr.Zhao");
    }
})
```

*   just: 对 create 的简洁操作：将传入的参数依次发送出来

```Java
Observable observable = Observable.just("Mr.Li", "Mr.Fu", "Mr.Zhao");
```

*   from(T[]) / from(Iterable<? extends T>): 对 create 的简洁操作：将传入的数组或 Iterable（集合或者列表） 拆分成具体对象后，依次发送出来。

```Java
String[] s = {"Mr.Li", "Mr.Fu", "Mr.Zhao"};
Observable observable = Observable.from(s);
```

```Java
ArrayList<String> list = new ArrayList();
list.add("1");
list.add("2");
list.add("3");
list.add("4");
list.add("5");
list.add("6");
Observable observable = Observable.from(list);
```

*   interval: 创建一个按固定时间间隔发射整数序列的 Observable，相当于定时器

```Java
    Observable.interval(3, TimeUnit.SECONDS)
    .subscribe(new Subscriber<Long>() {
        @Override
        public void onCompleted() {
            Log.d(TAG, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.d(TAG, "onError");
        }

        @Override
        public void onNext(Long aLong) {
            Log.d(TAG, "onNext:" + aLong);
        }
    });

10-14 14:51:42.089 3785-3802/com.best.rxjava D/MainActivity: onNext:0
10-14 14:51:45.089 3785-3802/com.best.rxjava D/MainActivity: onNext:1
10-14 14:51:48.089 3785-3802/com.best.rxjava D/MainActivity: onNext:2
10-14 14:51:51.089 3785-3802/com.best.rxjava D/MainActivity: onNext:3
10-14 14:51:54.089 3785-3802/com.best.rxjava D/MainActivity: onNext:4
10-14 14:51:57.088 3785-3802/com.best.rxjava D/MainActivity: onNext:5
10-14 14:52:00.089 3785-3802/com.best.rxjava D/MainActivity: onNext:6
10-14 14:52:03.089 3785-3802/com.best.rxjava D/MainActivity: onNext:7
10-14 14:52:06.088 3785-3802/com.best.rxjava D/MainActivity: onNext:8
10-14 14:52:09.089 3785-3802/com.best.rxjava D/MainActivity: onNext:9
10-14 14:52:12.089 3785-3802/com.best.rxjava D/MainActivity: onNext:10
..............
```

*   range: 创建发射指定范围的整数序列的 Observable，可以拿来替代 for 循环，发射一个范围内的有序整数序列。第一个参数是起始值，并且不小于 0；第二个参数为个数。

```java
    Observable.range(1,5).subscribe(new Subscriber<Integer>() {
        @Override
        public void onCompleted() {
            Log.d(TAG_RANGE, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.d(TAG_RANGE, "onError");
        }

        @Override
        public void onNext(Integer integer) {
            Log.d(TAG_RANGE, "onNext:" + integer);
        }
    });
}

10-16 07:21:20.017 9564-9564/com.best.rxjava D/Range: onNext:1
10-16 07:21:20.017 9564-9564/com.best.rxjava D/Range: onNext:2
10-16 07:21:20.017 9564-9564/com.best.rxjava D/Range: onNext:3
10-16 07:21:20.017 9564-9564/com.best.rxjava D/Range: onNext:4
10-16 07:21:20.018 9564-9564/com.best.rxjava D/Range: onNext:5
10-16 07:21:20.018 9564-9564/com.best.rxjava D/Range: onCompleted
```

*   repeat：创建一个 N 次重复发射特定数据的 Observable：

```java
        Observable.range(0,3).repeat(3).subscribe(new Subscriber<Integer>() {
            @Override
            public void onCompleted() {
                Log.d(TAG_REPEAT, "onCompleted");
            }

            @Override
            public void onError(Throwable e) {
                Log.d(TAG_REPEAT, "onError");
            }

            @Override
            public void onNext(Integer integer) {
                Log.d(TAG_REPEAT, "onNext:" + integer.intValue());
            }
        });

10-16 08:48:20.006 22148-22148/com.best.rxjava D/Repeat: onNext:0
10-16 08:48:20.006 22148-22148/com.best.rxjava D/Repeat: onNext:1
10-16 08:48:20.006 22148-22148/com.best.rxjava D/Repeat: onNext:2
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:0
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:1
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:2
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:0
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:1
10-16 08:48:20.007 22148-22148/com.best.rxjava D/Repeat: onNext:2
10-16 08:48:20.008 22148-22148/com.best.rxjava D/Repeat: onCompleted

```

*   defer：延迟创建 Observable, 直到被观察者订阅才开始创建：

```java
    Observable observable = Observable.defer(new Func0<Observable<String>>() {
        @Override
        public Observable<String> call() {
            return Observable.just(mString);
        }
    });
    observable.subscribe(new Subscriber<String>() {
        @Override
        public void onCompleted() {
            Log.d(TAG_DEFER, "onCompleted");
        }

        @Override
        public void onError(Throwable e) {
            Log.d(TAG_DEFER, "onError");
        }

        @Override
        public void onNext(String s) {
            Log.d(TAG_DEFER, "onNext:" + s);
        }
    });

10-16 08:48:19.993 22148-22148/com.best.rxjava D/Deffer: onNext:null
10-16 08:48:19.993 22148-22148/com.best.rxjava D/Deffer: onCompleted
```

```java
        Observable observable = Observable.defer(new Func0<Observable<String>>() {
            @Override
            public Observable<String> call() {
                return Observable.just(mString);
            }
        });
        mString = "RxJava";
        observable.subscribe(new Subscriber<String>() {
            @Override
            public void onCompleted() {
                Log.d(TAG_DEFER, "onCompleted");
            }

            @Override
            public void onError(Throwable e) {
                Log.d(TAG_DEFER, "onError");
            }

            @Override
            public void onNext(String s) {
                Log.d(TAG_DEFER, "onNext:" + s);
            }
        });
10-16 22:01:18.496 30581-30581/? D/Deffer: onNext:RxJava
10-16 22:01:18.496 30581-30581/? D/Deffer: onCompleted
```

### 13\. 变换操作符

变换操作符，顾名思义，它的作用就是对 Observable 发射的数据按照一定的规则做一些变换操作，然后将变换后的数据发射出去。这里讲解 map、flatmap、cast、flatMapIterable、buffer 和 groupBy.

*   map: 通过指定一个 Func 对象，将 Observable 转换为一个新的 Observable 对象并发射，观察者将收到新的 Observable 处理：意思就是将一个 Observable 转为另外一个新的 Observable。

```java
//将Integer转换为String
        Observable.just(123).map(new Func1<Integer, String>() {
            @Override
            public String call(Integer integer) {
                return integer+"";
            }
        }).subscribe(new Subscriber<String>() {
            @Override
            public void onCompleted() {
                Log.d(TAG_MAP, "onCompleted");
            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(String s) {
                Log.d(TAG_MAP, "onNext:" + s);
            }
        });
```

*   flatmap、cast: 将 Observable 发射的数据集合变换为 Observable 集合，然后将这些 Observable 发射的数据平坦化地放进一个单独的 Observable。cast 操作符的作用是强制将 Observable 发射的所有数据转换为指定类型。

```java
/**
*需求：访问网络，但是要访问同一个Host的多个界面，我们可以使用fo*r循环在每个界面的URL前添加Host，但是RxJava提供了一个更方便的操*/作。
final String Host = "http://blog.csdn.net/";
        List<String> mlist = new ArrayList<>();
        mlist.add("fukaiqiang01");
        mlist.add("fukaiqiang02");
        mlist.add("fukaiqiang03");
        mlist.add("fukaiqiang04");
        mlist.add("fukaiqiang05");
        Observable.from(mlist).flatMap(new Func1<String, Observable<?>>() {
            @Override
            public Observable<?> call(String s) {
                return Observable.just(Host + s);
            }
        }).cast(String.class).subscribe(new Subscriber<String>() {
            @Override
            public void onCompleted() {
                Log.d(TAG_FLATMAP, "onCompleted");
            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(String s) {
                Log.d(TAG_FLATMAP, "onNext:" + s);
            }
        });

10-17 09:23:28.255 14668-14668/? D/FlatMap: onNext:http://blog.csdn.net/fukaiqiang01
10-17 09:23:28.255 14668-14668/? D/FlatMap: onNext:http://blog.csdn.net/fukaiqiang02
10-17 09:23:28.255 14668-14668/? D/FlatMap: onNext:http://blog.csdn.net/fukaiqiang03
10-17 09:23:28.255 14668-14668/? D/FlatMap: onNext:http://blog.csdn.net/fukaiqiang04
10-17 09:23:28.255 14668-14668/? D/FlatMap: onNext:http://blog.csdn.net/fukaiqiang05
10-17 09:23:28.255 14668-14668/? D/FlatMap: onCompleted
```

说明：首先用 ArrayList 存储要访问的界面 URL, 然后通过 flatMap 转换成 Observable。cast 操作符将 Observable 中的数据转换为 String 类型。

注意：flatMap 的合并允许交叉，也就是说可能会交错地发送事件，最终结果的顺序可能并不是原始 Observable 发送时的顺序。

*   flatMapIterable：将数据转换为 Iterable，在 Iterable 里面进行数据的处理：

```java
Observable.just(1,2,3).flatMapIterable(new Func1<Integer, Iterable<Integer>>() {
            @Override
            public Iterable<Integer> call(Integer integer) {
                List<Integer> mlist = new ArrayList<Integer>();
                mlist.add(integer+1);
                return mlist;
            }
        }).subscribe(new Subscriber<Integer>() {
            @Override
            public void onCompleted() {

            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(Integer integer) {
                Log.d(FLATMAPITERABLE, "onNext:" + integer);
            }
        });
```

*   buffer: 顾名思义，设置缓冲区大小：它可以将原 Observable 变换为一个新的 Observable，这个新的 Observable 每次发射一组列表值，而不是一个一个发射。buffer 意思就是设置缓存容量值。

```java
Observable.just(1,2,3,4,5,6).buffer(3).subscribe(new Subscriber<List<Integer>>() {
            @Override
            public void onCompleted() {

            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(List<Integer> integers) {
                for (Integer integer : integers){
                    Log.d(BUFFER,"buffer:"+integer);
                }
                Log.d(BUFFER,"---------------------");
            }
        });

10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:1
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:2
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:3
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: ---------------------
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:4
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:5
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: buffer:6
10-17 11:38:47.340 30993-30993/com.best.rxjava D/Buffer: ---------------------
```

*   groupBy：用于分组元素，将源 Observable 变换成一个发射 Observables 的新 Observable（分组后的）。它们中的每一个新 Observable 都发射一组指定的数据。

```java
        Student s1 = new Student("杨过", "SSS");
        Student s2 = new Student("金轮法王", "SSS");
        Student s3 = new Student("周伯通", "S");
        Student s4 = new Student("东邪", "S");
        Student s5 = new Student("吸毒", "S");
        Student s6 = new Student("南帝", "S");
        Student s7 = new Student("北丐", "S");
        Student s8 = new Student("中神通", "SS");
        Student s9 = new Student("王蓉", "A");
        Observable<GroupedObservable<String, Student>> GroupedObservable =
                Observable.just(s1, s2, s3, s4, s5, s6, s7, s8, s9).groupBy(new Func1<Student, String>() {
                    @Override
                    public String call(Student student) {
                        return student.getLevel();
                    }
                });
        Observable.concat(GroupedObservable).subscribe(new Subscriber<Student>() {
            @Override
            public void onCompleted() {

            }

            @Override
            public void onError(Throwable e) {

            }

            @Override
            public void onNext(Student student) {
                Log.d(GROUPBY, "groupby:" + student.getName() + "-----" + student.getLevel());
            }
        });

10-17 13:07:42.583 11707-11707/? D/GroupBy: groupby:杨过-----SSS
10-17 13:07:42.583 11707-11707/? D/GroupBy: groupby:金轮法王-----SSS
10-17 13:07:42.583 11707-11707/? D/GroupBy: groupby:周伯通-----S
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:东邪-----S
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:吸毒-----S
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:南帝-----S
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:北丐-----S
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:中神通-----SS
10-17 13:07:42.584 11707-11707/? D/GroupBy: groupby:王蓉-----A
```

说明：这里创建了 9 个学生，按照其功夫水平的高低，对其进行了划分，从高到低依次是 SSS、SS、S、A. 使用 groupby 可以帮助我们队某一个 key 值进行分组，将相同的 key 值数据排在一起。这里的 key 指的就是等级，其中 concat 是组合操作符，后面会介绍。
