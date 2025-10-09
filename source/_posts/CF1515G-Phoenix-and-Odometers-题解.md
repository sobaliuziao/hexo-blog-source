---
title: CF1515G Phoenix and Odometers 题解
date: 2025-05-08 19:17:00
---

## Description

给定一张 $n$ 个点 $m$ 条边的有向图，有边权，进行 $q$ 次询问（$n,m,q\leq 2\times 10^5$，边权为不超过 $10^9$ 的正整数）。

每次询问给定三个参数 $v,s,t(0\leq s<t\leq 10^9)$，你需要回答是否存在一条起点终点均为 $v$ 的路径，满足 $路径长+s\equiv 0\pmod t$。

## Solution

先缩强连通分量，容易发现一个点只能走与其属于同一个强连通分量的点。

把强连通分量中的所有环拿出来，然后把这些环都走 $t$ 遍，根据欧拉回路，一定存在这样的走法。后面想走任何一个环任意次都是可以的了，因为已经先把每个环走 $t$ 次，整个分量已经连通，而加入一个环仍然满足入度出度的限制，所以仍然存在从任意一点开始的回路。

现在设环长为 $a_1,a_2,\ldots,a_k$，根据贝祖定理，所有满足是 $\gcd(a_1,a_2,\ldots,a_k,t)$ 的倍数的数都能被表示，于是现在只需要求出每个环长的 $\gcd$ 了。

由于环的数量可能很多，不能一一找出。但是注意到只需要保留简单环，而一个简单环一定包含至少一条返祖边或者横叉边，考虑对这两种边进行分讨。设边为 $(u\to v,w)$，点 $u$ 到根的距离是 $dis_u$。

1. 返祖边：把 $dis_u+w-dis_v$ 加入贡献。
2. 横叉边：由于 $u$ 走到 $v$ 之后要再走回来就必须经过一个只有返祖边的简单环，把这个有横叉边的环边权减去只有返祖边的环的值加入贡献，这个贡献还是 $dis_u+w-dis_v$。

tarjan 求出强连通分量并用一遍 dfs 求出每个强连通分量环长的 $\gcd$ 即可。

时间复杂度：$O(n+(m+q)\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = long long;

const int kMaxN = 2e5 + 5;

int n, m, q, cnt_scc;
int dfn[kMaxN], low[kMaxN], bel[kMaxN];
bool ins[kMaxN];
i64 dis[kMaxN], res[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u) {
  static bool vis[kMaxN];
  vis[u] = 1;
  for (auto [v, w] : G[u]) {
    if (bel[v] != bel[u]) continue;
    if (!vis[v]) {
      dis[v] = dis[u] + w;
      dfs(v);
    } else {
      res[bel[u]] = std::__gcd(res[bel[u]], llabs(dis[u] + w - dis[v]));
    }
  }
}

void tarjan(int u) {
  static int cnt = 0;
  static std::stack<int> stk;
  dfn[u] = low[u] = ++cnt, ins[u] = 1, stk.emplace(u);
  for (auto [v, w] : G[u]) {
    if (!dfn[v]) {
      tarjan(v);
      low[u] = std::min(low[u], low[v]);
    } else if (ins[v]) {
      low[u] = std::min(low[u], dfn[v]);
    }
  }
  if (low[u] == dfn[u]) {
    ++cnt_scc;
    for (; !stk.empty();) {
      int t = stk.top(); stk.pop();
      bel[t] = cnt_scc, ins[t] = 0;
      if (t == u) break;
    }
    dfs(u);
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w);
  }
  for (int i = 1; i <= n; ++i)
    if (!dfn[i])
      tarjan(i);
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int v, s, t;
    std::cin >> v >> s >> t;
    std::cout << (s % std::__gcd((i64)t, res[bel[v]]) == 0 ? "YES\n" : "NO\n");
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