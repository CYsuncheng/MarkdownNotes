# Builder 模式

## Builder 模式概述

可能我们经常会听到链式调用，在 Java 中用的最广泛的一个可能就是:

``` java
    StringBuilder sb = new StringBuilder();
    sb.append("a").append("b").append("c").append("d");
```

其实这种链式调用，就是 Builder 模式的应用，可以不断的往后面添加，我们来看看 append 方法的源码：

``` java
    public StringBuilder append(String str) {    
    	super.append(str);    
    	return this;
    }
    
    public AbstractStringBuilder append(String str) {    
    	if (str == null) 
    		str = "null";    
    	int len = str.length();    
    	ensureCapacityInternal(count + len);    
    	str.getChars(0, len, value, count);    
    	count += len;    
    	return this;
    }
```

顿时豁然开朗，原来 Builder 模式的精髓就在`return this;`，只有返回当前对象后，才能接着调用当前对象里的方法。

## 测试开发应用场景

在 Java 中，新建一个 HashMap 的对象并初始化，一般我们会这样做：

``` java
    Map map = new HashMap();
    map.put("a","1");
    map.put("b","2");
    map.put("c","3");
```

以上只是一个 HashMap，就搞出了 4 行代码，如果要初始化的数据更多，那代码行数就会越来越多，太难看了，难怪别人会说 Java 太重。可能这时你会立刻想到链式调用，也就是 Builder 模式，我们来实现一下：

``` java
    public class MapBuilder {    
    	public Map map;
      
    	public MapBuilder() {        
    		map = new HashMap();    
    	}
    	   
    	public MapBuilder put(K k, V v) {
    		map.put(k, v);        
    		return this;    
    	}    
    	
    	public V get(K k){        
    		return map.get(k);    
    	}    
    
    	public static void main(String[] args) {        
    		MapBuilder builder = new MapBuilder().put("a","1").put("b","2").put("c","3");        
    		System.out.println(builder.get("a"));    
    	}
    }
```

代码行数由不可预知变成了一行了，这就到了可接受的范围了，再联想到之前介绍过的简单工厂模式，代码再次优化：

``` java
    public class MapperBuilder {    
    	public static  Builder getBuilder(){        
    		return new Builder();    
    	}    
    
    	public static class Builder{        
    		public Map map; 
           
    		private Builder(){            
    			map = new HashMap();        
    		}        
    
    		public Builder put(K k, V v){            
    			map.put(k, v);            
    			return this;        
    		}        
    
    		public Map build(){            
    			return map;        
    		}    
    }    
    
    public static void main(String[] args) {        
    	Map map = MapperBuilder.getBuilder().put("a", "a").put("b", "b").build();        
    	System.out.println(map);        
    	Map map1 = MapperBuilder.getBuilder().put(1, 1).put(2, 2).build();        
    	System.out.println(map1);        
    	StringBuilder sb = new StringBuilder();        
    	sb.append("a").append("b").append("c").append("d");    
    	}
    }
```

一小段代码，里面竟然有两种设计模式，所以，代码无处不设计模式！