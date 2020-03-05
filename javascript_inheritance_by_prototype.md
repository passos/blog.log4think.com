---
title: JavaScript 中几种不同的基于 prototype 继承方式的区别
date: '2016-12-13 19:24:52 +0800'
---
#JavaScript 中几种不同的基于 prototype 继承方式的区别

## 普通属性的继承

### 第一种方式

来自于 <a href="https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Guide/Details_of_the_Object_Model">MDN 对象模型的细节</a>

```
function Employee1 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
    this.work = function() {console.log("Employee.work")}
    this.workAsEmployee = function() { this.work() }
}

function WorkerBee1 (projs) {
    console.log('WorkerBee constructor')
    this.projects = projs || [];
    this.work = function() {console.log("WorkerBee.work")}
    this.workAsBee = function() { this.work() }
}
WorkerBee1.prototype = new Employee1;

function Engineer1 (mach) {
    console.log('Engineer constructor')
    this.dept = "engineering";
    this.machine = mach || "";
    this.work = function() {console.log("Engineer.work")}
    this.workAsEngineer = function() { this.work() }
}

Engineer1.prototype = new WorkerBee1;

e1 = new Engineer1()
e1.work()
console.log(Employee1.prototype.isPrototypeOf(e1))
console.log(WorkerBee1.prototype.isPrototypeOf(e1))
console.log(e1)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_1.png" alt="Alt text" title="第一种方式的对象结构" />

### 第二种方式

来自于 YUI 的实现，利用中间对象传递 prototype

```
function extend(Child, Parent) {
    var F = function () { };
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
    Object.defineProperty(Child, "super", { "value": Parent.prototype })
}

function Employee2 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
    this.work = function() {console.log("Employee.work")}
    this.workAsEmployee = function() { this.work() }
}

function WorkerBee2 (projs) {
    console.log('WorkerBee constructor')
    this.projects = projs || [];
    this.work = function() {console.log("WorkerBee.work")}
    this.workAsBee = function() { this.work() }
}
extend(WorkerBee2, Employee2);

function Engineer2 (mach) {
    console.log('Engineer constructor')
    this.dept = "engineering";
    this.machine = mach || "";
    this.work = function() {console.log("Engineer.work")}
    this.workAsEngineer = function() { this.work() }
}
extend(Engineer2, WorkerBee2);

e2 = new Engineer2()
e2.work()

console.log(Employee2.prototype.isPrototypeOf(e2))
console.log(WorkerBee2.prototype.isPrototypeOf(e2))
console.log(e2)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_2.png" alt="Alt text" title="第二种方式的对象结构" />

可以看到，区别主要在于，直接 `Child.prototype = new Parent()` 会把定义在 Parent 里面的方法也带到 prototype 里面去。另外，这种方式并没有执行父类的构造函数。

## 对于定义在 prototype 里面的方法呢

下面对上面的方法定义进行一点改进，把方法定义在 prototype 里，类似正常的 OO 编程中在类里面定义方法。

### 第一种方式改进

```
function Employee3 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
}
Employee3.prototype.work = function() {console.log("Employee.work")}
Employee3.prototype.workAsEmployee = function() { this.work() }

function WorkerBee3 (projs) {
    console.log('WorkerBee constructor')
    this.projects = projs || [];
}
WorkerBee3.prototype = new Employee3;
WorkerBee3.prototype.work = function() {console.log("WorkerBee.work")}
WorkerBee3.prototype.workAsBee = function() { this.work() }

function Engineer3 (mach) {
    console.log('Engineer constructor')
    this.dept = "engineering";
    this.machine = mach || "";
}
Engineer3.prototype = new WorkerBee3;
Engineer3.prototype.work = function() {console.log("Engineer.work")}
Engineer3.prototype.workAsEngineer = function() { this.work() }

e3 = new Engineer3()
e3.work()

console.log(Employee3.prototype.isPrototypeOf(e3))
console.log(WorkerBee3.prototype.isPrototypeOf(e3))
console.log(e3)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_3.png" alt="Alt text" title="第一种方式改进后的对象结构" />

### 第二种方式的改进

```
function extend(Child, Parent) {
    var F = function () { };
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
    Object.defineProperty(Child, "super", { "value": Parent.prototype })
}

function Employee4 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
}
Employee4.prototype.work = function() {console.log("Employee.work")}
Employee4.prototype.workAsEmployee = function() { this.work() }

function WorkerBee4 (projs) {
    console.log('WorkerBee constructor')
    this.projects = projs || [];

}
extend(WorkerBee4, Employee4);
WorkerBee4.prototype.work = function() {console.log("WorkerBee.work")}
WorkerBee4.prototype.workAsBee = function() { this.work() }

function Engineer4 (mach) {
    console.log('Engineer constructor')
    this.dept = "engineering";
    this.machine = mach || "";
}
extend(Engineer4, WorkerBee4);
Engineer4.prototype.work = function() {console.log("Engineer.work")}
Engineer4.prototype.workAsEngineer = function() { this.work() }

e4 = new Engineer4()
e4.work()

console.log(Employee4.prototype.isPrototypeOf(e4))
console.log(WorkerBee4.prototype.isPrototypeOf(e4))
console.log(e4)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_4.png" alt="Alt text" title="第二种方式改进后的对象结构" />

注意观察 `constructor` 和 `__proto__` 属性。

#   要执行所有构造函数

上述第二种方法，都没有执行父类的构造函数，也就没有真正的继承父类的初始化数据。为了弥补这一点，如下两种写法都可以达到目的。

## 利用 `super` 变量

```
function extend(Child, Parent) {
    var F = function () { };
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
}

function Employee5 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
}
Employee5.prototype.work = function() {console.log("Employee.work")}
Employee5.prototype.workAsEmployee = function() { this.work() }

function WorkerBee5 (projs) {
    console.log('WorkerBee constructor')

    this.super = Employee5;
    this.super();

    this.projects = projs || [];

}
extend(WorkerBee5, Employee5);
WorkerBee5.prototype.work = function() {console.log("WorkerBee.work")}
WorkerBee5.prototype.workAsBee = function() { this.work() }

function Engineer5 (mach) {
    console.log('Engineer constructor')

    this.super = WorkerBee5;
    this.super();

    this.dept = "engineering";
    this.machine = mach || "";
}
extend(Engineer5, WorkerBee5);
Engineer5.prototype.work = function() {console.log("Engineer.work")}
Engineer5.prototype.workAsEngineer = function() { this.work() }

e5 = new Engineer5()
e5.work()

console.log(Employee5.prototype.isPrototypeOf(e5))
console.log(WorkerBee5.prototype.isPrototypeOf(e5))
console.log(e5)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_5.png" alt="Alt text" title="利用 super 变量" />

## 类似，但是用 `Parent.apply` 方法

```
function extend(Child, Parent) {
    var F = function () { };
    F.prototype = Parent.prototype;
    Child.prototype = new F();
    Child.prototype.constructor = Child;
}

function Employee6 (name, dept) {
    console.log('Employee constructor')
    this.name = name || "";
    this.dept = dept || "general";
}
Employee6.prototype.work = function() {console.log("Employee.work")}
Employee6.prototype.workAsEmployee = function() { this.work() }

function WorkerBee6 (projs) {
    console.log('WorkerBee constructor')
    Employee6.apply(this)
    this.projects = projs || [];
}
extend(WorkerBee6, Employee6);
WorkerBee6.prototype.work = function() {console.log("WorkerBee.work")}
WorkerBee6.prototype.workAsBee = function() { this.work() }

function Engineer6 (mach) {
    console.log('Engineer constructor')
    WorkerBee6.apply(this)
    this.dept = "engineering";
    this.machine = mach || "";
}
extend(Engineer6, WorkerBee6);
Engineer6.prototype.work = function() {console.log("Engineer.work")}
Engineer6.prototype.workAsEngineer = function() { this.work() }

e6 = new Engineer6()
e6.work()

console.log(Employee6.prototype.isPrototypeOf(e6))
console.log(WorkerBee6.prototype.isPrototypeOf(e6))
console.log(e6)
```

<img src="http://log4think.com/wp-content/uploads/2016/12/prototype_inheritance_6.png" alt="Alt text" title="利用 Parent.apply 方法" />
