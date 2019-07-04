# Boolean还是boolean？

我们知道，boolean是基本数据类型，而Boolean是包装类型。

``` Java
public class BooleanMainTest { 
	public static void main(String[] args) { 
		Model model1 = new Model(); 
		System.out.println("default model : " + model1); 
	} 
} 

class Model { 
/** * 定一个Boolean类型的success成员变量 */ 
	private Boolean success; 
/** * 定一个boolean类型的failure成员变量 */ 
	private boolean failure; 
/** * 覆盖toString方法，使用Java 8 的StringJoiner */ 
	@Override public String toString() { 
		return new StringJoiner(", ", Model.class.getSimpleName() + "[","]").add("success=" + success).add("failure=" + failure) .toString(); 
	} 
}
```

以上代码输出结果为：
``` Java
default model : Model[success=null, failure=false]
```

可以看到，当我们没有设置Model对象的字段的值的时候，Boolean类型的变量会设置默认值为null，而boolean类型的变量会设置默认值为false。
我建议，在代码中，尽量避免出现和处理null。


