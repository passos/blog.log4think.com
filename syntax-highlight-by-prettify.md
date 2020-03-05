---
title: 利用google-code-prettify做网页内源码的语法高亮
date: '2010-09-16 20:54:23 +0800'
---
由于HTML本身并不认空格，因此网页中如果要展现程序代码通常会用`````标签来保留缩进、空格等格式。

作为程序员的Blog，对此的需求更是高很多。单单利用`````标签保留代码格式还不能让代码看起来很漂亮，通常在IDE中都会有语法高亮的特性，利用<a title="google-code-prettify" href="http://code.google.com/p/google-code-prettify/">google-code-prettify</a>可以很方便的在网页中实现这一功能。

官方主页在此：http://code.google.com/p/google-code-prettify/
下载最新的源码之后，在网页的HEAD部分加入以下两行

```
<link href="prettify.css" type="text/css" rel="stylesheet" />
<script type="text/javascript" src="prettify.js"></script>
```

然后在需要高亮代码的地方，将代码放在 pre 标签中。在class中lang-X的X可以是下面几种语言之一：
bsh", "c", "cc", "cpp", "cs", "csh", "cyc", "cv", "htm", "html", "java", "js", "m", "mxml", "perl", "pl", "pm", "py", "rb", "sh", "xhtml", "xml", "xsl"

如果是在Wordpress中的话，可以使用Code Block Enabler这个插件。

在配置完成之后，还有一个小小的缺憾。通常程序的代码都是使用等宽字体，最常见的就是Courier New字体。而google-code-prettify并没有设置代码的字体。简单的对其css文件作一个小小的修改即可实现这一点，打开WordPress的wp-content/plugins/code-block-enabler/prettify.css文件，找到pre.prettyprint的定义后面加上字体的定义，改为：

```
<pre class="prettyprint lang-css">
pre.prettyprint { padding: 2px; border: 1px solid #888; font-family: Courier New; font-size: 9px;}
```