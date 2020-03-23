---
title: LD_LIBRARY_PATH shouldn't contain the current directory
date: '2014-01-17 14:21:40 +0800'
---

# 2014-01-17  LD\_LIBRARY\_PATH shouldn't contain the current directory

I am trying to build a self-contain GLIBC 2.7. It shows following error when I run `configure`

```text
checking whether ranlib is necessary... no
checking LD_LIBRARY_PATH variable... contains current directory
configure: error:
*** LD_LIBRARY_PATH shouldn't contain the current directory when
*** building glibc. Please change the environment variable
*** and run configure again.
```

my LD\_LIBRARY\_PATH is

```text
$ echo $LD_LIBRARY_PATH
/home/sliu/opt/lib:/home/sliu/opt/libexec/gcc/x86_64-unknown-linux-gnu/4.8.1:/home/sliu/opt/lib64:/home/sliu/opt/lib64/gcj-4.8.1-14:
```

The error message complains that LD\_LIBRARY\_PATH contain the current directory. However my LD\_LIBRARY\_PATH doesn't contain any "current directory". Actually, it's caused by the path seperate character ":" instead of "current directory". If you search LD\_LIBRARY\_PATH in `configure`, you will find this comments

```text
# Test if LD_LIBRARY_PATH contains the notation for the current directory
# since this would lead to problems installing/building glibc.
# LD_LIBRARY_PATH contains the current directory if one of the following
# is true:
# - one of the terminals (":" and ";") is the first or last sign
# - two terminals occur directly after each other
# - the path contains an element with a dot in it
```

Which means, **The LD\_LIBRARY\_PATH can not start or end with character ":".**

So this issue can be fixed by removing the last ':' character in LD\_LIBRARY\_PATH.

解决办法就是，去掉 LD\_LIBRARY\_PATH 最后的那个路径分隔符':'.

