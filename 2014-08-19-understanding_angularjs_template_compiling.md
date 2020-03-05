---
title: 理解AnguarJS中的模板编译
date: '2014-08-19 05:08:00 +0800'
---
在一开始学习AngularJS的过程中，模板的工作原理可能是最令人难解的问题之一。在其他的框架中，一般来说模板就是一个字符串，在这个字符串中使用一个特殊的表达方式可以嵌入一个传入的外部对象的数据，其本质上就是一个字符串的操作：输入字符串，输出字符串，然后通过`.innerHTML()`把所有搞出来的东西塞到DOM里面去。

很明显AngularJS的模板不是这样做的。它有双向数据绑定，可以完美的在视图中与最新的数据模型同步。它还会自动在`ng-click`上注册事件监听器，甚至可以将视图中输入控件中的数据同步回数据模型。太神奇了！

这个当然不是什么魔术，事实上将一个模板转换为一个带动态绑定和事件监听功能的动态视图，这中间的过程其实很简单。一旦搞明白了这个过程，对于AngularJS应用的理解也会上升一个台阶。

这里有一个模板

    <div ng-app>
        <label>Name:</label>
        <input type="text" ng-model="yourName" placeholder="Enter a name here">
        # Hello {{yourName}}!
    </div>

如你所见，这是个最简单的AngularJS的应用页面。

##反向控制（IoC）

第一个需要了解的概念是"反向控制"（IoC）。AngularJS不需要手工启动应用，而是假定你会遵循一定的规则在代码中放一些基本的设定。

例如，AngularJS会假定HTML代码中有一个带有`ng-app`属性的元素，表示你的应用的"根"节点。它表示AngularJS可以接管这个节点以及之下所有子节点。这一点可以保证AngularJS可以和其他的JavaScript框架共存。当AngularJS启动应用的时候，它会遍历DOM内的节点，并查找这个属性，这个在AngularJS术语中叫"指令"（Directive）。注意这个`ng-app`指令可以放在任何DOM节点上，包括`<html>`和`<body>`标签。

AngularJS还会假定其他的框架不会接触到它的"根"节点下面的所有内容，否则可能会导致未知行为，或者打破双向数据绑定和事件监听器。

##深入模板

    <label>Name:</label>
    <input type="text" ng-model="yourName" placeholder="Enter a name here">

# Hello {{yourName}}!

这一部分是模板。"根"节点下面的所有内容都会被视为模板，之后将会被编译。模板与数据模型（`$scope`）和控制器一起构成了动态视图，用户可以在浏览器中看到并与之交互。本例中没有控制器和明确的数据模型，但AngularJS会在后台创建对应的内容。

所有的AngularJS都会有一个`$rootScope`，它会持有所有子scope的引用，它自身保存的数据也可以被所有的`$scope`共享。本例中，由于没有明确指定控制器，所以模板会被绑定到这个`$rootScope`上，并设置一个子`$scope`。

在模板中，给输入控件绑定了一个模型（由ng-model指明的yourName），AngularJS会在这个数据控件上注册一个键盘事件监听器，并且将所有输入到这个控件中的内容自动保存到`$rootScope.yourName`，但我们并没有也并不需要声明这个变量。`scope`中的变量会被初始化为`undefined`，就像正常的JavaScript对象一样。

模板中还用到了`$interpolate`指令，表示为两对大花括号 `{{ yourName }}`。这个指令会创建一个`$watcher`，监听模型的变化，并在发生变化的时候将数据更新到视图上。

接下来看看如何将一个DOMElement转换成动态视图。

##编译模板

AngularJS找到`ng-app`指令之后，它会启动并创建一个新的`$rootScope`，开始编译"根"节点（带`ng-app`的那个节点）下面所有的子节点。

接下来发生的事情分为两步，编译和链接（这里借用了编译原理中的术语，但本质上是一样的）。更深的介绍可以参考文档[AngularJS documentation on the HTML Compiler](http://docs.angularjs.org/guide/compiler)。

首先，Angular的`$compile`函数将传入的DOMElement作为输入。这一点与其它的框架很不一样，AngularJS会使用浏览器的API遍历整个DOM，而其它模板只是在做字符串替换。如果需要用字符串作为传入的模板，则先要用`$angular.element`函数将字符串转为DOMElement。这个函数实际上就是jQuery中的`$()`函数的。

`$compile`函数会遍历DOM，并查找"指令"（Directive），将找到的每个"指令"添加到一个列表中，整个DOM遍历完成后，再将列表中的"指令"按照"优先级"排序。之后，执行每个"指令"自己的`compile`函数，让"指令"有机会去修改DOM。每个指令的`compile`函数会返回一个"链接"函数，该函数会被拼接成一个完整的链接函数，并被返回。

接下来，AngularJS会执行返回的"链接"函数，对应的scope会被传入到这个执行过程中。这一步中，所有的子"链接"函数都会被执行，并绑定在同一个scope上，或依照"指令"的设定创建一个新的scope。所有的"链接"函数执行完毕后，每个"链接"函数都会返回一组DOMElement，这些DOMElement已经完成数据绑定和事件监听，AngularJS会将它们添加到父节点。

上述过程的伪代码可以表示如下

    var $compile = ...; //注入到你的代码
    var $rootScope = ...; //注入
    var parent = ...; //编译过的模板内容会被添加到该DOMElement下
    var template = ...; //我们的模板的DOMElement

    var linkFn = $compile(template); //编译模板，返回"链接"函数

    var element = linkFn(scope); //"链接"，返回处理好的DOMElement

    parent.appendChild(element); //将处理好的DOMElement添加到父节点

##总结
基本就是这些了。如你所见，AngularJS完全不同于其他的模板系统，它约定了一些规则，并基于这些规则做了一些假定，之后你就不必将精力耗费在启动代码上，而可以放在真正的应用上。这只是AngularJS的一部分，之后会继续讲讲`$watch`和`$digest`如何保证视图刷新。

via [src](http://daginge.com/technology/2014/03/04/understanding-template-compiling-in-angularjs/)

