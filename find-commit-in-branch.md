---
title: Git中判断一个commit是否在某个branch中
date: '2010-08-18 17:08:16 +0800'
---
方法1：`git branch --contains commit`

方法2：查找reflog `git reflog show --all | grep a871742`

会有类似如下的结果：`a871742 refs/heads/completion@{0}: commit (amend): mpc-completion: total rewrite`，其中 completion 就是所在的 branch

注：`git reflog show`等价于`git log -g --abbrev-commit --pretty=oneline`
