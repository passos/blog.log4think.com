---
title: 长距离打车如何省钱？
date: '2008-11-18 23:02:52 +0800'
---
学JavaScript的时候写的一个用于在长距离打车时，计算多远抬一次表最省钱的抬表方案的小程序，参数可以根据需要随意修改。

X轴是距离，Y轴是费用，不同的颜色表示不同的抬表方案

大致的简单结论是20公里以上的时候，每15公里抬一次表，能省出10%左右吧。

<a href="http://log4think.com/wp-content/uploads/2008/11/taxi.jpg"><img src="http://log4think.com/wp-content/uploads/2008/11/taxi.jpg" alt="taxi" width="891" height="816" class="alignnone size-full wp-image-751" /></a>
下面代码存为taxi.html，然后打开即可在浏览器中看到结果。

-----------------------------------------------
```
<html>
<script type="text/javascript" src="http://www.walterzorn.com/scripts/wz_jsgraphics.js"></script>

<body>
<script type="text/javascript">
<!--
function getPrice(distance, night) {
    var unitPrice = 2.0,
    basicDistance = 3,
    basicPrice = 10,
    extDistance = 15,
    extPrice = 3.0;

    var price = 0.0;
    if ( distance == 0 ) return 0;
    if ( distance <= basicDistance ) return basicPrice;

    if ( distance <= extDistance ) {
        price = basicPrice + unitPrice * (distance - basicDistance);
        return price;
    }

    price += basicPrice + unitPrice*(extDistance-basicDistance) + extPrice*(distance-extDistance)
    return price;
}

function getPriceWithReset(distance, night, reset) {
    if ( reset == 0 ) {
        return getPrice(distance, night);
    } else {
        return getPrice(reset, night) * Math.floor(distance/reset) + getPrice(distance % reset, night);
    }
}

var coordXUnit = 8, coordYUnit = 3,
basicX = 100, basicY = 50,
coordMaxX = 101, coordMaxY = 251;

function drawString(str, x, y) {
    jg.drawString(str, basicX+x*coordXUnit, basicY+(coordMaxY-y)*coordYUnit);
}

function drawPoint(x, y) {
    drawLine(x, y, x, y);
}

function drawLine(x1, y1, x2, y2) {
    jg.drawLine(basicX + x1*coordXUnit, basicY + (coordMaxY-y1)*coordYUnit, basicX + x2*coordXUnit, basicY + (coordMaxY-y2)*coordYUnit);
}

function drawPolyline(ax, ay) {
    var axx = new Array(), ayy = new Array();

    for (var e in ax) {
        axx.push(basicX + (ax[e] * coordXUnit) );
    }

    for (var e in ay) {
        ayy.push(basicY + (coordMaxY - ay[e])*coordYUnit);
    }

    jg.drawPolyline(axx, ayy);
}

function drawCoordinate() {
    jg.setColor("#ee8800");
    drawLine(0, 0, coordMaxX, 0);
    drawLine(0, 0, 0, coordMaxY);

    drawString(0, -2, -2);
    for (var i = 1; i < coordMaxX; i++) {
        if (i%5==0) {
            // draw grid
            jg.setStroke(Stroke.DOTTED);
            drawLine(i, 0, i, coordMaxY);
            // draw mark
            jg.setStroke(0);
            drawLine(i, 0, i, -2);
            drawString(i, i-1, -3);
        } else {
            drawLine(i, 0, i, -1);
        }
    }

    for (var i = 1; i < coordMaxY ; i++) {
        if (i%5==0) {
            // draw grid
            jg.setStroke(Stroke.DOTTED);
            drawLine(0, i, coordMaxX, i);
            // draw mark
            jg.setStroke(0);
            drawLine(0, i, -2, i);
            drawString(i, -7, i+1);
        } else {
            drawLine(0, i, -1, i);
        }
    }
}

function drawPriceLine(night, reset) {
    var ax = new Array(), ay = new Array();

    for (var d=0; d<70; d++) {
        ax.push(d);
        ay.push(getPriceWithReset(d, 0, reset));
    }
    drawPolyline(ax, ay);
}

/////////////// main section ///////////////
var jg = new jsGraphics();
jg.setFont("verdana,geneva,sans-serif", "10px", Font.PLAIN);

drawCoordinate();
drawString("reset:", 0, -10);
jg.setColor("#000000");
drawPriceLine(0, 0);
drawString("0", 5, -10);
jg.setColor("#FF0000");
drawPriceLine(0, 10);
drawString("10", 10, -10);
jg.setColor("#00FF00");
drawPriceLine(0, 15);
drawString("15", 15, -10);
jg.setColor("#0000FF");
drawPriceLine(0, 20);
drawString("20", 20, -10);

///////////////// from wangjing to my home, 35KM /////////////////
jg.setColor("#880000");
var xp = new Array(), yp = new Array();
for ( var i=10; i<30; i++) {
    xp.push(i);
    yp.push(getPriceWithReset(35, 0, i));
}
drawPolyline(xp, yp);

drawString(getPriceWithReset(35, 0, 15), 0, -20);
jg.paint();
//-->
</script>
</body>
</html>
```
