---
title: 解决搜狗输入法Ubuntu 14.04下黑块状态条
date: '2014-04-23 19:07:59 +0800'
---
搜狗的Linux输入法正式版发布之时，恰好Ubuntu 14.04 LTS也刚刚发布正式版。尝试安装搜狗的Linux输入法之后，出现了一个小小的问题：输入法状态条是一个黑色块。

我的Linux桌面用的是i3平铺式桌面管理器，多显示器环境下非常好用，[强烈推荐](http://i3wm.org)。除此之外，GUI底层用的是KDE。

做了一番功课之后，结果发现因为搜狗要支持皮肤，所以那个状态条是半透明状态的。而我目前的默认环境下不支持compositor窗口管理器，无法处理半透明窗口的效果，于是就只能显示一个黑色块。

解决办法是安装[Compton](https://github.com/chjj/compton)，以支持窗口的半透明效果。Ubuntu默认情况下没有可用的APT源，有两种办法安装：一个是从源码编译（不赘述），另外一个是使用一个第三方的源。

## 安装第三方源并安装compton

    sudo apt-add-repository ppa:richardgv/compton
    sudo apt-get update && sudo apt-get install compton

## 配置compton
编辑文件 `~/.compton.conf`，输入如下内容

    backend = "glx";
    paint-on-overlay = true;
    glx-no-stencil = true;
    glx-no-rebind-pixmap = true;
    vsync = "opengl-swc"; 

    # These are important. The first one enables the opengl backend. The last one
    # is the vsync method. Depending on the driver you might need to use a
    # different method.
    # The other options are smaller performance tweaks that work well in most
    # cases.
    # You can find the rest of the options here:
    # https://github.com/chjj/compton/wiki/perf-guide, and here:
    # https://github.com/chjj/compton/wiki/vsync-guide

    # Shadow
    shadow = false;          # Enabled client-side shadows on windows.
    no-dock-shadow = true;      # Avoid drawing shadows on dock/panel windows.
    no-dnd-shadow = true;       # Don't draw shadows on DND windows.
    clear-shadow = true;        # Zero the part of the shadow's mask behind the window (experimental).
    shadow-radius = 7;      # The blur radius for shadows. (default 12)
    shadow-offset-x = -7;       # The left offset for shadows. (default -15)
    shadow-offset-y = -7;       # The top offset for shadows. (default -15)
    shadow-exclude = [
        "! name~=''",
        "n:e:Notification",
        "n:e:Plank",
        "n:e:Docky",
        "g:e:Synapse",
        "g:e:Kupfer",
        "g:e:Conky",
        "n:w:*Firefox*",
        "n:w:*Chrome*",
        "n:w:*Chromium*",
        "class_g ?= 'Notify-osd'",
        "class_g ?= 'Cairo-dock'",
        "class_g ?= 'Xfce4-notifyd'",
        "class_g ?= 'Xfce4-power-manager'"
    ];                                                                                                                                                                                                            

    # The shadow exclude options are helpful if you have shadows enabled. Due to
    # the way compton draws its shadows, certain applications will have visual
    # glitches
    # (most applications are fine, only apps that do weird things with xshapes or
    # argb are affected).
    # This list includes all the affected apps I found in my testing. The "!
    # name~=''" part excludes shadows on any "Unknown" windows, this prevents a
    # visual glitch with the XFWM alt tab switcher.                                                                                                                                                               

    # Fading
    fading = true; # Fade windows during opacity changes.
    fade-delta = 4; # The time between steps in a fade in milliseconds. (default 10).
    fade-in-step = 0.03; # Opacity change between steps while fading in. (default 0.028).
    fade-out-step = 0.03; # Opacity change between steps while fading out. (default 0.03).
    #no-fading-openclose = true; # Fade windows in/out when opening/closing

    detect-client-opacity = true; # This prevents opacity being ignored for some apps. For example without this enabled my xfce4-notifyd is 100% opacity no matter what.

    # Window type settings
    wintypes:
    {
      tooltip = { fade = true; shadow = false; };
    };

重点是其中 shadow 一项的值设置为 false 。

## 自启动
最后，修改i3配置文件 `~/.i3/config`，在最后加入下面的代码，实现自动启动compton和搜狗输入法

    # auto start commands
    exec --no-startup-id fcitx -r
    exec --no-startup-id fcitx-qimpanel
    exec --no-startup-id compton -b

安装完成了，系统也顺便带了半透明和淡入淡出效果。

