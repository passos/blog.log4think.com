---
title: 利用ipkall+xlite+iptel.org开通google voice
date: '2010-08-30 06:19:32 +0800'
---

# 2010-08-30  利用ipkall+xlite+iptel.org开通google voice

Google Voice开通需要一个米国的电话号码用于确认，所以在去搞Google Voice之前，得先弄到一个免费的、能用的米国电话号码。以下经验是俺综合了各方资料，加上自己研究得出的可能是最顺利的开通方式了，一切顺利的话15分钟就搞定了。

## **利用iptel.org开一个免费的sip帐号**

1、到这里来注册一个iptel.org的帐号：[http://serweb.iptel.org/user/reg/](http://serweb.iptel.org/user/reg/)

email：写自己的邮件地址 phone： 这里填稍后在ipkall中申请到的电话号码 pick your user name: 选一个用户名，可以用数字、小写字母、点（.\) pick password: 输入一个密码，这个是这个sip服务器的认证密码，对应上面的用户名 confirmation password: 重复密码

## 从www.ipkall.com注册个米国的电话号码

 有人说要几天的人工验证时间，我是注册后马上邮箱就收到了电话号码。也许是因为google voice的原因申请号码的人太多--人工验证忙不过来了... ...

## 配置sip客户端x-lite

[http://www.counterpath.com/x-lite-download.html](http://www.counterpath.com/x-lite-download.html) 下载、安装，无需重启。 点左上角的小三角，选择SIP Account Setting开始配置sip账号。用户名和密码，都写刚刚从iptel.org申请到的账户信息。

确认，x-lite会尝试登陆到sip服务器：disconvering network、registering，然后是ready，屏幕上会显示sip的用户名。

## **开通Google Voice**

准备工作做完，现在有了一个米国的电话号码，并配好了客户端能接电话了。现在开始注册google voice。

[https://www.google.com/voice（我肉身在国内，可以正常访问。但有的人即使将gmail语言设置为英语，仍然会被提示所在国家未开通服务。难道是因为我曾经在米国用过google](https://www.google.com/voice（我肉身在国内，可以正常访问。但有的人即使将gmail语言设置为英语，仍然会被提示所在国家未开通服务。难道是因为我曾经在米国用过google) maps被记录下来了？访问不了的只能翻墙了）。

选择电话号码、确认就不赘述了，确认用的电话填写刚刚从ipkall申请到的电话号码，到第四步的验证会给出两个数字。打开x-lite，然后点google voice那个页面的"Call Now"，几秒种后x-lite会有一个呼入的电话，接起来，在x-lite的键盘上输入那两个数字。google voice的页面会自动跳转到成功页面。现在你有了两个米国的电话号码，一个是ipkall申请到的，一个是google voice分配给你的电话号码。 因为ipkall申请到的电话号码如果30天内没有电话进来的话，会自动回收注销号码。所以现在就可以用gtalk给自己的ipkall的电话号码打个电话了（自娱自乐、左右互搏）。

**注意1**：iptel.org申请到的sip可以免费接电话，可以打sip电话，但是是不可以打普通电话的。但google voice的电话号码是可以打普通电话的（无需翻墙），目前给美国和加拿大打是免费的，给国内打是0.02美元一分钟（大概是1毛4人民币）。但是通过web页面的google voice打电话没有电话拨号盘，也就是说如果在语音期间需要输入数字选择菜单的时候，是没办法的。只能通过google chat里面的call phone图标才会有拨号盘\(需翻墙获得一个米国的ip地址\)。

**注意2**：用iptel.org申请到的电话号码可以利用sip客户端打sip电话，电话号码就用username@gtalk2voip.com这样的形式（前面是你的sip用户名，后面是sip服务器地址）。比如给自己的google voice打电话，我的sip电话号码就是yuntao.liu@gtalk2voip.com （如果是给gtalk2voip的用户打的话，被呼叫方的gtalk上会有一个添加好友的请求，同意了之后就能接电话了）。

**注意3：**目前还未找到能够使用google voice的电话号码打电话的sip客户端。

**注意4：**到现在为止已经你已经有了一个ipkall的电话号码，一个google voice的电话号码，还有对对应的sip帐号。是不是有点乱？我来整理一下，以我自己的账号为例：

| \*\*电话号码类型\*\* | \*\*sip号码\*\* | \*\*电话号码\*\* |
| :--- | :--- | :--- |


| ipkall | yuntao.liu@iptel.org | 从ipkall的邮件得到 |
| :--- | :--- | :--- |


| google voice | yuntao.liu@gtalk2voip.com | Google voice中选的号码 |
| :--- | :--- | :--- |


 sip号码，可以在任何一个支持输入字符串格式的电话号码的sip客户端上拨打和接听，拨打对应的数字电话号码会转到sip号码上。google voice的电话号码默认是拨给google chat的，如果不在线则会转给ipkall的电话号码（我们认证的时候就是关联的这个号码）。总结一下：

| \*\*拨号终端\*\* | \*\*拨号号码\*\* | \*\*可行性\*\* |
| :--- | :--- | :--- |


| 实际电话 | 电话号码 | 可 |
| :--- | :--- | :--- |


| 实际电话 | sip号码 | 不可 |
| :--- | :--- | :--- |


| sip客户端 | sip号码 | 可（看具体客户端支持情况） |
| :--- | :--- | :--- |


| sip客户端 | 电话号码 | 可（一般都要充值收费） |
| :--- | :--- | :--- |


| google voice | 电话号码 | 可（美加免费，国内收费） |
| :--- | :--- | :--- |


| google voice |
| :--- |


| sip号码 |
| :--- |


不可

**此外**：还有一个问题是x-lite只能输入数字格式的电话号码，得找一个能输入这种格式的电话的sip客户端，下面推荐两个客户端nimbuzz和fring。

2011-01-18更新：最新版的x-lite 4 已经可以支持username@gtalk2voip.com这样的sip电话号码了。

**nimbuzz作为sip客户端接打电话**

x-lite不错，不过可惜只是一个sip客户端，也只能打数字形式的电话，不能打sip电话。通常我们要开很多im的客户端，nimbuzz是一个非常好的万金油客户端，除了是一个SIP客户端之外，还是GTalk、MSN、Yahoo、Facebook、twitter、ICQ、myspace等等im的客户端。除了PC版本之外，也有手机版本和Web版本...

这里下载：[http://www.nimbuzz.com/en/pc/](http://www.nimbuzz.com/en/pc/)

下载客户端、注册账号、登陆，在Tools--Option--Call Service，右边sip provider选择Other，然后输入从iptel那儿的sip账号信息。然后就可以接打sip电话了。

## Fring作为手机sip 客户端

fring是一个手机上的支持twitter、gtalk、msn、yahoo等IM的客户端，同时也支持SIP。只是可惜的是没有PC上的客户端。

在这里 [http://www.fring.com/download/](http://www.fring.com/download/) 。 在手机上安装完成后，启动、选项--转至--addons--SIP，输入iptel.org对应的账户认证信息。

然后，有人给你的google voice的号码拨号，或者给你的ipkall的电话号码拨号，手机都会响了。

注意：没有wifi宽带接入的情况下，语音有延迟。

