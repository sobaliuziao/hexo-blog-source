---
title: CF576D Flights for Regular Customers 题解
date: 2024-07-26 17:18:00
---

## Description

- 给定一张 $n$ 个点 $m$ 条边的有向图。
- 一开始你在 $1$ 号节点，你要走到 $n$ 号节点去。
- 只有当你已经走过了至少 $d_i$ 条边时，你才能走第 $i$ 条边。
- 问最少要走多少条边，或判断无法到达。
- $n,m \le 150$，$d_i \le 10^9$。

## Solution

注意到如果直接跑最短路可能走着走着突然有些边可以走了，这样就不太好做。

考虑枚举当前解锁了哪些边，即枚举 $w$，把所有边权 $\leq w$ 的边加入图中，并选择从 $1$ 走 $w$ 步能到达的点跑多源 bfs 就可以求出只用边权 $\leq w$ 的边能到达 $n$ 的最短距离。

容易发现 $w$ 只有 $O(m)$ 种，所以可以从小到大枚举边权，每次加入一条边。要找到从 $1$ 走 $w$ 步能到达的点就直接用矩阵乘法维护即可。不过这里直接矩乘会是 $O(n^3m\log V)$ 的，显然过不了。

由于矩乘只需维护 0/1 信息，所以 bitset 优化即可。

时间复杂度：$O\left(\frac{n^3m\log V}{\omega}\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 155;

int n, m;
int g[kMaxN][kMaxN], dis[kMaxN];
bool vis[kMaxN];
std::vector<std::tuple<int, int, int>> ed;
std::vector<std::pair<int, int>> G[kMaxN];

struct Matrix {
  int n, m;
  std::bitset<kMaxN> a[kMaxN];

  void set(int _n, int _m) { n = _n, m = _m; }
  friend Matrix operator *(const Matrix &m1, const Matrix &m2) {
    static Matrix ret;
    assert(m1.m == m2.n);
    ret.set(m1.n, m2.m);
    for (int i = 1; i <= m1.n; ++i)
      ret.a[i].reset();
    for (int i = 1; i <= m1.n; ++i) {
      for (int k = 1; k <= m1.m; ++k) {
        if (m1.a[i][k]) ret.a[i] |= m2.a[k]; 
      }
    }
    return ret;
  }
} S, M, O;

void dijkstra() {
  std::priority_queue<std::pair<int, int>> q;
  for (int i = 1; i <= n; ++i) {
    dis[i] = 1e18, vis[i] = 0;
    if (S.a[1][i]) q.emplace(dis[i] = 0, i);
  }
  for (; !q.empty();) {
    auto [d, u] = q.top(); q.pop();
    if (vis[u]) continue;
    vis[u] = 1;
    for (auto [v, w] : G[u]) {
      if (M.a[u][v] && dis[v] > dis[u] + 1) {
        dis[v] = dis[u] + 1, q.emplace(-dis[v], v);
      }
    }
  }
}

Matrix qpow(Matrix bs, int idx) {
  Matrix ret = O;
  for (; idx; idx >>= 1, bs = bs * bs)
    if (idx & 1)
      ret = ret * bs;
  return ret;
}

void dickdreamer() {
  std::cin >> n >> m;
  memset(g, 0x3f, sizeof(g));
  for (int i = 1; i <= m; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    ed.emplace_back(w, u, v);
    G[u].emplace_back(v, w);
    g[u][v] = w;
  }
  std::sort(ed.begin(), ed.end());
  int lst = 0, ans = 1e18;
  S.set(1, n), M.set(n, n), O.set(n, n);
  for (int i = 1; i <= n; ++i) O.a[i][i] = 1;
  S.a[1][1] = 1;
  for (int i = 0; i < m; ++i) {
    auto [w, u, v] = ed[i];
    if (ans < w) break;
    if (w != lst) S = S * qpow(M, w - lst);
    M.a[u][v] = 1, lst = w;
    dijkstra();
    ans = std::min(ans, w + dis[n]);
  }
  if (ans >= 1e15) std::cout << "Impossible\n";
  else std::cout << ans << '\n';
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