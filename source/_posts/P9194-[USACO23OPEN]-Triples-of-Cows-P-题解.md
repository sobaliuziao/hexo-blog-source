---
title: P9194 [USACO23OPEN] Triples of Cows P 题解
date: 2023-11-09 22:29:00
---

## Description

给定一棵初始有 $n$ 个点的树。

在第 $i$ 天，这棵树的第 $i$ 个点会被删除，所有与点 $i$ **直接相连**的点之间都会**两两**连上一条边。你需要在每次删点**发生前**，求出满足 $(a,b)$ 之间有边，$(b,c)$ 之间有边且 $a\not=c$的**有序**三元组 $(a,b,c)$ 对数。

$n\leq 2\times 10^5$。

## Solution

考虑把每个原图中的点看成白点，边看成黑点，原图中有连边的两个点就向他们对应的黑点连边。

那么每次删点操作就相当于把一个白点的所有相邻黑点合并，并且删除这个黑点。

所以所有 $(a,b,c)$ 可以看成 $(a,x,b,y,c)$，其中 $x$ 是 $a,b$ 连边对应的黑点，$y$ 是 $b,c$ 连边对应的黑点。

容易发现把 $n$ 作为根可以保证图始终是个树。

设 $s_x$ 表示 $x$ 的儿子数，$t_x$ 表示 $x$ 儿子的 $s$ 之和，$w_x$ 表示 $x$ 儿子的 $t$ 之和。然后考虑分类讨论。

首先如果 $x=y$，答案就是 $\sum_{x为黑点}{(s_x+1)s_x(s_x-1)}$。

如果 $x\neq y$ 但是 $x,y$ 都是 $b$ 的儿子，答案就是 $\sum_{b为白点}{\left(t_b^2-\sum_{x\in son(b)}{s_x^2}\right)}$。

最后就是 $x\neq y$ 且 $x,y$ 一个是 $b$ 的儿子，一个是 $b$ 的父亲。

答案就是 $2\sum_{x是黑点}{s_x w_x}$。

把所有的加起来就是：

$$\sum_{x是黑点}{s_x^3-s_x^2-s_x+2s_x w_x}+\sum_{y是白点}{t_y^2}$$

每次合并的时候用并查集维护即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 4e5 + 5;

int n;
int64_t ans;
int fa[kMaxN], s[kMaxN], t[kMaxN], w[kMaxN];
std::vector<int> G[kMaxN];

struct DSU {
  int fa[kMaxN];

  void init(int n) { std::iota(fa + 1, fa + 1 + n, 1); }

  int find(int x) { return x == fa[x] ? x : fa[x] = find(fa[x]); }
} dsu;

void dfs(int u) {
  for (auto v : G[u]) {
    if (v == fa[u]) continue;
    fa[v] = u, ++s[u];
    dfs(v);
    t[u] += s[v], w[u] += t[v];
  }
}

int64_t getcnt(int u) {
  if (!u) return 0;
  else if (u <= n) return (int64_t)t[u] * t[u];
  else return (int64_t)s[u] * s[u] * s[u] - (int64_t)s[u] * s[u] - s[u] + (int64_t)2 * s[u] * w[u];
}

void work(int u) {
  int ffa = dsu.find(fa[u]), fffa = dsu.find(fa[ffa]), ffffa = dsu.find(fa[fffa]);
  ans -= getcnt(u) + getcnt(ffa) + getcnt(fffa) + getcnt(ffffa);
  --s[ffa], --t[fffa], --w[ffffa];
  for (auto v : G[u]) {
    if (v == fa[u]) continue;
    int fv = dsu.find(v);
    dsu.fa[fv] = ffa;
    ans -= getcnt(fv);
    s[ffa] += s[fv], t[ffa] += t[fv], w[ffa] += w[fv];
    --t[ffa], w[ffa] -= s[fv];
    --w[fffa], w[fffa] += t[fv], t[fffa] += s[fv];
    w[ffffa] += s[fv];
  }
  ans += getcnt(ffa) + getcnt(fffa) + getcnt(ffffa);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(n + i), G[n + i].emplace_back(u);
    G[v].emplace_back(n + i), G[n + i].emplace_back(v);
  }
  dfs(n);
  dsu.init(2 * n - 1);
  for (int i = 1; i <= 2 * n - 1; ++i)
    ans += getcnt(i);
  for (int i = 1; i <= n; ++i) {
    std::cout << ans << '\n';
    work(i);
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