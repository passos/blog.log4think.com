---
title: 在Eclipse中查看Android SDK的源代码
date: '2010-08-27 15:43:56 +0800'
---

# 2010-08-27  在Eclipse中查看Android SDK的源代码

via [https://stuffthathappens.com/blog/2008/11/01/browsing-android-source-in-eclipse/](https://stuffthathappens.com/blog/2008/11/01/browsing-android-source-in-eclipse/)

Google的Android SDK中包含一个android.jar文件，里面有Android所有的公开类的API接口。同时，Google还提供了一个Eclipse插件，可以很容易的开始进行开发。但是，这里并没有一个类似于androidSrc.jar的文件，因此当我们试图在Eclipse去查看Android SDK的源代码的时候，会得到"源码无法找到"这样一个页面

Google已经发布了Android所有的源代码，很大。要在Eclipse中查看Android的源代码，需要去[https://source.android.com/](https://source.android.com/)（国内需翻墙），Get Source那个页面内按照指示一步步的将所有的东西都通过Git弄下来。很值得抽出一个晚上的时间来做这件事，因为如果能够随时查看源码，对于理解SDK如何工作的是非常有帮助的。

## 链接到Eclipse

现在我们有了源码，应该可以告诉Eclipse如何找到它了。右键点击android.jar--属性，可是却发现了这样的信息："Modifications Not Allowed"

嗯....那段话的大意是，当前的class path的设置属于'Android Library'，不允许用户修改。好吧，只能去看看ADT的源码了，看能否找到什么办法。

## 查看ADT源码

当下载完Android源码之后，我们已经得到了所有内容，包括：操作系统、Dalvik虚拟机、Eclipse插件、公开的SDK...等等。

在 com.android.ide.eclipse.adt.project.internal 包里，我找到一个名为 AndroidClassspathContainerInitializer.java 的类，包含如下代码：

```text
IPath android_src = new Path(AdtPlugin.getOsAbsoluteAndroidSources());
```

好，再来看看 AdtPlugin.java:

```text
/** Returns the absolute android sources path in the sdk */
public static String getOsAbsoluteAndroidSources() {
  return getOsSdkFolder() + getOsRelativeAndroidSources();
}

/** Returns the android sources path relative to the sdk folder */
public static String getOsRelativeAndroidSources() {
  return AndroidConstants.FD_ANDROID_SOURCES;
}
```

最后来看看 `AndroidConstants.java`: `public static final String FD_ANDROID_SOURCES = "sources";` 搞定！

## 解决方案 \#1

根据上面的分析，我们可以在android SDK的安装目录内创建一个sources目录，与android.jar位于同一个目录内。之后，我们可以在之前下好的Android源码中找到所有我们需要的代码。SDK的代码在frameworks/base/core/java，在这个目录下有一个android目录，我们需要将这个目录拷贝（链接）到SDK安装目录中的sources目录。你可能需要想想办法，把所有分散在不同Component的源码都弄到一起去。最终我们的目录结构大致如下：

```text
SDK_PATH
  |-- android.jar
  +--docs/...
  +--samples/...
  +--sources
       +--android
       |      ...accounts, annotation, app, bluetooth, etc...
       +--com/android/etc...
       +--dalvik/...
       +--java/...
       +--javax/...
```

我把所有这样的目录都弄进来了，但是没有详细记录。

译注： 上面的代码是适用于以前的老版本的ADT，目前最新版本的ADT已经不适用了。经过查看源代码发现，最新版本的ADT需要在SDK目录下的platforms\android-X对应的目录下建立sources目录，其中X是3、4、7、8之一的数字，对应不同的SDK版本。这也是一个比较合理的方案，毕竟不同版本的SDK的源码还是不一样的。

如果你在Linux或者Mac下工作，sources的源码目录结构可以用我写的如下的一个Shell脚本来完成这个事情，在Android的源码目录下运行这个脚本，然后会在 `~/workspace/src-tree` 创建"几乎"所有Java源码的soft symbol link。之后也可以用tar带-h参数打包到windows下使用。你可以根据自己的需求修改一下。

```text
simon@simon-desktop:~/bin$ cat make-src-tree
#!/bin/bash
# Author: Simon Liu <simon@log4think.com>
# Date: 2010-08-27
# License: MIT

curr_dir=$PWD
dest_dir=~/workspace/src-tree
if [ ! -z "$1" ]; then
        dest_dir=$1
fi

rm -rf $dest_dir
mkdir -p $dest_dir

for d in $(find -path .repo -prune \
    -or -path .git -prune \
    -or -path "*/src/com/*" -type d -print \
    -or -path "*/src/org/*" -type d -print \
    -or -path "*/java/com/*" -type d -print \
    -or -path "*/java/org/*" -type d -print \
    -or -path "*/java/android/*" -type d -print \
    -or -path "*/java/javax/*" -type d -print)
do
        sd=$(echo $d | sed 's#.*/src/\(.*\)/#\1/#g' | sed 's#.*/java/\(.*\)/#\1/#g')
        echo ";; $sd"

        mkdir -p $dest_dir/$sd
        for f in $(cd $d; find . -mindepth 0 -maxdepth 1 -type f | sed 's#^./##g'); do
                echo "        $f"
                ln -s $curr_dir/$d/$f $dest_dir/$sd/$f
        done
done
```

现在，当我再去查看Android SDK类的时候，可以看到源码了

## 解决方案 \#2

如果你实在不愿意把所有的Android源码拷贝到SDK目录里面去，也可以创建一个Eclispe User Library并把源码附加上去。

via [https://stuffthathappens.com/blog/2008/11/01/browsing-android-source-in-eclipse/](https://stuffthathappens.com/blog/2008/11/01/browsing-android-source-in-eclipse/)

