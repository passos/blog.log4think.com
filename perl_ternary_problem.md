---
title: 'Perl中不寻常的 ?: 运算符'
date: '2006-04-01 15:37:47 +0800'
---
前几天写一个perl的脚本 在:?运算符上遇到了一个很诡异的问题

	$data->{$id}->{'total'} ?
	    $data->{$id}->{'ratio'} = sprintf("%.2f%%", 100 * $data->{$id}->{'succ'} / $data->{$id}->{'total'}) :
	    $data->{$id}->{'ratio'} = 'N/A';

我的本意是 如果 `$data->{$id}->{'total'}` 未定义则不计算ratio,把ratio赋值为N/A. 这条语句等同于

	if ( $data->{$id}->{'total'} ) {
	    $data->{$id}->{'ratio'} = sprintf("%.2f%%", 100 * $data->{$id}->{'succ'} / $data->{$id}->{'total'});
	} else {
	    $data->{$id}->{'ratio'} = 'N/A';

可奇怪的是，当无论total是否有定义 ratio的结果居然都是N/A. 可后面`if else`的语句是没有问题的，真的是让我百思不得其解。跑去查Perl的文档，其中对于?:的运算符号的解释是 

_Ternary `?:` is the conditional operator, just as in C. It works much like an if-then-else. If the argument before the ? is true, the argument before the : is returned, otherwise the argument after the : is returned._

貌似是return the argument，于是乎脑子里突然闪过一个念头, 在前后都加上了括号...

	$data->{$id}->{'total'} ?
	    ( $data->{$id}->{'ratio'} = sprintf("%.2f%%", 100 * $data->{$id}->{'succ'} / $data->{$id}->{'total'}) ) :
	    ( $data->{$id}->{'ratio'} = 'N/A' );

...居然就对了。既然是return the argument，我就又换了一种方式：

	$data->{$id}->{'ratio'} = $data->{$id}->{'total'} ?
	    sprintf("%.2f%%", 100 * $data->{$id}->{'succ'} / $data->{$id}->{'total'}) :
	    'N/A';

虽然后面两种方式都可以理解，那确实是一种正确的做法。 但为什么第一种方式的结果不对呢？我又写了一个简单的小程序测试

	#!/usr/bin/perl

	use strict;

	my $total=1;
	my $rval;

	############################`
	$total ?
	    $rval = $total :
	    $rval = 'N/A';

	print $rval, "\n";

	############################
	$total ?
	    ( $rval = $total ) :
	    ( $rval = 'N/A' );

	print $rval, "\n";

	############################
	$rval = $total ? $total : 'N/A';

	print $rval, "\n";

	############################
	if ($total) {
	    $rval = $total;
	} else {
	    $rval = 'N/A';
	}

	print $rval;

运行的结果显示, 无论第5行给$total赋什么值...包括1, "abc", "true", undef 等,执行的结果第一个print打印出来的都是N/A。 难道 $total? 不等价于 if ($total) 吗? 

后来偶然的一次机会在PerlChina上问过此问题，才发现原来C和Perl对于 `:?` 和 `=`的优先级定义是不同的。在C中，`=`
的优先级高于`:?`，而Perl中则正好相反。这直接导致了第一种情况对于语句的解释顺序与C截然不同。对于`x ? a = 1 : a = 2;`，你期望解释为`x ? (a = 1) : (a = 2);`，实际却解释成了另外一个形式。

因此教训就是，文档在解释 ?: 的时候说的很清楚 `If the argument before the ? is true, the argument before the : is returned`，重点在*return*。所以，:? 里面应该尽量写"表达式"，而非"语句"。非要用语句，那么请加括号避免优先级问题。 

