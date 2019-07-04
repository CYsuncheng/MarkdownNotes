# 迭代器与ConcurrentModificationException

1. 使用 for 循环
``` Java
List<String> list = new ArrayList<>();
        list.add(“1”);
        list.add(“2”);
        list.add(“3”);
        for (int i = 0; i < list.size(); i++) {
            System.out.println(list.size());
            if (“1”.equals(list.get(i))){
                list.add(“4”);
                list.remove(“1”);
            }
        }
```

2. 使用 foreach 遍历
``` Java
List<String> list = new ArrayList<>();
        list.add(“1”);
        list.add(“2”);
        list.add(“3”);
        for (String s : list){
            if (“1”.equals(s)){
                list.add(“4”);
                list.remove(“1”);
            }
        }
```

3. 使用 Iterator 迭代器
``` Java
List<String> list = new ArrayList<>();
        list.add(“1”);
        list.add(“2”);
        list.add(“3”);
        Iterator<String> iterator = list.iterator();
        while(iterator.hasNext()) {
            if (“1”.equals(iterator.next())) {
                iterator.remove();
                list.add(“4”);
                list.remove(“1”);
            }
        }
```

结果：
在第一种情况下编译和运行都是可以的，第二种和第三种则会抛出 java.util.ConcurrentModificationException 的异常，这是为什么呢？

原因：
逻辑上讲，迭代时可以添加元素，但是一旦开放这个功能，很有可能造成很多意想不到的情况。
比如你在迭代一个 ArrayList，迭代器的工作方式是依次返回给你第0个元素，第1个元素，等等，假设当你迭代到第5个元素的时候，你突然在ArrayList的头部插入了一个元素，使得你所有的元素都往后移动，于是你当前访问的第5个元素就会被重复访问。
Java 认为在迭代过程中，容器应当保持不变。因此，java 容器中通常保留了一个域称为 modCount，每次你对容器修改，这个值就会加1。当你调用 iterator 方法时，返回的迭代器会记住当前的 modCount，随后迭代过程中会检查这个值，一旦发现这个值发生变化，就说明你对容器做了修改，就会抛异常。

**即使第一个不报错，但是，在进行操作的时候，需要根据逻辑，相应的改变i的值，加一或减一，不然很有可能导致对一个元素重复操作or少操作一个元素**