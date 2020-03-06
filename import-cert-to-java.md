---
title: 为Java运行环境导入根证书解决Eclipse的TFS插件的"PKIX path building failed"错误
date: '2013-01-23 18:50:14 +0800'
---
最近在项目中必须要使用微软的TFS作为项目管理工具以及版本控制，而开发的IDE使用的是Eclipse。好在TFS有一个Eclipse的插件能够在跨平台的环境下工作。不过这个插件的11.0版本中，连结服务器的时候如果使用HTTPS连结，可能会有一个证书的认证错误问题，

    sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
    ...
    Caused by: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
    ...

这个问题的是由于Java自带的根证书库中不包含HTTPS服务器上的根证书，因此无法得到认证。解决办法是将服务器的根证书导入到Java运行环境中的根证书库中。假设我的证书文件是zero.cer，首先确保命令行下所引用的java是下文命令中所指向`$JAVA_HOME/jre/bin`的是一个JRE，如果不是则需要修改JAVA_HOME的位置。

    $ keytool -import -noprompt -trustcacerts -alias zero -file zero.cer -keystore ~/mykeystore

这个命令会新建一个keystore文件，命令运行后会要求输入密码，这个密码是新建的keystore文件的访问密码。

For Linux:

    $ sudo keytool -importkeystore -srckeystore ~/mykeystore -destkeystore $JAVA_HOME/jre/lib/security/cacerts

For Mac:

    $ sudo keytool -importkeystore -srckeystore ~/mykeystore -destkeystore /Library/Java/Home/lib/security/cacerts

第二个命令将之前建好的keystore中的证书导入jre自带的keystore文件中。过程中会要求输入目标keystore（也就是jre自带的keystore）文件的密码，这个密码默认是 changeit （linux和mac下），或者是 changeme 。

之后，重启Eclipse，再次连结TFS服务器，即可成功通过服务器验证。此外，可以下载一个小工具 [SSLPoke](https://confluence.atlassian.com/download/attachments/180292346/SSLPoke.class?version=1&modificationDate=1236556489366&api=v2) 验证证书是否导入正常，下载之后在文件所在目录下，命令行运行

    $ java SSLPoke tfs.yourserver.com 4343
    Successfully connected

如果显示成功则说明证书导入的没有问题。

