---
title: 魔兽世界 3.3.5 13930 Trinity 认证补丁
date: '2011-06-13 22:09:47 +0800'
---
2011年6月13日，Trinity官方代码针对WoW客户端3.3.5 13930版本登陆有问题。经过代码跟踪调试，发现需要在认证服务器中加入如下补丁：
位于文件 `TrinityCore\src\server\authserver\Authentication\AuthCodes.h`

```
#define POST_BC_ACCEPTED_CLIENT_BUILD   {13930, 12340, 11723, 11403, 11159, 10571, 10505, 10146, 9947, 8606, 0}
```

改动之处就是，在这个客户端支持版本号的列表中加入13930。改动之后需要重新编译authserver和worldserver。

