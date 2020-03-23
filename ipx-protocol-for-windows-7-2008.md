---
title: 为Windows 7/Windows Server 2008添加IPX协议
date: '2010-11-26 06:15:39 +0800'
---

# 2010-11-26  为Windows 7/Windows Server 2008添加IPX协议

Windows 7 或者 Windows Server 2008 默认情况下不支持IPX协议，而在很多需要局域网的游戏中还是经常需要用到IPX协议的。解决办法就是从XP系统中复制出IPX协议的驱动文件，然后在Windows 7的网卡的配置界面中就可以找到IPX协议的添加项了。 相关文件是：

X86版本

```text
Windows\inf\netnwlnk.pnf
Windows\inf\netnwlnk.inf
Windows\System32\rtipxmib.dll
Windows\System32\nwprovau.dll
Windows\System32\wshisn.dll
Windows\System32\drivers\nwlnkflt.sys
Windows\System32\drivers\nwlnkfwd.sys
Windows\System32\drivers\nwlnkipx.sys
Windows\System32\drivers\nwlnknb.sys
Windows\System32\drivers\nwlnkspx.sys
```

x64版本

```text
Windows\nwlnkipx.sys
Windows\nwlnknb.sys
Windows\nwlnkspx.sys
Windows\inf\netnwlnk.inf
Windows\inf\netnwlnk.PNF
Windows\system32\nwprovau.dll
Windows\system32\wshisn.dll
Windows\system32\drivers\nwlnkipx.sys
Windows\system32\drivers\nwlnknb.sys
Windows\system32\drivers\nwlnkspx.sys
```

