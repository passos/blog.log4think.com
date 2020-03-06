---
title: Facebook的Dalvik运行期补丁
date: '2014-09-02 22:24:42 +0800'
---
对于一个功能丰富的Android应用来说，要面对的挑战很多，其中很多问题绝大多数开发者都可能意识不到。Android应用的方法数量限制可能就是一个。

在一些传统的企业应用中，当处理跟业务数据相关的时候，通常不会将数据变量设置为公开访问 `public`，而是会用getter/setter这样的存取方法来封装访问数据模型中的私有变量。在一般的编程实践中，这是一个被推荐和鼓励的做法。但是其副作用是类文件中会产生大量的方法（每一个私有变量都对应着2个方法）。

这个副作用带来的问题是，当应用安装在一些老机型上的时候，可能导致Android的一个Bug[https://code.google.com/p/android/issues/detail?id=22586](https://code.google.com/p/android/issues/detail?id=22586)。原因在于，在应用的安装过程中，会运行一个程序（dexopt）去根据当前机型为应用做一些特定的准备和优化。dexopt中使用了一个固定大小的缓冲区（名为LinearAlloc）来存储应用中方法的信息。最新的几个Android版本中，该缓冲的大小是8MB或16MB。但是Froyo（2.2）和Gingerbread（2.3）只有5MB。因为老版Android的这个限制，当方法数量超过这个缓冲大小的时候，会导致应用崩溃。

解决办法之一是可以利用[https://android-developers.blogspot.hk/2011/07/custom-class-loading-in-dalvik.html](https://android-developers.blogspot.hk/2011/07/custom-class-loading-in-dalvik.html)提到的技术，将dex分成多个dex文件分别加载，首先加载核心dex，其他的模块和扩展功能放在其他的dex文件中。

但是某些时候，如果第二个dex包中的类需要被Android
Framework直接访问到的话，上述方案就是不可行的。此时必须要将第二个dex文件注入到Android的系统class loader中。这个一般情况下是无法做到的，但好在Android是开源的系统，可以利用Java的反射去修改Android内部的一些数据结构来解决这个问题。

这个方案在实际运行中，你会发现其实LinearAlloc不仅仅只是在dexopt中存在，而是在每个运行中的Android程序中都有它的身影。dexopt使用LinearAlloc储存dex文件的方法信息的时候，运行期的Android应用使用它访问实际用到的方法。如果在运行期将所有的dex文件都加载到一个进程中的话，实际的方法数量还是会超过限制。应用虽然可以启动但是很快就会崩溃。

看起来似乎要么只能精简应用的功能，要么就只能放弃支持Android部分版本而只支持最新的ICS以上的版本。

再次回头去看Android的源码，找到LinearAlloc缓冲的定义[https://github.com/android/platform_dalvik/blob/android-2.3.7_r1/vm/LinearAlloc.h#L33](https://github.com/android/platform_dalvik/blob/android-2.3.7_r1/vm/LinearAlloc.h#L33)，也许你能意识到：其实只要能将缓冲从5MB增加到8MB就可以安全运转了。

也许，可以使用JNI把当前的缓冲替换成一个更大的缓冲区。这个方案看起来太疯狂了。修改Java的Class Loader的内部是一回事儿，修改运行中的Davlik虚拟机的内部可是另外一回事儿--运行中的代码可能会很危险。但是仔细查看过代码、分析所有使用LinearAlloc的地方后发现，只要在应用启动的时候去做，应该没什么危险。所需要做的就是，找到LinearAlloc对象，锁定，然后替换缓冲。

事实上，只要找到它，后面的事情就很顺利了。在这里[https://github.com/android/platform_dalvik/blob/android-2.3.7_r1/vm/Globals.h#L519](https://github.com/android/platform_dalvik/blob/android-2.3.7_r1/vm/Globals.h#L519)，DvmGlobals对象中保存了LinearAlloc缓冲区。大概距离对象的开始地址700个字节的位置。从对象的开头开始扫描到这里风险很大，但是幸运的是，可以用距离一步之遥的vmList对象作为起点。这里包含了一个值，可以通过JNI和JavaVM的指针做比较。

最终方案是，找到vmList的值，扫描DvmGlobals对象找到匹配的位置，往后跳几个字节找到LinearAlloc的头，然后替换缓冲区。编写JNI扩展，嵌入到应用中，启动，然后应用应该可以正常运行在Gingerbread上了。

但是又有一个问题是，这个方案在Sumsung Galaxy S II上会失败，这可是最流行的运行Gingerbread的手机。

似乎三星对Android做了一些改动，导致这个方案的失败。其它的厂商可能会做同样的事情。所以这个方案的代码应该得更加健壮才行。

经过观察，在GS II上，LinearAlloc的缓冲区地址距离实际要找的地址只有4个字节。于是调整代码，如果在期望的地址没有找到LinearAlloc，那么就在附近几个字节的范围内查找。做这件事需要获取当前线程的内存映射表，确保没有在附近的查找过程中访问到无效地址（否则会立刻导致应用崩溃）。

（以上就是Facebook的故事，[Via](https://www.facebook.com/notes/facebook-engineering/under-the-hood-dalvik-patch-for-facebook-for-android/10151345597798920)

