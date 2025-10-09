---
title: '[ABC327G] Many Good Tuple Problems 题解'
date: 2024-02-08 09:42:00
---

## Description

对于一对长度均为 $M$ 且元素值在 $\left[1, N\right]$ 之间的序列 $(S, T)$，定义其为好的当且仅当：

- 存在一个长度为 $N$ 的 $01$ 序列 $X$，使得其满足如下条件：

    - 对于任意 $i \in \left[1, M\right]$，有 $X_{S_i} \neq X_{T_i}$。

给定 $N, M$，求在所有可能的 $N^{2M}$ 种长度均为 $M$ 且元素值在 $\left[1, N\right]$ 之间的序列对 $(A, B)$ 中，有多少对序列是好的。

对 $998244353$ 取模。

$1 \le N \le 30, 1 \le M \le 10^9$。

## Solution

首先对于两个序列他们合法的条件就是把所有 $S_i$ 和 $T_i$ 连边后是个二分图，于是原题就等价于要求有多少个 $n$ 个点 $m$ 条边的有标号二分图。

先考虑如何求出 $n$ 个点 $m$ 条边的**简单**有标号二分图数量。然后会发现不好把染色方式的影响去掉，所以先不考虑染色方式的影响去做。

设 $f_{n,m}$ 表示 $n$ 个点 $m$ 条边的简单二分图数（染色方式不同算不同的方式），那么可以得到：

$$f_{n,m}=\sum_{i=0}^{n}{\binom{n}{i}\binom{i(n-i)}{m}}$$

但是这个状态无法把连通块个数表示出来，而无法去除染色方式的影响，所以可以考虑求出 $n$ 个点 $m$ 条边的简单**连通**二分图数（染色方式不同算不同的方式），这样只要把方案数除以 $2$ 就能去掉连通图染色方式的影响，最后把再把连通图重组成普通简单二分图即可求出答案。

那么设 $g_{n,m}$ 表示 $n$ 个点 $m$ 条边的简单**连通**二分图数（染色方式不同算不同的方式），可以得到：

$$g_{n,m}=f_{n,m}-\sum_{i=1}^{n-1}\sum_{j=0}^{m}{\binom{n-1}{i-1}\times g_{i,j}\times h_{n-i,m-j}}$$

这个式子就是用总方案减去有至少两个连通块的方案数。

然后设 $h_{n,m}$ 表示 $n$ 个点 $m$ 条边的简单二分图数（染色方式不同算相同的方式），可以得到：

$$h_{n,m}=\frac{\sum_{i=1}^{n}\sum_{j=0}^{m}{\binom{n-1}{i-1}\times g_{i,j}\times h_{n-i,m-i}}}{2}$$

---

最后考虑怎么处理有重边的情况，先设有 $k$ 种边。

题目转化为有一个长度为 $m$ 的序列，序列每个数的取值范围为 $[1,k]$，问有多少个序列满足他们 $k$ 种数都出现过。容易发现直接容斥即可。

时间复杂度：$O(n^6+n^4\log m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 35, kMaxM = 505, kMod = 998244353, kInv2 = 499122177;

int n, m;
int C[kMaxM][kMaxM], pw[kMaxM], f[kMaxN][kMaxM], g[kMaxN][kMaxM], h[kMaxN][kMaxM];

int add(int x, int y) { return (x + y) >= kMod ? (x + y - kMod) : (x + y); }
int sub(int x, int y) { return (x - y) < 0 ? (x - y + kMod) : (x - y); }
void inc(int &x, int y) { (x += y) >= kMod ? (x -= kMod) : x; }
void dec(int &x, int y) { (x -= y) < 0 ? (x += kMod) : x; }

int qpow(int bs, int idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = 1ll * bs * bs % kMod)
    if (idx & 1)
      ret = 1ll * ret * bs % kMod;
  return ret;
}

void prework() {
  C[0][0] = 1;
  for (int i = 1; i <= 500; ++i) {
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j)
      C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  prework();
  f[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= i * (i - 1) / 2; ++j) {
      for (int k = 0; k <= i; ++k) {
        inc(f[i][j], 1ll * C[i][k] * C[k * (i - k)][j] % kMod);
      }
    }
  }
  g[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= i * i / 4; ++j) {
      g[i][j] = f[i][j];
      for (int k = 1; k < i; ++k) {
        for (int s = 0; s <= std::min(k * k / 4, j); ++s) {
          dec(g[i][j], 1ll * C[i - 1][k - 1] * g[k][s] % kMod * f[i - k][j - s] % kMod);
        }
      }
      // std::cerr << i << ' ' << j << ' ' << g[i][j] << '\n';
    }
  }
  h[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= i * i / 4; ++j) {
      for (int k = 1; k <= i; ++k) {
        for (int s = 0; s <= std::min(k * k / 4, j); ++s) {
          inc(h[i][j], 1ll * C[i - 1][k - 1] * g[k][s] % kMod * h[i - k][j - s] % kMod * kInv2 % kMod);
        }
      }
      // std::cerr << i << ' ' << j << ' ' << h[i][j] << '\n';
    }
  }
  int ans = 0;
  for (int i = 0; i <= std::min(n * (n - 1) / 2, m); ++i) {
    int w = 0;
    for (int j = 0; j <= i; ++j) {
      inc(w, 1ll * (((i - j) & 1) ? (kMod - 1) : 1) * C[i][j] % kMod * qpow(j, m) % kMod);
    }
    inc(ans, 1ll * w * h[n][i] % kMod);
    // std::cerr << w << ' ' << h[n][i] << '\n';
  }
  std::cout << 1ll * ans * qpow(2, m) % kMod << '\n';
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  // std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```