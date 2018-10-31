
## 原因：
1. 首先，在线唱整体是一个 listView，演唱会区域布局文件（*R.layout.concert_entry_header_view*）整体可以理解为一个 listView 的 headerView，内部包含子 View，这个 headerView 四周的留白使用了 padding，padding 的意思是内部子 View 和当前 View 的间距，所以，padding 区域依旧属于当前 View。
2. 当点击到 padding 区域时，由于 padding 依旧属于 headerView，而其自身没有处理点击事件，所以会回调父 View 的，而父 View 属于 listView，listView 有 onItemClick() 方法处理点击事件，所以，最终调用了 headerView 的 onItemClick() 。
3. 修改前的 onItemClick() 代码

```java
@Override
public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
		if (mLiveRoomOnline == null || mLiveRoomOnline.list == null) {
			return;
		}
		int headerCnt = listView.getHeaderViewsCount();
		int index = position - headerCnt;//如果点击 headerView 的话，index 已经是 -1 了
		LiveRoomInfo model = index < mLiveRoomOnline.list.size() ? mLiveRoomOnline.list.get(index) : null;//mLiveRoomOnline.list.get(index) 走到这里，index=-1，就 crash 了
		if (model == null) {
			return;
		}
```

4. 点击其他子 View 的时候，由于其他的子 View 监听并处理了点击事件，所以，不会有问题。

## 解决：去除headerview的点击事件

```java
@Override
public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
		if (mLiveRoomOnline == null || mLiveRoomOnline.list == null) {
			return;
		}
		int headerCnt = listView.getHeaderViewsCount();
		int index = position - headerCnt;
		//下面条件判断了，如果是 headerView ，就不处理点击事件
		LiveRoomInfo model = (0 <= index && index < mLiveRoomOnline.list.size()) ? mLiveRoomOnline.list.get(index) : null;
		if (model == null) {
			return;
		}
```

## 事件分发知识点：
1. Android 事件分发是先传递到 ViewGroup，再由 ViewGroup 传递到 View 的。
2. 在 ViewGroup 中可以通过 onInterceptTouchEvent 方法对事件传递进行拦截，onInterceptTouchEvent 方法返回 true 代表不允许事件继续向子 View 传递，返回 false 代表不对事件进行拦截，默认返回 false。
3. 子 View 中如果将传递的事件消费掉，ViewGroup 中将无法接收到任何事件。
4. 总结一下，就是**事件由上向下传递，传递到最终被点击的 View 时，处理点击由下向上**
[Android事件分发机制完全解析，带你从源码的角度彻底理解(上) - 郭霖的专栏        - CSDN博客](http://blog.csdn.net/guolin_blog/article/details/9097463)
[Android事件分发机制完全解析，带你从源码的角度彻底理解(下) - 郭霖的专栏        - CSDN博客](http://blog.csdn.net/guolin_blog/article/details/9153747)



