---
title: P3547 [POI2013] CEN-Price List 题解
date: 2024-08-24 20:03:00
---

## Description

给定一个 $n$ 个点 $m$ 条边的无向图，边权均为 $a$。

现在将原来图中满足最短路等于 $2a$ 所有的点对 $(x,y)$ 之间加一条长度为 $b$ 的无向边。

给定 $k$，求点 $k$ 到所有点的最短路是多少。

$1\leq n,m\leq 10^5$。

## Solution

首先有个显然的结论是对于所有加边前 $k\to i$ 的最短路 $p_1(k)\to p_2\to\dots\to p_{m}(1)$，对于 $\forall 1\leq i\leq m-2$，一定满足 $p_i$ 和 $p_{i+2}$ 没有连边，否则最短路一定会更短。

那么加边之后的最短路就只有三种了：全 $a$；前面一堆 $a$ 加 $0/1$ 个 $b$；全 $b$。

对于前两种情况可以直接在原图上跑 bfs 求出。

考虑怎么做全 $b$ 的情况。

有一种暴力也是 bfs，每次转移就暴力枚举所有 $u\to v\to w$，满足 $(u,w)$ 没有边然后让 $dis_w\leftarrow dis_u+1$。

但是这样做是 $O(m^2)$ 的。

注意到对于一个转移 $u\to v\to w$ 如果 $(u,w)$ 没有边，那么这次转移后 $(v,w)$ 这条边就再也无法作为转移的第二条边进行成功的转移，可以直接删掉。

然后会发现如果 $u,v,w$ 不构成三元环则每次枚举必然会删掉至少一条边。如果构成三元环，由于三元环个数是 $O(m\sqrt m)$ 级别的，而每个三元环只会遍历 $O(1)$ 次，所以复杂度是 $O(m\sqrt m)$ 的。

时间复杂度：$O(m\sqrt m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, m, s, A, B;
int ans[kMaxN];
std::vector<int> G[kMaxN], _G[kMaxN];

void del(std::vector<int> &vec, int p) {
  std::swap(vec[p], vec[(int)vec.size() - 1]);
  vec.pop_back();
}

void bfs1() {
  static int dis[kMaxN];
  static bool vis[kMaxN];
  std::queue<int> q;
  q.emplace(s), dis[s] = 0, vis[s] = 1;
  for (; !q.empty();) {
    int u = q.front(); q.pop();
    for (auto v : G[u]) {
      if (!vis[v]) {
        dis[v] = dis[u] + 1, vis[v] = 1, q.emplace(v);
      }
    }
  }
  for (int i = 1; i <= n; ++i)
    ans[i] = std::min(dis[i] * A, (dis[i] / 2) * B + (dis[i] % 2) * A);
}

void bfs2() {
  static int dis[kMaxN];
  static bool vis[kMaxN], have[kMaxN];
  std::queue<int> q;
  q.emplace(s), dis[s] = 0, vis[s] = 1;
  for (; !q.empty();) {
    int u = q.front(); q.pop();
    for (auto v : G[u]) have[v] = 1;
    for (auto v : G[u]) {
      std::vector<int> vec;
      for (int i = 0; i < (int)_G[v].size(); ++i) {
        int w = _G[v][i];
        if (w != u && !have[w]) {
          if (!vis[w]) dis[w] = dis[u] + 1, vis[w] = 1, q.emplace(w);
          vec.emplace_back(i);
        }
      }
      for (auto p : vec) {
        del(_G[v], p);
      }
    }
    for (auto v : G[u]) have[v] = 0;
  }
  for (int i = 1; i <= n; ++i)
    if (vis[i])
      ans[i] = std::min(ans[i], dis[i] * B);
}

void dickdreamer() {
  std::cin >> n >> m >> s >> A >> B;
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
    _G[u].emplace_back(v), _G[v].emplace_back(u);
  }
  memset(ans, 0x3f, sizeof(ans));
  bfs1(), bfs2();
  for (int i = 1; i <= n; ++i) std::cout << ans[i] << '\n';
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