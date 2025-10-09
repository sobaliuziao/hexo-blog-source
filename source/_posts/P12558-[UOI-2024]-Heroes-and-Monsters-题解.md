---
title: P12558 [UOI 2024] Heroes and Monsters 题解
date: 2025-09-15 21:24:00
---

## Description

有 $n$ 个英雄和 $n$ 个怪物。英雄和怪物分别编号为 $1$ 到 $n$ 的整数。第 $i$ 个英雄的战斗力为 $a_i$，第 $i$ 个怪物的战斗力为 $b_i$。保证所有 $a_1, a_2, \ldots, a_n, b_1, b_2, \ldots, b_n$ 的值都是**两两不同**的。

将进行总共 $n$ 场战斗。每场战斗中恰好有一个英雄和一个怪物参与，且每个英雄和每个怪物都恰好参与一场战斗。假设某场战斗由编号为 $i$ 的英雄和编号为 $j$ 的怪物进行。如果 $a_i > b_j$，则编号为 $i$ 的英雄会感到高兴；否则，他会感到悲伤。

定义 $ans_k$ 为大小为 $k$ 的不同英雄集合 $S$ 的数量，满足存在一种战斗分配方式使得集合 $S$ 中的所有英雄都高兴，而其他英雄都悲伤。

给定 $q$ 个形如 $l$、$r$ 的查询。对于每个查询，计算 $(\sum\limits_{i=l}^{r} ans_i) \bmod 998244353$ 的值。

$n\leq 5000$。

## Solution

先把 $a$ 和 $b$ 分别排序。

不妨设选出来的英雄的集合是 $S$，没选的是 $T$，则需要满足：

1. $a_{S_i}<b_i$
2. $a_{T_i}>b_{i+|S|}$

先枚举 $|S|$ 再从小到大扫，设 $f_{i,j}$ 表示前 $i$ 个英雄，选了 $j$ 个的方案数，直接转移是 $O(n^3+q)$。

考虑优化。

容易发现 $|S|$ 的枚举是很难去掉的，所以还是先枚举 $|S|$。

注意到 $T$ 值域在 $[1,b_{|S|}]$ 的部分一定合法，$S$ 值域在 $[b_{|S|}+1,2n]$ 的部分也一样合法。所以直接前缀维护 $f_{i,j}$ 表示前 $i$ 个选 $j$ 个的方案数，$g_{i,j}$ 表示 $i$ 开始的后缀有 $j$ 个不选的方案数。

两者的转移是一样的。

时间复杂度：$O(n^2+q)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e3 + 5, kMod = 998244353;

int n, q;
int a[kMaxN], b[kMaxN], op[kMaxN * 2], pre[kMaxN * 2], suf[kMaxN * 2];
int f[kMaxN * 2][kMaxN], g[kMaxN * 2][kMaxN], res[kMaxN];

int qpow(int bs, int64_t idx = kMod - 2) {
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
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i], op[a[i]] = 0;
  for (int i = 1; i <= n; ++i) std::cin >> b[i], op[b[i]] = 1;
  for (int i = 1; i <= 2 * n; ++i) pre[i] = pre[i - 1] + !op[i];
  for (int i = 2 * n; i >= 1; --i) suf[i] = suf[i + 1] + !op[i];
  f[0][0] = g[2 * n + 1][0] = 1;
  for (int i = 1; i <= 2 * n; ++i) {
    for (int j = 0; j <= std::min(n, i - 1); ++j) {
      if (op[i] == 1) {
        inc(f[i][j], f[i - 1][j]);
      } else {
        inc(f[i][j], f[i - 1][j]);
        if (j + 1 <= i - pre[i]) inc(f[i][j + 1], f[i - 1][j]);
      }
    }
  }
  for (int i = 2 * n; i; --i) {
    for (int j = 0; j <= std::min(n, 2 * n - i); ++j) {
      if (op[i] == 1) {
        inc(g[i][j], g[i + 1][j]);
      } else {
        inc(g[i][j], g[i + 1][j]);
        if (j + 1 <= 2 * n - i + 1 - suf[i]) inc(g[i][j + 1], g[i + 1][j]);
      }
    }
  }
  for (int i = 0; i <= 2 * n; ++i) {
    if (!i || op[i] == 1) {
      int k = i - pre[i];
      for (int j = 0; j <= std::min(k, suf[i + 1]); ++j)
        inc(res[k], 1ll * f[i][k - j] * g[i + 1][suf[i + 1] - j] % kMod);
    }
  }
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int l, r;
    std::cin >> l >> r;
    int ans = 0;
    for (int j = l; j <= r; ++j) inc(ans, res[j]);
    std::cout << ans << '\n';
  }
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