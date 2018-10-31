# Android RecyclerView 

## RecyclerView 简介

> A flexible view for providing a limited window into a large data set
> 大体意思就是RecyclerView是一个用于显示大量数据的弹性视图控件

### RecyclerView 与 ListView 区别

- ListView 只能实现垂直显示一组数据
- RecylclerView 能够很容易的实现水平、垂直、瀑布流等显示样式
- 性能优势，RecylclerView 可以复用回收的 View

### RecyclerView的 adapter

* 继承 RecyclerView.Adapter
* 重写 onCreateViewHolder：创建 viewType 类型的 ViewHolder
* 重写 onBindViewHolder：将数据绑定到 ViewHolder
* 其中ViewHolder将会被复用，去展示在数据集中的不同items。ViewHolder的数目最多为一屏内所能容纳的最大item个数+2


```java
public class RecycleViewAdapter extends RecyclerView.Adapter {
    private ArrayList<String> datas;
    private Context context;
    private OnItemClickListener onItemClickListener;
    public RecycleViewAdapter(ArrayList<String> datas, Context context) {
        this.datas = datas;
        this.context = context;
    }

    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View root= LayoutInflater.from(context).inflate(R.layout.layout_item,parent,false);
        return new MyViewHolder(root);
    }

    @Override
    public void onBindViewHolder(RecyclerView.ViewHolder holder, int position) {
        (((MyViewHolder)holder).info).setText(datas.get(position));
    }

    @Override
    public int getItemCount() {
        return datas.size();
    }

    public class MyViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener{
        public TextView info;
        public MyViewHolder(View itemView) {
            super(itemView);
            info= (TextView) itemView.findViewById(R.id.itemText);
            info.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            onItemClickListener.onItemClick(v,getAdapterPosition());
        }
    }

    public interface OnItemClickListener{
        void onItemClick(View view ,int position);
    }

    public void setOnItemClickListener(OnItemClickListener onItemClickListener){
        this.onItemClickListener=onItemClickListener;
    }
}
```

#### Scrap & Recycle

- Scrap Heap(垃圾堆)是一个轻量的集合，View不会经过适配器而是直接返回给LayoutManager，当需要一个View时首先回去 Scrap缓存里面找有没有所需要的View，而这里面的View已经绑定了需要的数据所以无需适配直接使用
- Recycle Pool(回收池)这里面回收的View如果再次使用需要重新经过适配器绑定数据，即调用onBindViewHolder()进行绑定数据， 当然如果Recycle Pool里面也没有View就只有重新创建View


#### Detach和Remove

- 通过Detach和Remove决定把View缓存在Recycle或者Scrap
- 使用Detach是把View缓存在Scrap，这种缓存方式可以方便如果还需要把缓存的View添加进来的场景，可以明显提高效率，它可 以通过调用detachAndScrapView()方法来实现
- Remove就是把View移除掉，放到Recycle里面，以备后面的再次利用，调用方法removeAndRecycleView()实现
- **当一个view只是暂时被清除掉，稍后就会用到，使用detach，它会被缓存进scrapCache的区域;当一个view不再显示 在屏幕上，需要被清除掉，并且下次再显示它的时机未知，使用remove,他会被以viewType分组，缓存进RecyclerViewPool里**

### 布局管理器（LayoutManager）
- LinearLayoutManager
- GridLayoutManager
- StaggeredGridLayoutManager


```java
//设置布局管理器（LayoutManager）
    recyclerView.setLayoutManager(new LinearLayoutManager(this,LinearLayoutManager.VERTICAL,false));
    //recyclerView.setLayoutManager(new GridLayoutManager(RecycleViewTestActivity.this,3));
    //recyclerView.setLayoutManager(new StaggeredGridLayoutManager(4, StaggeredGridLayoutManager.HORIZONTAL));
    //设置Adapter
    recyclerView.setAdapter(adapter);
    //设置分割线（ItemDecoration）
    recyclerView.addItemDecoration(new RecycleViewItemDecoration());
    adapter.setOnItemClickListener(new RecycleViewAdapter.OnItemClickListener() {
        @Override
        public void onItemClick(View view, int position) {
			Snackbar.make(recyclerView,"setOnItemClickListener:"+position,Snackbar.LENGTH_SHORT).show();
        }
    });
```

### ItemDecoration

> ItemDecoration，用来修饰RecyclerView里的Item，可以用来制造分割线和吸顶效果
常用方法：

- onDraw：设置绘制范围，而这个绘制范围可以超出在 getItemOffsets 中设置的范围，超出部分不可见；在drawChildren之前调用
- onDrawOver()：在drawChildren之后调用，绘制出的内容是在RecyclerView的最上层，会遮挡住ItemView
- getItemOffsets()： 可以通过outRect.set()为每个Item设置四周间距，这些值被计入了 RecyclerView 每个 item 的 padding 中


1. 绘制分割线


```java
public class DividerGridItemDecoration extends RecyclerView.ItemDecoration {

    private Drawable mDivider;

    public DividerGridItemDecoration(Context context) {
        mDivider = context.getResources().getDrawable(R.drawable.divider_recycle_view);
    }

    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
        drawHorizontal(c, parent);
        drawVertical(c, parent);
    }

    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        int spanCount = getSpanCount(parent);
        //int childCount = parent.getAdapter().getItemCount();
        int itemPosition = parent.getChildLayoutPosition(view);
        if (isFirstRow(itemPosition, spanCount)) {
            //如果是第一行，绘制top和bottom  Offset,
            if (isFirstColumn(itemPosition, spanCount)) {
                //如果是第一列，padding、padding/2
                outRect.set(mDivider.getIntrinsicWidth(), mDivider.getIntrinsicHeight(),
                        mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight());
            } else if (isLastColumn(itemPosition, spanCount)) {
                //如果是最后一列，padding/2、padding
                outRect.set(mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight(),
                        mDivider.getIntrinsicWidth(), mDivider.getIntrinsicHeight());
            } else {
                //padding/2、padding/2
                outRect.set(mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight(),
                        mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight());
            }

        } else {
            //仅仅绘制bottom  Offset
            if (isFirstColumn(itemPosition, spanCount)) {
                //如果是第一列，padding、padding/2
                outRect.set(mDivider.getIntrinsicWidth(), 0,
                        mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight());
            } else if (isLastColumn(itemPosition, spanCount)) {
                //如果是最后一列，padding/2、padding
                outRect.set(mDivider.getIntrinsicWidth() / 2, 0,
                        mDivider.getIntrinsicWidth(), mDivider.getIntrinsicHeight());
            } else {
                //padding/2、padding/2
                outRect.set(mDivider.getIntrinsicWidth() / 2, 0,
                        mDivider.getIntrinsicWidth() / 2, mDivider.getIntrinsicHeight());
            }
        }
    }


    public void drawHorizontal(Canvas c, RecyclerView parent) {
        int childCount = parent.getChildCount();
        int spanCount = getSpanCount(parent);
        for (int i = 0; i < childCount; i++) {
            final View child = parent.getChildAt(i);
            final RecyclerView.LayoutParams params = (RecyclerView.LayoutParams) child
                    .getLayoutParams();
            int left = child.getLeft() - params.leftMargin;
            if (isFirstColumn(i, spanCount)) {
                left = left - mDivider.getIntrinsicWidth();
            }
            int right = child.getRight() + params.rightMargin
                    + mDivider.getIntrinsicWidth();

            if (isFirstRow(i, spanCount)) {
                int bottom = child.getTop() - params.bottomMargin;
                int top = bottom - mDivider.getIntrinsicHeight();
                mDivider.setBounds(left, top, right, bottom);
                mDivider.draw(c);
            }
            int top2 = child.getBottom() + params.bottomMargin;
            int bottom2 = top2 + mDivider.getIntrinsicHeight();
            mDivider.setBounds(left, top2, right, bottom2);
            mDivider.draw(c);

        }
    }

    public void drawVertical(Canvas c, RecyclerView parent) {
        final int childCount = parent.getChildCount();
        int spanCount = getSpanCount(parent);
        for (int i = 0; i < childCount; i++) {
            View child = parent.getChildAt(i);
            RecyclerView.LayoutParams params = (RecyclerView.LayoutParams) child
                    .getLayoutParams();
            int top = child.getTop() - params.topMargin;
            int bottom = child.getBottom() + params.bottomMargin;
            if (isFirstColumn(i, spanCount)) {
                int left2 = child.getRight() + params.rightMargin;
                int right2 = left2 + mDivider.getIntrinsicWidth() / 2;
                mDivider.setBounds(left2, top, right2, bottom);
                mDivider.draw(c);
                int right = child.getLeft() - params.leftMargin;
                int left = right - 20;
                mDivider.setBounds(left, top, right, bottom);
            } else if (isLastColumn(i, spanCount)) {
                final int right = child.getLeft() - params.leftMargin;
                final int left = right - mDivider.getIntrinsicWidth() / 2;
                mDivider.setBounds(left, top, right, bottom);
                mDivider.draw(c);
                final int left2 = child.getRight() + params.rightMargin;
                final int right2 = left2 + mDivider.getIntrinsicWidth();
                mDivider.setBounds(left2, top, right2, bottom);
            } else {
                final int right = child.getLeft() - params.leftMargin;
                final int left = right - mDivider.getIntrinsicWidth() / 2;
                mDivider.setBounds(left, top, right, bottom);
                mDivider.draw(c);
                final int left2 = child.getRight() + params.rightMargin;
                final int right2 = left2 + mDivider.getIntrinsicWidth() / 2;
                mDivider.setBounds(left2, top, right2, bottom);
            }
            mDivider.draw(c);
        }
    }

    private boolean isFirstRow(int itemPosition, int spanCount) {
        return (itemPosition < spanCount);
    }

    private boolean isFirstColumn(int itemPosition, int spanCount) {
        return ((itemPosition) % spanCount == 0);
    }

    private boolean isLastColumn(int itemPosition, int spanCount) {
        return ((itemPosition + 1) % spanCount == 0);
    }

    private int getSpanCount(RecyclerView parent) {
        // 列数
        int spanCount = -1;
        RecyclerView.LayoutManager layoutManager = parent.getLayoutManager();
        if (layoutManager instanceof GridLayoutManager) {

            spanCount = ((GridLayoutManager) layoutManager).getSpanCount();
        } else if (layoutManager instanceof StaggeredGridLayoutManager) {
            spanCount = ((StaggeredGridLayoutManager) layoutManager)
                    .getSpanCount();
        }
        return spanCount;
    }

}
```

2. 吸顶效果
> 可以使用ItemDecoration的 getItemOffsets()、onDraw() 方法 为Item分类头部 留出空间， 在onDrawOver() 方法中绘制悬停的头部View

```java
public class TopItemDecoration extends RecyclerView.ItemDecoration {
    //type 1 的items的容量大小
    private int firstItemSize=3;
    //显示 type1 第一个item的位置
    private int firstItemPosition=2;
    //type的高度
    private int mTopHeight=0;
    //背景
    private Paint mbgPaint;
    private TextPaint mTextPaint;
    //文字距离左侧的间距
    private int outPadding;
    //用于存放测量文字Rect
    private Rect mBounds;

    public TopItemDecoration(Context context) {
        mbgPaint=new Paint();
        mTextPaint=new TextPaint();
        mBounds=new Rect();

        mbgPaint.setColor(context.getResources().getColor(R.color.defaultBg));
        mTextPaint.setTextSize(12*context.getResources().getDisplayMetrics().scaledDensity);
        mTextPaint.setTextAlign(Paint.Align.LEFT);
        mTextPaint.setAntiAlias(true);
        mTopHeight= DeviceUtil.dp2px(context,28);
        outPadding=DeviceUtil.dp2px(context,16);
    }

    public void setItemSize(int size){
        this.firstItemSize=size;
    }

    private String getTitleName(int index){
        if(index>=firstItemSize+firstItemPosition){
            return "最新";
        }else if(index>=firstItemPosition){
            return "推荐";
        }
        return "";
    }

    private boolean isFirstOfGroup(int index){
        if(index==firstItemPosition || index==firstItemSize+firstItemPosition){
            return true;
        }
        return false;
    }

    //显示在最上方
    @Override
    public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDrawOver(c, parent, state);
        int left=parent.getPaddingLeft()+outPadding;
        int right=parent.getWidth();
        //得到第一个可见item的位置
        int index= ((LinearLayoutManager)(parent.getLayoutManager())).findFirstVisibleItemPosition();
        //出现一个奇怪的bug，有时候child为空，所以将 child = parent.getChildAt(i)。-》 parent.findViewHolderForLayoutPosition(index).itemView
        View child = parent.findViewHolderForLayoutPosition(pos).itemView;
        String tag = getTitleName(index);
        //第一个类型的Item 的 header 在 position==2（firstItemPosition）处，如果index==2，则说明此item在顶部
        //index>=2，说明之后的item都有吸顶效果
        if(index-firstItemPosition>=0){
            int top=parent.getPaddingTop();
            int bottom=parent.getPaddingTop() + mTopHeight;
            //制造"最新"（下一组第一个item）和"推荐"交接时，被顶上去的效果
            //在还没开始交接的时候，"最新"的getBottom()>bottom
            if(isFirstOfGroup(index+1)){
                bottom=Math.min(child.getBottom(),bottom);
            }
            c.drawRect(0, top, right, bottom, mbgPaint);
            mTextPaint.getTextBounds(tag, 0, tag.length(), mBounds);
            c.drawText(tag, left, bottom - mTopHeight/2+mBounds.height()/2,
                    mTextPaint);
        }



    }

    /**
     * 绘制Item分类头部
     */
    @Override
    public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
        super.onDraw(c, parent, state);
        int left=parent.getPaddingLeft()+outPadding;
        int right=parent.getWidth();
        //getChildCount：得到当前页面的child，去计算真实的position
        for(int i=0;i!=parent.getChildCount();i++){
            View child=parent.getChildAt(i);
            //计算真实的position
            int index=parent.getChildAdapterPosition(child);
            String tag = getTitleName(index);
            L.e("onDraw","i:"+i+",index:"+index);
            if(isFirstOfGroup(index)){
                int top=child.getTop()-mTopHeight;
                int bottom=child.getTop();
                c.drawRect(0,top,right,bottom,mbgPaint);
                mTextPaint.getTextBounds(tag,0,tag.length(),mBounds);
                c.drawText(getTitleName(index),left,bottom-mTopHeight/2+mBounds.height()/2,mTextPaint);
            }
        }
    }

    /**
     * 为满足添加的item，增加顶部的padding
     */
    @Override
    public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
        super.getItemOffsets(outRect, view, parent, state);
        //利用parent，得到view的位置（在总的adapter中的位置）
        int index=parent.getChildAdapterPosition(view);
        //使满足条件的item，顶部多出 mTopHeight 的距离
        if(isFirstOfGroup(index)){
            outRect.top=mTopHeight;
        }
    }
}
```

[参考文章](http://www.jianshu.com/p/9306b365da57?utm_campaign=hugo&utm_medium=reader_share&utm_content=note)



