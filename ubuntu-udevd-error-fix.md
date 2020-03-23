---
title: Ubuntu升级导致的udevd错误修复
date: '2011-01-14 12:17:23 +0800'
---

# 2011-01-14  Ubuntu升级导致的udevd错误修复

Linode上的VPS服务器，从Ubuntu Lucid升级至Karmic后，重启后启动失败。用Linode的RemoteAccess连上去看到如下启动错误信息：

```text
init: ureadahead main process (986) terminated wit  status 5
udevd[1012]: failed to create queue file: No such file or directory

udevd[1012]: error creating queue file                                                              

init: udev main process (1012) terminated with sta us 1
init: udev main process ended, respawning
init: udevmonitor main process (1014) terminated w th status 2
udevadm[1734]: error sending message: Connection r fused                                            

mountall: Disconnected from Plymouth
init: plymouth main process (989) killed by SEGV signal
init: plymouth-splash main process (1735) terminat d with status 2
init: hwclock-save main process (1740) terminated  ith status 1
```

经查，由于udevd升级后不支持自动mount自身到/dev节点导致。需要手工修改/etc/fstab文件修复。用Linode的Recure Boot方式启动，mount上原分区，在/etc/fstab最后加入如下一行

```text
dev /dev tmpfs rw 0 0
```

再次重启，没问题了。

