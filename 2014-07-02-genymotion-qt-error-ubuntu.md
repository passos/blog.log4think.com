---
title: genymotion Qt error in Ubuntu
date: '2014-07-02 23:40:55 +0800'
---
When I was trying to install Genymotion on Ubuntu 14.04, I got this error

    Installing log handler
    Logging activities to file: /home/****
    Aborted (core dumped)

the log file /home/xx/.Genymotion/genymotion.log has the following message:

    ... [Genymotion] [Fatal] Cannot mix incompatible Qt library (version 0x40806) with this library (version 0x40804)

The reason of this error is that Genymotion has its own Qt library which is not compatable with the system Qt library.

To fix this error, we need to let genymotion use system's Qt library. The following commands can fix this issue

    sudo apt-get install libxi-dev libxmu-dev
    # go to your genymotion directory
    mkdir QtLibs && mv *Qt*.so* QtLibs

