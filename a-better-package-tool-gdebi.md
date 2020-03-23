---
title: 可自动安装依赖的Ubuntu离线包安装工具 gdebi
date: '2014-04-30 13:00:48 +0800'
---

# 2014-04-30  可自动安装依赖的Ubuntu离线包安装工具 gdebi

Ubuntu下，通用的在线包管理工具是`apt`，但是对于下载好的离线deb包，我们通常会用`dpkg -i xxx.dev`来安装，但是这样常常会遇到依赖包不存在而无法安装的错误。dpkg不会为我们自动解决包依赖的问题，也不会自动下载安装所依赖的包。 gdebi是一个类似的管理工具，但是会自动下载安装依赖。

对于一个离线包，只需要使用下面的命令即可自动下载安装，包括所有依赖包

```text
gdebi package_name.deb
```

可以使用下面这条命令安装这个工具

```text
sudo apt-get install gdebi
```

better-package-tool-gdebi

