---
title: hostname自动变成bogon的问题
date: '2012-02-05 16:28:20 +0800'
---
Mac下开iTerm2，发现hostname经常自己变来变去的，有的时候是本机的名字，有的时候自己就变成了bogon。一查，发现：

```
simon@bogon:~$ nslookup
> 192.168.1.1
Server: 124.89.1.129
Address: 124.89.1.129#531.1.168.192.in-addr.arpa name = bogon.
> 10.1.1.1
Server:     124.89.1.129
Address:    124.89.1.129#53

1.1.1.10.in-addr.arpa   name = bogon.
```

原来 192.168.*， 10.* 被DNS反向解析成了bogon，换个DNS（比如8.8.8.8）就没问题了
