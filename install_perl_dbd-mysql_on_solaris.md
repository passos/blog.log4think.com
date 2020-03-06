---
title: Solaris 下安装Perl的DBD-mysql模块失败的原因以及解决办法
date: '2005-07-16 11:41:04 +0800'
---
Solaris下安装Perl的`DBD::Mysql`模块，已经出了两次问题了。现总结如下：

问题一：无法找到mysql_config
1. 下载DBD-mysql-3.0000
2. 解压
3. make Makefile.PL
4. 提示找不到mysql_config

解决办法：
出现这个问题是因为没有将`mysql_config`加入环境变量PATH中，只要将`mysql/bin`目录加入到路径中就可以了。
```
PATH=$PATH:/usr/local/mysql/bin
export PATH
```
然后重新 `make Makefile.PL`

问题二：无法找到库 `libmysqlclient.so`
Solaris 的mysql发行版本的库文件都是.a的静态库，`DBD::Mysql`模块需要.so的动态库编译。可以下载带源码的Mysql自行编译出.so的动态库。

问题三：编译不通过
那是因为mysql_config给Makefile.PL的cflags参数不正确。在我的Solaris上，给的参数是 `-I/usr/local/mysql/include -Xa -xstrconst -mt -D_FORTEC_ -xarch=v9`，gcc 版本是 3.4.0，而`-Xa -xstrconst -mt -xarch=v9`这几个参数，solaris上的gcc不认。

因此我手工指定参数生成 Makefile：`perl Makefile.PL --cflags="-I/usr/local/mysql/include -D_FORTEC_"`，之后`make ; make install` 一切顺利。