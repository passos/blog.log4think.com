---
title: Perl与数据库DBI快速入门
date: '2005-09-13 18:27:18 +0800'
---
上次的文章[Perl无废话入门指南](http://log4think.com/perl_fast_tutorial/)中，简单的介绍了Perl的开发环境。为了完成提到的任务，还需要做几个知识点。无论是写脚本还是做CGI，如何使用Perl来访问数据库就是很有用的一个知识。

各种语言和开发环境访问数据库有各种不同的方式，比如可以用C和数据库提供的API接口来进行访问，也可以用JDBC、ODBC、ADO等封装好的统一接口来进行访问。Perl访问数据库最常用的包是DBI，可以在[www.cpan.org](http://www.cpan.org)找到。另外还需要安装对应数据库的驱动包，例如DBD::MySQL、DBD::Oracle、DBD::Sybase或者DBD::ODBC等。具体的安装方法请参考上期文章，在此就不赘述了。

下文以常见的MySQL为例，说说如何实现对数据库的操作。

## 1 基本流程 ##
习惯在Windows下开发数据库、熟悉ADO、ADO.NET的朋友，一定对ADOConnection/ADODataSet/ADOTable等类耳熟能详。DBI的接口与之类似，但在操作方法上又有不同，对ADO熟悉的朋友不妨比较一下异同。一般来说，数据库操作由以下几个步骤组成一个常见的流程：

1． 建立一个数据库连接

2． 通过建立的数据库连接，执行SQL语句

3． 执行SQL后获取返回的数据集

4． 在数据集中对记录进行处理，一般是一个循环的过程

5． 处理完毕，关闭数据库连接，释放资源

下面是按照上述的流程，在Perl中访问MySQL的一段代码，以这段代码为例，详细说明DBI的使用方法。

	#!/usr/bin/perl -w
	use strict;
	use DBI;

	my $dbh = DBI->connect("DBI:mysql:test:192.168.1.2", 'root', 'password');
	my $sth = $dbh->prepare("SELECT * FROM test1");
	$sth->execute();

	while ( my @row = $sth->fetchrow_array() )
	{
	       print join('\t', @row)."\n";
	}

	$sth->finish();
	$dbh->disconnect();

注意代码中的灰色部分就是要特别关注的数据库访问接口，这里展现的只是一部分，下面将会依次说明每一个步骤，以及其它的操作在Perl中是如何实现的。

### 1.1 连接数据库 ###

	my $dbh = DBI->connect("DBI:mysql:test:192.168.1.2", 'root', 'password');

调用DBI的方法
```
DBI->connect
```
来建立一个数据库的连接，如果连接成功则返回一个数据库连接句柄，之后执行SQL等操作都要把这个连接句柄作为一个操作参数。在connect调用中，首先要提供一个数据库连接串。这个连接串用冒号分为了几个部分，请看下表

<TABLE border=0>
<THEAD>
	<TH>小节</TH>
	<TH>说明</TH>
</THEAD>

<TBODY>
<TR>
	<TD>DBI </TD>
	<TD>接口类型 </TD>
</TR>

<TR>
	<TD>mysql </TD>
	<TD>数据库类型 </TD>
</TR>

<TR>
	<TD>test </TD>
	<TD>数据库名称 </TD>
</TR>

<TR>
	<TD>192.168.1.2 </TD>
	<TD>数据库主机地址 </TD>
</TR>

</TBODY>
</TABLE>

在前面例子中的连接串中，DBI表示这是DBI接口的一个连接串；mysql表示要连接的数据库是MySQL数据库（如果要连接Oracle数据库，这里则是oracle），不同的数据库有不同的连接串定义，可以参考DBI对应的访问驱动的说明；test指明了连接到数据库主机上的数据库名称；192.168.1.2就是MySQL服务器的IP地址。这里要注意的是，连接串中的数据库类型mysql必须小写。如果省略了主机名，则缺省为localhost。connect方法的后面两个参数是连接数据库主机的用户名和密码，这个可是不可缺少的 J

如果在连接过程中出现任何错误，则connect的返回值都会是undef（和C语言中的NULL是一回事）。这里为了简化而略去了错误检查，实际做项目的时候应当对这些错误和返回值的进行检查。

### 1.2 执行SQL语句 ###

	my $sth = $dbh->prepare("SELECT * FROM test1");
	$sth->execute();

	$dbh->do("UPDATE test1 SET time=now()");

连接上了数据库，获得了数据库连接句柄，就可以利用这个句柄来对数据库进行操作了。要执行一条SQL语句，为了提高性能，DBI分两个步骤来做。先把SQL语句通过prepare方法提交到数据库，数据库为该语句分配执行资源，之后调用execute方法通知数据库执行该SQL语句。注意prepare方法是通过数据库连接句柄调用的，如果成功则返回一个该SQL的句柄，之后通过该SQL语句句柄调用execute执行SQL。
一般来说execute执行的都是返回数据的语句（例如SELECT语句）。反之如果执行INSERT、UPDATE、DELETE、CREATE TABLE等不需要返回数据的语句，则有一个更方便、快速的方法 
```
$dbh->do(SQL语句)
```
，可以省去prepare的步骤。do方法返回的是受该SQL影响的记录数量。

#### 1.2.1 技巧：对SQL进行排版 ####

常写大段SQL的朋友可能会对于SQL中的引号很头痛，每每都因为引号的问题搞的SQL语句乱成一团分辨不清。还记得上篇文章讲过的qq吗？这里正是它的好用处。由于qq中的字符串同双引号" "内的字符串一样会对变量进行解释，同时qq还可以换行。因此使用它来对SQL进行排版是非常好的一个选择，例如像这样的一条SQL语句：

	my $res_operator = $dbhandle->prepare( qq{
	       SELECT o_customerid, COUNT(*) AS totalMsgNum FROM mm4fcdrs
	       WHERE (m_date>'$begindate') AND (m_date<'enddate')
	       GROUP BY o_customerid
	});

根本无需考虑引号的问题，可以和正常情况一样的写SQL，是不是方便了很多？

#### 1.2.2 通过SQL语句中的参数优化查询执行效率 ####

在执行大量INSERT之类的语句的时候，反复向数据库服务器提交同样结构的一个SQL语句，在这种情况下可以利用prepare和SQL参数来优化执行效率：

1．先使用prepare提交一个SQL模板给数据库服务器，把其中值的部分用参数占位符代替。
2．使用prepare让服务器为该SQL准备了执行资源后，调用execute并在该方法中传入参数实际的值执行SQL。
3．之后可以反复调用execute，不需要服务器重新prepare

假设要执行这样的一个系列的SQL

	INSERT INTO test1 VALUES (NULL, &lsquo;a&rsquo;, &lsquo;2005-04-01&rsquo;)
	... ...
	INSERT INTO test1 VALUES (NULL, &lsquo;z&rsquo;, &lsquo;2005-04-01&rsquo;)

其中第二个字段的值是从a到z的字母。那么可以这样来优化执行效率：

	my $sth = $dbh->prepare( qq{
		INSERT INTO test1 VALUES (NULL, ?, &lsquo;2005-04-01&rsquo;)
	} );

	for my $value('a'..'z')  {
		$sth->execute($value);
	}

其中的问号就是前面说的参数占位符了，它的意思就是告诉在准备执行资源的服务器：这个SQL的这个位置会有一个值，但是现在还不知道，等下执行的时候再告诉你。 prepare了之后，用一个循环产生a-z的字符给变量$value，然后将$value在execute方法中作为一个参数传入，服务器那里会自动用传入的值替换前面的"?"。需要提醒的是，传入的参数个数一定要和SQL中的占位符的数量一样。

### 1.3 读取记录 ###

熟悉ADO的朋友一定知道里面有一个DataReader对象，DBI中读取数据的方法和它非常的相似。简单来说，就是单向、流式的读取数据，也就是每次只能向后读一条数据直到没有数据可以读取。

文章开头的例子中，用了 
```
$sth->fetchrow_array()
```
 方法来读取数据。其实DBI读取数据还有几种常见的方法，这几个方法是类似的，所不同的是返回记录的形式。

#### 1.3.1 fetchrow_array ####
返回一个由字段的值组成的数组。该数组的第1个元素就是当前记录第1个字段的值。

	while ( my @row = $sth->fetchrow_array() )  {
		print "$row[0], $row[1], $row[2]\n";
	}

或者这样，不过要注意字段对应的顺序

	while ( my ($id, $name, $time) = $sth->fetchrow_array() )  {
		print "$id, $name, $time\n";
	}

#### 1.3.2 fetchrow_arrayref ####
返回由字段的值组成的数组的引用。同
```
fetchrow_array
```
的区别很明显，
```
fetchrow_arrayref
```
返回的数组的引用。

	while ( my $row_ref = $sth->fetchrow_arrayref() ) {
		for (my $i = 0; $i < @{$row_ref}; $i++)       {
			print "$row_ref->[$i]\t";
		}
		print "\n";
	}

这里要注意的是，如果要取字段的个数，需要把这个引用转成数组的形式获得 
```
@{$row_ref}
```
 。获取数组元素的值的时候，因为$row_ref是引用，因此需要使用
```
->
```
操作符。

#### 1.3.3 fetchrow_hashref ####
返回一个由"字段名－字段值"这样的"键－值"对组成的HASH表。关键的不同就是，只有这个方法可以通过一个字段名获得它的值，而不必关心这个字段是第几个字段。而前者只能依靠索引来访问值。不过缺点就是，效率要比前面两个差一些。

	while ( my $record = $sth->fetchrow_hashref() ) {
		for my $field( keys %{$record} ) {
			print "$field: $record->{$field}\t";
		}
		print "\n";
	}

这里需要复习一下HASH表的操作方法。keys操作符获取HASH的键(key)的数组，
```
$record->{$field}
```
获得HASH表中$field对应的值。注意这里同样是引用，因此要用
```
->
```
操作符。

使用上面三个方法可以基本解决问题了。此外，还有两个方法
```
fetchall_arrayref
```
和
```
selectall_arrayref
```
可以直接通过SQL一次性获取整个数据集，不过使用上稍微复杂一些，要涉及到 perl的scalar 操作符，这里就不赘述了。有兴趣的读者可以参考DBI的相关资料。

最后是收尾工作。

### 1.4 结束一个SQL会话 ### 

	$sth->finish();

### 1.5 断开数据库连接 ### 

	$dbh->disconnect();

很简单明了，就不赘述了。

Perl中利用DBI访问数据库的接口基本上就是这些了，还有一些高级的内容留给有兴趣的读者自己发掘研究了。可能有些读者会感觉没有ADO、ADO.NET操作起来方便，但是在脚本的环境下能够如此方便的操作数据库，比起用C接口来说已经方便很多了。也许在看完这片文章之后的不久，可以在cpan上发现你的Module和全世界的Perl程序员一起分享呢。

## 2 参考资源 ## 

- 《Programming the Perl DBI》 O&rsquo;Reily
- [DBI官方网站 http://dbi.perl.org/](http://dbi.perl.org/)
- [一个DBI编程的简短介绍](http://www.perl.com/pub/a/1999/10/DBI.html)

