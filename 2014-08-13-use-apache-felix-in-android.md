---
title: 在Android中使用OSGi框架(Apache Felix)
date: '2014-08-13 15:26:12 +0800'
---
本文描述了如何在Android中使用Apache Felix

## Dalvik VM
Android允许开发者使用Java开发应用，但出于某些原因，代码实际是运行在名为Dalvik的一个针对移动设备平台的虚拟机上，而不是标准的Java虚拟机。Dalvik并不使用标准的Java字节码格式，而是使用Android SDK中的一个工具`dx`将由Java编译出来的类文件转换为另外一种类文件格式(.dex格式)。这个转换是在编译期完成的。

## 准备Bundles
虽然Felix从1.0.3开始内置了Android的支持，但是想要成功的让它跑起来还是需要费点力气。我们仍然需要安装Android SDK，并且PATH环境变量中包含Android SDK的工具目录`<android_SDK_HOME>/tools`。

*第一步：* 每一个用到的Jar文件，无论是Felix库还是你自己写的Bundle，都需要包含对应的DEX。也就说，需要为jar文件创建对应的dex文件：

    dx --dex --output=classes.dex JAR_file.jar

然后将这个dex文件加入到jar文件中：

    aapt add JAR_file.jar classes.dex

*第二步：* 将处理过的jar文件传到模拟器（或真机）中：

    adb push JAR_file.jar path_emulator/JAR_file.jar

*第三步：* 以演示代码为例，准备Felix的jar文件和Bundle的jar文件：

目录结构

    osgi-android: /
    \- bin
    \- bundle
    \- conf
    \- felix.sh

准备Felix jar文件

    export PATH=<path-to-android>/tools:$PATH
    cd bin
    dx --dex --output=classes.dex felix.jar
    aapt add felix.jar classes.dex

准备bundle的jar文件

    cd bundle
    dx --dex --output=classes.dex     org.apache.felix.shell-1.0.0.jar
    aapt add org.apache.felix.shell-1.0.0.jar classes.dex
    dx --dex --output=classes.dex org.apache.felix.shell.tui-1.0.0.jar
    aapt add org.apache.felix.shell.tui-1.0.0.jar classes.dex
    dx --dex --output=classes.dex EnglishDictionary.jar
    aapt add EnglishDictionary.jar classes.dex
    dx --dex --output=classes.dex FrenchDictionary.jar
    aapt add FrenchDictionary.jar classes.dex
    dx --dex --output=classes.dex SpellChecker.jar
    aapt add SpellChecker.jar classes.dex

复制到模拟器中

    cd osgi-android
    find * -type f -exec adb push {} /data/felix/{} \;

## 启动Felix

完成上面的步骤之后，现在可以准备在Android上启动Felix和Bundle了

    adb shell
    cd /data/felix
    sh felix.sh

`felix.sh`是一个shel脚本，用于启动Felix main class。

    /system/bin/dalvikvm -Xbootclasspath:/system/framework/core.jar -classpath bin/felix.jar org.apache.felix.main.Main

如果一切顺利，现在你应该能看到Felix的命令行shell了。输入`help`可以看到命令说明。

现在可以安装EnglishDictionary,FrenchDictionary和SpellChecker来试试看Felix是否工作正常。这里有几个Apache Felix的示例：[Apache Felix 教程例子2](http://felix.apache.org/site/apache-felix-tutorial-example-2.html)，[Apache Felix 教程例子2b](http://felix.apache.org/site/apache-felix-tutorial-example-2b.html)，[Apache Felix 教程例子5](http://felix.apache.org/site/apache-felix-tutorial-example-5.html)。

- *EnglishDictionary* - 提供一个字典服务，支持下面几个词"welcome", "to", "the", "osgi", "tutorial"
- *FrenchDictionary* -  提供一个字典服务，支持下面几个词"bienvenue", "au", "tutoriel", "osgi"
- *SpellChecker* - 提供一个拼写检查服务，可以检查第一个英文此单的几个单词

在Felix Shell中启动Bundle

    start file:bundle/EnglishDictionary.jar
    start file:bundle/FrenchDictionary.jar
    start file:bundle/SpellChecker.jar

## 嵌入Felix

Apache Felix也可以被集成到Android的应用中。只需要在Activity的onCreate中嵌入Felix，然后用上面的办法启动bundle即可。

## 下载

上面的演示代码[在此下载](http://felix.apache.org/site/documentation.data/osgi-android%20-%20felix%201.4,%20android%20SDK%201.0.zip)

via [source](http://felix.apache.org/site/apache-felix-framework-and-google-android.html)

