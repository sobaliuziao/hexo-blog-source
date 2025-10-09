---
title: [AGC039F] Min Product Sum 题解
date: 2025-06-27 10:08:00
---

## Description

有一个大小为 $N\times M$ 的矩阵。矩阵中每个数的取值都是 $[1,K]$。

对于一个矩阵，定义函数 $f(x,y)$ 为：第 $x$ 行和第 $y$ 列的一共 $N+M-1$ 个数中的最小值。

对于一个矩阵，定义其权值为 $\displaystyle\prod_{x=1}^{N}\prod_{y=1}^{M}{f(x,y)}$。

你需要求出，对于所有 $K^{NM}$ 种矩阵，每个矩阵的权值和对 $D$ 取模的结果。

$1\leq N,M,K\leq 100$，$10^8\leq D\leq 10^9$，保证 $D$ 为质数。

## Solution

首先设矩阵为 $b$，$c_i$ 表示 $b$ 第 $i$ 行的最小值，$d_j$ 表示 $b$ 第 $j$ 列的最小值，它的权值可以转化为有多少个矩阵 $a$，满足：$a_{i,j}\leq \min\{c_i,d_j\}$，也就是说 $a$ 的第 $i$ 行最大值小于等于 $c_i$ 且 $a$ 的第 $j$ 行最大值小于等于 $d_j$，同时显然需要满足 $b_{i,j}\geq \max\{c_i,d_j\}$。

显然是按照权值从小到大确定，但是需要满足 $c_i$ 和 $d_j$ 的限制，所以还需要对两维进行容斥，具体来说有四种贡献：

1. $\min\{c_i,d_j\}\times(k-\max\{c_i,d_j\}+1)$
2. $\min\{c_i-1,d_j\}\times(k-\max\{c_i,d_j\}+1)$
3. $\min\{c_i,d_j-1\}\times(k-\max\{c_i,d_j\}+1)$
4. $\min\{c_i-1,d_j-1\}\times(k-\max\{c_i,d_j\}+1)$

设 $f_{v,i,j}$ 表示已经确定了 $\leq v$ 的位置，已经确定 $i$ 个行和 $j$ 个列的贡献。由于状态数已经达到 $O(knm)$ 级别，所以转移只能 $O(n+m)$，这样就只能两维分开转移。

但是在 $c_i=d_j$ 时的 corner case 会导致必须同时枚举两个的个数，就不能分开了。

---

所以考虑转换 $c_i$ 和 $d_j$ 的定义。

将 $c_i$ 变为 $a$ 第 $i$ 行的最大值，那么同样需要满足 $a_{i,j}\leq\min\{c_i,d_j\},b_{i,j}\geq\max\{c_i,d_j\}$，但是贡献变为：

1. $\min\{c_i,d_j\}\times(k-\max\{c_i,d_j\}+1)$
2. $\min\{c_i-1,d_j\}\times(k-\max\{c_i,d_j\}+1)$
3. $\min\{c_i,d_j\}\times(k-\max\{c_i,d_j+1\}+1)$
4. $\min\{c_i-1,d_j\}\times(k-\max\{c_i,d_j+1\}+1)$

现在先转移 $c_i$，再转移 $d_j$ 时，原来的 corner case 就消失了！

对这个 dp 即可。

时间复杂度：$O\left(knm(n+m)\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 105;

int n, m, k, mod;
int f[kMaxN][kMaxN], C[kMaxN][kMaxN];

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

void prework() {
  C[0][0] = 1;
  for (int i = 1; i <= std::max(n, m); ++i) {
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j)
      C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
}

void dickdreamer() {
  std::cin >> n >> m >> k >> mod;
  prework();
  f[0][0] = 1;
  for (int v = 1; v <= k; ++v) {
    for (int i = n; ~i; --i) {
      for (int j = m; ~j; --j) {
        int val = 1ll * sub(qpow(v, m - j), qpow(v - 1, m - j)) * qpow(k - v + 1, j) % mod, coef = 1;
        for (int w = 1; w <= i; ++w) {
          coef = 1ll * coef * val % mod;
          inc(f[i][j], 1ll * f[i - w][j] * C[n - i + w][w] % mod * coef % mod);
        }
      }
    }
    for (int i = n; ~i; --i) {
      for (int j = m; ~j; --j) {
        int val = 1ll * qpow(v, n - i) * sub(qpow(k - v + 1, i), qpow(k - v, i)) % mod, coef = 1;
        for (int w = 1; w <= j; ++w) {
          coef = 1ll * coef * val % mod;
          inc(f[i][j], 1ll * f[i][j - w] * C[m - j + w][w] % mod * coef % mod);
        }
      }
    }
  }
  std::cout << f[n][m] << '\n';
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