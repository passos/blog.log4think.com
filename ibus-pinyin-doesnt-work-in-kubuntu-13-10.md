---
title: ibus-pinyin doesn't work in KUbuntu 13.10
date: '2013-11-12 11:59:40 +0800'
---

# 2013-11-12  ibus-pinyin doesn't work in KUbuntu 13.10

ibus and ibus-pinyin doesn't work in KUbuntu 13.10. It looks like this

```text
$ ibus-setup
ERROR:root:Could not find any typelib for Gtk
Traceback (most recent call last):
  File "/usr/share/ibus/setup/main.py", line 29, in <module>
    from gi.repository import Gtk
ImportError: cannot import name Gtk
```

The problem is a dependency package is missing. This problem can be solved by this command: `sudo apt-get install gir1.2-gtk-3.0`.

