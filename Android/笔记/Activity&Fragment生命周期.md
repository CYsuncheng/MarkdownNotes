# Activity&Fragment生命周期

## Activity生命周期

![](https://ws4.sinaimg.cn/large/006tNbRwly1fwqg0ih54yj30f50jrjsw.jpg)

## Fragment的生命周期
![](https://ws4.sinaimg.cn/large/006tNbRwly1fwqg9v7eorj308t0nj0ui.jpg)

## 两者对比
![](https://ws3.sinaimg.cn/large/006tNbRwly1fwqggmzti1j309g0irdgq.jpg)

## Fragment 生命周期调用详解

### onAttach方法
Fragment和Activity建立关联的时候调用（获得activity的传递的值）

### onCreateView方法
为Fragment创建视图（加载布局）时调用（给当前的fragment绘制UI布局，可以使用线程更新UI）

### onActivityCreated方法
当Activity中的onCreate方法执行完后调用（表示activity执行oncreate方法完成了的时候会调用此方法）

### onDestroyView方法
Fragment中的布局被移除时调用（表示fragment销毁相关联的UI布局）

### onDetach方法
Fragment和Activity解除关联的时候调用（脱离activity）

## fragment生命周期解析

当一个fragment被创建的时候：
onAttach()
onCreate()
onCreateView()
onActivityCreated()

当这个fragment对用户可见的时候，它会经历以下状态。
onStart()
onResume()

> 1.2可以理解为从创建到显示（或切换）

当这个fragment进入“后台模式”的时候，它会经历以下状态。
onPause()
onStop()

当这个fragment被销毁了（或者持有它的activity被销毁了）：
onPause()
onStop()
onDestroyView()
onDestroy()
onDetach()

就像Activity一样，在以下的状态中，可以使用Bundle对象保存一个fragment的对象。
onCreate()
onCreateView()
onActivityCreated()

## 其他场景的调用
屏幕灭掉
onPause() onSaveInstanceState() onStop()

屏幕解锁
onStart() onResume()

切换到其他Fragment
onPause() onStop() onDestroyView()

切换回本身的Fragment
onCreateView() onActivityCreated() onStart() onResume()

回到桌面
onPause() onSaveInstanceState() onStop()

回到应用
onStart() onResume()

退出应用
onPause() onStop() onDestroyView() onDestroy() onDetach()
