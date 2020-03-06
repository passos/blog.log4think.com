---
title: Go 编程语言入门教程
date: '2010-03-31 02:21:04 +0800'
---
> 原文：http://golang.org
> 翻译：刘金雨 http://log4think.com

## 介绍

本文档是关于Go编程语言基础的一个介绍性的入门教程，偏向于熟悉C或C++的读者。本文并非一份语言的完整指南，如果需要的话可以参考[语言规范](http://golang.org/ref/spec)。读完本教程之后，你可以继续学习[Effective Go](http://golang.org/doc/effective_go.html)，这份文档会更深入的挖掘如何使用Go语言。

此外还有一份《三日入门》的教程可供参考:

- [第一日](http://www.yeeyan.com/doc/GoCourseDay1.pdf)
- [第二日](http://www.yeeyan.com/doc/GoCourseDay2.pdf)
- [第三日](http://www.yeeyan.com/doc/GoCourseDay3.pdf)

本文将会以一系列适当的程序来说明语言的一些关键特性。所有的示例程序都是可运行的（在撰写本文时），并且这些程序都会提交到版本库的
```
/doc/progs/
```
目录下。

程序片段都会标注上在源文件中的行号，为了清晰起见，空行前面的行号留空。

## Hello World

先从一个最常见的开始:

    05    package main

    07    import fmt "fmt"  // 本包实现了格式化输入输出

    09    func main() {
    10        fmt.Printf("Hello, world; or &Kappa;&alpha;&lambda;&eta;&mu;έ&rho;&alpha; &kappa;ό&sigma;&mu;&epsilon;; or こんにちは 世界n");
    11    }

每份Go的源文件都会使用
```
package
```
语句声明它的包名。同时也可以通过导入其它包来使用其中定义的功能。这段代码导入了包
```
fmt
```
来调用我们的老朋友--现在它的开头字母是大写的，并且前面带有包名限定
```
fmt.Printf
```
。

函数的声明使用关键字func，整个程序将会从为
```
main
```
包中的
```
main
```
函数开始（经过初始化之后）。

字符串常量可以包含Unicode字符，采用UTF-8编码（事实上，所有Go程序的源文件都是使用UTF-8编码的）。

注释的方式同C++一样：
```
/* ... */
```
或
```
// ...
```
稍后我们会继续提到
```
print
```
。

## 编译

Go是一个编译型语言。目前有两个编译器，其中
```
gccgo
```
编译器采用了GCC作为后端，此外还有一系列根据其所适用的架构命名的编译器，例如
```
6g
```
适用于64位的x86结构，8g 适用于32位的x86结构，等等。这些编译器比gccgo运行的更快、生成的代码更加有效率。在撰写本文的时候（2009年底），他们还具有一个更加健壮的运行期系统，但是gccgo也正在迎头赶上。

下面来看看如何编译和运行程序。采用
```
6g
```
是这样的

    $ 6g helloworld.go  编译; 中间代码位于 helloworld.6 中
    $ 6l helloworld.6   链接; 输出至 6.out
    $ 6.out
    Hello, world; or &Kappa;&alpha;&lambda;&eta;&mu;έ&rho;&alpha; &kappa;ό&sigma;&mu;&epsilon;; or こんにちは 世界
    $
```
gccgo
```
的方式看起来更加传统一些。

    $ gccgo helloworld.go
    $ a.out
    Hello, world; or &Kappa;&alpha;&lambda;&eta;&mu;έ&rho;&alpha; &kappa;ό&sigma;&mu;&epsilon;; or こんにちは 世界
    $

## Echo

下一步，来实现一个Unix的传统命令Echo：

    05    package main

    07    import (
    08        "os";
    09        "flag";  // command line option parser
    10    )

    12    var omitNewline = flag.Bool("n", false, "don't print final newline")

    14    const (
    15        Space = " ";
    16        Newline = "n";
    17    )

    19    func main() {
    20        flag.Parse();   // Scans the arg list and sets up flags
    21        var s string = "";
    22        for i := 0; i < flag.NArg(); i++ {
    23            if i > 0 {
    24                s += Space
    25            }
    26            s += flag.Arg(i);
    27        }
    28        if !*omitNewline {
    29            s += Newline
    30        }
    31        os.Stdout.WriteString(s);
    32    }

这段程序很小，但是却有几个新出现的概念。前面这个例子中，我们看到可以使用
```
func
```
来声明一个函数，同时关键字
```
var、const
```
和
```
type
```
目前还没有用到）也可以用于声明，就好像
```
import
```
一样。

注意，我们可以将同一类的声明放到括号中，以分号分隔。例如第7-10行和第14-17行。但也并非一定要如此，例如可以这样写
```
    const Space = " "
    const Newline = "n"

分号在此处并不是必须的。事实上，任何顶层声明后面都不需要分号。但如果要是在一个括号内进行一系列的声明，就需要用分号来分割了。

你可以像在C、C++或Java中那样去使用分号，但如果你愿意的话，在很多情况下都可以省略掉分号。分号是用于表示语句间的**分隔**，而非表示其**中止**。因此，对于一个代码块中的最后一条语句来说，有无分号皆可。大括号之后的分号也是可选的，就像C语言中的一样。

比对一下
```
echo
```
的源代码，只有第8、15和21行必须要加分号，当然第22行中的
```
for
```
语句中为了分隔三个表达式也需要加分号。第9、16、26和31行的分号都不是必须的，加上分号只是为了以后再增加语句的时候方便而已。

这个程序导入了os包以访问
```
Stdout
```
变量，
```
Stdout
```
的类型是
```
*os.File
```
。
```
import
```
语句实际上是个声明：通常情况下（如hello world程序中那样），它声明了一个标识符
```
fmt
```
用于访问导入的包的成员变量，而包是从当前目录或标准库下的
```
fmt
```
文件中导入的。在这个程序中，我们为导入的包显式的指定了一个名字，默认情况下，包名是采用在导入的包里面已经定义好的名字，通常会与文件名一致。因此在这个"hello world"程序中，可以只写
```
import "fmt"
```
。你可以任意为包指定一个导入名，但通常只有在解决名字冲突的情况下才有必要这样做。

有了
```
os.Stdout
```
，我们就可以用它的
```
WriteString
```
方法打印字符串了。

导入了
```
实 际flag
```
包之后，第12行创建了一个全局变量来保存 echo 的
```
-n
```
选项标志。
```
omitNewline
```
变量的类型是 *bool --指向bool值的指针。

在
```
main.main
```
中进行了参数解析，并创建了一个本地字符串类型的变量用于构造输出的内容。声明语句如下

    var s string = "";

这里用到了关键字
```
var
```
，后面跟变量名和数据类型，之后可以继续接=来赋初值。

Go试图尽量保持简洁，这个声明也可以用更短的形式。因为初值是一个字符串类型的常量，没有必要再声明数据类型了，因此这个声明可以写成这样：

    var s = "";

或者也可以直接用更短的形式：

    s := "";

操作符
```
:=
```
在 Go 语言里经常会用在赋初值的声明中，比如下面这个
```
for
```
语句的声明：

    22    for i := 0; i < flag.NArg(); i++ {
```
flag
```
包会解析命令行参数，并将参数值保存在一个列表中。

Go语言中的
```
for
```
语句和C语言中的有几个不同之处。首先，for是唯一的循环语句，没有
```
while
```
语句或
```
do
```
语句。其次，for语句后面的三个子句不需要圆括号，但大括号是必须的。这一条对
```
if
```
和
```
switch
```
语句同样适用。稍后还会有几个例子演示
```
for
```
语句的其它用法。

循环体中通过追加（+=）标志和空格构造字符串
```
s
```
。循环之后，如果没有设置
```
-n
```
标志，程序追加一个空行，最后输出结果。

注意，函数
```
main.main
```
没有返回值。它就是这样定义的，如果到达了
```
main.main
```
的末尾就表示"成功"，如果想表明出错并返回，可以调用

    os.Exit(1)
```
os
```
包还包含一些其他的常用功能，例如
```
os.Args
```
会被
```
flag
```
包用于访问命令行参数。

## 插播：数据类型 Types

Go支持一些常见的数据类型，例如
```
int
```
和
```
float
```
，其值采用机器"适用"的大小来表示。也有定义了明确大小的数据类型，例如
```
int8
```
、
```
float64
```
等，以及无符号整数类型，例如
```
uint
```
、
```
uint32
```
等。这些都是完全不同的数据类型，即使
```
int
```
和
```
int32
```
都是32位整数，但它们是不同的类型。对于表示字符串元素的类型
```
byte
```
和
```
uint8
```
也是同样如此。

说到字符串（
```
string
```
），这也是一个内置的数据类型。字符串的值不仅仅是一个
```
byte
```
的数组，它的值是**不可改变**的。一旦确定了一个字符串的值，就不能再修改了。但一个字符串**变量**的值可以通过重新赋值来改变。下面这段来自
```
strings.go
```
的代码是合法的：

    11    s := "hello";
    12    if s[1] != 'e' { os.Exit(1) }
    13    s = "good bye";
    14    var p *string = &s;
    15    p = "ciao";

然而下面这段代码是非法的，因为它试图修改一个字符串的值：

    s[0] = 'x';
    (*p)[1] = 'y';

按照C++的说法，Go的字符串有点类似带了
```
const
```
修饰符，指向字符串的指针也类似于一个 const 字符串的引用（reference）.

没错，前面看到的那些是指针，然而Go语言中的指针在用法方面有所简化，后文会提到。

数组的声明如下所示：

    var arrayOfInt [10]int;

数组同字符串一样是"值"，但是却是可变的。与C不同的是，C语言中
```
arrayOfInt
```
可以当做一个指向int的指针来用。在Go中，因为数组是**值**，因此
```
arrayOfInt
```
被看做（也被用做）指向数组的指针。

数组的大小是其数据类型的一部分。但是，你可以声明一个**slice**变量，然后可以用一个指向具有相同元素类型的数组指针给它赋值，更常见的是用一个形式为
```
a[low : high]
```
的**slice**表达式，该表达式表示下标从
```
low
```
到
```
high-1
```
的子数组。 Slice 类型类似数组，但没有显式指定大小(
```
[]
```
之于
```
[10]
```
)，用于表示一个隐性（通常是匿名的）数组。如果不同的 slice 都是表示同一个数组中的数据，它们可以共享该数组的内存，但不同的数组则永远不会共享内存数据。

Slice 在 Go 程序中比数组更常见。它更灵活，并且具有引用的语义，效率也更高。其不足之处在于无法像数组一样精确控制存储方式，如果想在一个数据结构中保存一个具有 100个元素的序列，应该采用数组。

当给函数传一个数组参数的时候，绝大多数情况下都会把参数声明为 slice 类型。当调用函数时，先取数组地址，然后Go会创建一个 slice 的引用，然后传这个引用过去。

可以用 slice 来写这个函数(来自
```
sum.go
```
)：

    09    func sum(a []int) int {   // 返回一个整数
    10        s := 0;
    11        for i := 0; i < len(a); i++ {
    12            s += a[i]
    13        }
    14        return s
    15    }

之后这样来调用：

    19    s := sum(&[3]int{1,2,3});  // a slice of the array is passed to sum

注意在
```
sum()
```
的参数列表后面加 int 定义了其返回值类型（int）。
```
[3]int{1,2,3}
```
的形式是一个数据类型后面接一个大括号括起来的表达式，整个这个表达式构造出了一个值，这里是一个包含三个整数的数组。前面的
```
&
```
表示提取这个值的地址。这个地址会被隐性的转为一个 slice 传给
```
sum()
```
。

如果想创建一个数组，但希望编译器来帮你确定数组的大小，可以用
```
...
```
作为数组大小：

    s := sum(&[...]int{1,2,3});

实际使用中，除非非常在意数据结构的存储方式，否则 slice 本身 （用[]且不带
```
&
```
） 就足够了：

    s := sum([]int{1,2,3});

除此之外还有map，可以这样初始化：

    m := map[string]int{"one":1 , "two":2}
```
sum还第一次出现 了
```
内置函数
```
len()，用于返回元素数量。
```
可以用于字符串、数组、slice、map、map和channel.

此外，
```
for
```
循环中的
```
range
```
也可以用于字符串、数组、slice、map、map和channel。例如

    for i := 0; i < len(a); i++ { ... }

遍历一个序列的每个元素，可以写成

    for i, v := range a { ... }

其中， i 会赋值为下标， v 会赋值为 a 中对应的值，[Effective Go](http://golang.org/doc/effective_go.html)中包含了更多的用法演示。

## An Interlude about Allocation

Go中的大多数数据类型都是值类型。对
```
int
```
、
```
struct
```
或数组的赋值会拷贝其内容。
```
new()
```
可以分配一个新的变量，并返回其分配的存储空间的地址。例如

    type T struct { a, b int }
    var t *T = new(T);

或者更常见的写法：

    t := new(T);

Some types-maps, slices, and channels (see below)-have reference semantics. If you're holding a slice or a map and you modify its contents, other variables referencing the same underlying data will see the modification. For these three types you want to use the built-in function
```
make()
```
:

    m := make(map[string]int);

This statement initializes a new map ready to store entries. If you just declare the map, as in

    var m map[string]int;

it creates a
```
nil
```
reference that cannot hold anything. To use the map, you must first initialize the reference using
```
make()
```
or by assignment from an existing map.

Note that
```
new(T)
```
returns type
```
*T
```
while
```
make(T)
```
returns type
```
T
```
. If you (mistakenly) allocate a reference object with
```
new()
```
, you receive a pointer to a nil reference, equivalent to declaring an uninitialized variable and taking its address.

## An Interlude about Constants

Although integers come in lots of sizes in Go, integer constants do not. There are no constants like
```
0LL
```
or
```
0x0UL
```
. Instead, integer constants are evaluated as large-precision values that can overflow only when they are assigned to an integer variable with too little precision to represent the value.

    const hardEight = (1 << 100) >> 97  // legal

There are nuances that deserve redirection to the legalese of the language specification but here are some illustrative examples:

    var a uint64 = 0  // a has type uint64, value 0
    a := uint64(0)    // equivalent; uses a "conversion"
    i := 0x1234       // i gets default type: int
    var j int = 1e6   // legal - 1000000 is representable in an int
    x := 1.5          // a float
    i3div2 := 3/2     // integer division - result is 1
    f3div2 := 3./2.   // floating point division - result is 1.5

Conversions  only work for simple cases such as converting
```
ints
```
of one sign or size to another, and between
```
ints
```
and
```
floats
```
, plus a few other simple cases. There are no automatic numeric  conversions of any kind in Go, other than that of making constants have concrete size and type when assigned to a variable.

## An  I/O Package

Next we'll look at a simple package for doing file I/O with the usual sort of open/close/read/write interface. Here's the  start of
```
file.go
```
:

    05    package file

    07    import  (
    08        "os";
    09        "syscall";
    10    )

    12    type File  struct {
    13        fd      int;    // file descriptor number
    14        name    string; // file name at Open time
    15    }

The first few lines declare the name of the package-
```
file
```
-and then import two packages. The
```
os
```
package hides the differences between various operating systems to give a consistent view of files and so on; here we're going to use its error handling utilities and reproduce the rudiments of its file I/O.

The other item is the low-level, external
```
syscall
```
package, which provides a primitive interface to the underlying operating system's calls.

Next is a type definition: the
```
type
```
keyword introduces a type declaration, in this case a data structure called
```
File
```
. To make things a little more interesting, our
```
File
```
includes the name of the file that the file descriptor refers to.

Because
```
File
```
starts with a capital letter, the type is available outside the package, that is, by users of the package. In Go the rule about visibility of information is simple: if a name (of a top-level type, function, method, constant or variable, or of a structure field or method) is capitalized, users of the package may see it. Otherwise, the name and hence the thing being named is visible only inside the package in which it is declared. This is more than a convention; the rule is enforced by the compiler. In Go, the term for publicly visible names is ''exported''.

In the case of
```
File
```
, all its fields are lower case and so invisible to users, but we will soon give it some exported, upper-case methods.

First, though, here is a factory to create a
```
File
```
:

    17    func newFile(fd int, name string) *File {
    18        if fd < 0 {
    19            return nil
    20        }
    21        return &File{fd, name}
    22    }

This returns a pointer to a new
```
File
```
structure with the file descriptor and name filled in. This code uses Go's notion of a ''composite literal'', analogous to the ones used to build maps and arrays, to construct a new heap-allocated object. We could write

    n := new(File);
    n.fd = fd;
    n.name = name;
    return n

but for simple structures like
```
File
```
it's easier to return the address of a nonce composite literal, as is done here on line 21.

We can use the factory to construct some familiar, exported variables of type
```
*File
```
:

    24    var (
    25        Stdin  = newFile(0, "/dev/stdin");
    26        Stdout = newFile(1, "/dev/stdout");
    27        Stderr = newFile(2, "/dev/stderr");
    28    )

The
```
newFile
```
function was not exported because it's internal. The proper, exported factory to use is
```
Open
```
:

    30    func Open(name string, mode int, perm int) (file *File, err os.Error) {
    31        r, e := syscall.Open(name, mode, perm);
    32        if e != 0 {
    33            err = os.Errno(e);
    34        }
    35        return newFile(r, name), err
    36    }

There are a number of new things in these few lines. First,
```
Open
```
returns multiple values, a
```
File
```
and an error (more about errors in a moment). We declare the multi-value return as a parenthesized list of declarations; syntactically they look just like a second parameter list. The function
```
syscall.Open
```
also has a multi-value return, which we can grab with the multi-variable declaration on line 31; it declares
```
r
```
and
```
e
```
to hold the two values, both of type
```
int
```
(although you'd have to look at the
```
syscall
```
package to see that). Finally, line 35 returns two values: a pointer to the new
```
File
```
and the error. If
```
syscall.Open
```
fails, the file descriptor
```
r
```
will be negative and
```
NewFile
```
will return
```
nil
```
.

About those errors: The
```
os
```
library includes a general notion of an error. It's a good idea to use its facility in your own interfaces, as we do here, for consistent error handling throughout Go code. In
```
Open
```
we use a conversion to translate Unix's integer
```
errno
```
value into the integer type
```
os.Errno
```
, which implements
```
os.Error
```
.

Now that we can build
```
Files
```
, we can write methods for them. To declare a method of a type, we define a function to have an explicit receiver of that type, placed in parentheses before the function name. Here are some methods for
```
*File
```
, each of which declares a receiver variable
```
file
```
.

    38    func (file *File) Close() os.Error {
    39        if file == nil {
    40            return os.EINVAL
    41        }
    42        e := syscall.Close(file.fd);
    43        file.fd = -1;  // so it can't be closed again
    44        if e != 0 {
    45            return os.Errno(e);
    46        }
    47        return nil
    48    }
    50    func  (file *File) Read(b []byte) (ret int, err os.Error) {
    51        if file  == nil {
    52            return -1, os.EINVAL 

    53        }
    54        r, e  := syscall.Read(file.fd, b);
    55        if e != 0 {
    56            err =  os.Errno(e);
    57        }
    58        return int(r), err
    59    }

    61    func  (file *File) Write(b []byte) (ret int, err os.Error) {
    62        if  file == nil {
    63            return -1, os.EINVAL 

    64        }
    65        r, e := syscall.Write(file.fd, b);
    66        if e != 0 {
    67            err = os.Errno(e);
    68        }
    69        return int(r),  err
    70    }

    72    func (file *File) String() string {
    73        return file.name
    74    }

There is no implicit
```
this
```
and the receiver variable must be used to access members of the structure. Methods are not declared within the
```
struct
```
declaration itself. The
```
struct
```
declaration defines only data members. In fact, methods can be created for almost any type you name, such as an integer or array, not just for
```
structs
```
. We'll see an example with arrays later.

The
```
String
```
method is so called because of a printing convention we'll describe later.

The methods use the public variable
```
os.EINVAL
```
to return the (
```
os.Error
```
version of the) Unix error code
```
EINVAL
```
. The
```
os
```
library defines a standard set of such error values.

We can now use our new package:

    05    package main
    07    import  (
    08        "./file";
    09        "fmt";
    10        "os";
    11    )

    13    func  main() {
    14        hello := []byte{'h', 'e', 'l', 'l', 'o', ',', ' ',  'w', 'o', 'r', 'l', 'd', 'n'};
    15        file.Stdout.Write(hello);
    16        file, err := file.Open("/does/not/exist",  0,  0);
    17        if file == nil {
    18            fmt.Printf("can't open file;  err=%sn",  err.String());
    19            os.Exit(1);
    20        }
    21    }

The ''
```
./
```
'' in the import of ''
```
./file
```
'' tells the compiler to use our own package rather than something from the directory of installed packages.

Finally we can run the program:

    % helloworld3
    hello, world
    can't open file; err=No such file or directory
    %

## Rotting cats

Building on the
```
file
```
package, here's a simple version of the Unix utility
```
cat(1)
```
,
```
progs/cat.go
```
:

    05    package main

    07    import (
    08        "./file"
    09        "flag"
    10        "fmt"
    11        "os"
    12    )

    14    func cat(f *file.File) {
    15        const NBUF = 512
    16        var buf [NBUF]byte
    17        for {
    18            switch nr, er := f.Read(&buf); true {
    19            case nr < 0:
    20                fmt.Fprintf(os.Stderr, "cat: error reading from %s: %s\n", f.String(), er.String())
    21                os.Exit(1)
    22            case nr == 0:  // EOF
    23                return
    24            case nr > 0:
    25                if nw, ew := file.Stdout.Write(buf[0:nr]); nw != nr {
    26                    fmt.Fprintf(os.Stderr, "cat: error writing from %s: %s\n", f.String(), ew.String())
    27                }
    28            }
    29        }
    30    }

    32    func main() {
    33        flag.Parse()   // Scans the arg list and sets up flags
    34        if flag.NArg() == 0 {
    35            cat(file.Stdin)
    36        }
    37        for i := 0; i < flag.NArg(); i++ {
    38            f, err := file.Open(flag.Arg(i), 0, 0)
    39            if f == nil {
    40                fmt.Fprintf(os.Stderr, "cat: can't open %s: error %s\n", flag.Arg(i), err)
    41                os.Exit(1)
    42            }
    43            cat(f)
    44            f.Close()
    45        }
    46    }

By now this should be easy to follow, but the
```
switch
```
statement introduces some new features. Like a
```
for
```
loop, an
```
if
```
or
```
switch
```
can include an initialization statement. The
```
switch
```
on line 18 uses one to create variables
```
nr
```
and
```
er
```
to hold the return values from
```
f.Read()
```
. (The
```
if
```
on line 25 has the same idea.) The
```
switch
```
statement is general: it evaluates the cases from top to bottom looking for the first case that matches the value; the case expressions don't need to be constants or even integers, as long as they all have the same type.

Since the
```
switch
```
value is just
```
true
```
, we could leave it off-as is also the situation in a
```
for
```
statement, a missing value means
```
true
```
. In fact, such a
```
switch
```
is a form of
```
if-else
```
chain. While we're here, it should be mentioned that in
```
switch
```
statements each
```
case
```
has an implicit
```
break
```
.

Line 25 calls
```
Write()
```
by slicing the incoming buffer, which is itself a slice. Slices provide the standard Go way to handle I/O buffers.

Now let's make a variant of
```
cat
```
that optionally does
```
rot13
```
on its input. It's easy to do by just processing the bytes, but instead we will exploit Go's notion of an**interface**.

The
```
cat()
```
subroutine uses only two methods of
```
f
```
:
```
Read()
```
and
```
String()
```
, so let's start by defining an interface that has exactly those two methods. Here is code from
```
progs/cat_rot13.go
```
:

    26    type reader interface {
    27        Read(b []byte) (ret int, err os.Error);
    28        String() string;
    29    }

Any type that has the two methods of
```
reader
```
-regardless of whatever other methods the type may also have-is said to**implement**the interface. Since
```
file.File
```
implements these methods, it implements the
```
reader
```
interface. We could tweak the
```
cat
```
subroutine to accept a
```
reader
```
instead of a
```
*file.File
```
and it would work just fine, but let's embellish a little first by writing a second type that implements
```
reader
```
, one that wraps an existing
```
reader
```
and does
```
rot13
```
on the data. To do this, we just define the type and implement the methods and  with no other bookkeeping, we have a second implementation of the
```
reader
```
interface.

    31    type rotate13 struct {
    32        source    reader
    33    }

    35    func newRotate13(source reader) *rotate13 {
    36        return &rotate13{source}
    37    }

    39    func (r13 *rotate13) Read(b []byte) (ret int, err os.Error) {
    40        r, e := r13.source.Read(b)
    41        for i := 0; i < r; i++ {
    42            b[i] = rot13(b[i])
    43        }
    44        return r, e
    45    }

    47    func (r13 *rotate13) String() string {
    48        return r13.source.String()
    49    }
    50    // end of rotate13 implementation

(The
```
rot13
```
function called on line 42 is trivial and not worth reproducing here.)

To use the new feature, we define a flag:

    14    var rot13Flag = flag.Bool("rot13", false, "rot13 the input")

and use it from within a mostly unchanged
```
cat()
```
function:

    52    func cat(r reader) {
    53        const NBUF = 512
    54        var buf [NBUF]byte

    56        if *rot13Flag {
    57            r = newRotate13(r)
    58        }
    59        for {
    60            switch nr, er := r.Read(&buf); {
    61            case nr < 0:
    62                fmt.Fprintf(os.Stderr, "cat: error reading from %s: %s\n", r.String(), er.String())
    63                os.Exit(1)
    64            case nr == 0:  // EOF
    65                return
    66            case nr > 0:
    67                nw, ew := file.Stdout.Write(buf[0:nr])
    68                if nw != nr {
    69                    fmt.Fprintf(os.Stderr, "cat: error writing from %s: %s\n", r.String(), ew.String())
    70                }
    71            }
    72        }
    73    }

(We could also do the wrapping in
```
main
```
and leave
```
cat()
```
mostly alone, except for changing the type of the argument; consider that an exercise.) Lines 56 through 58 set it all up: If the
```
rot13
```
flag is true, wrap the
```
reader
```
we received into a
```
rotate13
```
and proceed. Note that the interface variables are values, not pointers: the argument is of type
```
reader
```
, not
```
*reader
```
, even though under the covers it holds a pointer to a
```
struct
```
.

Here it is in action:

    % echo abcdefghijklmnopqrstuvwxyz | ./cat
    abcdefghijklmnopqrstuvwxyz
    % echo abcdefghijklmnopqrstuvwxyz | ./cat --rot13
    nopqrstuvwxyzabcdefghijklm
    %

Fans of dependency injection may take cheer from how easily interfaces allow us to substitute the implementation of a file descriptor.

Interfaces are a distinctive feature of Go. An interface is implemented by a type if the type implements all the methods declared in the interface. This means that a type may implement an arbitrary number of different interfaces. There is no type hierarchy; things can be much more**ad hoc**, as we saw with
```
rot13
```
. The type
```
file.File
```
implements
```
reader
```
; it could also implement a
```
writer
```
, or any other interface built from its methods that fits the current situation. Consider the**empty interface**

    type Empty interface {}

**Every**type implements the empty interface, which makes it useful for things like containers.

## Sorting

Interfaces provide a simple form of polymorphism. They completely separate the definition of what an object does from how it does it, allowing distinct implementations to be represented at different times by the same interface variable.

As an example, consider this simple sort algorithm taken from
```
progs/sort.go
```
:

    13    func Sort(data Interface) {
    14        for i := 1; i < data.Len(); i++ {
    15            for j := i; j > 0 && data.Less(j, j-1); j-- {
    16                data.Swap(j, j-1)
    17            }
    18        }
    19    }

The code needs only three methods, which we wrap into sort's
```
Interface
```
:

    07    type Interface interface {
    08        Len() int;
    09        Less(i, j int) bool;
    10        Swap(i, j int);
    11    }

We can apply
```
Sort
```
to any type that implements
```
Len
```
, 
```
Less
```
, and
```
Swap
```
. The
```
sort
```
package includes the necessary methods to allow sorting of arrays of integers, strings, etc.; here's the code for arrays of
```
int
```
    33    type IntArray []int

    35    func (p IntArray) Len() int            { return len(p) }
    36    func (p IntArray) Less(i, j int) bool  { return p[i] < p[j] }
    37    func (p IntArray) Swap(i, j int)       { p[i], p[j] = p[j], p[i] }

Here we see methods defined for non-
```
struct
```
types. You can define methods for any type you define and name in your package.

And now a routine to test it out, from
```
progs/sortmain.go
```
. This uses a function in the
```
sort
```
package, omitted here for brevity, to test that the result is sorted.

    12    func ints() {
    13        data := []int{74, 59, 238, -784, 9845, 959, 905, 0, 0, 42, 7586, -5467984, 7586};
    14        a := sort.IntArray(data);
    15        sort.Sort(a);
    16        if !sort.IsSorted(a) {
    17            panic()
    18        }
    19    }

If we have a new type we want to be able to sort, all we need to do is to implement the three methods for that type, like this:

    30    type day struct {
    31        num        int
    32        shortName  string
    33        longName   string
    34    }

    36    type dayArray struct {
    37        data []*day
    38    }

    40    func (p *dayArray) Len() int            { return len(p.data) }
    41    func (p *dayArray) Less(i, j int) bool  { return p.data[i].num < p.data[j].num }
    42    func (p *dayArray) Swap(i, j int)       { p.data[i], p.data[j] = p.data[j], p.data[i] }

## Printing

The examples of formatted printing so far have been modest. In this section we'll talk about how formatted I/O can be done well in Go.

We've seen simple uses of the package
```
fmt
```
, which implements
```
Printf
```
, 
```
Fprintf
```
, and so on. Within the
```
fmt
```
package,
```
Printf
```
is declared with this signature:

    Printf(format string, v ...) (n int, errno os.Error)

That 
```
...
```
represents the variadic argument list that in C would be handled using the
```
stdarg.h
```
macros but in Go is passed using an empty interface variable (
```
interface {}
```
) and then unpacked using the reflection library. It's off topic here but the use of reflection helps explain some of the nice properties of Go's
```
Printf
```
, due to the ability of
```
Printf
```
to discover the type of its arguments dynamically.

For example, in C each format must correspond to the type of its argument. It's easier in many cases in Go. Instead of
```
%llud
```
you can just say
```
%d
```
;
```
Printf
```
knows the size and signedness of the integer and can do the right thing for you. The snippet

    10    var u64 uint64 = 1<<64-1;
    11    fmt.Printf("%d %dn", u64, int64(u64));

prints

     18446744073709551615 -1

In fact, if you're lazy the format
```
%v
```
will print, in a simple appropriate  style, any value, even an array or structure. The output of

    14    type T struct { a int; b string };
    15    t := T{77, "Sunset Strip"};
    16    a := []int{1, 2, 3, 4};
    17    fmt.Printf("%v %v %vn", u64, t, a);

is

    18446744073709551615 {77 Sunset Strip} [1 2 3 4]

You can drop the formatting altogether if you use
```
Print
```
or
```
Println
```
instead of
```
Printf
```
. Those routines do fully automatic formatting. The
```
Print
```
function just prints its elements out using the equivalent of
```
%v
```
while
```
Println
```
inserts spaces between arguments and adds a newline. The output of each of these two lines is identical to that of the
```
Printf
```
call above.

    18    fmt.Print(u64, " ", t, " ", a, "n");
    19    fmt.Println(u64, t, a);

If you have your own type you'd like
```
Printf
```
or
```
Print
```
to format, just give it a
```
String()
```
method that returns a string. The print routines will examine the value to inquire whether it implements the method and if so, use it rather than some other formatting. Here's a simple example.

    09    type testType struct {
    10        a int
    11        b string
    12    }

    14    func (t *testType) String() string {
    15        return fmt.Sprint(t.a) + " " + t.b
    16    }

    18    func main() {
    19        t := &testType{77, "Sunset Strip"}
    20        fmt.Println(t)
    21    }

Since
```
*testType
```
has a
```
String()
```
method, the default formatter for that type will use it and produce the output

    77 Sunset Strip

Observe that the
```
String()
```
method calls
```
Sprint
```
(the obvious Go variant that returns a string) to do its formatting; special formatters can use the
```
fmt
```
library recursively.

Another feature of
```
Printf
```
is that the format
```
%T
```
will print a string representation of the type of a value, which can be handy when debugging polymorphic code.

It's possible to write full custom print formats with flags and precisions and such, but that's getting a little off the main thread so we'll leave it as an exploration exercise.

You might ask, though, how
```
Printf
```
can tell whether a type implements the
```
String()
```
method. Actually what it does is ask if the value can be converted to an interface variable that implements the method. Schematically, given a value
```
v
```
, it does this:

    type Stringer interface {
        String() string
    }

    s, ok := v.(Stringer);  // Test whether v implements "String()"
    if ok {
        result = s.String()
    } else {
        result = defaultOutput(v)
    }

The code uses a ``type assertion'' (
```
v.(Stringer)
```
) to test if the value stored in
```
v
```
satisfies the
```
Stringer
```
interface; if it does,
```
s
```
will become an interface variable implementing the method and
```
ok
```
will be
```
true
```
. We then use the interface variable to call the method. (The ''comma, ok'' pattern is a Go idiom used to test the success of operations such as type conversion, map update, communications, and so on, although this is the only appearance in this tutorial.) If the value does not satisfy the interface,
```
ok
```
will be false.

In this snippet the name
```
Stringer
```
follows the convention that we add ''[e]r'' to interfaces describing simple method sets like this.

One last wrinkle. To complete the suite, besides
```
Printf
```
etc. and
```
Sprintf
```
etc., there are also
```
Fprintf
```
etc. Unlike in C,
```
Fprintf
```
's first argument is not a file. Instead, it is a variable of type
```
io.Writer
```
, which is an interface type defined in the
```
io
```
library:

    type Writer interface {
        Write(p []byte) (n int, err os.Error);
    }

(This interface is another conventional name, this time for
```
Write
```
; there are also
```
io.Reader
```
,
```
io.ReadWriter
```
, and so on.) Thus you can call
```
Fprintf
```
on any type that implements a standard
```
Write()
```
method, not just files but also network channels, buffers, whatever you want.

## Prime numbers

Now we come to processes and communication-concurrent programming. It's a big subject so to be brief we assume some familiarity with the topic.

A classic program in the style is a prime sieve. (The sieve of Eratosthenes is computationally more efficient than the algorithm presented here, but we are more interested in concurrency than algorithmics at the moment.) It works by taking a stream of all the natural numbers and introducing a sequence of filters, one for each prime, to winnow the multiples of that prime. At each step we have a sequence of filters of the primes so far, and the next number to pop out is the next prime, which triggers the creation of the next filter in the chain.

Here's a flow diagram; each box represents a filter element whose creation is triggered by the first number that flowed from the elements before it.

To create a stream of integers, we use a Go**channel**, which, borrowing from CSP's descendants, represents a communications channel that can connect two concurrent computations. In Go, channel variables are references to a run-time object that coordinates the communication; as with maps and slices, use
```
make
```
to create a new channel.

Here is the first function in
```
progs/sieve.go
```
:

    09    // Send the sequence 2, 3, 4, ... to channel 'ch'.
    10    func generate(ch chan int) {
    11        for i := 2; ; i++ {
    12            ch <- i  // Send 'i' to channel 'ch'.
    13        }
    14    }

The 
```
generate
```
function sends the sequence 2, 3, 4, 5, ... to its argument channel,
```
ch
```
, using the binary communications operator
```
<-
```
. Channel operations block, so if there's no recipient for the value on
```
ch
```
, the send operation will wait until one becomes available.

The
```
filter
```
function has three arguments: an input channel, an output channel, and a prime number. It copies values from the input to the output, discarding anything divisible by the prime. The unary communications operator
```
<-
```
(receive) retrieves the next value on the channel.

    16    // Copy the values from channel 'in' to channel 'out',
    17    // removing those divisible by 'prime'.
    18    func filter(in, out chan int, prime int) {
    19        for {
    20            i := <-in;  // Receive value of new variable 'i' from 'in'.
    21            if i % prime != 0 {
    22                out <- i  // Send 'i' to channel 'out'.
    23            }
    24        }
    25    }

The generator and filters execute concurrently. Go has its own model of process/threads/light-weight processes/coroutines, so to avoid notational confusion we call concurrently executing computations in Go**goroutines**. To start a goroutine, invoke the function, prefixing the call with the keyword
```
go
```
; this starts the function running in parallel with the current computation but in the same address space:

    go sum(hugeArray); // calculate sum in the background

If you want to know when the calculation is done, pass a channel on which it can report back:

    ch := make(chan int);
    go sum(hugeArray, ch);
    // ... do something else for a while
    result := <-ch;  // wait for, and retrieve, result

Back to our prime sieve. Here's how the sieve pipeline is stitched together:

    28    func main() {
    29        ch := make(chan int);  // Create a new channel.
    30        go generate(ch);  // Start generate() as a goroutine.
    31        for {
    32            prime := <-ch;
    33            fmt.Println(prime);
    34            ch1 := make(chan int);
    35            go filter(ch, ch1, prime);
    36            ch = ch1
    37        }
    38    }

Line 29 creates the initial channel to pass to
```
generate
```
, which it then starts up. As each prime pops out of the channel, a new
```
filter
```
is added to the pipeline and**its**output becomes the new value of
```
ch
```
.

The sieve program can be tweaked to use a pattern common in this style of programming. Here is a variant version of
```
generate
```
, from
```
progs/sieve1.go
```
:

    10    func generate() chan int {
    11        ch := make(chan int);
    12        go func(){
    13            for i := 2; ; i++ {
    14                ch <- i
    15            }
    16        }();
    17        return ch;
    18    }

This version does all the setup internally. It creates the output channel, launches a goroutine running a function literal, and returns the channel to the caller. It is a factory for concurrent execution, starting the goroutine and returning its connection.

The function literal notation (lines 12-16) allows us to construct an anonymous function and invoke it on the spot. Notice that the local variable
```
ch
```
is available to the function literal and lives on even after
```
generate
```
returns.

The same change can be made to
```
filter
```
:

    21    func filter(in chan int, prime int) chan int {
    22        out := make(chan int);
    23        go func() {
    24            for {
    25                if i := <-in; i % prime != 0 {
    26                    out <- i
    27                }
    28            }
    29        }();
    30        return out;
    31    }

The 
```
sieve
```
function's main loop becomes simpler and clearer as a result, and while we're at it let's turn it into a factory too:

    33    func sieve() chan int {
    34        out := make(chan int);
    35        go func() {
    36            ch := generate();
    37            for {
    38                prime := <-ch;
    39                out <- prime;
    40                ch = filter(ch, prime);
    41            }
    42        }();
    43        return out;
    44    }

Now
```
main
```
's interface to the prime sieve is a channel of primes:

    46    func main() {
    47        primes := sieve();
    48        for {
    49            fmt.Println(<-primes);
    50        }
    51    }

## Multiplexing

With channels, it's possible to serve multiple independent client goroutines without writing an explicit multiplexer. The trick is to send the server a channel in the message, which it will then use to reply to the original sender. A realistic client-server program is a lot of code, so here is a very simple substitute to illustrate the idea. It starts by defining a
```
request
```
type, which embeds a channel that will be used for the reply.

    09    type request struct {
    10        a, b    int;
    11        replyc  chan int;
    12    }

The server will be trivial: it will do simple binary operations on integers. Here's the code that invokes the operation and responds to the request:

    14    type binOp func(a, b int) int

    16    func run(op binOp, req *request) {
    17        reply := op(req.a, req.b)
    18        req.replyc <- reply
    19    }

Line 18 defines the name
```
binOp
```
to be a function taking two integers and returning a third.

The
```
server
```
routine loops forever, receiving requests and, to avoid blocking due to a long-running operation, starting a goroutine to do the actual work.

    21    func server(op binOp, service chan *request) {
    22        for {
    23            req := <-service;
    24            go run(op, req);  // don't wait for it
    25        }
    26    }

We construct a server in a familiar way, starting it and returning a channel connected to it:

    28    func startServer(op binOp) chan *request {
    29        req := make(chan *request);
    30        go server(op, req);
    31        return req;
    32    }

Here's a simple test. It starts a server with an addition operator and sends out
```
N
```
requests without waiting for the replies. Only after all the requests are sent does it check the results.

    34    func main() {
    35        adder := startServer(func(a, b int) int { return a + b });
    36        const N = 100;
    37        var reqs [N]request;
    38        for i := 0; i < N; i++ {
    39            req := &reqs[i];
    40            req.a = i;
    41            req.b = i + N;
    42            req.replyc = make(chan int);
    43            adder <- req;
    44        }
    45        for i := N-1; i >= 0; i-- {   // doesn't matter what order
    46            if <-reqs[i].replyc != N + 2*i {
    47                fmt.Println("fail at", i);
    48            }
    49        }
    50        fmt.Println("done");
    51    }

One annoyance with this program is that it doesn't shut down the server cleanly; when
```
main
```
returns there are a number of lingering goroutines blocked on communication. To solve this, we can provide a second,
```
quit
```
channel to the server:

    32    func startServer(op binOp) (service chan *request, quit chan bool) {
    33        service = make(chan *request);
    34        quit = make(chan bool);
    35        go server(op, service, quit);
    36        return service, quit;
    37    }

It passes the quit channel to the
```
server
```
function, which uses it like this:

    21    func server(op binOp, service chan *request, quit chan bool) {
    22        for {
    23            select {
    24            case req := <-service:
    25                go run(op, req);  // don't wait for it
    26            case <-quit:
    27                return;
    28            }
    29        }
    30    }

Inside 
```
server
```
, the
```
select
```
statement chooses which of the multiple communications listed by its cases can proceed. If all are blocked, it waits until one can proceed; if multiple can proceed, it chooses one at random. In this instance, the
```
select
```
allows the server to honor requests until it receives a quit message, at which point it returns, terminating its execution.

All that's left is to strobe the
```
quit
```
channel at the end of main:

    42        adder, quit := startServer(func(a, b int) int { return a + b });
    ...
    55        quit <- true;

关于Go编程和并发程序设计还有许多其它的内容，但这份快速入门教程应该已经给你提供了一点基础知识。

