---
title: '[AT WTF2022 Day2 D] Cat Jumps 题解'
date: 2025-06-27 17:10:00
---

## Description

给定一个正整数序列 $A_1, A_2, \cdots, A_N$。定义 $S = N + \sum_{1 \leq i \leq N} A_i$。

猫 Snuke 拥有 $S$ 张卡片。每张卡片上写有一个整数，分别为 $A_1, A_2, \cdots, A_N, -1, \cdots, -1$。特别地，写有 $-1$ 的卡片共有 $\sum_{1 \leq i \leq N} A_i$ 张。

Snuke 现在位于数轴上坐标为 $0$ 的位置。接下来，它将进行 $S$ 次如下操作：

- 设 Snuke 当前所在位置的坐标为 $x$。从持有的卡片中选择一张并丢弃。设丢弃的卡片上的数为 $v$，则跳跃到坐标为 $x + v$ 的位置。如果跳跃后的坐标为 $0$，则获得 $1$ 枚硬币。

对于每个 $k = 1, 2, \cdots, N$，求 Snuke 恰好获得 $k$ 枚硬币的跳跃序列有多少种，结果对 $998244353$ 取模。

注意计数的是跳跃序列。也就是说，如果两张卡片上的数相同，则丢弃它们的操作被视为相同的。

$1 \leq N \leq 5000$，$1 \leq A_i \leq 5000$。

## Solution

先把所有 $a_i$ 相同的卡片看成不同的，最后除以每个出现次数的阶乘即可。

考虑求出**钦定** $k$ 个硬币的方案数，最后再二项式反演回去即可。

对于一个集合 $S$，设其大小为 $c$，总和为 $sum$，则它的内部出现一个硬币的方案数为 $(sum+1)(sum+2)\cdots(sum+c)$。

现在相当于是要求将整个集合划分为 $k$ 个非空子集后，每个子集的权值乘积之和。

但是单个子集的权值很复杂，不好刻画。考虑组合意义。

建出一个有 $n^2$ 条边的有向图，$w_{i,j}=a_j+[j\leq i]$。确定了一个集合划分后，每个点向任意与其在同一集合内的点连边，求连出来的边的权值乘积之和。

这是因为显然每个点之间互相独立，而一个集合内编号第 $i$ 小的点所能连的边的边权之和为 $sum+i$，所以这个边权乘积之和就是答案！

---

由于每个点出度为一，所以连出来的图是个内向基环树森林，求出每个连通块数对应的方案数再乘上第二类斯特林数就是上面问题的答案。

考虑容斥环数。

对于没有钦定在环上的点，显然是随便连，贡献为 $\sum_{j=1}^{n}a_j+i$。

对于环上的点，由于环的问题不好做，所以考虑将其断为链。

具体的，将 $w_{i,j}$ 的形式变为 $a_j+1-[i<j]$，现在问题变为每条边可以在 $a_j+1$ 和 $-[i<j]$ 里任选一个乘起来，问乘积之和。

由于要对答案有贡献，一个环不可能都选 $-[i<j]$，所以所有选 $a_j+1$ 的边就能把环断成链，显然每条链的编号大小一定递增，且一个链的链头权值为 $a_i+1$，后面的全是 $-1$。

把这些链找出来，再随意组合成环后权值是不变的，这部分的贡献是第一类斯特林数。

考虑 dp。

设 $f_{i,j}$ 表示考虑了编号为 $1\sim i$ 的点，目前有 $j$ 条链的贡献之和，转移为：$f_{i,j}\leftarrow f_{i-1,j}\cdot(-j)+f_{i-1,j-1}\cdot(a_i+1)+f_{i-1,j}\cdot(S+i)$。

这三种转移分别代表 $i$ 是接在原来的链的末尾，还是新开一条链，还是直接不钦定在环上。

做完 dp 后在反推回去即可。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e3 + 5, kMod = 998244353;

int n;
int a[kMaxN], cnt[kMaxN];
int fac[kMaxN], C[kMaxN][kMaxN], S1[kMaxN][kMaxN], S2[kMaxN][kMaxN];
int f[kMaxN], g[kMaxN], h[kMaxN];

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

void prework(int n = 5e3) {
  fac[0] = S1[0][0] = S2[0][0] = C[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j) {
      C[i][j] = add(C[i - 1][j - 1], C[i - 1][j]);
      S1[i][j] = add(S1[i - 1][j - 1], 1ll * (i - 1) * S1[i - 1][j] % kMod);
      S2[i][j] = add(S2[i - 1][j - 1], 1ll * j * S2[i - 1][j] % kMod);
    }
  }
}

void dickdreamer() {
  std::cin >> n;
  int S = 0, coef = 1;
  for (int i = 1; i <= n; ++i) std::cin >> a[i], S += a[i], coef = 1ll * coef * qpow(++cnt[a[i]]) % kMod;
  prework();
  h[0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = i; ~j; --j) {
      h[j] = 1ll * (S + i - j) * h[j] % kMod;
      if (j) inc(h[j], 1ll * (a[i] + 1) * h[j - 1] % kMod);
    }
  }
  for (int i = 1; i <= n; ++i)
    for (int j = i; j <= n; ++j)
      inc(g[i], 1ll * h[j] * S1[j][i] % kMod);
  for (int i = n; i; --i)
    for (int j = n; j > i; --j)
      dec(g[i], 1ll * g[j] * C[j][i] % kMod);
  // for (int i = 1; i <= n; ++i) std::cerr << g[i] << " \n"[i == n];
  for (int i = 1; i <= n; ++i)
    for (int j = i; j <= n; ++j)
      inc(f[i], 1ll * g[j] * S2[j][i] % kMod);
  for (int i = 1; i <= n; ++i) f[i] = 1ll * f[i] * fac[i] % kMod;
  // for (int i = 1; i <= n; ++i) std::cerr << f[i] << " \n"[i == n];
  for (int i = n; i; --i)
    for (int j = n; j > i; --j)
      dec(f[i], 1ll * f[j] * C[j - 1][i - 1] % kMod);
  for (int i = 1; i <= n; ++i) std::cout << 1ll * f[i] * coef % kMod << '\n';
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