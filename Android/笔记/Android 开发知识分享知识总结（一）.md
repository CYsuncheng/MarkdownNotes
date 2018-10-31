# Android 开发知识分享知识总结（一）

## Activity 
### 生命周期
![activity_lifecycle](https://developer.android.com/images/activity_lifecycle.png)

#### 代码示例

```java
public class ExampleActivity extends Activity {    
	@Override    
	public void onCreate(Bundle savedInstanceState) { 
	       super.onCreate(savedInstanceState);       
	 // The activity is being created.   
	 }    
	@Override    
	protected void onStart(){        
	super.onStart();       
	 // The activity is about to become visible.    
	}    
	@Override    
	protected void onResume(){        
	super.onResume();        
	// The activity has become visible (it is now "resumed").    
	}    
	@Override    
	protected void onPause() {        
	super.onPause();        
	// Another activity is taking focus (this activity is about to be "paused").    
	}    
	@Override    
	protected void onStop(){        
	super.onStop();        
	// The activity is no longer visible (it is now "stopped")    
	}    
	@Override    
	protected void onDestroy(){        
	super.onDestroy();        
	// The activity is about to be destroyed.    
}}
```

### 返回栈
- 当前 Activity 启动另一个 Activity 时，该新 Activity 会被推送到堆栈顶部，成为焦点所在
- 前一个 Activity 仍保留在堆栈中，但是处于停止状态。Activity 停止时，系统会保持其用户界面的当前状态
- 用户按“返回”按钮时，当前 Activity 会从堆栈顶部弹出（Activity 被销毁），而前一个 Activity 恢复执行（恢复其 UI 的前一状态）
- 堆栈中的 Activity 永远不会重新排列，仅推入和弹出堆栈：由当前 Activity 启动时推入堆栈；用户使用“返回”按钮退出时弹出堆栈。 因此，返回栈以“后进先出”对象结构运行
![backstack](https://developer.android.com/images/fundamentals/diagram_backstack.png)

### 启动模式

- Standard
- SingleTop
- SingleTask
- SingleInstance

#### 设置方法

- 在 AndroidMainfest 文件中设置
- 启动 Activity 时，通过 Intent 的 Flag 来设置（FLAG_ACTIVITY_NEW_TASK，FLAG_ACTIVITY_SINGLE_TOP）

### 启动 Activity
#### Intent 启动 Activity

- 显式
	- 按名称（完全限定类名）指定要启动的组件。通常，您会在自己的应用中使用显式 Intent 来启动组件，这是因为您知道要启动的 Activity 或服务的类名。例如，启动新 Activity 以响应用户操作，或者启动服务以在后台下载文件

```java
	// 示例一
	Intent intent = new Intent(this, SecondActivity.class);  
    startActivity(intent);
    // 示例二
    Component component = new Component(this,SecondActivity.class);
    Intent intent = new Intent();
    intent.setComponent(component);
    startActivity(intent);
```

- 隐式
	- 不会指定特定的组件，而是声明要执行的常规操作，从而允许其他应用中的组件来处理它。例如，如需在地图上向用户显示位置，则可以使用隐式 Intent，请求另一具有此功能的应用在地图上显示指定的位置

```xml
	<activity android:name=".SecondActivity">
		<intent-filter>
			<action android:name="com.suncheng"/>
			<category 　android:name="android.intent.category.DEFAULT"/>
		</intent-filter>
	</activity>
```

```java
	Intent intent = new Intent();
	intent.setAction("com.suncheng");
	intent.addCategory("android.intent.category.DEFAULT");
	startActivity(intent);
```

#### 附Intent七大属性：

- component (组件) ：目的组件
- action（动作）：用来表现意图的行动
- category（类别）：用来表现动作的类别
- data（数据）：表示与动作要操纵的数据
- type（数据类型）：对于data范例的描写
- extras（扩展信息）：扩展信息
- Flags（标志位）：期望这个意图的运行模式

#### startActivityForResult

```java
public class MainActivity extends Activity {
    private final static String TAG="MainActivity";
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        Button btnOpen=(Button)this.findViewById(R.id.btnOpen);
        btnOpen.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                //得到新打开Activity关闭后返回的数据
                //第二个参数为请求码，可以根据业务需求自己编号
                startActivityForResult(new Intent(MainActivity.this, OtherActivity.class), 1);
            }
        });
    }

    /**
     * 为了得到传回的数据，必须在前面的Activity中（指MainActivity类）重写onActivityResult方法
     * 
     * requestCode 请求码，即调用startActivityForResult()传递过去的值
     * resultCode 结果码，结果码用于标识返回数据来自哪个新Activity
     */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        String result = data.getExtras().getString("result");//得到新Activity 关闭后返回的数据
        Log.i(TAG, result);
    }
}

//被启动的 Activity 的代码
public class OtherActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.other);
        Button btnClose=(Button)findViewById(R.id.btnClose);
        btnClose.setOnClickListener(new View.OnClickListener(){
            public void onClick(View v) {
                //数据是使用Intent返回
                Intent intent = new Intent();
                //把返回数据存入Intent
                intent.putExtra("result", "My name is linjiqin");
                //设置返回数据
                OtherActivity.this.setResult(RESULT_OK, intent);
                //关闭Activity
                OtherActivity.this.finish();
            }
        });
    }
}
```

### Bundle

> Bundle主要用于传递数据；它保存的数据，是以key-value(键值对)的形式存在的

- 我们经常使用 Bundle 在 Activity 之间传递数据，传递的数据可以是 boolean、byte、int、long、float、double、string 等基本类型或它们对应的数组，也可以是对象或对象数组
- 当 Bundle 传递的是**对象**或**对象数组**时，必须实现 **Serializable** 或 **Parcelable** 接口

#### 举例

```java
	// 写入
    Intent intent = new Intent().setClassName("com.bundletest", "com.bundletest.Bundle02");  
    Bundle bundle = new Bundle();  
	bundle.putString("name", "skywang");  
	bundle.putInt("height", 175);  
	intent.putExtras(bundle);  
	startActivity(intent); 

	//读取
	Bundle bundle = this.getIntent().getExtras(); 
	String name = bundle.getString("name");    
	int height = bundle.getInt("height"); 
```

#### 关于序列化

*序列化这块需要大家理解，三言两语说不清楚，所以这块还是推荐大家看一篇文章*
[Android 序列化](http://www.cnblogs.com/JarvisHuang/p/5550109.html)

## SharePreferences

> 一个轻量级的存储类，特别适合用于保存软件配置参数，比如我们平时常说的数据持久化
> 用xml文件存放数据，文件存放在/data/data/package name/shared_prefs目录下（需 root）

### 使用方法

1. 创建 SharedPreferences 对象（三种方式）
	- Context：getSharedPreferences(String name, int mode)
	- Activity：getPreferences(int mode)
	- PreferenceManager.getDefaultSharedPreferences(Context context)
2. 创建 SharedPreferences.Editor 对象，用于存储数据修改
3. 通过 Editor 对象的 putXxx() 方法，存储 key-value 对数据信息
4. 通过 Editor 对象的 commit() or apply() 方法提交对 SharedPreferences 的修改
	关于 **commit** 和 **apply** 两个方法的区别，有一篇文章挺好，建议大家看看
	[深入理解 SharedPreferences 的 commit 与 apply](http://www.jianshu.com/p/3b2ac6201b33)

#### 代码示例

```java
	/**
     * 保存用户信息
     */
    private void saveUserInfo(){
        SharedPreferences userInfo = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = userInfo.edit();//获取Editor
        //得到Editor后，写入需要保存的数据
        editor.putString("username", "老干部");
        editor.putInt("age", 30);
        editor.commit();//提交修改
        Log.i(TAG, "保存用户信息成功");
    }
    /**
     * 读取用户信息
     */
    private void getUserInfo(){
        SharedPreferences userInfo = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String username = userInfo.getString("username", null);//读取username
        int age = userInfo.getInt("age", 0);//读取age
        Log.i(TAG, "读取用户信息");
        Log.i(TAG, "username:" + username + "， age:" + age);
    }
    /**
     * 移除年龄信数据
     */
    private void removeUserInfo(){
        SharedPreferences userInfo = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = userInfo.edit();//获取Editor
        editor.remove("age");
        editor.commit();
        Log.i(TAG, "移除年龄数据");
    }

    /**
     * 清空数据
     */
    private void clearUserInfo(){
        SharedPreferences userInfo = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        SharedPreferences.Editor editor = userInfo.edit();//获取Editor
        editor.clear();
        editor.commit();
        Log.i(TAG, "清空数据");
    }
```

## Android 布局

> 这块许多都是概念，大家自己去看就行了

### 常用 View

- TextView
- Button
- ImageView
- EditText
- ProgressBar
- listView
- 等

### 布局文件

布局文件中各个参数需要了解，如：

- gravity
- textSize（sp 和 dp 的区别）
- visibility
- maxLines
- ellipsize
- 等

### 基础的布局类型

- LinearLayout 布局以及常用的属性
- RelativeLayout 布局以及常用的属性
- FrameLayout 布局以及常用的属性
- TableLayout 布局以及常用的属性
- **ConstraintLayout**，这是个新的布局，比较重要
	- 推荐文章：[ConstraintLayout](http://quanqi.org/2016/05/20/code-labs-constraint-layout/)

## BroadcastReceiver

### 分类

- 按发送方式
	- 标准广播
	- 有序广播
- 按注册方式
	- 动态广播
	- 静态广播
- 按定义方式
	- 系统广播
	- 自定义广播

### 实现的基本流程

- 广播接收者 BroadcastRecevier 向 AMS(Activity manager Service) 进行注册
- 广播发送者向 AMS 发送广播
- AMS查找符合条件 (intentFilter/permission) 的 BroadcastRecevier，将广播发送给 ReceiverDispatcher，Dispatcher将广播发送到BroadcastReceiver 的消息循环队列中
- 消息循环执行此广播，回调到 BoradcastReceiver 中的 onReceiver() 方法中

### 注册 Reveiver

#### 静态注册:

```xml
    <receiver android:name=".MyBroadcastReceiver" >
        <intent-filter>
            <action android:name="android.net.conn.CONNECTIVITY_CHANGE" />
        </intent-filter>
        <intent-filter>
            <action android:name="android.intent.action.BOOT_COMPLETED" />
        </intent-filter>
    </receiver>
```

#### 动态注册:

> 动态注册广播对使用的 Context 要注意，因为广播接受者的存在取决于注册的 context，如果是 Activity，广播在当前 Activity 中有效，如果是 Application context 则与 App 应用生命周期相同

```java
	registerReceiver(BroadcastReceiver receiver, IntentFilter filter)
	registerReceiver(BroadcastReceiver receiver, IntentFilter filter, String broadcastPermission, Handler scheduler)
```

### 发送的方式

- sendOrderedBroadcast(Intent, String) 发送有序广播
- sendBroadcast(Intent) 发送普通广播
- localBroadcastManager.sendBroadcast(intent) 发送应用内广播
	- **只能动态注册，不能静态注册**

#### 代码示例（动态）

```java
	//注册
	MyReceiver myReceiver= new MyReceiver();
	IntentFilter filter = new IntentFilter();
	filter.addAction("XXX");   //加入Action条件
	registerReceiver(myReceiver, filter);  //注册接收器的方法:1.接收器的实体类 2.action频道的信息
	
	//发送
	Intent intent = new Intent();
	intent.setAction("XXX");
	intent.putExtra("key", "传递的value");
	sendBroadcast(intent);
	
	//接收
	public class MyReceiver2 extends BroadcastReceiver {
		@Override
		public void onReceive(Context context, Intent intent) {
		String value = intent.getStringExtra("value");
		Toast.makeText(context, value, Toast.LENGTH_LONG).show();
		}
	}

	//注销
	@Override
	protected void onDestroy() {
		super.onDestroy();
		unregisterReceiver(myReceiver);//注销接收器
	}
```

## Handler

### 引入 handler 的原因

> Android 中更新 UI 的操作只能放到 UI 线程中处理，也就是主线程。Google 由此引入了 Handler 机制来解决这个问题


#### 代码示例

``` java
	Handler handler = new Handler({    
	    @Override    
	    public void handleMessage(Message msg) {  
            super.handleMessage(msg);
            ...//更新UI
	    }
	});
```

### 主要组成成员

- **Message** 是在线程之间传递的消息，它可以在内部携带少量的信息，用于在不同线程之间交换数据
- **Handler** 顾名思义也就是处理者的意思，它主要是用于发送和处理消息的
	- 发送消息一般是使用 Handler 的 sendMessage() 方法，而发出的消息经过一系列地辗转处理后，最终会传递到 Handler 的handleMessage() 方法中
- **MessageQueue** 是消息队列的意思，它主要是用于存放所有的 Handler 发送的消息。这部分消息会一直存在于消息队列中，等待被处理
	- 每个线程中只有一个 MessageQueue 对象
- **Looper** 是每个线程中的 MessageQueue 的管家，调用 Looper 的 loop() 方法后，就会进入到一个无限循环当中，然后每当发现MessageQueue 中存在一条消息，就会将它取出，并传递到 Handler 的 handleMessage() 方法中
	- 每个线程中也只会有一个Looper对象

### 流程

**创建 Handler -> 获取消息对象 -> 发送消息 -> 处理消息**

> 1. 首先需要在主线程当中创建一个 Handler 对象，并重写 handleMessage() 方法
> 2. 然后当子线程中需要进行 UI 操作时，就创建一个 Message 对象，并通过 Handler 将这条信息发送出去。之后这条消息会被添加到 MessageQueue 的队列中等待被处理，而 Looper 则会一直尝试从 MessageQueue 中取出待处理消息，最后分发回 Handler 的 handleMessage() 方法中
> 3. 由于 Handler 是在主线程中创建的，所以此时 handleMessage() 方法中的代码也会在主线程运行，于是我们在这里就可以安心地进行 UI 操作了

## RecyclerView

> 使用 RecylclerView 能够很容易的实现水平、垂直、瀑布流等显示样式，而 ListView 只能进行垂直显示

### LayoutManager

- LinearLayoutManager
- GridLayoutManager
- StaggeredGridLayoutManager

### RecyclerView.Adapter

> Adapter 是连接后端数据和前端显示的适配器接口，是数据和 UI（View）之间的一个重要纽带。

使用RecyclerView之前，我们需要一个继承自 RecyclerView.Adapter 的适配器，将数据与每一个 item 的界面进行绑定，要实现我们自己的 Adapte，首先必须 override 三个方法：

```java
方法1：public RecyclerView.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType)
方法2：public void onBindViewHolder(RecyclerView.ViewHolder holder, int position)
方法3：public int getItemCount()
```

#### onCreateViewHolder

- 这个方法主要为每个 Item inflater 出一个 View，但是该方法返回的是一个 ViewHolder
- 该方法把 View 直接封装在 ViewHolder 中，然后我们面向的是 ViewHolder 这个实例，当然这个 ViewHolder 需要我们自己去编写


#### onBindViewHolder
- 这个方法主要用于适配渲染数据到 View 中。方法提供给你了一个 viewHolder，而不是原来的 convertView。


#### getItemCount
- 这个方法就类似于 BaseAdapter 的 getCount 方法了，即总共有多少个条目。

#### 代码示例

```java
public class MyRecyclerViewAdapter extends RecyclerView.Adapter<MyRecyclerViewAdapter.RecyclerHolder> {
    private Context mContext;
    private List<String> dataList = new ArrayList<>();

    public MyRecyclerViewAdapter(RecyclerView recyclerView) {
        this.mContext = recyclerView.getContext();
    }

    public void setData(List<String> dataList) {
        if (null != dataList) {
            this.dataList.clear();
            this.dataList.addAll(dataList);
            notifyDataSetChanged();
        }
    }

    @Override
    public RecyclerHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(mContext).inflate(R.layout.id_rv_item_layout, parent, false);
        return new RecyclerHolder(view);
    }

    @Override
    public void onBindViewHolder(RecyclerHolder holder, int position) {
        holder.textView.setText(dataList.get(position));
    }

    @Override
    public int getItemCount() {
        return dataList.size();
    }

    class RecyclerHolder extends RecyclerView.ViewHolder {
        TextView textView;

        private RecyclerHolder(View itemView) {
            super(itemView);
            textView = (TextView) itemView.findViewById(R.id.tv__id_item_layout);
        }
    }
}
```

#### 点击事件

```java
//设置点击事件
adapter.setItemListener(new MyRecyclerViewAdapter.onRecyclerItemClickerListener() {
    @Override
    public void onRecyclerItemClick(View view, Object data, int position) {
        String s = (String) data;
        adapter.getDataList().set(position, s + "---->hi");
        adapter.notifyItemChanged(position);
        }
});
```

## 结语
- **以上是我总结的，Android 开发基础知识，第一轮分享的知识点，也许会有遗漏，不过如果这些大家都能记住并掌握了的话，我觉得每个人的收获应该还是挺明显的。**
- **这个学习分享，我们还会继续，第二轮的课程除了延续之外，还会增加深度，所以还需要大家一起努力。**




