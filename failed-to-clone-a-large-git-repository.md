---
title: 'Failed to clone a large git repository: The remote end hung up unexpectedly'
date: '2014-07-21 16:36:41 +0800'
---

# 2014-07-21  'Failed to clone a large git repository: The remote end hung up unexpectedly'

When git clone a large repository sometimes it give you the error message like this:

```text
$ git clone ssh://xxx@xxx:29418/xxx
Cloning into 'xxx'...
remote: Counting objects: 356213, done
remote: Finding sources: 100% (356213/356213)
Corrupted MAC on input. (277847/356213), 123.59 MiB | 3.86 MiB/s
Finished discarding for xxx
fatal: The remote end hung up unexpectedly
fatal: early EOF
fatal: index-pack failed
```

If you got this error message, you might want to try run the following command to fix it

```text
git config --global http.postBuffer 524288000
git config --global --add core.compression -1
```

