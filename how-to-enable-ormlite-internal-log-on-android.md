---
title: How to enable ORMLite internal log on Android
date: '2013-04-19 13:10:27 +0800'
---

# 2013-04-19  How to enable ORMLite internal log on Android

When using ORM system sometimes we want to what SQLs are executed at background to understand how it works. The ORMLite support several different log system, like SLF4J,COMMONS\_LOGGING, LOG4J and ANDROID native log android.util.Log. It will use Android log for internal log by default. In code `com.j256.ormlite.android.AndroidLog` method `isLevelEnabledInternal`, it will determinate if log is enabled by `Log.isLoggable`

```text
private final static String ALL_LOGS_NAME = "ORMLite";
...
return Log.isLoggable(className, androidLevel) || Log.isLoggable(ALL_LOGS_NAME, androidLevel);
```

That means there are two ways to enable ORMLite internal log.

1. You can change the default level by setting a system property: 'setprop log.tag. ' Where level is either VERBOSE, DEBUG, INFO, WARN, ERROR, ASSERT, or SUPPRESS. SUPPRESS will turn off all logging for your tag.
2. You can also create a local.prop file that with the following in it: 'log.tag.=' and place that in /data/local.prop.

The YOUR\_LOG\_TAG could be any ORMLite short class name or "ORMLite" for all of them. So that you can enable ORMLite internal log like this:

```text
$ adb shell
# setprop log.tag.ORMLite DEBUG
```

Notice that setprop is temporary until you reboot your device, even on rooted phones. You can persist properties through reboots if you write them into local.prop which is only possible on rooted phones.

