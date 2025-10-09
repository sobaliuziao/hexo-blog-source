---
title: CF2089E Black Cat Collapse 题解
date: 2025-07-31 17:12:00
---

## Description

好排列满足以下条件：

1. 若点 $u,v$ 都被选中且 $u$ 是 $v$ 的祖先，那么在排列中 $u$ 在 $v$ 后面。
2. 若点 $u$ 被选中，那么 $u$ 必须出现在序列中前 $(n−i+1)$ 个位置。

现有一棵 dfs 序为 $1,2,...,n$ 的树。对于所有 $i$ 求选出 $i$ 个点的好排列的方案数。

$n\leq 80$。

## Solution

首先如果没有 2 的限制，可以直接树形 dp 求。

加入 2 的限制后就不能按照树的形态进行转移了。

先把询问的序列翻转，注意到对于所有的 2 限制，只需要考虑前缀最大值的限制，因为不是前缀最大值的数一定会被某个前缀最大值偏序。

同时由于一个子树的编号一定构成一段区间，所以考虑从大到小按照编号往序列中插入元素。

具体地，设 $f_{i,j,k}$ 表示已经插入了 $[i,n]$ 的数，目前插入了 $j$ 个数，已经插入的数中在序列中最前面的位置到末尾有 $k$ 个数的方案数；$g_{i,j}$ 表示 $i$ 的子树不考虑 2 限制选 $j$ 个数，要求满足 1 限制的方案数。转移如下：

1. $i$ 不插入：$f_{i,j,k}\leftarrow f_{i+1,j,k}$。
2. $i$ 插入到开头，即钦定 $i$ 是前缀最大值：$f_{i,j+1,k'}\leftarrow f_{i+1,j,k}(k<k'\leq n-i+1)$。
3. $i$ 不插入到开头：注意到 $i$ 子树里的点必须在 $i$ 后面，且 $>i$ 的点不会是 $i$ 的祖先，所以从把 $i$ 子树内的点去掉后的状态转移过来，即 $f_{i,j+x,k}\leftarrow f_{i+sz_i,j,k}(1\leq x\leq sz_i)$。

时间复杂度：$O(n^4)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 85, kMod = 998244353;

int n;
int C[kMaxN][kMaxN], sz[kMaxN], f[kMaxN][kMaxN][kMaxN], g[kMaxN][kMaxN], h[kMaxN][kMaxN];
std::vector<int> G[kMaxN];

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

void prework(int n = 80) {
  C[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j)
      C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    if (u > v) std::swap(u, v);
    G[u].emplace_back(v);
  }
  for (int u = n; u; --u) {
    std::fill_n(g[u], n + 1, 0);
    sz[u] = 0, g[u][0] = 1;
    for (auto v : G[u]) {
      static int tmp[kMaxN];
      for (int i = 0; i <= sz[u]; ++i) tmp[i] = g[u][i], g[u][i] = 0;
      for (int i = 0; i <= sz[u]; ++i)
        for (int j = 0; j <= sz[v]; ++j)
          inc(g[u][i + j], 1ll * C[i + j][i] * tmp[i] % kMod * g[v][j] % kMod);
      sz[u] += sz[v];
    }
    ++sz[u];
    for (int i = sz[u]; i; --i) inc(g[u][i], g[u][i - 1]), h[u][i] = g[u][i - 1];
  }
  for (int i = 0; i <= n + 1; ++i)
    for (int j = 0; j <= n + 1; ++j)
      for (int k = 0; k <= n + 1; ++k)
        f[i][j][k] = 0;
  f[n + 1][0][0] = 1;
  for (int i = n; i; --i) {
    for (int j = 0; j <= n - i; ++j) {
      for (int k = j; k <= n; ++k) {
        if (i != 1) inc(f[i][j][k], f[i + 1][j][k]);
        for (int kk = k + 1; kk <= n - i + 1; ++kk)
          inc(f[i][j + 1][kk], f[i + 1][j][k]);
        for (int x = 1; x <= sz[i]; ++x) {
          if (j + x <= n) inc(f[i][j + x][k], 1ll * f[i + sz[i]][j][k] * C[k - j][x] % kMod * h[i][x] % kMod);
        }
      }
    }
  }
  for (int i = 1; i <= n; ++i) std::cout << f[1][i][i] << " \n"[i == n];
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  prework();
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```