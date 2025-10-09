---
title: 'P12445 [COTS 2025] Promet 题解'
date: 2025-06-17 21:11:00
---

## Description

给定正整数 $N$ 和素数 $P$。

$\forall K=0,1,\ldots,N$，求出满足以下条件的**简单**有向图的数量：

- 图中仅包含 $i\to j$（$1\le i\lt j\le N$）的边；
- 满足以下条件的点 $u$ 恰好有 $K$ 个：
  - 存在 $1\to u$ 和 $u\to N$ 的路径。

只需要输出答案对 $P$ 取模后的结果。

$2\le N\le 2\,000$。

## Solution

首先考虑 $k=n$ 怎么求。

容易发现这个一个连边方案合法的充要条件就是 $[1,n-1]$ 内的点都有出度，$[2,n]$ 内的点都有入度，考虑先保证每个点都有入度，并容斥出度为 $0$ 的点的个数。

具体地，设 $f_{i,j}$ 表示前 $i$ 个点，钦定 $i-j$ 个点出度为 $0$ 的方案数，转移即为：$f_{i,j}\leftarrow f_{i-1,j}\cdot(2^j-1)+f_{i-1,j-1}\cdot(2^{j-1}-1)$。求出 $f_{i,j}$ 之后再二项式定理求出恰好一个点（因为 $n$ 一定没有出度）出度为 $0$ 的方案数即可。设 $i$ 个点的方案数为 $h_i$。

然后考虑 $k$ 更小的情况怎么做。

先对点进行分类：

1. 既存在 $1\to u$ 也存在 $u\to n$ 的路径。
2. 只存在 $1\to u$ 但不存在 $u\to n$ 的路径。
3. 不存在 $1\to u$ 的路径。

容易发现，对于 $1$ 类点往前只能连 $1,3$ 类点，且 $1$ 类点至少一个。$2$ 类点能连 $1,2,3$ 类点，且 $1,2$ 类点至少一个。$3$ 类点能连 $1,3$ 类点。

这里不考虑 $1$ 类点内部的贡献，因为这个可以已经得到了，为 $h_n$。

注意到 $3$ 类点作为起点时，终点是没有限制的，并且所有 $3$ 类点参与的边中，$3$ 类点一定是起点。所以设 $p_i$ 表示第 $i$ 个 $3$ 类点的位置，那么所有 $3$ 的贡献即为 $2^{\sum(n-p_i)}$。于是只要求出 $1,2$ 类点的贡献后，乘上预处理出来的 $3$ 类点贡献即可。设 $i$ 个 $3$ 类点的贡献为 $s_i$。

对于 $1,2$ 类点之间的贡献，考虑设 $g_{i,j}$ 表示前 $i$ 个点，现在有 $j$ 个 $1$ 类点的贡献，转移为：$g_{i,j}\leftarrow g_{i-1,j-1}+g_{i-1,j}\cdot (2^i-1)$。

然后枚举 $1,2$ 类点的总数 $i$，和 $1$ 类点的个数 $j$ 并让 $res_j\leftarrow g_{i-1,j-1}\cdot s_{n-i}\cdot h_j$ 即可（这里只有 $g_{i-1,j-1}$ 的原因是最后一个点必须是 $1$ 类点）。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e3 + 5;

int n, mod;
int pw[kMaxN], f[kMaxN][kMaxN], g[kMaxN], h[kMaxN], s[kMaxN], res[kMaxN];

int qpow(int bs, int64_t idx = mod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % mod)
    if (idx & 1)
      ret = (int64_t)ret * bs % mod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= mod ? x + y - mod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + mod); }
inline void inc(int &x, int y) { (x += y) >= mod ? x -= mod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += mod : x; }
inline int getop(int x) { return (~x & 1) ? 1 : (mod - 1); }

void prework() {
  pw[0] = 1;
  for (int i = 1; i <= n; ++i) {
    pw[i] = 2ll * pw[i - 1] % mod;
  }
}

void gets() {
  static int f[kMaxN][kMaxN];
  f[1][0] = f[1][1] = 1;
  for (int i = 2; i <= n; ++i) {
    for (int j = 0; j <= i - 1; ++j) {
      int val = f[i - 1][j];
      inc(f[i][j], 1ll * val * (pw[j] - 1) % mod);
      inc(f[i][j + 1], 1ll * val * (pw[j] - 1) % mod);
    }
  }
  for (int i = 2; i <= n; ++i) {
    // for (int j = 0; j <= i; ++j)
    //   for (int k = 0; k < j; ++k)
    //     dec(f[i][j], 1ll * f[i][k] * C[i - k][i - j] % mod);
    // for (int j = 0; j <= i; ++j) inc(s[i], 1ll * getop(i - j) * f[i][j] % mod);
    // for (int j = 0; j <= i; ++j) std::cerr << f[i][j] << " \n"[j == i];
    // std::cerr << s[i] << '\n';
    // s[i] = f[i][i - 1];
    for (int j = 0; j <= i - 1; ++j) inc(s[i], 1ll * getop(i - 1 - j) * (i - j) % mod * f[i][j] % mod);
  }
}

void dickdreamer() {
  std::cin >> n >> mod;
  prework();
  // g[i] : xuan i ge 3 de gong xian
  g[0] = 1;
  for (int i = 2; i <= n - 1; ++i) {
    for (int j = i - 1; j; --j) inc(g[j], 1ll * pw[n - i] * g[j - 1] % mod);
  }
  gets();
  // for (int i = 0; i <= n - 2; ++i) std::cerr << g[i] << " \n"[i == n - 2];
  f[1][1] = 1;
  for (int i = 2; i <= n; ++i) {
    for (int j = 1; j <= i - 1; ++j) {
      int val = f[i - 1][j];
      inc(f[i][j + 1], val);
      // std::cerr << "??? " << j + 1 << ' ' << i << ' ' << 1ll * val * g[n - i] % mod << '\n';
      inc(h[j + 1], 1ll * val * g[n - i] % mod);
      if (i != n) {
        inc(f[i][j], 1ll * val * (pw[i - 1] - 1) % mod);
      }
    }
  }
  for (int i = 2; i <= n; ++i) res[i] = 1ll * h[i] * s[i] % mod;
  res[0] = qpow(2, n * (n - 1) / 2);
  for (int i = 1; i <= n; ++i) dec(res[0], res[i]);
  for (int i = 0; i <= n; ++i) std::cout << res[i] << " \n"[i == n];
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