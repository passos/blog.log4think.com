---
title: 在Android中使用OSGi框架(Knopflerfish)
date: '2014-08-13 15:51:00 +0800'
---

# 2014-08-13  在Android中使用OSGi框架\(Knopflerfish\)

OSGi是用Java实现的一个模块化服务平台。每个模块被称之为Bundle，可以提供服务，也可以在不重启OSGi框架的情况下被安装或卸载。Knopflerfish是一个完全开源的OSGi R4.2标准的实现。

Android能够无缝的集成现有的Java代码，尽管使用的是与现有java字节码格式不兼容的虚拟机Dalvik，但是它可以轻松的将现有的jar文件和类转换为Android使用的Dalvik字节码格式。由于OSGi框架自身和Bundle都只是普通的jar文件，所以他们都应该可以在Android上运行。事实上，大多数时候是没问题的。

> 注意：这里只是如何在Android中嵌入OSGi系列文章的第一部分

如果只是想让OSGi框架在Android上跑起来，那么只需要编译Knopflerfish的Android版本，复制到设备上，然后就可以通过命令行启动起来了（见[上一篇文章](http://log4think.com/use-apache-felix-in-android/)和[这里](http://log4think.com/use-apache-felix-in-android/)）。

现在来看看如何将Knopflerfish和一系列Bundle嵌入到Android应用中，并且从应用中启动和管理OSGi框架和Bundle。

通过代码启动OSGi大概需要下面这几个步骤：

1. 创建framework实例（通过framework factory）
2. 初始化framework
3. 设置initlevel，并启动/安装 bunldes
4. 为所有的initlevel重复前述步骤
5. 设置startlevel
6. 启动framework

## 嵌入Framework

现在创建一个Android应用，包含一个Actviity。然后在app中引入`framework.jar`，这样就可以通过一个`FrameworkFactory`创建OSGi的framework实例了。

```text
import org.knopflerfish.framework.FrameworkFactoryImpl;
import org.osgi.framework.BundleException;
import org.osgi.framework.launch.Framework;
import org.osgi.framework.launch.FrameworkFactory;
...
private Framework mFramework;
...
Dictionary fwprops = new Hashtable();
// add any framework properties to fwprops
FrameworkFactory ff = new FrameworkFactoryImpl();
mFramework = ff.newFramework(fwprops);
try {
    mFramework.init();
} catch (BundleException be) {
    // framework initialization failed
}
```

引入的jar文件不需要dex化，后面build的时候会自动完成这一步的。

## Bundle文件dex化

现在bundle的jar文件可以被添加到应用中了，可以作为raw资源放在`res/raw`下面，也可以放在`assets/bunldes`。后面这种方式有一个优势：不需要被重命名，而且res资源的名字数量是有限的。

Bundle的jar文件需要被转换成dex格式，下面这个简单的脚本可以完成这件事：

```text
dexify() {
    for f in $*; do
        tmpdir="`mktemp -d`"
        tmpfile="${tmpdir}/classes.dex"
        dx --dex --output=${tmpfile} ${f}
        aapt add ${f} ${tmpfile}
        rm -f ${tmpfile}
        rmdir ${tmpdir}
    done
}
```

然后就可以通过命令`dexify assets/bundles/*`将bundles转换为dex文件。如果是按照Knopflerfish的[教程](http://www.knopflerfish.org/releases/3.2.0/docs/android_dalvik_tutorial.html)编译的Knopflerfish，那么不需要将这些bundle的jar文件dex化，但是必须从knopflerfish的framework.jar文件中去掉classes.dex。

## 安装、启动Bundles

下面这段代码可以帮助启动bundle，并设置initlevel/startlevel。

```text
private void startBundle(String bundle) {
    Log.d(TAG, "starting bundle " + bundle);
    InputStream bs;
    try {
        bs = getAssets().open("bundles/" + bundle);
    } catch (IOException e) {
        Log.e(TAG, e.toString());
        return;
    }

    long bid = -1;
    Bundle[] bl = mFramework.getBundleContext().getBundles();
    for (int i = 0; bl != null && i < bl.length; i++) {
        if (bundle.equals(bl[i].getLocation())) {
            bid = bl[i].getBundleId();
        }
    }

    Bundle b = mFramework.getBundleContext().getBundle(bid);
    if (b == null) {
        Log.e(TAG, "can't start bundle " + bundle);
        return;
    }

    try {
        b.start(Bundle.START_ACTIVATION_POLICY);
        Log.d(TAG, "bundle " + b.getSymbolicName() + "/" + b.getBundleId() + "/"
                + b + " started");
    } catch (BundleException be) {
        Log.e(TAG, be.toString());
    }

    try {
        bs.close();
    } catch (IOException e) {
        Log.e(TAG, e.toString());
    }
}

private void installBundle(String bundle) {
    Log.d(TAG, "installing bundle " + bundle);
    InputStream bs;
    try {
        bs = getAssets().open("bundles/" + bundle);
    } catch (IOException e) {
        Log.e(TAG, e.toString());
        return;
    }

    try {
        mFramework.getBundleContext().installBundle(bundle, bs);
        Log.d(TAG, "bundle " + bundle + " installed");
    } catch (BundleException be) {
        Log.e(TAG, be.toString());
    }

    try {
        bs.close();
    } catch (IOException e) {
        Log.e(TAG, e.toString());
    }
}

private void setStartLevel(int startLevel) {
    ServiceReference sr = mFramework.getBundleContext()
        .getServiceReference(StartLevel.class.getName());
    if (sr != null) {
        StartLevel ss =
            (StartLevel)mFramework.getBundleContext().getService(sr);
        ss.setStartLevel(startLevel);
        mFramework.getBundleContext().ungetService(sr);
    } else {
        Log.e(TAG, "No start level service " + startLevel);
    }
}

private void setInitlevel(int level) {
    ServiceReference sr = mFramework.getBundleContext()
        .getServiceReference(StartLevel.class.getName());
    if (sr != null) {
        StartLevel ss =
            (StartLevel)mFramework.getBundleContext().getService(sr);
        ss.setInitialBundleStartLevel(level);
        mFramework.getBundleContext().ungetService(sr);
        Log.d(TAG, "initlevel " + level + " set");
    } else {
        Log.e(TAG, "No start level service " + level);
    }
}
```

现在可以安装并启动bundle了

```text
setInitlevel(1);
installBundle("event_all-3.0.4.jar");
startBundle("event_all-3.0.4.jar");
// install/start other bundles...

setStartLevel(10);

try {
    mFramework.start();
} catch (BundleException be) {
    Log.e(TAG, be.toString());
    // framework start failed
}

Log.d(TAG, "OSGi framework running, state: " + mFramework.getState());
```

## 问题

如果你按照上文所述一步步做下来了，你可能会发现还是没法跑起来。由于framework的classloader是在运行期加载的bundle文件，Dalvik虚拟机会试图将优化过的dex类文件放到一个系统目录下面`/data/dalvik-cache`，但是没有root权限的普通应用程序是不能写入那儿的。

下回将如何解决这个问题。

via [source](http://nilvec.com/embedding-osgi-into-an-android-application-part-1.html)

