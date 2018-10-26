
1. 触摸事件的传递流程是从 dispatchTouchEvent开始的，如果不进行人为干预（也就是默认返回父类的同名函数），则事件将会依照嵌套层次从外层向内层传递，到达最内层的 View时，就由它的 onTouchEvent方法处理，该方法如果能够消费该事件，则返回 true，如果处理不了，则返回 false，这时事件会重新向外层传递，并由外层 View的 onTouchEvent方法进行处理，依此类推。
2. 如果事件在向内层传递过程中由于人为干预，事件处理函数返回 true，则会导致事件提前被消费掉，内层 View将不会收到这个事件。
3. View控件的事件触发顺序是先执行 onTouch方法，在最后才执行 onClick方法。如果 onTouch返回 true，则事件不会继续传递，最后也不会调用 onClick方法；如果 onTouch返回 false，则事件继续传递。
4. 触摸事件的传递顺序是由 Activity到 ViewGroup，再由 ViewGroup递归传递给它的子 View。 
5. ViewGroup通过 onInterceptTouchEvent方法对事件进行拦截，如果该方法返回 true，则事件不会继续传递给子 View，如果返回 false或者 super. onInterceptTouchEvent，则事件会继续传递给子 View。
6. 在子 View中对事件进行消费后， ViewGroup将接收不到任何事件。