---
title: 'CF715B Complete The Graph 题解'
date: 2024-11-18 20:11:00
---

## Description

给 $n$ 点 $m$ 边的无向图，$L$，$s$，$t$。

修改 $m$ 条边中边为 $0$ 的边，使满足 $s,t$ 的最短路长度是 $L$，且输出答案的时候边为 $0$ 的边的权值必须在 $[1,10^{18}]$ 内。

## Solution

考虑怎么判有无解。

容易发现将所有未知边边权设为 $10^{18}$，如果最短路小于 $L$，或者未知边设为 $1$ 后最短路大于 $L$ 时无解，否则有解。因为每次只将一条边的长度加 $1$ 后最短路至多增加 $1$。

不妨设 $dis_i$ 表示 $i$ 在未知边边权为 $1$ 时与 $s$ 的距离，$det$ 表示 $L-dis_t$。容易发现我们的任务就是让 $dis_t$ 增加 $det$。

考虑再进行一次 dijkstra，如果当前松弛的边 $(u,v,w)$ 满足 $dis_{v}+det>dis^{'}_{u}+w$ 且这条边未确定，就将 $w$ 调整为 $dis_{v}+det-dis^{'}_u$，这样的话每个点的最短路一定不会增加超过 $det$，且 $dis_t$ 一定能增加 $det$。

时间复杂度：$O((n+m)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e3 + 5, kMaxM = 1e4 + 5;

int n, m, L, s, t, det;
int u[kMaxM], v[kMaxM], w[kMaxM];
int dis1[kMaxN], dis2[kMaxN];
bool del[kMaxM];
std::vector<std::tuple<int, int, int>> G[kMaxN];

int dijkstra1(int *dis) {
  static bool vis[kMaxN];
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (int i = 1; i <= m; ++i) {
    if (w[i]) {
      G[u[i]].emplace_back(v[i], w[i], i), G[v[i]].emplace_back(u[i], w[i], i);
    }
  }
  for (int i = 1; i <= n; ++i) {
    dis[i] = 1e18, vis[i] = 0;
  }
  std::priority_queue<std::pair<int, int>> q;
  q.emplace(0, s), dis[s] = 0;
  for (; !q.empty();) {
    int u = q.top().second; q.pop();
    if (vis[u]) continue;
    vis[u] = 1;
    for (auto [v, w, id] : G[u]) {
      if (dis[v] > dis[u] + w) {
        dis[v] = dis[u] + w;
        q.emplace(-dis[v], v);
      }
    }
  }
  return dis[t];
}

int dijkstra2(int *dis) {
  static bool vis[kMaxN];
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (int i = 1; i <= m; ++i) {
    if (w[i]) {
      G[u[i]].emplace_back(v[i], w[i], i), G[v[i]].emplace_back(u[i], w[i], i);
    }
  }
  for (int i = 1; i <= n; ++i) {
    dis[i] = 1e18, vis[i] = 0;
  }
  std::priority_queue<std::pair<int, int>> q;
  q.emplace(0, s), dis[s] = 0;
  for (; !q.empty();) {
    int u = q.top().second; q.pop();
    if (vis[u]) continue;
    vis[u] = 1;
    for (auto [v, w, id] : G[u]) {
      if (del[id] && dis1[v] + det > dis[u] + ::w[id])
        ::w[id] = dis1[v] + det - dis[u];
      if (dis[v] > dis[u] + ::w[id]) {
        dis[v] = dis[u] + ::w[id];
        q.emplace(-dis[v], v);
      }
    }
  }
  return dis[t];
}

void print() {
  std::cout << "YES\n";
  for (int i = 1; i <= m; ++i)
    std::cout << u[i] - 1 << ' ' << v[i] - 1 << ' ' << w[i] << '\n';
}

void dickdreamer() {
  std::cin >> n >> m >> L >> s >> t;
  ++s, ++t;
  for (int i = 1; i <= m; ++i) {
    std::cin >> u[i] >> v[i] >> w[i];
    ++u[i], ++v[i];
    if (!w[i]) del[i] = 1, w[i] = 1e18;
  }
  int dis = dijkstra1(dis1);
  if (dis < L) return void(std::cout << "NO\n");
  if (dis == L) return print();
  for (int i = 1; i <= m; ++i)
    if (del[i])
      w[i] = 1;
  int now = dijkstra1(dis1);
  if (now > L) return void(std::cout << "NO\n");
  det = L - now;
  dijkstra2(dis2);
  print();
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