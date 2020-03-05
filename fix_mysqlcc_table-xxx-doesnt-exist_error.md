---
title: 修正mysqlcc在MySQL 5.0上常报的 Table 'xxx' doesn't exist 错误
date: '2006-04-19 15:13:59 +0800'
---
公司上了MySQL 5.0， 随之而来的不是用的有多爽的问题， 而是一直用的很顺手的mysqlcc...不行了， 其表现形式为经常会在状态栏中提示 "[192.168.22.72] ERROR 1146: Table 'rimkpi.1' doesn't exist" 之类的。 选出数据来也不能在表格中直接修改了，到底mysqlcc出了啥问题呢？

经过观察，发现在MySQL 5.0上 EXPLAIN 语句的结果和4.1一下的版本不同了。4.1以前的返回的结果第一个字段是tablename， 而4.1以后和5.0的返回的是id号（一般情况下就是1了），第三个字段才是tablename。看来是这里出了问题，不过怎么会在4.1上可以，5.0反而不行了呢？ 很不爽，于是去MySQL的官方网站把mysqlcc的source拖了一份下来，用Source-Navigator跟了一把，发现原来是在CQueryWindow.cpp的execQuery的方法(line 447)中的一段白痴代码：

	default_table = explain_query->row( mysql()->mysql()->version().major >= 4 &&
	    mysql()->mysql()->version().minor >= 1 ? 2 : 0);

如果版本号是4.1或者5.1的话，这个判断的结果是2；而如果版本号是5.0的话，结果就是0了。正确的代码至少也应该是

	default_table = explain_query->row(
	    ( mysql()->mysql()->version().major == 4 && mysql()->mysql()->version().minor >= 1 ) ||
	    ( mysql()->mysql()->version().major >= 5 ) ? 2 : 0);

真是...大概开源就这点好处了。 mysqlcc现在已经不再继续维护了，看来只能自己找到mysql的开发包重新编译个自用版本的mysqlcc了，哈哈

