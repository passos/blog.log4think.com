---
title: 循环有序数组的二分查找
date: '2013-01-27 20:12:27 +0800'
---

# 2013-01-27  循环有序数组的二分查找

亚马逊面试题：给定一个循环有序数组，形如 `[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8]` ，在其中查找某个元素。

最简单直接朴素的算法，从头至尾依次遍历，复杂度O\(n\)。如果只能做到这样的话，就不必再说了。 对于普通的有序数组，通常会采用二分法查找元素，这样复杂度可以降低至O\(logN\)。但是这个循环的有序数组的最大最小部分在数组中间而不是在头尾，是否还可以采用二分法查找呢？ 普通的二分法思路是：在中间取一元素，与要查找的目标元素对比，若中间元素较大，则在左半部继续二分法查找；反之，若中间元素较小，则在右半部继续二分法查找。如下：

```text
/*
   p is the start index,
   q is the end index,
   x is the target data
*/
int binary_search(int x, int p, int q, int *a) {
    if (p >= q && a[p] != x)
        return -1;

    int m = (p + q) / 2;

    if (a[m] == x)
        return m;

    if (x > a[m])
        p = m + 1;
    else
        q = m - 1;

    return binary_search(x, p, q, a);
}
```

该算法应用到这个循环数组上的时候，以在数组`[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8]`中查找元素 0 为例，第一步取中间第 9 个元素值为 18 :

```text
search: 0        |   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
----------------------------------------------------------------------------------------------------
p= 0, m= 9, q=19 |   9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,  0,  1,  2,  3,  4,  5,  6,  7,  8,
```

此时目标元素 0 小于中间元素 19，该如何判断下一步是应该在左半边查找还是在右半边查找呢？仔细观察该数组，在下标9处被分为两个部分，左边为`[9, 10, ..., 18]`，右边为`[19, 0, ..., 8]`。以目测的结果来看，应该在右半边继续查找，与原始二分法的判断结果恰好相反。原始的算法，只能应用于一个单调递增的数组，而循环数组则将一个单调递增数组变成了两个单调递增数组。第一部取完中点之后，数组被分为两个部分。一般的情况下，一部分必然为单调递增，一部分为非单调递增（含有断点）。很容易想到，如果目标元素在单调递增那一部分，则可继续在此区间查找，此区间内的查找则是原始的二分查找；如果目标元素在非单调递增部分，则又还原成了原问题，只是查找范围缩小了一半。重复这个过程，则可以得到查找结果。

```text
search : 0       |  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
----------------------------------------------------------------------------------------------------
p= 0, m= 9, q=19 |  9, 10, 11, 12, 13, 14, 15, 16, 18, 18, 19,  0,  1,  2,  3,  4,  5,  6,  7,  8,
p=10, m=14, q=19 |                                         19,  0,  1,  2,  3,  4,  5,  6,  7,  8,
p=10, m=11, q=13 |                                         19,  0,  1,  2,
result: 11
```

在这个过程中，需要注意几个个问题：

1. 如何判断一段数组是单调递增呢？在该段数组的头、中间、尾三个位置p,m,q取三个值a\[p\], a\[m\], a\[q\]，如果是单调递增则一定满足 a\[p\] &gt;= a\[m\] &gt;= a\[q\]，否则则非单调递增。
2. 判断目标元素下一步所在区间，有几种情况：
   * 当 x &gt; a\[m\] 时，
     * 右半边是单调递增区间，并且x在此区间内，下一步则可在此右半边区间内查找
       * 右半边是单调递增区间，并且x不在此区间内，下一步在左半边查找
       * 右半边是非单调递增区间，则x必然在此区间内，下一步在右半边查找
   * 当 x &lt; a\[m\] 时， 同理类似
     * 左半边是单调递增区间，并且x在此区间内，下一步则可在此左半边区间内查找
     * 左半边是单调递增区间，并且x不在此区间内，下一步在右半边查找
     * 左半边是非单调递增区间，则x必然在此区间内，下一步在左半边查找
3. 判断是否在单调递增部分，只需与区间的另外一头的元素比较一下大小即可知道

样例代码：

```text
#include <stdio.h>

#define N 20
int arr[N] = {9,10,11,12,13,14,15,16,17,18,19,0,1,2,3,4,5,6,7,8};

void print_header(int target) {
    printf("search :%2d %*c | ", target, 5, ' ');
    for (int i = 0; i < N; i++) {
        printf("%2d  ", i);
    }
    printf("\n");
    for (int i = 0; i< N; i++) {
        printf("-----");
    }
    printf("\n");
}

void print_array(int p, int m, int q, int *a) {
    printf("p=%2d, m=%2d, q=%2d |%*c", p, m, q, 4 * p + (p>0?1:0), ' ');
    for (int i = p; i <= q; i++) {
        printf("%2d, ", a[i]);
    }
    printf("\n");
}

/* 非递归方式 */
int search_loop_array(int x, int* a, int length) {
    int p = 0;
    int q = length - 1;

    while ( p <= q ) {
        int m = ( p + q ) / 2;

        print_array(p, m, q, a);

        if ( x == a[m] )
            return m;

        if ( x > a[m] ) {
            int mm = ( m + q ) / 2;
            int increase = (a[m] <= a[mm] && a[mm] <= a[q]);
            if ( ( increase && x <= a[q] ) || ! increase)
                p = m + 1;
            else
                q = m - 1;
        } else {
            int mm = ( p + m ) / 2;
            int increase = a[p] <= a[mm] && a[mm] <= a[m];
            if ( increase && x >= a[p] || !increase)
                q = m - 1;
            else
                p = m + 1;
        }
    }

    return -1;
}

/* 递归方式 */
int search_loop_array2(int x, int low, int high, int* a) {
    if (low >= high && a[low] != x)
        return -1;

    int m = (low + high) / 2;

    print_array(low, m, high, a);

    if ( x == a[m] )
        return m;

    if ( x > a[m] ) {
        int mm = (m + high) / 2;
        int increase = (a[m] <= a[mm] && a[mm] <= a[high]);

        if ( !increase || (increase && x <= a[high] ) )
            low = m + 1;
        else
            high = m - 1;

    } else {
        int mm = (low + m) / 2;
        int increase = (a[low] <= a[mm] && a[mm] <= a[m]);

        if ( !increase || (increase && x >= a[low] ) )
            high = m - 1;
        else
            low = m + 1;
    }

    return search_loop_array2(x, low, high, a);
}

int main() {

    for (int i = 0; i < N; i++) {
        print_header(i);

        // printf("result: %d\n\n", search_loop_array(i, arr, N));
        printf("result: %d\n\n", search_loop_array2(i, 0, N-1, arr));
    }
    return 0;
}
```

完。

