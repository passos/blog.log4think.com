---
title: ant 中通过重新定义  project.all.jars.path 在 classpath 中引入外部 jar 文件
date: '2013-01-21 12:54:12 +0800'
---
在Android开发中，除了通常在Eclipse中的编译方法之外，有的时候为了进行持续集成，可能还需要用ant进行自动化编译。Android SDK本身已经提供了默认的ant编译脚本，就在每个工程下的build.xml中，其中引用了SDK的编译脚本${sdk_dir}/tools/ant/build.xml 。 通常情况下，在工程根目录下直接执行 ant debug 即可进行一次正常的build。默认的classpath会包括libs目录下的所有jar文件。但是如果工程中使用了USER LIBRARY，或者引用了外部的jar文件，那么在编译中就可能会遇到问题，因为这些jar文件不会被自动包含在classpath中，这时就要扩展ant的path变量，把自己的jar文件加入到classpath中。

通过察看sdk提供的build.xml编译脚本，可以发现javac使用的classpath定义如下：
```
<path id="project.javac.classpath">
<path refid="project.all.jars.path"></path>

<path refid="tested.project.classpath"></path>
</path>

<javac encoding="${java.encoding}"
        source="${java.source}" target="${java.target}"
        debug="true" extdirs="" includeantruntime="false"
        destdir="${out.classes.absolute.dir}"
        bootclasspathref="project.target.class.path"
        verbose="${verbose}"
        classpathref="project.javac.classpath"
        fork="${need.javac.fork}">
    <src path="${source.absolute.dir}"></src>
    <src path="${gen.absolute.dir}"></src>
    <compilerarg line="${java.compilerargs}"></compilerarg>
</javac>
```

其中 project.all.jars.path 包含了所有的jar文件，我们可以通过在工程目录下的buildxml中重新定义这个变量来引入其他的jar文件。例如在我的工程中，引用了ormlite这个ORM库，为了能够在开发中使用"attach source"察看源码，该jar文件不能放在libs目录中，因为Eclipse不允许对libs目录中的jar文件"attach source"。因此我将此文件放到了libs/ormlite目录中，为了能够将这两个jar文件加入到classpath中，就要重新定义 project.all.jars.path 这个元素。

基本思路是，重新定义-pre-compile这个target，在其中重新定义 project.all.jars.path 的值。
```
<target name="-pre-compile">
    <echo message="JARPATH=${toString:project.all.jars.path}"></echo>

<property name="ormlite.dir" value="${jar.libs.dir}/ormlite"></property>

<path id="ormlite.lib">
<path path="${toString:project.all.jars.path}"></path>

<pathelement location="${ormlite.dir}/ormlite-android-4.41.jar"></pathelement>

<pathelement location="${ormlite.dir}/ormlite-core-4.41.jar"></pathelement>
    </path>

<path id="project.all.jars.path">
<path refid="ormlite.lib"></path>
    </path>

    <echo message="JARPATH=${toString:project.all.jars.path}"></echo>
</target>
```
