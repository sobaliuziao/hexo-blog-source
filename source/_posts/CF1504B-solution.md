---
title: 'CF1504B Flip the Bits 题解'
date: 2021-04-04 20:20:00
---

赛时调了半天没调出来，赛后又调了半天还发帖询问后才过的。。。

## 题意

给定两个 $01$ 串 $a,b$，定义操作规则：

对于一个 $01$ 串，每次只能选择串中从 $1\sim i$ 的数字进行翻转（$0$变$1$，$1$变$0$），而且这 $i$ 个数字 $0$ 的个数与 $1$ 的个数是相同的。

问你能否对 $a$ 操作后变成 $b$。

## 思路

这题我是从后往前考虑的。

结论：从后往前扫，如果碰到 $a_i=b_i$ 且 $a_{i-1} \neq b_{i-1}$ 则就必须将 $1\sim i-1$ 翻转。易知此时 $1\sim i-1$ 中 $0$ 的个数不等于 $1$ 的个数则输出$\texttt{NO}$。如果坚持到底的话，就输出$\texttt{YES}$。

感性理解：找到从右到左满足 $a_i=b_i$ 并且 $a_{i-1} \neq b_{i-1}$ 的第一个 $i$，任意取一数 $j(i<j\leq n)$。那么我们将 $1\sim j-1$ 翻转后，此时 $i\sim j-1$ 就不满足了，所以还要再翻转一次，就跟只翻转 $1\sim i - 1$ 一样了。

## 实现

很明显我们每一次对 $1\sim i-1$ 进行翻转操作时，不能直接模拟，否则时间卡爆你。那么怎么优化呢？

考虑到这是一个 $01$ 串，所以翻转结果只跟翻转次数有关，而且这里的操作是对一个连续的区间考虑的，所以完全可以用树状数组来写（类似于[树状数组 2](https://www.luogu.com.cn/problem/P3368)），然后正常写就可以了。

Tip：多组数据时，树状数组清空不能用 ```memset```，否则会 T。

## 代码

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 3e5 + 5;

int T, n;
int s[N];

string a1, b1;
int a[N], b[N];

int sum[N << 2];
int lowbit (int x) {
  return x & (-x);
}

void update (int x, int y) {//树状数组
  while (x <= n) {
    sum[x] += y;
    x += lowbit(x);
  }
  return ;
}

int query (int x) {
  int res = 0;
  while (x != 0) {
    res += sum[x];
    x -= lowbit(x);
  }
  return res;
}

int main() {
  cin >> T;
  while (T--) {
    cin >> n >> a1 >> b1;
    s[0] = 0;
    for (int i = 1; i <= n; ++i) a[i] = a1[i - 1] - '0', b[i] = b1[i - 1] - '0', s[i] = s[i - 1] + a[i];//求前缀1的个数
    for (int i = 1; i <= n; ++i) sum[i] = 0;
    bool flag = true;
    for (int i = n; i >= 1; --i) {
      int k = query(i);
      if (k % 2 == 1) {
        a[i] ^= 1;
      }
      if (a[i] == b[i]) continue ;
      if (s[i] != i - s[i]) { flag = false; break ; }//如果不能进行翻转，就退出
      update(1, 1), update(i, -1);//对1~i-1 全部加上1
      s[i - 1] = i - 1 - s[i - 1];//前缀1变化
    }
    puts(flag == true ? "YES" : "NO");
  }
  return 0;
}
```

时间复杂度：$O(n\log n)$

能过。

$\text{Upd on 2021.4.10}$

这种思路可以 $O(n)$ 写，而且 $n\log n$ 的写法貌似复杂了（

定义一个计数器 $k$ 当这个时候需要翻转时就将 $k+1$，那么每次遍历到时，$k$ 就是次数。

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 3e5 + 5;

int T, n;
int s[N];

string a1, b1;
int a[N], b[N];

int main() {
  cin >> T;
  while (T--) {
    cin >> n >> a1 >> b1;
    s[0] = 0;
    for (int i = 1; i <= n; ++i) a[i] = a1[i - 1] - '0', b[i] = b1[i - 1] - '0', s[i] = s[i - 1] + a[i];
    bool flag = true; int k = 0;
    for (int i = n; i >= 1; --i) {
      if (k % 2 == 1) {
        a[i] ^= 1;
      }
      if (a[i] == b[i]) continue ;
      if (s[i] != i - s[i]) { flag = false; break ; }
      ++k;
      s[i - 1] = i - 1 - s[i - 1];
    }
    puts(flag == true ? "YES" : "NO");
  }
  return 0;
}
```