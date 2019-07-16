> 所谓的回调函数就是：在A类中定义了一个方法，这个方法中用到了一个接口和该接口中的抽象方法，但是抽象方法没有具体的实现，需要B类去实现，B类实现该方法后，它本身不会去调用该方法，而是传递给A类，供A类去调用，这种机制就称为回调。

因为android回调中最常见的是Button的点击事件的回调，这里以此为参照：

1、定义一个接口：需要我们在类中定义出一个接口，并且给这个接口定义出一个抽象方法，就像下面这样：

``` Java
public interface C {
    public void onCallBack(String textstring);
}
```

以下是View.java类中定义的响应点击事件的接口：

``` Java
    /**
     * Interface definition for a callback to be invoked when a view is clicked.
     */
    public interface OnClickListener {
        /**
         * Called when a view has been clicked.
         *
         * @param v The view that was clicked.
         */
        void onClick(View v);
    }
```

2、在B类中定义出该接口的一个成员变量：

``` Java
public class B {

    private C c;

    public void setCallBack(C c) {
        this.c = c;
    }

    public void Call() {
        String string = "你好，我是B！";
        this.c.onCallBack(string);
    }
}
```

以下是View.java类中获取点击事件接口成员变量的源码：

``` Java
/**
 * Listener used to dispatch click events.
 * This field should be made private, so it is hidden from the SDK.
 * {@hide}
 */
public OnClickListener mOnClickListener;
```

3、在B类中定义出一个公共方法，可以用来设置这个接口的对象，调用该方法可以给接口对象变量赋值：

``` Java
public void setCallBack(C c) {
        this.c = c;
    }
```

以下是 setOnClickListener(OnClickListener l) 的源码：

``` Java
/**
 * Register a callback to be invoked when this view is clicked. If this view is not
 * clickable, it becomes clickable.
 *
 * @param l The callback that will run
 *
 * @see #setClickable(boolean)
 */
public void setOnClickListener(@Nullable OnClickListener l) {
    if (!isClickable()) {
        setClickable(true);
    }
    getListenerInfo().mOnClickListener = l;
}
```

最后一步

4、在B类中调用接口对象中的方法：

``` Java
 public void Call() {
        String string = "你好，我是B！";
        this.c.onCallBack(string);
    }
```

在View.java中的体现：

``` Java
/**
 * Call this view's OnClickListener, if it is defined.  Performs all normal
 * actions associated with clicking: reporting accessibility event, playing
 * a sound, etc.
 *
 * @return True there was an assigned OnClickListener that was called, false
 *         otherwise is returned.
 */
public boolean performClick() {
    final boolean result;
    final ListenerInfo li = mListenerInfo;
    if (li != null && li.mOnClickListener != null) {
        playSoundEffect(SoundEffectConstants.CLICK);
        li.mOnClickListener.onClick(this);//就是这里
        result = true;
    } else {
        result = false;
    }
```

这里附上整个项目的代码：

``` Java
public class A implements C {

    public static void main(String args[]) {
        B b = new B();
        b.setCallBack(new A());
        b.Call();
    }

    @Override
    public void onCallBack(String textstring) {
        System.out.println(textstring);
    }
}

public class B {

    private C c;

    public void setCallBack(C c) {
        this.c = c;
    }

    public void Call() {
        String string = "你好，我是B！";
        this.c.onCallBack(string);
    }
}

public interface C {
    public void onCallBack(String textstring);
}
```

附上我们最常用的Button点击事件的处理的代码：

``` Java
public class TestCallBack{
    private Button button;
    button.setOnClickListener(new OnClickListener() {
        @Override
        public void onClick(View v) {
           //做一些操作
            doWork();
        }
    });
    
}
```

我们接着往下看，我们就来好好的分析一下这个Button点击事件。

首先，在View类中我们能找到setOnClickListener(OnClickListener l)方法：

``` Java
public void setOnClickListener(@Nullable OnClickListener l) {
    if (!isClickable()) {
        setClickable(true);
    }
    getListenerInfo().mOnClickListener = l;
    }
```

这里将OnClickListener赋值给了mOnClickListener，我们想要找到onClick()方法是由View回调而不是Button自己回调的证据，就在这里：

``` Java
public boolean performClick() {  
     sendAccessibilityEvent(AccessibilityEvent.TYPE_VIEW_CLICKED);  
     ListenerInfo li = mListenerInfo;  
     if (li != null && li.mOnClickListener != null) {  
         playSoundEffect(SoundEffectConstants.CLICK);  
         li.mOnClickListener.onClick(this);  
         return true;  
     }  
     return false;  
}
```

对此我们的解释是：在父类中我们要用到onClick()方法，但是父类却没有去实现该方法，而是定义了一个方法setOnClickListener(OnClickListener l)，如果子类想要自己能够响应点击事件，则它就必须重写父类的该方法，实现OnClickListener接口和它的onClick()方法。在子类实现该接口和方法后，将其通过参数传递给父类，在父类中执行onClick()方法。那么我们是如何运行到这个OnClick()函数的呢，这里由于涉及到View的事件分发机制不细说，想了解的话网上有很多资料，这里只给出结论，因为我们在TestCallBack这个类中没有实现OnTouchListener，这个接口，那么当点击事件分发的时候必然会运行到onTouchEvent()

这个方法，我们来看一下这个方法：

``` Java
public boolean onTouchEvent(MotionEvent event) {  
    // 略去无用代码...  
    if (((viewFlags & CLICKABLE) == CLICKABLE || (viewFlags & LONG_CLICKABLE) == LONG_CLICKABLE)) {  
  
         switch (event.getAction()) {  
  
              case MotionEvent.ACTION_UP:  
                      
            // 略去无用代码...  
                if (!mHasPerformedLongPress) {   
                    // This is a tap, so remove the longpress check removeLongPressCallback();   
                    // Only perform take click actions if we were in the pressed state   
                    if (!focusTaken) {   
                        // Use a Runnable and post this rather than calling   
                        // performClick directly. This lets other visual state   
                        // of the view update before click actions start.   
                        if (mPerformClick == null) {   
                            mPerformClick = new PerformClick();   
                        }   
                        if (!post(mPerformClick)) {  
                            performClick(); //重点在这  
                        }   
                    }   
                }   
                //略去无用代码..  
                break;   
        }   
        return true;   
    }   
    return false;   
}
```

还记得前面我们在performClick();类里面找到的关于View.java类中对于回调方法onClick的调用么

``` Java
li.mOnClickListener.onClick(this);//就是这里
```

这样我们就完整的了解了整个OnClickListener()接口中体现出来的回调机制

回掉的写法和结构大概清楚了，那B类如何告诉A类调用自己的方法的呢？
在Android中，涉及到了事件传递的机制，下面简单说明：

``` Java
public boolean dispatchTouchEvent(MotionEvent event) {
 
        if (mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onTouchEvent(event, 0);
        }
        if (onFilterTouchEventForSecurity(event)) {
            ListenerInfo li = mListenerInfo;
            if (li != null && li.mOnTouchListener != null 
                    && (mViewFlags & ENABLED_MASK) == ENABLED
                    && li.mOnTouchListener.onTouch(this, event)) {
                return true;
            }
            if (onTouchEvent(event)) {
                return true;
            }
        }
        if (mInputEventConsistencyVerifier != null) {
            mInputEventConsistencyVerifier.onUnhandledEvent(event, 0);
        }
        return false;
}
```

由于我们没有实现OnTouchListener接口，而onTouch()方法的默认返回值为false，所以第一个if语句中的代码不会被执行到，进入第二个if语句中，执行了onTouchEvent()方法。那么我们再来看一下该方法：

``` Java
public boolean onTouchEvent(MotionEvent event) {
    // 略去无用代码...
    if (((viewFlags & CLICKABLE) == CLICKABLE || (viewFlags & LONG_CLICKABLE) == LONG_CLICKABLE)) {
         switch (event.getAction()) {
              case MotionEvent.ACTION_UP:
			// 略去无用代码...
				    if (!mHasPerformedLongPress) { 
					// This is a tap, so remove the longpress check removeLongPressCallback(); 
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
				//略去无用代码..
				break; 
		} 
		return true; 
	} 
	return false; 
}
```

我们只看重点，在ACTION_UP这个case当中，我们找到了关键的代码：

``` Java
if (!post(mPerformClick)) {
    performClick();
}
```