# Android 触摸事件分发机制详解

触摸事件分发机制一直以来都是 Android 中比较重要的一大块，自定义 view，各种复杂的自定义手势交互都与触摸事件分发机制关系密切，想要做好这些，就要对触摸事件了解透彻，并且需要不断的去实践来加深印象，否则在自己去实现的时候就会茫然不知所措，同时这个知识点也是面试必问的经典题目，所以说掌握它是必须的，今天就来详细分析一下整个触摸事件的分发流程和相关知识。（本文理论知识较多，比较枯燥，需要极大耐心观看~）

## **触摸事件相关方法**

触摸事件大致涉及以下几个方法：

### **dispatchTouchEvent**

```java
/**
     * Pass the touch screen motion event down to the target view, or this
     * view if it is the target.
     *
     * @param event The motion event to be dispatched.
     * @return True if the event was handled by the view, false otherwise.
     */
    public boolean dispatchTouchEvent(MotionEvent event) {
        //......
  }
```

从源码里的注解可以看到，该方法主要是用来进行事件分发和传递的，当返回 true 的时候代表自己去处理，把事件传递给自己，否则就传递给其他的 view。该方法也是触摸事件第一个执行的方法，后续的几个是否执行都取决于它。

- **onInterceptTouchEvent**

这个方法主要是 viewGroup 特有的，用来做触摸事件拦截的，默认返回 false：

```java
/**
     * Implement this method to intercept all touch screen motion events.  This
     * allows you to watch events as they are dispatched to your children, and
     * take ownership of the current gesture at any point.
     *
     * <p>Using this function takes some care, as it has a fairly complicated
     * interaction with {@link View#onTouchEvent(MotionEvent)
     * View.onTouchEvent(MotionEvent)}, and using it requires implementing
     * that method as well as this one in the correct way.  Events will be
     * received in the following order:
     *
     * <ol>
     * <li> You will receive the down event here.
     * <li> The down event will be handled either by a child of this view
     * group, or given to your own onTouchEvent() method to handle; this means
     * you should implement onTouchEvent() to return true, so you will
     * continue to see the rest of the gesture (instead of looking for
     * a parent view to handle it).  Also, by returning true from
     * onTouchEvent(), you will not receive any following
     * events in onInterceptTouchEvent() and all touch processing must
     * happen in onTouchEvent() like normal.
     * <li> For as long as you return false from this function, each following
     * event (up to and including the final up) will be delivered first here
     * and then to the target's onTouchEvent().
     * <li> If you return true from here, you will not receive any
     * following events: the target view will receive the same event but
     * with the action {@link MotionEvent#ACTION_CANCEL}, and all further
     * events will be delivered to your onTouchEvent() method and no longer
     * appear here.
     * </ol>
     *
     * @param ev The motion event being dispatched down the hierarchy.
     * @return Return true to steal motion events from the children and have
     * them dispatched to this ViewGroup through onTouchEvent().
     * The current target will receive an ACTION_CANCEL event, and no further
     * messages will be delivered here.
     */
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        if (ev.isFromSource(InputDevice.SOURCE_MOUSE)
                && ev.getAction() == MotionEvent.ACTION_DOWN
                && ev.isButtonPressed(MotionEvent.BUTTON_PRIMARY)
                && isOnScrollbarThumb(ev.getX(), ev.getY())) {
            return true;
        }
        return false;
    }
```

可以看到注释是很长的，也是很详细的，我这里大致翻译一下里面几个重要的点：

- 主要是用来做事件分发过程中的拦截的，相当于一个拦截器
- 如果返回 false 或者 super，则事件继续传递，事件所经过的每一层的 viewGroup 都会去调用该方法来询问是否拦截
- 如果返回 true，则代表拦截该事件，停止传递给子 view，会走自己的 onTouchEvent 事件
- 不像 onTouchEvent 是否拦截取决于 down 事件，该方法每个事件都可以去做拦截
- 事件一经拦截，后续 move、up 事件都直接交给 onTouchEvent，不会重新去询问是否拦截 (即不再调用 onInterceptTouchEvent)
- 事件被拦截后，子 view 会接收到一个 cancel 事件，来恢复之前的状态，结束当前事件流

### **requestDisallowInterceptTouchEvent**

```java
/**
     * Called when a child does not want this parent and its ancestors to
     * intercept touch events with
     * {@link ViewGroup#onInterceptTouchEvent(MotionEvent)}.
     *
     * <p>This parent should pass this call onto its parents. This parent must obey
     * this request for the duration of the touch (that is, only clear the flag
     * after this parent has received an up or a cancel.</p>
     *
     * @param disallowIntercept True if the child does not want the parent to
     *            intercept touch events.
     */
    public void requestDisallowInterceptTouchEvent(boolean disallowIntercept);
```

这个方法也是用来做事件拦截的，也是 viewGroup 专有的方法，不过一般是在子 view 中来调用的，根据注释：当一个子 view 不希望它的父 view 来通过 onInterceptTouchEvent 方法拦截事件的时候，调用该方法即可实现事件的传递和接管，并且在整个事件流中，父 view 以及再往上的父 view 都要遵守该规则。

### **onTouch**

```java
/**
     * Called when a touch event is dispatched to a view. This allows listeners to
     * get a chance to respond before the target view.
     *
     * @param v The view the touch event has been dispatched to.
     * @param event The MotionEvent object containing full information about
     *        the event.
     * @return True if the listener has consumed the event, false otherwise.
     */
    boolean onTouch(View v, MotionEvent event);
```

这个也是触摸事件，方便给开发者调用的。根据注释：当一个触摸事件被分发到一个 view 的时候，就会调用该方法，它是在事件传递到 onTouchEvent 之前被调用的。

### **onTouchEvent**

```java
/**
     * Implement this method to handle touch screen motion events.
     * <p>
     * If this method is used to detect click actions, it is recommended that
     * the actions be performed by implementing and calling
     * {@link #performClick()}. This will ensure consistent system behavior,
     * including:
     * <ul>
     * <li>obeying click sound preferences
     * <li>dispatching OnClickListener calls
     * <li>handling {@link AccessibilityNodeInfo#ACTION_CLICK ACTION_CLICK} when
     * accessibility features are enabled
     * </ul>
     *
     * @param event The motion event.
     * @return True if the event was handled, false otherwise.
     */
    public boolean onTouchEvent(MotionEvent event) {
        //......
    }
```

该方法就是真正用来处理触摸事件的最后调用的方法，在这里你可以自己写你的触摸事件算法。

### **onClick**

```java
/**
     * Called when a view has been clicked.
     *
     * @param v The view that was clicked.
     */
    void onClick(View v);
```

这个就是我们最熟悉的点击事件了，它也属于触摸事件的一个内容，有一点需要注意就是他是在 onTouchEvent 的 UP 事件里面执行的，这就是我们下面要讲的 onTouch、onClick、onTouchEvent 执行顺序。

## **onTouch、onTouchEvent、onClick 执行顺序**

执行顺序：onTouch—>onTouchEvent—>onClick，注意：onClick 直接消费掉了事件，不会再向上回溯事件了。下面我们就通过例子来验证，我们给 view 设置监听事件：

```java
setOnClickListener(new OnClickListener() {
    @Override
    public void onClick(View v) {
        Log.e(TAG, "onClick: ======" );
    }
});
setOnTouchListener(new OnTouchListener() {
    @Override
    public boolean onTouch(View v, MotionEvent event) {
        Log.e(TAG, "onTouch: ======" );
        return false;
    }
});
```

并重写 onTouchEvent：

```java
@Override
public boolean onTouchEvent(MotionEvent event) {
    switch (event.getAction()){
        case MotionEvent.ACTION_DOWN:
            Log.e(TAG, "onTouchEvent: ======ACTION_DOWN" );
            break;
        case MotionEvent.ACTION_MOVE:
            Log.e(TAG, "onTouchEvent: ======ACTION_MOVE" );
            break;
        case MotionEvent.ACTION_UP:
            Log.e(TAG, "onTouchEvent: ======ACTION_UP" );
            break;
        case MotionEvent.ACTION_CANCEL:
            Log.e(TAG, "onTouchEvent: ======ACTION_CANCEL" );
            break;
        default:
            Log.e(TAG, "onTouchEvent: ======default" );
            break;
    }
    return super.onTouchEvent(event);
}
```

打印日志如下：

```java
E/V: dispatchTouchEvent: ======ACTION_UP
    onTouch: ======
    onTouchEvent: ======ACTION_UP
    onClick: ======
```

证明了我们的顺序，下面把 onTouch 返回 true：

```java
E/V: dispatchTouchEvent: ======ACTION_UP
    onTouch: ======
```

说明 onTouch 优先消费掉了事件，如果把 onTouchEvent 返回 true 呢：

```java
E/V: dispatchTouchEvent: ======ACTION_UP
    onTouch: ======
    onTouchEvent: ======ACTION_UP
```

onClick 就不执行了，说明在 onTouchEvent 的 UP 事件中，事件已经被消费了，所以最终的 click 事件没有被执行，下面看看源码：

```java
public boolean dispatchTouchEvent(MotionEvent event) {
    //......
    boolean result = false;
    //......
    if (onFilterTouchEventForSecurity(event)) {
        //......
        //noinspection SimplifiableIfStatement
        ListenerInfo li = mListenerInfo;
        if (li != null && li.mOnTouchListener != null
                && (mViewFlags & ENABLED_MASK) == ENABLED
                && li.mOnTouchListener.onTouch(this, event)) {
            result = true;
        }

        if (!result && onTouchEvent(event)) {
            result = true;
        }
    }
    //......
    return result;
}
```

这里可以很明显看出，onTouch 优先于 onTouchEvent 执行。

```java
public boolean onTouchEvent(MotionEvent event) {
    //......
    if (clickable || (viewFlags & TOOLTIP) == TOOLTIP) {
        switch (action) {
            case MotionEvent.ACTION_UP:
                //......
                if ((mPrivateFlags & PFLAG_PRESSED) != 0 || prepressed) {
                    //......
                    if (!mHasPerformedLongPress && !mIgnoreNextUpEvent) {
                        // This is a tap, so remove the longpress check
                        removeLongPressCallback();

                        // Only perform take click actions if we were in the pressed state
                        if (!focusTaken) {
                            // Use a Runnable and post this rather than calling
                            // performClick directly. This lets other visual state
                            // of the view update before click actions start.
                            if (mPerformClick == null) {
                                mPerformClick = new PerformClick();
                            }
                            if (!post(mPerformClick)) {
                                performClick();
                            }
                        }
                    }
                    //......
                }
                mIgnoreNextUpEvent = false;
                break;
            case MotionEvent.ACTION_DOWN:
                //......
                break;
            case MotionEvent.ACTION_CANCEL:
                //......
                break;
            case MotionEvent.ACTION_MOVE:
                //......
                break;
        }
        return true;
    }
    return false;
}
```

performClick 里面就是执行的 onClick 事件，可以看到 onClick 是在 onTouchEvent 的 UP 事件里面才执行的，所以如果 onTouchEvent 返回了 true，那么事件就被消费掉了，这段代码就不会执行，所以 onClick 事件就不会发生了，到此这个顺序关系应该是比较明确了。

## **触摸事件传递顺序**

下面我们就来看一下整个触摸事件的流转机制，首先上图：

![触摸事件的流转](https://mmbiz.qpic.cn/mmbiz_png/v1LbPPWiaSt5iauPxyMAXt5WKMOAzmFG5BeCV9bW4xE94LBUmNSLuDCicR4wUQGvnBIoQryjWFwd0jFDadWdLNCkA/640?wx_fmt=png)

是不是被吓一跳？哈哈，下面我们就通过详细分析来解析上图。

上图一共分为三层，Activity——>ViewGroup——>View，其中 ViewGroup 比其他两个多了一个 onInterceptTouchEvent 方法，箭头代表了事件流的走向，箭头上的值则代表了该方法的返回值，绿色的消费框则代表了事件被消费掉，就此完结，不会再往下传递或者回溯。
仔细看图，我们可以总结出以下几点：

- **如果事件不被中断，则整个事件流就是一个完整的 U 型图**

事件依次从 `Activity` 的 `dispatchTouchEvent——>ViewGroup` 的 `dispatchTouchEvent——>ViewGroup` 的 `onInterceptTouchEvent——>View` 的 `dispatchTouchEvent——>View` 的 `onTouchEvent——>ViewGroup` 的 `onTouchEvent——>Activity` 的 onTouchEvent 流转完成。

- **dispatchTouchEvent 和 onTouchEvent 一旦返回 true，事件就被消费掉了，该事件就消失了，不会往下传递也不会向上回溯**
- **dispatchTouchEvent 和 onTouchEvent 一旦返回 false，事件就会回溯到父控件的 onTouchEvent，说明自己不处理**

dispatchTouchEvent 返回 false 和 true 对于 Activity 来说都是一样，因为他是最顶层的事件接收者，而 ViewGroup 和 View 返回 super 则是向下传递，返回 false 就是向父控件的 onTouchEvent 回溯事件。

onTouchEvent 返回 super 代表向上回溯事件，返回 false 则代表自己不处理，所以也是向上回溯事件，如果最终都没消费，则 Activity 消费，事件消失。

- **所有方法的 super 就是默认返回值，就是保证让整个事件流按照 U 型图走完**
- **onInterceptTouchEvent 默认返回 super，通过源码我们知道其实就是返回 false，默认是不去拦截事件的，这也符合常理，可以让子 view 有机会去捕获事件，返回 true 则代表拦截了这个事件，交给自己的 onTouchEvent 去处理，ViewGroup 的 dispatchTouchEvent 的 super 默认实现就是调用自己的 onInterceptTouchEvent，这也就可以保证事件有机会分发到自己的 onTouchEvent**
- **dispatchTouchEvent 和 onTouchEvent 都是以 Down 事件为基准，来判断后续事件是否经过自己，也就是自己消费，如果 Down 事件返回了 false 或者 super，则后续事件都不再经过自己了，包括 move，up，如只有返回 true 的时候，后续事件才会经过自己**

下面我们通过 demo 来说明上图逻辑，我们首先新建一个 ViewGroup，再新建一个 View，还有一个 Activity，分别重写他们的 dispatchTouchEvent、onInterceptTouchEvent、onTouchEvent，源码就不在展示了，比较简单，最终的效果图如下：

![效果图](https://mmbiz.qpic.cn/mmbiz_jpg/v1LbPPWiaSt5iauPxyMAXt5WKMOAzmFG5BNAYQPmxJCyUS7DoOd1TCNV67GIBbF7iclwDY0ZpTbSZgarWuw2IZDAg/640?wx_fmt=jpeg)

先全部按照默认的 super 去返回，点击中间的 view 看一下日志（VG 代表 ViewGroup，V 代表 View）：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====onTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
    =====onTouchEvent=====ACTION_UP
```

看日志可以分析出跟我们上图的 U 型路线是一致的，由于事件一路传递下来，又一路回溯回去，所以最终事件就被 Activity 消费了 (后续的 UP 事件)。注意，我们这里的返回值都是在方法的最后一行，而不是 DOWN 事件内，事件内产生的日志又会不一样，这个后面再说。

下面我们在 View 的 onTouchEvent 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onInterceptTouchEvent: ======ACTION_UP
E/V: dispatchTouchEvent: ======ACTION_UP
E/V: onTouchEvent: ======ACTION_UP
```

我们在 View 的 dispatchTouchEvent 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onInterceptTouchEvent: ======ACTION_UP
E/V: dispatchTouchEvent: ======ACTION_UP
```

我们在 ViewGroup 的 onTouchEvent 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
```

我们在 ViewGroup 的 onInterceptTouchEvent 返回 true，并且 onTouchEvent 也返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
E/VG: onInterceptTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onTouchEvent: ======ACTION_MOVE
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onTouchEvent: ======ACTION_MOVE
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
```

可以看到被拦截之后，后续 move,up 事件都交给自己处理，并且不再调用 onIntercepetTouchEvent，而且事件也不再传递到子 View。

下面再把 ViewGroup 的 dispatchTouchEvent 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
```

Activity 的 dispatchTouchEvent 返回 true 或者 false：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
```

通过以上日志，认真的对着上图分析一遍，可以发现流程完全一致，整个的流程按照图纸来记忆还是比较容易的。

## **关于 ACTION_DOWN 的理解**

上面说到 dispatchTouchEvent 和 onTouchEvent 对事件是否消费是在 DOWN 事件中来决定的，如果 DOWN 没有返回 true，则后续的 move、up 都不会再来找上门了，下面我们就在 down 事件返回 true 来看一下：

view 的 onTouchEvent 中 DOWN 事件返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onInterceptTouchEvent: ======ACTION_UP
E/V: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
E/MainActivity: =====onTouchEvent=====ACTION_UP
```

可以看到比上面直接在方法最后返回 true 多出了最后一行日志，其他完全一致，这是因为只有 down 返回了 true，仅仅是让后续事件经过自己，但是 move、up 事件返回的还是 super，而 ViewGroup 的 onTouchEvent 事件已经被跳过，所以 up 事件回溯到 Activity 了。而在 move 和 up 事件中返回 true 则没有 down 返回 true 的作用。下面我们在 down 返回 false 看一下：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
E/VG: onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====onTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
    =====onTouchEvent=====ACTION_UP
```

可以看到，后续 move,up 事件都不在经过自己了，所以说 down 事件起到了决定事件流向的作用。

我们在 view 的 dispatchTouchEvent 的 DOWN 返回 true 看一下：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onInterceptTouchEvent: ======ACTION_UP
E/V: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
E/MainActivity: =====onTouchEvent=====ACTION_UP
```

可以看到，事件走到 View 的 dispatchTouchEvent 后就停止了，因为这里返回了 true，代表事件在这里消费了，而后续的 UP 事件同样也是走到 view 的 dispatchTouchEvent，由于 up 返回的是 super，所以走了自身的 onTouchEvent 的 up，然后这里返回的也是 super，所以又回溯给 Activity 的 onTouchEvent 的 up 了。

如果这里返回的 false 呢：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====onTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
    =====onTouchEvent=====ACTION_UP
```

可以看到事件走到 view 的 dispatchTouchEvent 后回溯给父控件的 onTouchEvent 了，然后又继续回溯，而后续的 UP 事件也不会经过了。下面再来看看 ViewGroup 的 onTouchEvent 的 DOWN 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
E/MainActivity: =====onTouchEvent=====ACTION_UP
```

可以看到事件在 ViewGroup 的 OnTouchEvent 结束了，没有继续回溯，而 up 事件也经过了自己，由于返回了 super，所以回溯到 Activity。

onInterceptTouchEvent 放到下面一小节，我们继续把 ViewGroup 的 dispatchTouchEvent 的 DOWN 返回 true：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====onTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/MainActivity: =====onTouchEvent=====ACTION_UP
```

可以看到事件在 dispatchTouchEvent 中消费了，没有传递下去，后续的 up 也经过了自己。

综上可以分析到：收到了 ACTION_DOWN，就会收到 ACTION_MOVE、ACTION_UP 等后续的事件的前提条件就是必须消费该事件，也就是返回 true。如果仅仅是在 ACTION_DOWN 返回 true，其他事件返回 super，则其他事件没被消费，会继续向上回溯，但是一定会经过消费控件本身。

## **关于 onInterceptTouchEvent 的理解**

上面说了 onInterceptTouchEvent 不会像 onTouchEvent 一样必须在 DOWN 里面决定是否消费，它是用来做拦截的，也就相当于一个分流器，所以在它的所有事件都可以去分流，比如我们手指按下列表中的一个 view，然后过一会去滑动，这个时候依然会走 onInterceptTouchEvent 方法，不过走的就是 move 了 (前提是你在 DOWN 事件中没有去拦截，也就是让事件向子 view 传递)，这个时候你就可以在 move 事件中去做拦截，来进行列表的一个滑动，这种设计是符合正常逻辑的，下面我们看一下日志 (在 down 中返回 true)：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====onTouchEvent=====ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/MainActivity: =====onTouchEvent=====ACTION_UP
```

可以看到直接被拦下了，走了自己的 onTouchEvent，由于返回了 super，所以事件回溯给 Activity。再看在 move 中返回 true（onTouchEvent 中返回 true，因为 DOWN 事件代表拦截，如果不返回 true，后续 move 就不会再经过 ViewGroup）：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/VG: onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onTouchEvent: ======ACTION_MOVE
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onTouchEvent: ======ACTION_MOVE
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
    onTouchEvent: ======ACTION_UP
```

可以看到成功的拦下了 move 事件。

## **关于 ACTION_CANCEL 的出现场景**

在上述 onInterceptTouchEvent 场景中，其实还少了一步，就是 View 的 onTouchEvent 的也要返回 true，这样就代表一开始是点击，然后停顿一下，手指去滑动，变成滑动了，通过 onInterceptTouchEvent 去拦截，这个时候 View 就会收到一个 ACTION_CANCEL 事件来恢复自己初始按下的状态，看下日志：

```java
E/MainActivity: =====dispatchTouchEvent=====ACTION_DOWN
E/VG: dispatchTouchEvent: ======ACTION_DOWN
    onInterceptTouchEvent: ======ACTION_DOWN
E/V: dispatchTouchEvent: ======ACTION_DOWN
    onTouchEvent: ======ACTION_DOWN
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onInterceptTouchEvent: ======ACTION_MOVE
E/V: dispatchTouchEvent: ======ACTION_CANCEL
    onTouchEvent: ======ACTION_CANCEL
E/MainActivity: =====dispatchTouchEvent=====ACTION_MOVE
E/VG: dispatchTouchEvent: ======ACTION_MOVE
    onTouchEvent: ======ACTION_MOVE
E/MainActivity: =====dispatchTouchEvent=====ACTION_UP
E/VG: dispatchTouchEvent: ======ACTION_UP
E/VG: onTouchEvent: ======ACTION_UP
```

我们成功的模拟了上述场景，事件传递到 view 的 onTouchEvent，就在被系统认为消费的时候，然后手指滑动，进而 ViewGroup 去拦截该滑动，这个时候就会额外触发一个 ACTION_CANCEL 来传递给子 view 进而恢复子 view 的状态，设计可以说是非常巧妙，哈哈~

结尾

原文地址 [https://mp.weixin.qq.com/s/Rt2EV_hZ_CysUJ-fisj3ug](https://mp.weixin.qq.com/s/Rt2EV_hZ_CysUJ-fisj3ug)
