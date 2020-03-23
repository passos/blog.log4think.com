---
title: 魔兽世界私服Trinity，从源码开始
date: '2011-06-22 21:38:38 +0800'
---

# 2011-06-22  魔兽世界私服Trinity，从源码开始

## 缘起因由

在一个无所事事的周末下午，突然想起魔兽世界，官方的账号很久没有上了，里面的大小号现在连满级都不是。以前曾经搭过传奇和星际争霸战网的私服自娱自乐，也听说过魔兽世界有开源的服务端模拟，既然兴致来了就小小的研究一下。

目前魔兽世界的私服比较流行的是MaNGOS和Trinity，二者都是模拟魔兽世界服务端。MaNGOS"号称"是一个研究型项目，目的是为了学习大规模的C++项目开发，有道理，不过我不信。Trinity是基于MaNGOS的代码开发的，以前主要是为了合并用户提交的补丁代码而设立的一个项目，不过现在已经单独独立出来了，主要开发成员包括以前MaNGOS的一些老人，现在的主要工作包括清理代码、优化、提供一个更好的服务端内核。

二者现在的代码提交和更新都很频繁，但是具体是否会合并对方的代码就不清楚了。总而言之，也就是说，我感觉Trinity大概也许应该是目前最好的一个魔兽世界服务端模拟了。作为一个程序员来说，玩游戏还在其次，看看代码才是件有意思的事情。整个过程记录在案 [http://log4think.com/setup\_wow\_private\_server](http://log4think.com/setup_wow_private_server)，以便事后查询。

现在尝试一下从源码开始搭个魔兽世界的服务器，从源码开始主要还是想顺便看看代码的情况，基于Trinity来做。至于客户端的情况，截止到2011年6月12日，中国国服魔兽世界最新的版本是3.3.5 13930-巫妖王之怒。

### 安装基本工具

安装之前，需要准备几个要使用到的工具软件，用来下载、编译等等。

**版本控制工具 Git**  由于 MaNGOS 和 Trinity 都是托管在 GitHub 上，所以得用 Git 才能下到源码：

* [Git for Windows](http://code.google.com/p/msysgit/downloads/detail?name=Git-1.7.4-preview20110204.exe&can=2&amp)
* [Git 的图形化工具 TortoiseGit](http://code.google.com/p/tortoisegit/downloads/detail?name=Tortoisegit-1.6.5.0-32bit.msi&can=2&q=)

**编译工具和库**：

* [OpenSSL](http://www.slproweb.com/download/Win32OpenSSL-1_0_0d.exe)
* [CMake](http://www.cmake.org/cmake/resources/software.html)
* [Visual Studio 2010 Express](http://www.microsoft.com/express/Downloads/#2010-Visual-CPP) ，这个是Visual Studio的免费版本。如果装了要钱的Visual Studio 2010，就不必装这个了。

**运行环境：**

* [MySQL](http://dev.mysql.com/downloads/mysql)，安装后也包含编译需要的头文件和库。
* [MySQL的图形化客户端](http://dev.mysql.com/downloads/gui-tools/5.0.html)

以下二者按需选择其一

* [Microsoft Visual C++ 2010 Redistributable Package x86版本](http://www.microsoft.com/downloads/details.aspx?familyid=A7B7A05E-6DE6-4D3A-A423-37BF0912DB84&displaylang=en)
* [Microsoft Visual C++ 2010 Redistributable Package x64版本](http://www.microsoft.com/downloads/details.aspx?familyid=BD512D9E-43C8-4655-81BF-9350143D5867&displaylang=en)

以下非必需

* [.Net Framework 3.5](http://www.microsoft.com/downloads/details.aspx?FamilyId=333325FD-AE52-4E35-B531-508D977D32A6&displaylang=en)， Visual Studio 2010里面好像带，有了就不必装了

### 生成项目文件

各个工具都下载、安装完毕（具体细节可Google之，不赘述了），准备工作做完之后，开始下代码编译。

1. 建一个目录，譬如 D:\workspace\trinity
2. 进入这个目录，右键 Git Clone... ，Url那里填入

   ```text
   https://github.com/TrinityCore/TrinityCore.git
   ```

   ， 点OK。不喜欢图形化工具的可以直接进到新建的目录里面，命令行上运行

   ```text
   git clone https://github.com/TrinityCore/TrinityCore.git
   ```

   。 会自动建立一个名为 TrinityCore 的源码目录，然后就是等着代码下完。

3. 在 D:\workspace\trinity 下建一个目录是Build等下放编译结果文件
4. 运行CMake的图形化工具（开始菜单里 CMake 下的 CMake \(cmake-gui\)）
5. 点 Browse Source... ， 选 D:\workspace\trinity\TrinityCore
6. Browse Build... ，选 D:\workspace\trinity\Build
7. 点 Configure ，出一个对话框
8. 确保勾选了 Use default native compilers，下拉框里面选 Visual Studio 10，至于是32位还是64位版本的，根据自己的情况选
9. 点Finish，CMake 工具会搜索源码配置，分析出一些编译选项来。确保 cmake-gui 下面的信息提示里面没有 ERROR 字样，否则根据具体错误修正后重来。
   1. 在 cmake-gui 上面的编译选项里面选中 SCRIPTS、SERVERS、TOOLS、USE\_COREPCH、USE\_SCRIPTPCH ，不要选 USE\_MYSQL\_SOURCES 。
   2. 最后点 Generate ， CMake 会在 D:\workspace\trinity\Build 下面生成 Visual Stdio 2010 的项目文件。

配置完成后，我的是这样:

![](http://log4think.com/wp-content/uploads/2011/06/CMake.jpg)

> 可能出现的问题： 1. 第10步里面\_GIT\_EXEC应该是msysgit中git的绝对路径，如果没有则是msysgit安装的时候没有把自己加到系统路径里面去 2. 如果下面出现红色的ERROR提示，类似于
>
> > Could not copy from: D:/dev/cmake/share/cmake-2.8/Templates/CMakeVSMacros2.vsmacros to: C:/Documents and Settings/Administrator/ÎÒµÄÎÄµµ/Visual Studio 2010/Projects/VSMacros80/CMakeMacros/CMakeVSMacros2.vsmacros
>
> 这个好像是因为 CMake 无法识别中文路径，把"我的文档"的位置改一下吧，改成路径不带中文的。或者直接自己把提示中的 CMak&gt;eVSMacros2.vsmacros 拷到"我的文档"下的 Visual Studio 2010/Projects/VSMacros80/CMakeMacros/ 。

### 编译源码

注意以下几点：

1. 如果你的魔兽世界客户端是3.3.5 13930，那么记得给代码打个认证补丁以支持13930，具体请参考另一篇文章 [wow\_3-3-5\_13930\_auth\_patch](http://log4think.com/wow_3-3-5_13930_auth_patch)
2. 在 Visual Studio 里面打开 D:\workspace\trinity\Build\TrinityCore.sln ，先Build -&gt; Clean Solution，然后Build -&gt; Build Solution
3. 默认是生成 Debug ，结果在 D:\Build\bin\Debug下面，从 MySQL 的安装目录下的Lib目录里面拷一个 libmySQL.dll 到这个目录下， libeay32.dll 和 ssleay32.dll 是 OpenSSL 的，应该默认加到系统路径下了，如果后面提示找不到就从 OpenSSL 的安装目录里面拷过来。



### 安装数据库

简短截说：

1. 从 [https://github.com/TrinityCore/TrinityCore/downloads](https://github.com/TrinityCore/TrinityCore/downloads) 下载最新的（或者符合你的客户端版本号的）魔兽世界数据文件，
2. 用MySQL图形化工具，导入 D:\workspace\trinity\TrinityCore\sql\create\create\_mysql.sql 执行建立三个数据库

   > auth 数据库中导入 D:\workspace\trinity\TrinityCore\sql\base\auth_database.sql 执行， characte 数据库中导入 D:\workspace\trinity\TrinityCore\sql\base\character\_database.sql 执行， world 数据库中导入第一步中下载的 TDB\_full_???.sql 文件执行， 最终建立 auth、character、world 三个数据库。

### 生成地图文件

1. 在D:\Build\bin\Debug下面建一个makevmaps3\_simple.bat文件，内容为

   ```text
   vmap3extractor.exe
   md vmaps
   vmap3assembler.exe Buildings vmaps

   pause
   ```

   保存运行，会从魔兽世界的客户端目录里面解压缩服务端需要的地图出来。根据机器速度不同，大概需要20分钟到一个小时的时间。运行结束的时候会给个提示"Press any key..."，按任意键结束。生成 vmaps 和 buildings 目录， buildings 目录无用可以删除。

2. 假设魔兽世界的客户端目录在 D:\WOW 下面，在 D:\Build\bin\Debug 下运行

   ```text
   mapextractor.exe -i "d:\WOW"
   ```

   这样会生成 maps 和 dbc 目录。这个工具会根据客户端的雨中在 dbc 目录下生成不同的 dbc 语言版本。如果是中文的客户端，会提取出中文的 dbc 数据。

### 配置服务器

1. 在 D:\Build\bin\Debug 下有 worldserver.conf.dist 和 authserver.conf.dist 两个文件，分别是游戏服务器和认证服务器的配置模板文件。
2. 复制一份 worldserver.conf.dist 并改名为 worldserver.conf ，配置游戏服务器

   ```text
   LoginDatabaseInfo = "127.0.0.1;3306;root;trinity;auth"
   WorldDatabaseInfo = "127.0.0.1;3306;root;trinity;world"
   CharacterDatabaseInfo = "127.0.0.1;3306;root;trinity;characters"
   ```

   分别是认证数据库、世界数据库、玩家角色数据库的地址， root 后面的 trinity 是 MySQL 中 root 的密码，改成你在安装 MySQL 时设置 root 密码。

   之前生成了 vmap 文件，这个是地图的相关数据，服务器可以根据这个来判断怪物和玩家之间是否可见（是否有墙，是否在建筑物的同一层上）。没有这个的话，怪物会穿墙打你，或者从楼下直接漂上来打你... 服务器配置这里默认情况下是开启 vmap 数据检测的。如果不想开启 vmap 检测，则将下面这些配置的值改成0

   ```text
   vmap.enableLOS = 1
   vmap.enableHeight = 1
   vmap.petLOS = 1
   vmap.enableIndoorCheck = 1
   DetectPosCollision = 1
   ```

3. 复制一份 authserver.conf.dist 并改名为 authserver.conf ，配置认证服务器

   ```text
   LoginDatabaseInfo = "127.0.0.1;3306;root;trinity;auth"
   ```

   同样，把 trinity 改成 MySQL 的 root 密码。

4. 检查数据库 auth 里面 realmlist 表里面的记录，记录中 port 的值应该和 worldserver.conf 里面的

   ```text
   WorldServerPort = 8085
   ```

   这一项的值一样（这里是

   ```text
   8085
   ```

   ）。同时， gamebuild 的值应该和你客户端的版本号是一致的（登陆界面右下角，当前最新的是 13930）。如果realmlist里面没有记录，则应该加一条。

### 修改客户端配置

客户端默认是去登陆官方服务器，需要修改一下地址改成让客户端登陆我们自己架设的游戏服务器。假设魔兽世界客户端安装在 D:\WOW 下面，到 D:\WOW\Data\zhCN 下面，备份 realmlist.wtf 文件。该文件原来的内容是

```text
    set realmList cn.logon.warcraftchina.com
    set patchlist cn.version.warcraftchina.com
    set realmlistbn ""
    set portal cn
```

将其内容改成

```text
    SET realmlist "127.0.0.1"
    SET patchlist "127.0.0.1"
```

### 注册用户账号

客户端后登录会发现没有账号可用，注册账号的办法有两种：

1. 第一种方法是通过SQL语句直接在数据库里面加

   ```text
    INSERT INTO account
    (username, sha_pass_hash, email)
    VALUES
    ('用户名',SHA1(CONCAT(UPPER('用户名'),':',UPPER('密码'))), '邮件地址')
   ```

   替换命令中的 用户名、密码、邮件地址 即可。

2. 第二种方法最简单，后面启动游戏服务器worldserver之后，在这个命令窗口可以输入GM命令：

   ```text
    create account 用户名 密码
   ```

## 启动游戏

1. 运行D:\Build\bin\Debug\authserver.exe
2. 运行D:\Build\bin\Debug\worldserver.exe
3. 运行客户端wow.exe

如果运气好的话... 反正我运气不错...

相关的可能还需要一些配置和改动，不过目前我的这个版本能够正常运行，其它的未来再写吧。在此之前，至少可以先研究下源代码...

### 如何和朋友一起玩

如果想配个私服和朋友一起玩，那么需要一个公网 IP 地址。机房里面没有服务器没有关系，可以搭在自己家里的服务器上，然后去 [ip138](http://ip138.com) 上查到自己的IP地址，把 127.0.0.1 相关的地址都改成自己的IP地址就可以了。如果是通过ADSL路由上的网，去ADSL路由配置里面把自己的内外IP地址设置为DMZ主机地址开放给外网即可。

此外，如果是跑服务端的服务器有花生壳的动态域名或者自己的域名（比如我的 [http://log4think.com），可以将](http://log4think.com），可以将) 127.0.0.1 改成自己的域名。前面在 wowserver 和 authserver 中的地址中配置的 127.0.0.1 都要改，因为服务端要提供这个地址给客户端。 MySQL 相关的 127.0.0.1 地址不用改。非要改也可以，不过就是还得去配MySQL的外网访问的相关安全设置。

同时，如果是要搭在公网上对外提供服务，建议单独找个机器做 auth 服务器（配置不用太好），不同的游戏区跑在不同的服务器上（这个配置要好一点），每个服务器上都要跑worldserver。把服务器列表加到 auth 数据库里面的 realmlist 表里就是。

> 友情提示：提供公网服务小心被告。

#### 相关的几个小问题：

1. 连接服务器断开的话，到[这里](http://www.mangoscn.com/viewthread.php?tid=107229&extra=page%3D1)下个补丁覆盖安装。
2. 登入后没有服务器列表的话，看看客户端的版本号（登陆界面的右下角），然后把auth数据库realmlist表里面的记录最后一项gamebuild改为看到的版本号（比如13930） 。

### 开发调试

既然是从源码编译的，因此如果中间出了任何问题都是可以通过调试的方式去解决的。调试方法很简单，几个简单的手段 1. 抓包，分析数据记录 2. 启动编译好的程序，开 Visual Studio ，附加到该进程上，下断点跟踪 3. 进入游戏，进行操作，Visual Studio 中如果下了正确的断点，就会在相关的位置停下

## 退而求其次

如果你觉得以上太复杂搞不定，如果只是想自己随便玩一下而已，那么可以下个别人做好的包，比如 TCCN-3.3.5-Trinity8400.exe ，安装好启动 web 服务器和 wow 服务器，注册个账号就可以进去玩了，简单的无需解释了。不过这个有人数限制，具体限制多少人我也不清楚，总之做公网服务是没戏的。

## 参考资料

二者的一些相关网站列举如下：

* MaNGOS 官网: [http://getmangos.com](http://getmangos.com)
* MaNGOS 代码库: [http://github.com/mangos](http://github.com/mangos)
* 更多MaNGOS的链接: [http://getmangos.com/wiki](http://getmangos.com/wiki)
* Trinity 官网: [http://www.trinitycore.info](http://www.trinitycore.info)
* Trinity 项目首页: [http://trinitycore.github.com](http://trinitycore.github.com)
* Trinity 代码库: [https://github.com/TrinityCore/TrinityCore](https://github.com/TrinityCore/TrinityCore)

本站后续相关文章可以在 [http://log4think.com/category/practice/fun/wow-trinity/](http://log4think.com/category/practice/fun/wow-trinity/) 找到

本文全文参考Trinity官方文档 [http://www.trinitycore.info/How-to:Win](http://www.trinitycore.info/How-to:Win)

