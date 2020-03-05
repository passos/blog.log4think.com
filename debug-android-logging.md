---
title: How to debug with Android Logging
date: '2010-11-12 18:15:39 +0800'
---
# AP Logger Architecture

![AP Logger Architecture](http://log4think.com/wp-content/uploads/2010/11/aplogd.jpg)

The above image shows the architecture of Android logging system.It provides a java class for logging named android.util.Log. It also provides log macros for native C applications in liblog.

There are four log devices in the kernel. Three for user space log: `/dev/log/main`, `/dev/log/radio`, `/dev/log/events`. One for kernel space log: `/dev/log/kernel`.

For user space applications, those binary log messages will be written to `/dev/log/events`. Those log messages with the tag "HTC_RIL" "RILJ" "RILC" "RILD" "RIL" "AT" "GSM" "STK" will be written to `/dev/log/radio`. Other log messages will be written to `/dev/log/main`.

The log devices named `/dev/log/kernel` is for kernel log message collection. A console is registered in `/dev/log/kernel` and collect all the `printk` output to the device. It will output kernel log messages with the same log format as other log devices.`Logcat` is a tool provided by Android. It could read log messages from log devices and output to the console or to a file. You can find the detail usage later. 

An `aplog` daemon is added for offline log. A filter is added to do some security checking.

## Logging interface For Java applications

### Logging class Introduction

Class Name: `android.util.Log`

General method:

     Log.v()
     Log.d()
     Log.i()
     Log.w()

The order in terms of verbosity, from least to most is `ERROR, WARN, INFO, DEBUG, VERBOSE`. `VERBOSE` should never be compiled into an application except during development. `DEBUG` logs are compiled in but stripped at runtime. `ERROR`, `WARN` and `INFO` logs are always kept. 

>TIP: A good convention is to declare a TAG constant in your class: `private static final String TAG = "TAG_MyActivity";`>and use that in subsequent calls to the log methods. `Log.v(TAG, "index=" + i);`When you're building the string to pass into Log.d, Java uses a StringBuilder and at least three allocations occur: the StringBuilder itself, the buffer, and the String object. Realistically, there is also another buffer allocation and copy, and even more pressure on the GC. That means that if your log message is filtered out, you might be doing significant work and incurring significant overhead.

For more details, please visit [Android log reference](http://developer.android.com/reference/android/util/Log.html)

#### Program Example

    package com.android.hello;
    import android.app.Activity;
    import android.os.Bundle;
    import android.widget.TextView;
    import android.util.Log; /*import log class*/

    private static final String TAG = "MyActivity"; /* define log tag*/

    public class !HelloAndroid extends Activity {
        /** Called when the activity is first created. */
        @Override
        public void onCreaipte(Bundle savedInstanceState) {
            super.onCreate(savedInstanceState);

            TextView tv = new TextView(this);
            tv.setText("Hello, Android");
            setContentView(tv);

            Log.i(TAG, "this is a log.i message");
            Log.v(TAG, "test is a log.v message");
            Log.d(TAG, "test is a log.d message");
            Log.w(TAG, "test is a log.w message");
            Log.e(TAG, "test is a log.e message");
        }
    }

## Logging interface For Native applications

Header File `include <cutils/log.h>`###Logging Macros

Common Logging Macros

    LOGV LOGD LOGI LOGW LOGE

Condition Logging Macros

    LOGV_IF LOGD_IF LOGI_IF LOGW_IF LOGE_IF

The definition is as below:

    #define CONDITION(cond) (__builtin_expect((cond)!=0,0))
    #define LOGV_IF(cond, ...)   ( (CONDITION(cond)) ?((void)LOG(LOG_VERBOSE, LOG_TAG, VA_ARGS)) : (void)0 )

#### Logging Macros overview

API for sending log output.

>NOTE:
>
> 1.    You should define LOG_TAG in your C source code firstly.
> 2.    To build out C/C++ applications outside android, you should add `LOCAL_SHARED_LIBRARIES := liblog libcutils` in your Android.mk file

#### Program Example

    #include <stdio.h>
    #include <cutils/log.h> /* log header file*/
    #include <cutils/properties.h>

    /* define log tag */
    #ifdef LOG_TAG
    #undef LOG_TAG
    #define LOG_TAG "app"
    #endif
    int main()
    {
        LOGV("Verbose: _app");
        LOGD("Debug: _app");
        LOGI("Info: _app");
        LOGW("Warn: _app");
        LOGE("Error: _app");
        printf("Hello Android.\n");
        return 0;
    }

## Log command on Android

Command location

    /system/bin/log

Command usage

    log [-p priorityChar] [-t tag] message

priorityChar should be one of : `v, d, i, w, e`## Log format on Android
The format of a log messages is

    tv_sec	 tv_nsec	 priority	  pid	 tid 	 tag 	 messageLen 	  Message

- tag: log tag
- tv_sec & tv_nsec: the timestamp of the log messages
- pid: the process id of where log messages come from
- tid: the thread id
- Priority value is one of the following character values, ordered from lowest to highest priority:

    * V - Verbose (lowest priority)*
    * D - Debug*
    * I - Info*
    * W - Warning*
    * E - Error*
    * F - Fatal*
    * S - Silent (highest priority, on which nothing is ever printed)*

