---
title: [AGC050F] NAND Tree 题解
date: 2025-06-28 10:48:00
---

## Description

一个 $n$ 个点的树。每个点有点权 $0$ 或 $1$。

每次可以选择一条边，使两个端点缩成一个点，新点权值为两端点权值 AND 再取反。

一直操作直到只剩一个点。

求有多少种操作方案使最终剩下的点权值为 $1$。输出答案对 $2$ 取模的值。

$n\leq 300$。

## Solution

首先如果 $n$ 是偶数就先枚举第一步操作的边，将 $n$ 变为奇数。现在操作次数一定是偶数。

注意到只需要输出答案模 $2$ 的结果，所以很多操作方案之间可以抵消。考虑根据这个找一些性质。

显然对于在操作序列上相邻的两条边，如果把前面的操作做完后这两条边在图上没有公共点就可以交换，那么这样的操作方案就不用考虑了。

所以第 $2i-1$ 和 $2i$ 这两个操作边一定构成一个长度为 $2$ 的链，不妨设其为 $x\leftrightarrow y \leftrightarrow z$。

容易发现如果 $c_x=c_z$，则这样的链操作一定能够抵消，而 $c_x\neq c_z$，则这样的链可以操作成 $01$ 中的任意一个，设这样点的为自由元。

现在考虑有自由元的情况，如果 $y$ 是自由元，则显然会抵消。如果 $x$ 和 $z$ 都是自由元，则 $x$ 和 $z$ 分别取 $01$ 和 $10$，可以抵消。所以 $x$ 和 $z$ 中只能有一个自由元，且每次操作自由元数不降。

做完第一次操作后，图中至少存在一个自由元，而最后只会有一个自由元，所以每两次操作必定会以唯一的自由元为一端点，并将这个三元链合并为一个自由元。

我们枚举第一次操作的 $x$，钦定 $c_x=1$。

问题变为计数以 $x$ 为根的一个拓扑序 $p_1,p_2,\ldots,p_n$，满足：

1. $a_{p_3}=0$。
2. $p_{2i}$ 是 $p_{2i+1}$ 的父亲。

对于第一个条件，不妨先去掉，那么在 $p_3$ 为根，$x$ 为此时拓扑序的第三个元素时，不会影响其余拓扑序的结果，所以当 $a_x=a_{p_3}=1$ 的情况会被抵消，这个条件也就没用了。

对于第二个条件，同样可以去掉，这是因为如果 $p_{2i}$ 不是 $p_{2i+1}$ 的父亲，则将其交换后仍然符合拓扑序要求，会抵消。

现在只需要求一个有根树的拓扑序数量模 $2$ 的结果，答案是 $\displaystyle\frac{n!}{\prod sz_i}$，计算每个数含 $2$ 的数量即可。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 305;

int n, cnt;
int a[kMaxN], sz[kMaxN];
std::vector<int> g[kMaxN], G[kMaxN];

bool nand(bool a, bool b) { return !(a & b); }

void dfs(int u, int fa) {
  sz[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs(v, u);
    sz[u] += sz[v];
  }
  cnt += __builtin_ctz(sz[u]);
}

bool solve(int del = 0) {
  int ret = 0, tot = 0;
  for (int i = 1; i <= n - (bool)del; ++i) tot += __builtin_ctz(i);
  // std::cerr << n << ' ' << tot << '\n';
  for (int i = 1; i <= n; ++i) {
    if (i != del && a[i]) {
      cnt = 0, dfs(i, 0);
      // assert(cnt <= tot);
      ret ^= (cnt == tot);
    }
  }
  return ret;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
    g[u].emplace_back(v), g[v].emplace_back(u);
  }
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  bool ans = 0;
  if (n & 1) {
    ans ^= solve();
  } else {
    for (int u = 1; u <= n; ++u) {
      for (auto v : g[u]) {
        if (u > v) continue;
        for (int i = 1; i <= n; ++i) G[i].clear();
        for (auto i : g[u])
          if (i != v)
            G[u].emplace_back(i);
        for (auto i : g[v])
          if (i != u)
            G[u].emplace_back(i);
        for (int i = 1; i <= n; ++i) {
          if (i == u || i == v) continue;
          for (auto j : g[i]) {
            if (j == u || j == v) G[i].emplace_back(u);
            else G[i].emplace_back(j);
          }
        }
        int lst = a[u];
        a[u] = nand(a[u], a[v]), ans ^= solve(v), a[u] = lst;
      }
    }
  }
  std::cout << ans << '\n';
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