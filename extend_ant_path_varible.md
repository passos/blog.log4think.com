---
title: ant 中通过重新定义  project.all.jars.path 在 classpath 中引入外部 jar 文件
date: '2013-01-21 12:54:12 +0800'
---
在 Android 开发中，除了通常在 Eclipse 中的编译方法之外，有的时候为了进行持续集成，可能还需要用 ant 进行自动化编译。Android SDK 本身已经提供了默认的ant编译脚本，就在每个工程下的 `build.xml` 中，其中引用了SDK的编译脚本`${sdk_dir}/tools/ant/build.xml` 。 通常情况下，在工程根目录下直接执行 ant debug 即可进行一次正常的 build。默认的 classpath 会包括 libs 目录下的所有 jar 文件。但是如果工程中使用了 USER LIBRARY，或者引用了外部的 jar 文件，那么在编译中就可能会遇到问题，因为这些 jar 文件不会被自动包含在 classpath 中，这时就要扩展 ant 的 path 变量，把自己的 jar 文件加入到 classpath 中。

通过察看 sdk 提供的`build.xml`编译脚本，可以发现 javac 使用的 classpath 定义如下：
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

其中 `project.all.jars.path` 包含了所有的jar文件，我们可以通过在工程目录下的 `build.xml` 中重新定义这个变量来引入其他的jar文件。例如在我的工程中，引用了ormlite这个ORM库，为了能够在开发中使用"attach source"察看源码，该jar文件不能放在libs目录中，因为Eclipse不允许对libs目录中的jar文件 `attach source`。因此我将此文件放到了libs/ormlite目录中，为了能够将这两个jar文件加入到classpath中，就要重新定义 `project.all.jars.path` 这个元素。

基本思路是，重新定义 `-pre-compile` 这个target，在其中重新定义 `project.all.jars.path` 的值。
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
