---
title: CF1842G Tenzing and Random Operations 题解
date: 2024-10-02 09:22:00
---

## Description

有一长度为 $n$ 的序列 $a$ 和一整数 $v$，对该序列进行 $m$ 次操作。

每次操作中，等概率地随机选择一整数 $i \in [1, n]$，对所有的 $j \in [i, n]$，赋值 $a_j \gets a_j+v$，求出 $m$ 次操作后 $\Pi_{i=1}^n a_i$ 的期望值，对 $10^9+7$ 取模。

数据范围：$0\leq n \leq 5000$，$1 \leq m, v \leq10^9$，$a_i \in [1, 10^9] \cap \mathbb{Z}$。

## Solution

设 $b_i$ 表示第 $i$ 次操作随机选择的数，那么答案形如：

$$
\prod_{i=1}^{n}{\left(a_i+\sum_{j=1}^{m}{\left[b_j\leq i\right]v}\right)}
$$

这个东西显然是可以拆开的，最终答案一定形如一些 $a_i$ 的乘积和某些 $[b_j\leq i]v$ 的乘积。

假设 $[b_j\leq i]v$ 选的下标是 $i_1<i_2<\ldots<i_k$，如果 $b_j>i_1$，则乘积为 $0$，没有贡献。否则一定有贡献，所以选的 $b_j$ 只需要满足 $b_j$ 不超过第一个选 $j$ 的下标即可。

这样就可以 dp 了。

设 $f_{i,j}$ 表示 $[1,i]$ 的前缀，目前已经选好了 $j$ 的 $b_k$ 的位置。如果这一位选了 $a_i$，则 $f_{i,j}\leftarrow a_if_{i-1,j}$。如果这一位选了之前选过的 $b_k$，则 $f_{i,j}\leftarrow jvf_{i-1,j}$。如果这一位选了一个新的 $b_k$，则 $f_{i,j+1}\leftarrow (m-j)iv\cdot f_{i-1,j}$，这里的 $i$ 是从 $[1,i]$ 中选一个作为 $b_k$ 的方案数。

最终答案即为 $\sum \frac{f_{n,i}n^{m-i}}{n^m}$。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e3 + 5, kMod = 1e9 + 7;

int n, m, v;
int a[kMaxN], f[kMaxN][kMaxN];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

void dickdreamer() {
  std::cin >> n >> m >> v;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  f[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= std::min(n, m); ++j) {
      inc(f[i][j], 1ll * a[i] * f[i - 1][j] % kMod);
      inc(f[i][j], 1ll * j * v % kMod * f[i - 1][j] % kMod);
      inc(f[i][j + 1], 1ll * (m - j) * i % kMod * v % kMod * f[i - 1][j] % kMod);
    }
  }
  int ans = 0;
  for (int i = 0; i <= std::min(n, m); ++i)
    inc(ans, 1ll * f[n][i] * qpow(n, m - i) % kMod);
  std::cout << 1ll * ans * qpow(qpow(n), m) % kMod << '\n';
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