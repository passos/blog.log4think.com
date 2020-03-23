---
title: Log4perl多个Appender重复输出日志的问题解决办法
date: '2013-10-17 12:11:36 +0800'
---

# 2013-10-17  Log4perl多个Appender重复输出日志的问题解决办法

Perl开发中会经常用到Log4perl来输出日志，例如有类似如下配置：

```text
log4perl.rootLogger = DEBUG, Screen
log4perl.logger.Utils = DEBUG, Screen

log4perl.appender.Logfile = Log::Log4perl::Appender::File
log4perl.appender.Logfile.filename = test.log
log4perl.appender.Logfile.layout = Log::Log4perl::Layout::PatternLayout
log4perl.appender.Logfile.layout.ConversionPattern = %r %F %L %m%n

log4perl.appender.Screen = Log::Log4perl::Appender::Screen
log4perl.appender.Screen.stderr = 1
log4perl.appender.Screen.layout = Log::Log4perl::Layout::PatternLayout
log4perl.appender.Screen.layout.ConversionPattern = %M | %m%n
```

结果发现Utils中的消息，一次debug调用会输出两条同样的消息。Google一查发现还很常见，老祖宗Log4j下面也有类似的问题。作者在[FAQ中](http://log4perl.sourceforge.net/releases/Log-Log4perl/docs/html/Log/Log4perl/FAQ.html#a6c81)提到了这个问题，解决办法除了与Log4j类似的解决方案之外，Log4perl还有一个简单的办法，只要在配置加入一行

```text
log4perl.oneMessagePerAppender = 1 
```

