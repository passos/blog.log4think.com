---
title: SharpDevelop源码分析 (完整版)
date: '2004-10-14 18:55:22 +0800'
---
```
注：本文是我2004年写的一系列的心得，原文是发在[http://blog.csdn.net/passos/archive/2004/10/04/124722.aspx]下的系列文章。本站Log4think的Blog建立之后，把文章也迁移过来了。原文为三篇，迁移以后经过润色、合并，整理为一篇完整的文章。
```

## 〇、序 

最近开始学习.Net，遇到了一个比较不错的开源的IDE SharpDevelop。这个开发工具是使用C#开发的，比较吸引我的一点就是它是采用了和Eclipse类似的插件技术来实现整个系统的。而这个插件系统是我最感兴趣的地方，因此开始了一段代码的研究。在本篇之后，我会陆续把我研究的心得写下来。

## 一、基本概念 

首先，先从代码的角度来对 SharpDevelop 来一个感性的认识。可以从[这里](http://www.icsharpcode.com)下载到可执行程序和代码包。安装的细节略过不提，先运行一下看看，界面、风格的感觉是不是跟VS如出一辙。不过目前的版本是1.0.0.1550，还有很多地方需要完善。关于代码和系统结构，SharpDevelop的三个作者写了一本书，各位看官可以参考一下，不过我看过之后还是有很多地方不太理解。

然后，来解释一下什么叫插件以及为什么要使用插件系统。以往的系统，开发人员编译发布之后，系统就不允许进行更改和扩充了，如果要进行某个功能的扩充，则必须要修改代码重新编译发布，这就带来了比较大的不方便。解决的方法有很多，例如提供配置等等方法。在解决方案之中，插件是一个比较好的解决方法。大家一定知道PhotoShop、WinAmp吧，他们都有"插件"的概念，允许其他开发人员根据系统预定的接口编写扩展功能（例如PhotoShop中各种各样的滤镜）。所谓的插件就是系统的扩展功能模块，这个模块是以一个独立文件的形式出现的，与系统是相对独立。在系统设计期间并不知道插件的具体功能，仅仅是在系统中为插件留下预定的接口，系统启动的时候根据插件的配置寻找插件，根据预定的接口把插件挂接到系统中。

这样的方式带来什么样的优点呢？首先是系统的扩展性大大的增强了，如果在系统发布后需要对系统进行扩充，不必重新编译，只需要修改插件就可以了。其次有利与团队开发，各个功能模块由于是以插件的形式表现在系统中，系统的Daily Build 也变得很简单了，不会因为某个模块的错误而导致整个系统BUILD失败，失败的仅仅是一个插件而已。

PhotoShop和Winamp的插件系统是比较典型的，首先实现了一个包含基本功能的系统，然后在这个系统的基础上挂接其他扩展的功能插件。而SharpDevelop在插件的形式方面做的更加彻底，整个核心就仅仅是一个插件管理系统而已，没有任何具体的功能。而用户看到的所有的界面、功能全部都是以插件的形式挂入的。在这样的一个插件系统下，可以不修改基本的核心系统，仅仅开发不同的插件就keyhi构造出具备不同功能的应用系统。

进入到SharpDevelop的安装目录中，在Bin目录下的SharpDevelop.exe 和 SharpDevelop.Core.dll是它核心的插件系统。在Addins目录下有两个后缀为addin的文件，其中一个 SharpDevelopCore.addin 就是它的核心插件的定义（配置）文件，里面定义的各个功能模块存在于Bin\Sharpdevelop.Base.dll 文件中，另外还有一些插件定义在Addins目录下的addin文件中。

分析SharpDevelop的代码，首先要弄清楚几个基本的概念，某些概念的真实含义和从字面上看起来的有一些区别，这曾经让我非常困惑，直到深入了代码之后才发现其本来的含义。

### 1、AddInTree  插件树 

SharpDevelop 中的插件被组织成一棵插件树结构，树的结构是通过 Extension（扩展点）中定义的Path(路径)来定义的，类似一个文件系统的目录结构。系统中的每一个插件都在配置文件中指定了 Extension，通过Extension中指定的 Path 挂到这棵插件树上。在系统中可以通过 AddTreeSingleton对象来访问各个插件，以实现插件之间的互动。

### 2、 AddIn 插件 

在 SharpDevelop 的概念中，插件是包含多个功能模块的集合（而不是我过去认为的一个功能模块）。在文件的表现形式上是一个addin配置文件，在系统中对应 AddIn 类。

### 3、Extension 扩展点 

SharpDevelop中的每一个插件都会被挂到 AddInTree（插件树） 中，而具体挂接到这个插件树的哪个位置，则是由插件的 Extension 对象中的 Path 指定的。在addin 配置文件中，对应于`<Extension>`标签 。例如下面这个功能模块的配置

	<Extension path="/SharpDevelop/Workbench/Ambiences">
	    <Class id=".NET" class="ICSharpCode.SharpDevelop.Services.NetAmbience"/>
	</Extension>

指定了扩展点路径为 `/SharpDevelop/Workbench/Ambiences` ，也就是在插件树中的位置。

### 4、Codon 

这个是一个很不好理解的词儿，在 SharpDevelop 的三个作者写的书的中译版中被翻译为*密码子*，&^@#WTF%&^* 真是叫人凌乱，完全搞不懂是啥意思啊。这个单词在词典中还有一个翻译叫"基码"，总之是各种词不达意。

顺便对此抱怨两句，当在做一个其实已经有类似实现的系统的时候，某些作者经常喜欢用一些不同的词汇来表达其实以及存在的一个概念。比如把大家都能理解的plugin叫做addin，这个也就罢了，但是如果偏偏要新创一个陌生的词儿来表达已有的概念，我就不知该如何形容是好了。

根据我对代码的理解，Codon 的功能是描述(包装)一个功能模块（一个功能模块对应一个实现了具体功能的 Command 类）。为了方便访问各个插件中的功能模块， Codon 给各种功能定义了基本的属性，分别是 ID (功能模块的标识)，Name (功能模块的类型。别误会，这个Name 是addin文件定义中Codon的XML结点的名称，ID才是真正的名称)，其中Name可能是Class(类)、MenuItem(菜单项)、Pad(面板)等等。根据具体的功能模块，可以继承Codon定义其他的一些属性，SharpDevelop中就定义了 ClassCodon、MenuItemCodon、PadCodon等等，你可以根据需要自己定义其他类型的Codon。在addin定义文件中，Codon对应于 `<Extension>` 标签下的内容。例如下面这个定义

	<Extension
	    path = "/SharpDevelop/Workbench/Ambiences">
	    <Class id=".NET" class="ICSharpCode.SharpDevelop.Services.NetAmbience"/>
	</Extension>

`<Extension path=...>` 标签内部定义了一个Codon，扩展点路径为 `/SharpDevelop/Workbench/Ambiences`。内部的`<Class>` 标签表示该Codon是一个 Class(类)，接着定义了该Codon的 ID和具体实现该Codon的类名`ICSharpCode.SharpDevelop.Services.NetAmbience`。运行期间将通过反射来找到对应的类并创建出来。

再例如这一个定义

	<Extension
	    path="/SharpDevelop/Views/ProjectBrowser/ContextMenu/CombineBrowserNode">
	    <MenuItem id="Compile"
	        label="${res:XML.MainMenu.RunMenu.Compile}"
	        class="ICSharpCode.SharpDevelop.Commands.Compile"/>
	    <MenuItem id = "CompileAll"
	        label="${res:XML.MainMenu.RunMenu.CompileAll}"
	        class="ICSharpCode.SharpDevelop.Commands.CompileAll"/>
	    <MenuItem id="CombineBuildGroupSeparator" label="-" />
	        ...
	</Extension>

这个扩展点中定义了三个菜单项，以及各个菜单项的名字、标签和实现的类名。这里的Codon就对应于系统中的MenuCodon对象。

### 5、Command 命令 

正如前文所述，Codon描述了一个功能模块，而每个功能模块都是一个 ICommand 的实现。最基本的 Command 是  AbstractCommand，根据Codon的不同对应了不同的 Command。例如 MenuItemCodon 对应 MenuItemCommand 等等。

### 6、Service 服务 

插件系统中，有一些功能是整个系统都要使用的，例如文件访问、资源、消息等等。这些功能都作为插件系统的一个基本功能为整个系统提供服务，就叫"服务"好了。为了便于访问，这些服务都统一通过 ServiceManager 来管理。其实服务也是一种类型的插件，它们的扩展点路径在目录树中的 /Workspace/Services 中。

理解了这几个基本的概念之后，就可以看看 SharpDevelop 的代码了。起点在 `src\main\startup.cs` ，之后是 addin.cs 和 addinTree.cs 等几个文件。

## 二、主程序+隐藏的初始化 

在大学里，模拟电路这门课永远是我心头的痛，直到现在也是这样。我总会不自觉的按照程序设计的模块化思路去尝试理解电路图，会问"这部分电路是做什么用的"、"为什么会有这样的效果"之类。在我的印象里，每部分的电路都应该有一定的用处，可惜总是看不明白。妈妈说，电路图不应该总是一个个模块的看，而是应该是从电源的一极顺着电路看，一直看到电源的另一极。我现在仍然不懂看电路图，可是以我看代码的经验来说，我觉得分析源代码按照这样的思路来看会比较容易把脉络理清楚。也就是从入口开始，顺着逻辑流一路看下去，同时把数据结构分析清楚，就很容易理解代码的内容了。

在SharpDevelop的代码中，由于很多的接口和插件的原因，很多代码在看到某个地方会突然失去函数/方法调用的线索。例如看某个函数的实现的时候会跳到一个接口里面去，那是因为这部分功能在运行期才会给一个实现了这个接口的对象来进行具体的执行。从这个角度来说，设计模式也给研究代码稍微带来了一点小小的难度。在看Linux下源代码的时候也经常遇到这种问题，在这个时候寻找代码线索比较好的方法是用一个文本搜索工具来搜索相关的关键字。在Linux下经常会用grep，Windows下面类似UltraEdit的"批量文件查找"功能会很好用（或者"Search And Replace"之类的工具）。

我不会大段大段的贴原始代码，而是在需要的地方只抽出主要的代码。因此最好能够对照原始代码一起看。

原始代码包解压缩，由于SharpDevelop本身对于察看代码不是很方便，没有"转到定义"之类的功能，因此我建议你把它的代码转成VS的工程来看。不过很可惜，SharpDevelop的工程导出功能现在有问题，如果导出\src\SharpDevelop.cmbx 这个总的复合工程的话会失败（我记得RC1版本是可以成功的，不知道为什么后来的版本反而会出问题），所以只能一个一个工程的导出。

好了，开始读SharpDevelop的代码吧

### 1、起点 

在主程序的起点在\src\Main\StartUp\SharpDevelopMain.cs，找到Main函数这就是整个程序的起点了。开始的部分是显示封面窗体并加上命令行控制，其中SplashScreenForm 定义在\src\Main\Base\Gui\Dialogs\SplashScreen.cs文件中，这部分就不多说了。之后是

	Application.ThreadException += new ThreadExceptionEventHandler(ShowErrorBox);

SharpDevelop为了有效的进行错误报告，因此自己进行了异常的控制。系统出现异常的时候，SharpDevelop会拦截下来弹出它自己的异常提示报告对话框。这个代码就是在这一行实现的。其中 ShowErrorBox 这个方法就在类SharpDevelopMain中，ExceptionBox 定义在\src\Main\StartUp\Dialogs\ExceptionBox.cs中。如果需要进行自己的异常控制，可以学习一下这里的技巧。

### 2、充满玄机的初始化 

	string [] addInDirs = ICSharpCode.SharpDevelop.AddInSettingsHandler.GetAddInDirectories( out ignoreDefaultPath );
	AddInTreeSingleton.SetAddInDirectories(addInDirs, ignoreDefaultPath);

这段不起眼的代码是启动并初始化的真正的起点。

首先通过AddInSettingsHandler取得插件的目录，并告知AddInTreeSingleton。AddInSettingsHandler定义在\src\Main\StartUp\Dialogs\AddInTreeSettingsHandler.cs中，它通过读取系统配置（App.config）文件中的AddInDirectory节点的Path属性来确定插件的目录位置，或者你也可以通过自己定义的AddInDirectories节来指定插件目录。如果你没有做这些配置，默认的目录在SharpDevelop运行目录的..\Addins目录下。

	ServiceManager.Services.AddService(new MessageService());
	ServiceManager.Services.AddService(new ResourceService());
	ServiceManager.Services.AddService(new IconService());

通过ServiceManager(服务管理器)加入三个系统默认的服务，消息服务、资源服务、图标服务。这三个服务中，消息服务是显示各种信息提示，另外两个是属于系统的资源，SharpDevelop通过服务来进行统一调用和管理。

	ServiceManager.Services.InitializeServicesSubsystem("/Workspace/Services");

初始化其他的服务。SharpDevelop把服务定义在插件树的/Workspace/Services这个路径中，凡是在这个路径下的插件都被认为是服务，因此如果你自己定义了一个服务的话，也需要挂到这个路径下（这里就是系统服务的扩展点了）。

注意！这一步中，在我们的眼皮子底下悄悄的进行了一个重要的初始化工作。请看，ServiceManager 定义在\src\Main\Core\Services\ ServiceManager.cs文件中，察看它的InitializeServicesSubsystem方法，发现这样一行

	AddServices((IService[])AddInTreeSingleton.AddInTree.GetTreeNode(servicesPath).BuildChildItems(this).ToArray(typeof(IService)));

在这里，AddInTreeSingleton首次调用了AddInTree（插件树）的实例。按照Singleton模式，只有在首次调用的时候才会初始化实例，这里也是同样如此。整个系统的AddInTree是在这一步中进行了初始化工作，后面会详细讲AddInTree如何进行初始化工作，这里暂且先顺便看看服务的初始化。在ServiceManager的InitializeServicesSubsystem方法中，通过AddInTree检索服务插件路径下的所有配置，并通过它来读取、建立具体的对象，然后加入到服务列表中。之后通过一个循环，逐个的调用各个服务的InitializeService方法初始化服务。

AddInTree的初始化工作容稍候再看，先把主体的代码看完。

	commands = AddInTreeSingleton.AddInTree.GetTreeNode("/Workspace/Autostart").BuildChildItems(null);
	for (int i = 0; i < commands.Count - 1; ++i)
	{
	    ((ICommand)commands[i]).Run();
	}

/Workspace/Autostart是系统自动运行命令的扩展点路径，定义在这个路径下的插件会在系统启动的时候自动运行。在这里，通过插件树初始化建立处于这个路径下的Command（命令），并逐一执行。BuildChildItems方法的功能是建立这个扩展点下的Command列表，会在介绍AddTree的时候具体说明它的实现。

### 3、收尾 

主程序代码的最后，初始化完毕、关闭封面窗体，然后执行命令列表中最后一个命令（也就是系统的主界面）。在主界面退出的时候，系统卸载所有的服务。

在这部分代码中出现了两个系统指定的扩展点路径 /Workspace/Services 和 /Workspace/Autostart ，实现服务和指定系统自动运行命令的时候就可以挂到这两个扩展点路径下了。
托反射的福，ServiceManager.Services可以通过类型（接口）来查找具体的实例，也就是GetServices方法。但是ServiceManager的具体实现可以容后再看，这里已经不是最紧要的部分了。
接下来，来看看整个插件系统的核心－AddinTree的代码，看看它是如何通过插件配置进行初始化并建立起整个系统的插件树骨干。

## 三、插件系统 

上回说到SharpDevelop入口Main函数的结构，ServiceManager.Service在InitializeServicesSubsystem方法中首次调用了AddInTreeSingleton的AddInTree实例，AddInTree在这里进行了初始化。本回进入AddInTree着重讲述SharpDevelop的插件系统。在叙述的时候为了方便起见，对于"插件"和插件具体的"功能模块"这两个词不会特别的区分，各位看官可以从上下文分辨具体的含义（而事实上，SharpDevelop中的"插件"是指.addin配置文件，每一个"插件"都可能会包含多个"功能模块"）。

### 1、插件的配置 

既然说到插件系统，那么先来看一看SharpDevelop插件系统的组织形式和内部的数据结构。
很多时候，同一个事物从不同的角度来看会得出不一样的结论，SharpDevelop的插件系统也是如此。在看SharpDevelop的代码以前，按照对插件的理解，我认为所谓的"插件"就是代表一个功能模块，插件的配置就是描述该插件并指定如何把这个插件挂到系统中。SharpDevelop中有插件树的思想，也就是每一个插件在系统中都有一个扩展点的路径。那么按照最初对插件的理解，编写插件需要做的就是：
A、根据插件接口编写功能模块实现一个Command类
B、编写一个配置文件，指定Command类的扩展点(Extension)路径，挂到插件树中

之后按照这样的理解，我编写了一个察看插件树的插件AddinTreeView，打算挂到SharpDevelop中去。根据SharpDevelop对插件的定义，我把具体插件的AddinTreeViewCommand实现了之后，编写了一个配置文件AddinTreeView.addin如下：

	<AddIn
	    name="AddinTreeView"
	    author="SimonLiu"
	    copyright="GPL"
		url="http://www.icsharpcode.net"
		description="Display AddinTree"
		version="1.0.0">

		<Runtime>
			<Import assembly="../../bin/ AddinTreeView.dll" />
		</Runtime>
		<Extension path="/SharpDevelop/Workbench/MainMenu/Tools">
			<MenuItem id="AddinTreeView" label="View AddinTree"
				class="Addins.AddinTreeView.AddinTreeViewCommand" />
		</Extension>
	</AddIn>

在配置文件中，Runtime节指定了插件功能模块所在的库文件Addins.dll的具体路径，在Extension节中指定了扩展点路径/SharpDevelop/Workbench/MainMenu/Tools（我是打算把它挂到主菜单的工具菜单下），然后在Extension内指定了它的Codon为 MenuItem以及具体的ID、标签、Command类名。这样做，SharpDevelop运行的很不错，我的插件出现在了Tools菜单下。之后，我又编写了一个SharpDevelop的资源管理器（ResourceEditor）的插件类ResourceEditor.dll并把它挂到Tool菜单下。同样的，我也写了一个ResourceEditor.addin文件来对应。系统工作的很正常。

如果我们对于每一个插件都编写这样的一个配置文件，那么插件的库文件(.dll)、插件配置文件(.addin)是一一对应的。不过这样就带来了一个小小的问题，在这样的一个以插件为基础的系统中，每一个菜单、工具栏按钮、窗体、面板都是一个插件，那么我们需要为每一个插件编写配置文件，这样就会有很多个配置文件（似乎有点太多了，不是很好管理）。SharpDevelop也想到了这个问题，于是它允许我们把多个插件的配置合并在一个插件的配置文件中。因此，我把我的两个插件库文件合并到一个Addins工程内生成了Addins.dll，又重新编写了我的插件配置文件MyAddins.addin如下：

	<AddIn
	    name="MyAddins"
	    author="SimonLiu"
	    copyright="GPL"
		url="http://www.icsharpcode.net"
		description="Display AddinTree"
		version="1.0.0">

		<Runtime>
			<Import assembly="../../bin/Addins.dll" />
		</Runtime>

		<Extension path="/SharpDevelop/Workbench/MainMenu/Tools">
			<MenuItem id="ResourceEditor" label="Resource Editor"
				class="Addins.ResourceEditor.Command.ResourceEditorCommand" />
			<MenuItem id="AddinTreeView" label="View AddinTree"
				class="Addins.AddinTreeView.AddinTreeViewCommand" />
		</Extension>
	</AddIn>  

这样，我把两个插件的功能模块使用一个插件配置文件来进行配置。同样的，也可以把几十个功能模块合并到一个插件配置文件中。SharpDevelop把这个插件配置文件称为"Addin(插件)"，而把具体的功能模块封装为Codon，使用Command类来包装具体的功能。SharpDevelop本身的核心配置SharpDevelopCore.addin里面就包含了所有的基本菜单、工具栏、PAD的插件配置。

回过头来看一下，现在有了两颗树。首先，插件树本身是一个树形的结构，这个树是根据系统所有插件的各个Codon的扩展点路径构造的，表示了各个Codon在插件树中的位置，各位看官可以通过我写的这个小小的AddinTreeView来看看SharpDevelop中实际的结构。其次，插件的配置文件本身也具有了一个树形的结构，这个树结构的根节点是系统的各个插件配置文件，其下是根据这个配置文件中的Extension节点的来构成的，描述了每个Extension节点下具有的Codon。我们可以通过SharpDevelop的Tools菜单下的AddinScout来看看这个树的结构。
我为了试验，把SharpDevelop的插件精简了很多，构成了一个简单的小插件系统。下面是这个精简系统的两个树的截图。各位看官可以通过这两副图理解一下插件树和插件配置文件的关系（只是看同样问题的两个角度，一个是Codon的ExtensionPath，一个是配置文件的内容）。

<a href="http://log4think.com/wp-content/uploads/2004/10/AddinTreeView1.jpg"><img src="http://log4think.com/wp-content/uploads/2004/10/AddinTreeView1.jpg" alt="AddinTreeView" width="920" height="514" class="alignnone size-full wp-image-742" /></a>
<a href="http://log4think.com/wp-content/uploads/2004/10/AddinScout21.jpg"><img src="http://log4think.com/wp-content/uploads/2004/10/AddinScout21.jpg" alt="AddinScout2" width="920" height="514" class="alignnone size-full wp-image-741" /></a>

总结一下SharpDevelop插件的配置文件格式。首先是`<AddIn>`节点，指定AddIn的名称、作者之类的属性。其次，在AddIn节点下的`<Runtime>`节点内，使用`<Import ...>`来指定本插件配置中Codon所在的库文件。如果分布在多个库文件中，可以一一指明。然后，编写具体功能模块的配置。每个功能模块的配置都以扩展点`<Extension>`开始，指定了路径(Path)属性之后，在这个节点内配置在这个扩展点下具体的Codon。每个Codon根据具体不同的实现有不同的属性。各位看官可以研究一下SharpDevelop的核心配置文件SharpDevelopCore.addin的写法，相信很容易理解的。

### 2、插件系统的核心AddIn和AddInTree 
前文讲到，在SharpDevelop的Main函数中，ServiceManager.Service在InitializeServicesSubsystem方法中首次调用了AddInTreeSingleton的AddInTree实例，AddinTree在这个时候进行了初始化。现在我们就来看看AddInTreeSingleton.AddInTree到底做了些什么事情，它定义在\src\Main\Core\AddIns\AddInTreeSingleton.cs文件中。

	public static IAddInTree AddInTree
	{
		get
		{
			if (addInTree == null)
			{
				CreateAddInTree();
			}
			return addInTree;
		}
	}

AddInTreeSingleton是插件树的一个Singleton（具体的可以去看《设计模式》了），AddInTreeSingleton.AddInTree是一个属性，返回一个IAddinTree接口。这里我注意到一点，AddInTreeSingleton是从DefaultAddInTree继承下来的。既然它是一个单件模式，包含的方法全部都是静态方法，没有实例化的必要，而且外部是通过AddInTree属性来访问插件树，为什么要从DefaultAddInTree继承呢？这好像没有什么必要。这也许是重构过程中被遗漏的一个小问题吧。

我们先来看看IAddinTree接口的内容，它定义了这样的几个内容：
A、属性ConditionFactory ConditionFactory　返回一个构造条件的工厂类，这里的条件是指插件配置中的条件，我们以后再详细说明。
B、属性CodonFactory CodonFactory　返回一个构造Codon的工厂类。
C、属性AddInCollection AddIns 返回插件树的根节点Addin（插件）集合。
D、方法IAddInTreeNode GetTreeNode(string path) 根据扩展点路径（path）返回对应的树节点
E、方法void InsertAddIn(AddIn addIn) 根据AddIn中的扩展点路径添加一个插件到树中
F、方法void RemoveAddIn(AddIn addIn) 删除一个插件
G、方法Assembly LoadAssembly(string assemblyFile)  读入插件中Runtime节的Import指定的Assembly，并构造相应的CodonFactory和CodonFactory类。

AddInTreeSingleton在首次调用AddInTree的时候会调用CreateAddInTree方法来进行初始化。CreateAddInTree方法是这样实现的：

	addInTree = new DefaultAddInTree();

初始化插件树为DefaultAddInTree的实例，这里我感受到了一点重构的痕迹。首先，DefaultAddInTree从名称上看是默认的插件树（既然是默认，那么换句话说还可以有其他的插件树）。但是SharpDevelop并没有给外部提供使用自定义插件树的接口（除非修改这里的代码），也就是说这个名称并不像它本身所暗示的那样。其次，按照Singleton通常的写法以及前面提到AddInTreeSingleton是从DefaultAddInTree继承下来的疑问，我猜想DefaultAddinTree的内容本来是在AddinTreeSingleton里面实现的，后来也许为了代码的条理性，把实现IAddinTree内容的代码剥离了出去，形成了DefaultAddinTree类。至于继承DefaultAddInTree的问题，也许这里本来是一个AddInTree的基类。这是题外话，也未加证实，各位看官可以不必放在心上（有兴趣的可以去找找以前SharpDevelop的老版本的代码来看看）。

这里有两个察看代码的线路，一个是DefaultAddInTree的构造函数的代码，在这个构造函数中构造了Codon和Condtion的工厂类。另外一个是CreateAddInTree后面的代码，搜索插件文件，并根据插件文件进行AddIn的构造。各位看官可以选择走分支线路，也可以选择先看主线（不过这样你会漏掉不少内容）。

#### 2.1 支线 （DefaultAddInTree的构造函数）

此时把CreateAddInTree的代码中断一下压栈先，跳到DefaultAddInTree的构造函数中去看一看。DefaultAddInTree定义在\src\Main\Core\AddIns\DefaultAddInTree.cs文件中。在DefaultAddInTree的构造函数中，注意到它具有一个修饰符internal，也就是说这个类只允许Core这个程序集中的类对DefaultAddInTree进行实例化（真狠啊）。构造函数中的代码只有一句：

	LoadCodonsAndConditions(Assembly.GetExecutingAssembly());

虽然只有一行代码，不过这里所包含的内容却很精巧，是全局的关键，要讲清楚我可有得写了。首先，通过全局的Assembly对象取得入口程序的Assembly，传入LoadCodonsAndConditions方法中。在该方法中，枚举传入的Assembly中的所有数据类型。如果不是抽象的，并且是AbstractCodon的子类，并且具有对应的CodonNameAttribute属性信息，那么就根据这个类的名称建立一个对应的CodonBuilder并它加入CodonFactory中（之后对Condition也进行了同样的操作，专门来看Codon部分，Condition跟Codon基本上是一样的）。
这里的CodonFactory类和CodonBuilder类构成了SharpDevelop插件系统灵活的基础，这里可要看仔细了。

以实例来演示，以前文我编写的AddinTreeViewCommand为例。在入口的Assembly中会搜索到MenuItemCodon，它是AbstractCodon的一个子类、包装MenuItem(菜单项)Command（命令）的Codon。符合条件，执行

	codonFactory.AddCodonBuilder(new CodonBuilder(type.FullName, assembly));

首先根据类名MenuItemCodon和assembly 构造CodonBuilder。CodonBuilder定义在\src\Main\Core\AddIns\Codons\CodonBuilder.cs文件中。在CodonBuilder的构造函数中根据MenuItemCodon的CodonNameAttribute属性信息取得该Codon的名称MenuItem。CodonNameAttribute描述了Codon的名称，这个MenuItem也就是在.addin配置文件中对应的`<MenuItem>`标签，后文会看到它的重要用途。在CodonBuilder中除了包含了该Codon的ClassName（类名）和CodonName属性之外，就只有一个方法BuildCodon了。

	public ICodon BuildCodon(AddIn addIn)
	{
		ICodon codon;
		try {
			// create instance (ignore case)
			codon = (ICodon)assembly.CreateInstance(ClassName, true);

			// set default values
			codon.AddIn = addIn;
		} catch (Exception) {
			codon = null;
		}
		return codon;
	}

很明显，BuildCodon根据构造函数中传入的assembly和类型的ClassName，建立了具体的Codon的实例，并和具体的AddIn关联起来。
之后，codonFactory调用AddCodonBuilder方法把这个CodonBuilder加入它的Builder集合中。继续向上一层，看看codonFactory如何使用这个CodonBuilder。

在文件\src\Main\Core\AddIns\Codons\CodonFactory.cs中，codonFactory只有两个方法。AddCodonBuilder方法把CodonBuilder加入一个以CodonName为索引的Hashtable中。另外一个方法很重要：

	public ICodon CreateCodon(AddIn addIn, XmlNode codonNode)
	{
		CodonBuilder builder = codonHashtable[codonNode.Name] as CodonBuilder;

		if (builder != null) {
			return builder.BuildCodon(addIn);
		}

		throw new CodonNotFoundException(String.Format("no codon builder found for <{0}>", codonNode.Name));
	}

在这里，addin是这个配置文件的描述（也就是插件），而这个XmlNode类型的CodonNode是什么东西？
还记得配置文件中在<Extension>标签下的<Class>、<MenuItem>、<Pad>之类的标签吗？我曾经说过，这些就是Codon的描述，现在来看看到底是不是如此。以前文的AddinTreeView配置为例：

	<Extension path="/SharpDevelop/Workbench/MainMenu/Tools">
		<MenuItem id="AddinTreeView" label="View AddinTree"
			class="Addins.AddinTreeView.AddinTreeViewCommand" />
	</Extension> 

SharpDevelop在读入插件配置文件的`<Extension>`标签之后，就把它的ChildNodes（XmlElement的属性）依次传入CodonFactory的CreateCodon方法中。这里它的ChildNodes[0]就是这里的<MenuItem id = ..... />节点，也就是codonNode参数了。这个XML节点的Name是MenuItem，因此CreateCodon的第一行

	CodonBuilder builder = codonHashtable[codonNode.Name] as CodonBuilder;

根据节点的名称(MenuItem)查找对应的CodonBuilder。记得前面的CodonBuilder根据CodonNameAttribute取得了MenuItemCodon的CodonName吗？就是这个MenuItem了。CodonFactory找到了对应的MenuItemCodon的CodonBuilder（这个是在DefaultAddInTree的构造函数中调用LoadCodonsAndConditions方法建立并加入CodonFactory中的，还记得么？），之后使用这个CodonBuilder建立了对应的Codon，并把它返回给调用者。

就这样，通过CodonNameAttribute，SharpDevelop把addin配置文件的`<MenuItem>`节点、CodonBulder、MenuItemCodon三部分串起来形成了一个构造Codon的路线。

回过头来再整理一下思路，SharpDevelop进行了下面这样几步工作：

A、建立各个Codon，使用CodonNameAttribute指明它在配置节点中的名称
B、DefaultAddInTree的构造函数中调用LoadCodonsAndConditions方法，搜索所有的Codon，根据Codon的CodonNameAttribute建立对应的CodonBuilder加入CodonFactory中。
C、读取配置文件，在<Extension>标签下遍历所有的节点，根据节点的Name使用CodonFactory建立对应的Codon。
其中，Codon的CodonNameAttribute、CodonBuilder的CodonName以及<Extension>标签下XML节点的Name是一致的。对于Condition（条件）的处理也是一样。

到这里，可以再来看看SharpDevelop中插件的灵活性是如何体现的。首先，addin配置中的Extension节点下的Codon节点名称并没有在代码中和具体的Codon类联系起来，而是通过CodonNameAttribute跟Codon联系起来。这样做的好处是，SharpDevelop的Codon和XML的标签一样具有无限的扩展能力。假设要自己定义一个Codon类SplashFormCodon作用是指定某个窗体作为系统启动时的封面窗体。要做的工作很简单：首先，在SplashFormCodon中使用CodonNameAttribute指定CodonName为Splash，并且在SplashFormCodon中定义自己需要的属性。然后，在addin配置文件使用`<Splash>`标签这样写：

	<Extension path="/SharpDevelop/ ">
		<Splash id="MySplashForm" class="MySplashFormClass" />
	</Extension>

另外，对于Condition（条件）的处理也是一样，也就是说可以使用类似的方法灵活的加入自己定义的条件。

#### 2.2 主线 (AddInTreeSingleton. CreateAddInTree) 

继续读 AddInTreeSingleton中CreateAddInTree 的代码。

在建立了DefaultAddInTree的实例后，AddInTreeSingleton在插件目录中搜索后缀为.addin的文件。还记得在Main函数中曾经调用过AddInTreeSingleton.SetAddInDirectories吗，就是搜索这个传入的目录。看来SharpDevelop把在插件目录中所有后缀为.addin的文件都看做是插件了。

	FileUtilityService fileUtilityService = (FileUtilityService)ServiceManager.Services.GetService(typeof(FileUtilityService));

先学习一下如何从ServiceManager取得所需要的服务，在SharpDevelop中要取得一个服务全部都是通过这种方式取得的。调用GetService传入要获取的服务类的类型作为参数，返回一个IService接口，之后转换成需要的服务。

搜索插件目录找到一个addin文件后，调用InsertAddIns把这个addin文件中的配置加入到目录树中。

	static StringCollection InsertAddIns(StringCollection addInFiles)
	{
		StringCollection retryList  = new StringCollection();

		foreach (string addInFile in addInFiles) {
			AddIn addIn = new AddIn();
			try {
				addIn.Initialize(addInFile);
				addInTree.InsertAddIn(addIn);
			} catch (CodonNotFoundException) {
				retryList.Add(addInFile);
			} catch (ConditionNotFoundException) {
				retryList.Add(addInFile);
			} catch (Exception e) {
				throw new AddInInitializeException(addInFile, e);
			}
		}

		return retryList;
	}

InsertAddIns建立一个对应的AddIn（插件），调用AddInTree的InsertAddIn方法把它挂到插件树中。在这里有一个小小的处理，由于是通过Assembly查找和插件配置中Codon的标签对应的类，而Codon类所在的Assembly是通过Import标签导入的。因此在查找配置中某个Codon标签对应的Codon类的时候，也许Codon类所在的文件是在其他的addin文件中Import的。这个时候在前面支线中讲到CodonFactory中查找CodonBuilder会失败，因此必须等到Codon类所在的addin处理之后才能正确的找到CodonBuilder。这是一个依赖关系的处理问题。

SharpDevelop在这里处理的比较简单，调用InsertAddIns方法的时候，凡是出现CodonNotFoundException的时候，都加入一个retryList列表中返回。在CreateAddinTree处理完所有的addin文件之后，再重新循环尝试处理retryList列表中的addin。如果某次循环中再也无法成功的加入retryList中的addin，那么才提示失败错误。

回头再来看看对AddIn的处理。

#### 2.2.1  addIn.Initialize 

建立了AddIn的实例后，调用Initialize 方法进行初始化。AddIn是对一个.addin文件的封装，定义在\src\Main\Core\AddIns\AddIn.cs文件中。其中包含了.addin文件的根元素`<AddIn>`的描述，包括名称、作者、版权之类的属性。在`<AddIn>`节点下包括两种节点：一个是`<Runtime>`节点，包含了`<Import>`指定要导入的`Assembly`；另外一个是`<Extension>`节点，指定Codon的扩展点。在`AddIn.Initialize`方法中，使用XmlDocument对象来读取对应的addin文件。首先读取name、author 、copyright之类的基本属性，之后遍历所有的ChildNodes（子节点）。

如果子节点是Runtime节点，则调用AddRuntimeLibraries方法。

	foreach (object o in el.ChildNodes)
	{
		XmlElement curEl = (XmlElement)o;

		string assemblyName = curEl.Attributes["assembly"].InnerText;
		string pathName     = Path.IsPathRooted(assemblyName) ? assemblyName : fileUtilityService.GetDirectoryNameWithSeparator(path) + assemblyName;
		Assembly asm = AddInTreeSingleton.AddInTree.LoadAssembly(pathName);
		RuntimeLibraries[assemblyName] = asm;
	}

通过`AddInTreeSingleton.AddInTree.LoadAssembly`方法把Assembly中所有的Codon和Condition的子类加入对应Factory类中（调用了`LoadCodonsAndConditions`方法，在DefaultAddInTree的构造函数中见过了），并且把该文件和对应的Assembly保存到RuntimeLibraries列表中。

如果子节点是Extension节点，则调用AddExtensions方法。

	Extension e = new Extension(el.Attributes["path"].InnerText);
	AddCodonsToExtension(e, el, new ConditionCollection());
	extensions.Add(e);

根据这个扩展点的XML描述建立Extension对象加入到AddIn的Extensions列表中，并通过`AddCodonsToExtension`方法把其中包括的Codon加入到建立的Extension对象中。Extension对象是AddIn的一个内嵌类，其中一个重要的属性就是CodonCollection这个列表。`AddCodonsToExtension`就是把在配置中出现的Codon都加入到这个列表中保存。

来看看`AddCodonsToExtension`方法。在代码中我略过了对Condition（条件）的处理的分析和一些无关紧要的部分，把注意力集中在插件的处理。首先是一个 `foreach (object o in el.ChildNodes)` 遍历 `<Extension>` 下所有的子节点，对于每个子节点的处理如下：

	XmlElement curEl = (XmlElement)o;
	switch (curEl.Name)
	{
		（处理各种条件）
		default:
			ICodon codon = AddInTreeSingleton.AddInTree.CodonFactory.CreateCodon(this, curEl);
			AutoInitializeAttributes(codon, curEl);

			（对codon.InsertAfter 和codon.InsertBefore 的处理，主要是处理codon在列表中的顺序问题，这一点在对于MenuItemCodon的处理上比较重要）

			e.CodonCollection.Add(codon);
			if (curEl.ChildNodes.Count > 0)
			{
				Extension newExtension = new Extension(e.Path + '/' + codon.ID);
				AddCodonsToExtension(newExtension, curEl, conditions);
				extensions.Add(newExtension);
			}
			break;
	}

我们看到了一个期待已久的调用

	AddInTreeSingleton.AddInTree.CodonFactory.CreateCodon(this, curEl);

经过了上文支线2.1代码中的铺垫，SharpDevelop使用建立好的CodonFactory，调用CreateCodon方法根据`<Extension>`下的节点构造出实际的Codon对象，一切尽在不言中了吧。

	e.CodonCollection.Add(codon);

把构造出来的Codon对象加入到Extension对象的CodonCollection列表中。

之后，在形如菜单的这种允许无限嵌套的结构中，SharpDevelop对此进行了处理。如果该节点有嵌套的子节点，那么构造一个新的Extension对象，递归调用`AddCodonsToExtension`添加到这个Extension对象中。注意一点，这个新构造的Extension对象并不是分开保存在Codon中，而是直接保存在AddIn的扩展点列表中。这样是为了方便查找，毕竟保存在具体的Codon中也没有什么用处，我们可以通过Extension对象的Path属性得知它在插件树中的具体位置。

#### 2.2.2 addInTree.InsertAddIn（把AddIn添加到AddInTree中）

对AddIn的构造完成之后，需要把AddIn的实例对象添加AddInTree中管理。

	addIns.Add(addIn);
	foreach (AddIn.Extension extension in addIn.Extensions)
	{
		AddExtensions(extension);
	}

DefaultAddInTree中保存了两课树。一个是根据插件文件的结构形成的树，每个插件文件作为根节点，往下依次是Extension、Codon节点。

`addIns.Add(addIn);`这一行就是把插件加入到这个树结构中。另外一个树是根据Extension的Path＋Codon的ID作为路径构造出来的，每一个树节点是一个AddInTreeNode类，包含了在这个路径上的Codon对象。嵌套在这个节点中的Codon在通过它子节点来访问。在DefaultAddInTree中可以通过GetTreeNode来指定一个路径获得插件树上某一个节点的内容。

`AddExtensions`方法很简单，遍历Extension中所有的Codon，把Extension的Path＋Codon的ID作为路径，创建这个路径上的所有节点，并把Codon连接到这个AddInTreeNode上。由于Codon的ID是全局唯一的，因此每一个AddInTreeNode都具有一个唯一的Codon。

#### 3、最后一公里（Codon和Command的关联）

在插件树的讨论中，我们依次把AddIn－Extension－Codon的配置和他们对应的类关联了起来。不过我们一直没有涉及到Codon和它包含的Command是如何关联的。由于这个关联调用是在插件树外部的（记得在讲述SharpDevelop程序入口Main函数中，提到ServiceManager的方法`InitializeServicesSubsystem`吗？

`AddServices((IService[])AddInTreeSingleton.AddInTree.GetTreeNode(servicesPath).BuildChildItems(this).ToArray(typeof(IService)));`

这里就调用了 `BuildChildItems`，因此单独在这里说明。实现这个关联的就是AddInTreeNode的BuildChildItems和BuildChildItem方法以及Codon的BuildItem方法。

`BuildChildItem`方法和`BuildChildItems`方法仅有一字之差，

`BuildChildItem`是根据指定的Codon的ID在所属AddInTreeNode的子节点下查找包含该Codon的节点并调用该Codon的
`BuildItem`方法；而`BuildChildItems`则是首先遍历所属AddInTreeNode的所有子节点，依次调用各个子节点的Codon的`BuildItem`方法，之后再调用所属AddInTreeNode的Codon的`BuildItem`方法（也就是一个树的后根遍历）。

重点在Codon的`BuildItem`方法。在AbstractCodon中，这个方法是一个抽象方法，SharpDevelop的代码注释中并没有明确说清楚这个方法是做什么用的。但是我们可以找一个Codon的实例来看看。例如ClassCodon的BuildItem：

	public override object BuildItem(object owner, ArrayList subItems, ConditionCollection conditions)
	{
		System.Diagnostics.Debug.Assert(Class != null && Class.Length > 0);
		return AddIn.CreateObject(Class);
	}

调用AddIn的`CreateObject`，传入Codon的Class（类名）作为参数，建立这个类的实例。例如这个配置

	<Extension path = "/Workspace/Autostart">
		<Class id = "InitializeWorkbenchCommand"
			class = "ICSharpCode.SharpDevelop.Commands.InitializeWorkbenchCommand"/>
	</Extension>

而Codon的中的Class（类名）属性就是`ICSharpCode.SharpDevelop.Commands.InitializeWorkbenchCommand`。也就是说，Codon的Class指的是实现具体功能模块的Command类的名称。在读取addin配置中的`<Runtime>`节的时候，AddInTree把Assembly保存到了RuntimeLibraries中，因此`CreateObject`方法可以通过它们来查找并建立类的实例。

类似的，可以再看看MenuItemCodon的实现，同样是建立了对应的SdMenuCommand。

这样，SharpDevelop本身的插件结构可以和具体的对象建立分离开来，实际的对象建立是在各个Codon的BuildItem中进行的。因此我们可以发现在SharpDevelop整个是基础插件系统部分没有任何GUI的操作，实现了很好的解耦效果。

#### 4、问题 

好了，本文对插件树构造的分析到此告一段落。我提一个小小的问题给各位看官思考：在构造插件树的过程中，如果Codon的某一个节点路径不存在（也就是说它的依赖项不存在），那么SharpDevelop会提示失败并且终止程序运行。可是实际上可能因为部署的原因或者权限的原因，某些Codon的失败并不会影响整个系统的使用，例如试用版本仅仅提供部分插件给客户使用，而并不希望系统因此而终止运行。那么就存在一个Codon依赖项失败而允许继续运行的问题。另外，我希望各个插件不在系统启动的时候全部调入系统，而是在运行期实际调用的时候才调入系统，也就是一个缓存机制，这样就可以实现系统插件的热部署。如何修改SharpDevelop的插件系统来实现这两个功能呢？

