---
title: 'CF1917F Construct Tree 题解'
date: 2023-12-29 20:56:00
---

## Description

给你一个数组 $l_1,l_2,\dots.l_n$ 和一个数字 $d$。问你是否能够构造一棵树满足以下条件：

- 这棵树有 $n+1$ 个点。
- 第 $i$ 条边的长度是  $l_i$。
- 树的直径是 $d$。

只需要判断是否有解即可。

$2\le n\le2000,1\le d\le 2000,1\le l_i\le d$。

## Solution

先把 $l$ 从大到小排序。

容易发现把直径拉出来后，其他不在直径上的边 $l_k$ 挂在直径的点上要满足 $l_k\leq \min\{L,d-L\}$，其中 $L$ 和 $d-L$ 分别是直径上挂的点左右的长度和。

所以肯定是把不在直径上的边以类似菊花图的形式尽可能挂在中间，使得所有 $l_k\leq \min\{L,d-L\}$。

如果 $l_n>d$ 显然无解。

如果 $l_n>\left\lfloor\dfrac{d}{2}\right\rfloor$，则它一定不能是挂着的边，也就是一定在直径上，这时候只要判断 $l_1,l_2\dots. l_{n-1}$ 都 $\leq d-l_n$ 并且能够选出某些数和为 $d-l_n$。

如果 $l_n\leq\left\lfloor\dfrac{d}{2}\right\rfloor$，并且 $l_n$ 在直径上，则其他点一定能全挂上去，所以只要判断能否有若干个和为 $d-l_n$ 即可。如果 $l_n$ 不在直径上，那么就需要保证 $\min\{L,d-L\}\geq l_n$，所以直接设 $f_{i,j}$ 表示左边和为 $i$，右边和为 $j$ 是否可行即可求出。

时间复杂度：$O(nd^2)$，过不了。

但是注意到 $f_{i,j}$ 的转移只有 $0/1$，所以可以 bitset 优化至 $O\left(\frac{nd^2}{\omega}\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e3 + 5;

int n, d;
int a[kMaxN];
std::bitset<kMaxN> f[kMaxN];

void dickdreamer() {
  std::cin >> n >> d;
  for (int i = 1; i <= n; ++i)
    std::cin >> a[i];
  std::sort(a + 1, a + 1 + n);
  if (a[n] > d / 2) {
    if (a[n - 1] > d - a[n]) return void(std::cout << "No\n");
    f[0].reset();
    f[0][0] = 1;
    for (int i = 1; i < n; ++i)
      f[0] |= (f[0] << a[i]);
    std::cout << (f[0][d - a[n]] ? "Yes\n" : "No\n");
  } else {
    for (int i = 0; i <= d; ++i)
      f[i].reset();
    f[0][0] = 1;
    for (int i = 1; i < n; ++i) {
      for (int j = d; ~j; --j) {
        f[j] |= (f[j] << a[i]);
        if (j >= a[i]) f[j] |= f[j - a[i]];
      }
    }
    bool ans = f[0][d - a[n]];
    for (int i = a[n]; i <= d - a[n]; ++i)
      ans |= f[i][d - i];
    std::cout << (ans ? "Yes\n" : "No\n");
  }
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```