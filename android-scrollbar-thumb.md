---
title: Android的滚动条实现细节
date: '2012-09-22 13:37:14 +0800'
---
在Android的UI系统中，每个View都有一个ScrollabilityCache的单例对象。该对象定义在View.java中，用于保存ScrollBar的相关实例和属性(ScrollBar实际上是一个ScrollBarDrawable对象)，并且实现了淡入淡出动画效果的线程代码。这些会在该View的所有ScrollBar中共用。

以垂直滚动条为例，画出滚动条的过程大致是:
```
1. View::Draw
2. View::onDrawScrollBars
scrollBar.setParameters(computeVerticalScrollRange(),
            computeVerticalScrollOffset(),
            computeVerticalScrollExtent(), true);

3. View::onDrawVerticalScrollBar
    scrollBar.draw

4. ScrollBarDrawable::draw

Rect r = getBounds();

if (drawTrack) {
    drawTrack(canvas, r, vertical);
}

if (drawThumb) {
    int size = vertical ? r.height() : r.width();
    int thickness = vertical ? r.width() : r.height();
    int length = Math.round((float) size * extent / range);
    int offset = Math.round((float) (size - length) * mOffset / (range - extent));

    // avoid the tiny thumb
    int minLength = thickness * 2;
    if (length < minLength) {
        length = minLength;
    }
    // avoid the too-big thumb
    if (offset + length > size) {
        offset = size - length;
    }

    drawThumb(canvas, r, offset, length, vertical);
}
```
