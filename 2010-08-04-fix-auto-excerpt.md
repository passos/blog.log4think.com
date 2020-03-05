---
title: 修正auto-excerpt产生带格式的摘要
date: '2010-08-04 18:05:11 +0800'
---
Wordpress的正文通常都是显示全文，这样一来如果文章非常长的话，blog的首页的用户体验会很不好。网上有很多提到通过将index.php中的the_content改成the_excerpt来讲首页的文章内容显示为摘要的方法，但是这样的摘要要自己去写。

Wordpress的plugin库里面有一个auto-excerpt的插件，可以自动将文章的前几百字截取下来作为文章的摘要。确实是方便，但是却有一个小小的问题，截取出来的文字格式全部都丢失了，包括段落、链接等等。

通过对这个插件的代码做一点小小的改动可以恢复文字的格式。在后台管理中找到这个插件--edit

```
function auto_excerpt($content) {
    $content = substr(strip_tags($content),0,418)." [...]";
    return $content;
}
```

代码中可以看到，这个插件是用strip_tags来去除正文中的所有html标签，然后截取前418个字符。其实strip_tags还有一个可选的参数，可以指定忽略掉某些标签。为了保留基本格式，可以选择在strip_tags中忽略掉p、br、a等标签恢复文字的格式。

```
function auto_excerpt($content) {
    $content = substr(strip_tags($content, '
<br>'),0,418)."<br/> [...]";
    return $content;
}
```

如果想在缩略图中保留图片，也可以在忽略标签列表中加上<img>标签。

