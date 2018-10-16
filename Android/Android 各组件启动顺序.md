## Android 各组件启动顺序
---

### 结论：
1. Application 的 attachBaseContext 方法是优先执行的；
2. ContentProvider 的 onCreate 的方法比 Application 的 onCreate 的方法先执行；
3. Activity、Service的 onCreate 方法以及 BroadcastReceiver 的 onReceive 方法，是在 MainApplication 的 onCreate 方法之后执行的；
4. 调用流程为： Application 的 attachBaseContext ---> ContentProvider 的 onCreate ----> Application 的 onCreate ---> Activity、Service 等的 onCreate（Activity 和 Service 不分先后）；

### 坑：
1. 在 Application 的 attachBaseContext方法 中，使用了 getApplicationContext方法。当我发现在 attachBaseContext方法 中使用 getApplicationContext方法 返回null时，内心是崩溃。所以，如果在 attachBaseContext方法 中要使用 context 的话，那么使用 this 吧，别再使用 getApplicationContext() 方法了。
2. 这个其实不算很坑，也不会引起崩溃，但需要注意：在 Application 的 attachBaseContext方法 中，去调用自身的ContentProvider，那么这个 ContentProvider 会被初始化两次，也就是说这个 ContentProvider 会被两次调用到onCreate。如果你在 ContentProvider 的 onCreate 中有一些逻辑，那么一定要检查是否会有影响。



