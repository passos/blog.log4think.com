---
title: 制作ASCII字符动画
date: '2011-03-08 03:07:00 +0800'
---
看过Matrix的同学应该还记得，在母舰上一直在计算的电脑屏幕在Neo觉醒的时候，不停的下落的杂乱无章的字符组成了Neo当时所处的场景。其实利用开源和免费的工具，我们可以将现有的视频转换为ASCII字符格式的视频。

需要用到的工具是QQ影音、Ascgen dotNET、MPlayer和Mencoder。QQ影音用于提取视频和音频；MPlayer用于自动截图，可以从www.mplayerhq.hu下载，其中应该包含了mencoder.exe。如果没有的话，可以去下一个mediacoder，里面有mencoder这个工具。Ascgen dotNET用于将图片专为ASCII的，可以从http://ascgendotnet.jmsoftware.co.uk/download下载；最后使用mencoder将图片重新编码为视频。

第一步，找到需要转换的视频，利用QQ影音的"转码/截取/合并"功能，将想要转换的视频和音频分别截取出来。

第二步，用MPlayer打开要前面准备好的视频，播放的同时按"Shift-D"也就是启动"开始/停止自动截图"功能，截取的图片默认是保存在`C:\Documents and Settings\Administrator\.smplayer\screenshots`下面。每分钟的视频大概会有1500多张图片。

第三步，使用`Ascgen dotNET`的`Batch Conversion`功能，将截取的所有图片文件或目录加入到列表中，设置好输出目录，选择输出为jpg格式、75%大小，勾选Colour选项，然后点Convert开始转换。这一步会将原始图片转换为以ASCII字符构成的图片。

最后一步，在转换好的ASCII图片目录中，使用mencoder用命令行编码为视频：
```
[mencoder.exe所在的目录]\mencoder mf://*.jpg -mf w=[生成图片的宽度]:h=[生成图片的高度]:fps=[原始视频的fps]:type=jpg
-ovc lavc  -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -audiofile [第一步提取出来的mp3文件] -o output.avi
```
其中"生成图片的高度和宽度"可以从查看生成的图片的属性，在"摘要"中有图片的高度和宽度信息。原始视频的fps值一般情况下是30，可以用QQ影音打开视频文件，右键点视频窗口--文件信息--"视频帧率"中查到，也可以查看视频文件的"属性"--摘要--"帧速率"。如果不需要声音的话，可以去掉命令行中"-audiofile [第一步提取出来的mp3文件]"这一部分。

最终在当前目录下生成的output.avi文件就是转换好的ASCII字符视频了。

