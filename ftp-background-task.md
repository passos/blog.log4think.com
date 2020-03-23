---
title: ftp后台自动上传下载
date: '2007-02-08 16:16:09 +0800'
---

# 2007-02-08  ftp后台自动上传下载

## 方法一: 直接用ftp实现脚本upload.sh

```text
#!/bin/sh

host=xxx.xxx.xxx.xxx
user=xxx
pass=xxx
localdir=/xxx/xxx
remotedir=/xxx/xxx
filename=xxx

ftp -i -n $host <
user $user $pass
cd $remotedir
lcd $localdir
append $filename
quit
EOF
```

运行命令 `nohup ./upload.sh > upload.log 2>&1 &`

## 方法二:用lftp

编写一个脚本文件 upload.cfg,里面直接写ftp命令

```text
open xxx.xxx.xxx.xxx
user xxx xxx
cd xxx
lcd xxx
put xxx
quit
```

运行命令 `lftp -f upload.cfg`。缺点是,似乎不支持append断点续传

## 方法三:用工具,例如ncftpput, 编写一个配置文件 login.cfg

```text
host=xxx.xxx.xxx.xxx
user=xxx
pass=xxx
```

然后运行命令 `ncftpput -f login.cfg -z remote_dir local_dir/file`。缺点是,似乎也不支持断点续传\(本来有一个-z的参数,但是好像不好用\)

## 方法四: 用scp

假设远程机器和本地用户都是jack 首先用ssh-keygen在远程机器上生成一个密钥,密码为空. 然后把远程机器上的/home/jack/.ssh/id\_rsa.pub文件内容复制到本地机器上的/home/jack/.ssh/authorized\_keys 里面 这样再用ssh登录的时候就不用密码了

做好这个之后,可以用 `scp filename jack@remote_host`上传。缺点是,不支持断点续传,不支持后台运行...似乎是个垃圾解决方案,不过倒是支持加密,嗯

