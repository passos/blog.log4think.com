---
title: 编程之美 1.2 中国相帅问题的一个简洁解法
date: '2011-01-01 22:57:45 +0800'
---

# 2011-01-01  编程之美 1.2 中国相帅问题的一个简洁解法

题目意思大概是，象棋棋盘上只有一相一帅，只能在9宫格内移动，且不能对面。要求给出相帅所有的位置的可能性，只能用一个变量。

只用一个变量，第一感是用位操作。给九宫格编个号：

```text
1 2 3
4 5 6
7 8 9
```

遍历所有的位置，如果 位置编号 mod 3相同，说明在同一列中。按此思路，书中位操作的解法略显繁杂。这里一个简洁的的解法是：

```text
void main()
{
    short unsigned int x;
    for (x = 0; (x & 0xF0) < 0x90; x += 0x10 ) {
        for ( x &= 0xF0; (x & 0x0F) < 9; x++)
            if ((x >> 4) % 3 != (x & 0x0F) % 3)
                printf("A = %d, B = %d\n", (x >> 4) + 1, (x & 0x0F) + 1);
    }
}
```

如果不用位操作的话，另外一个解法比较赞：

```text
BYTE i = 81;
while (i--)
{
    if (i / 9 % 3 != i % 9 % 3)
        printf("A = %d, B = %d\n", i / 9 + 1, i % 9 + 1);
}
```

