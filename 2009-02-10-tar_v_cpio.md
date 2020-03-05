---
title: 为什么cpio要比tar好
date: '2009-02-10 08:07:03 +0800'
---
为什么cpio比tar好？有这样几个原因。
1、cpio会保留硬连接（hard link），备份的时候这个很重要
2、cpio没有文件名长度的限制。确实，guntar在这一点上做过改进，允许使用长文件名（实际上是创建了一个临时文件用来保存实际的文件名），但是在非gnu的tar工具上仍然存在这个问题。
3、默认情况下，cpio保留时间戳
4、在编写脚本的时候，cpio可以更好的控制要操作哪些文件。因为cpio需要显式的制定要操作的文件列表，例如下面哪个更加容易理解？

```
find . -type f -name '*.sh' -print | cpio -o | gzip >sh.cpio.gz
```

或者在Solaris上：

```
find . -type f -name '*.sh' -print >/tmp/includeme
tar -cf - . -I /tmp/includeme | gzip >sh.tar.gz
```

或者用gnutar：

``
find . -type f -name '*.sh' -print >/tmp/includeme
tar -cf - . --files-from=/tmp/includeme | gzip >sh.tar.gz
```

这儿有一个需要特别注意的：对于包含大量文件的列表，不能将find放在反引号（`）内，因为命令行长度会超出长度限制，因此必须使用中间文件。 find和tar分开跑很明显会使得速度减慢。

下面这个例子更加复杂，将一部分文件打包到一个文件中，其它部分打包到另外一个文件中：

```
find . -depth -print >/tmp/files
egrep '\.sh$' /tmp/files | cpio -o | gzip >with.cpio.gz
egrep -v '\.sh$' /tmp/files | cpio -o | gzip >without.cpio.gz
```

在 Solaris 下:

```
find . -depth -print >/tmp/files
egrep '\.sh$' /tmp/files >/tmp/with
tar -cf - . -I /tmp/with | gzip >with.tar.gz
tar -cf - . /tmp/without | gzip >without.tar.gz
```

使用 gnutar:

```
find . -depth -print >/tmp/files
egrep '\.sh$' /tmp/files >/tmp/with
tar -cf - . -I /tmp/with | gzip >with.tar.gz
tar -cf - . -X /tmp/without | gzip >without.tar.gz
```

同样的，find和tar分开跑会使得速度变慢。创建多个中间文件也搞出了更多的混乱。gnutar稍好些，但是它的命令行参数却是不兼容的。

5、如果有很多文件需要通过网络在两台机器之间复制，则可以并行的跑几个cpio。例如：

```
find . -depth -print >/tmp/files
split /tmp/files
for F in /tmp/files?? ; do
    cat $F | cpio -o | ssh destination "cd /target && cpio -idum" &
done
```

注意，如果能够将输入平均分成几个部分来进行并行处理会更好。

<a href="http://log4think.com" target="_blank">Simon Liu</a> translated from <a href="http://rightsock.com/~kjw/Ramblings/tar_v_cpio.html" target="_blank">Ramblings</a>

