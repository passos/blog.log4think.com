---
title: 旋转矩阵
date: '2009-12-30 18:19:41 +0800'
---

# 2009-12-30  旋转矩阵

前天在Google Groups的TopLanguge中看到的一个从JavaEye转过来的帖子。本来应该是给大学生做的课后习题，可是看到的坛友给出的C、C++、Python、Java等代码，都是一大堆的if/else要么就是 switch，何其冗长。和楼主给出的那个反例也差不了多少了。 when int i=5; output:

```text
1  2  3  4 5
16 17 18 19 6
15 24 25 20 7
14 23 22 21 8
13 12 11 10 9
```

when int i=6; output:

```text
1  2  3  4  5  6
20 21 22 23 24  7
19 32 33 34 25  8
18 31 36 35 26  9
17 30 29 28 27 10
16 15 14 13 12 11
```

## This is a simple python program which hate if/else and switch.

```text
MAX = 10
matrix = [[0 for col in range(MAX)] for row in range(MAX)]
(x, y, count, link) = (-1, 0, 1, {1:(1,0,2), 2:(0,1,3), 3:(-1,0,4), 4:(0,-1,1)})
(dx, dy, direct) = link[1]
while count <= MAX*MAX:
    (nx, ny) = (x + dx, y + dy)
    if (0 <= nx < MAX) and (0 <= ny < MAX) and (matrix[ny][nx] == 0):
        matrix[ny][nx] = count
        (x, y, count) = (nx, ny, count + 1)
    else:
        (dx, dy, direct) = link[direct]

for x in range(MAX):
    print matrix[x]
```

