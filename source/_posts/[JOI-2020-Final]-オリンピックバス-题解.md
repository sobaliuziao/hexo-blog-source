---
title: '[JOI 2020 Final] オリンピックバス 题解'
date: 2022-10-07 21:53:00
---

## Description

[link](https://www.luogu.com.cn/problem/P6880)

## Solution

可以发现 $m\leq 5\times 10^4$ 所以可以直接枚举 $m$ 来得到答案。

可以建 $4$ 个图，两个正图，两个反图，分别是求 $1\to i$ 的最短路，$i\to n$ 的最短路，$n\to i$ 的最短路，$i\to 1$ 的最短路。

先对于每个图跑最短路并求出最短路径树。

如果当前反转的边是 $(u,v)$，如果这条边在四个图中都不是最短路径树上的边那么翻转当前边对最短路没有影响，否则就把这条边反转后跑最短路，最后取 $\min$ 即可。

由于最短路径树上的边最多 $4(n-1)$ 条，所以最多跑 $4\times n$ 次最短路，所以时间复杂度为 $O(n^3)$。（这里是稠密图，所以直接不加堆优化的 dijkstra 就行）

## Code

<details>
<summary>代码</summary>

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include <debug.h>
#else
#define debug(...) 1
#endif

#define int long long
#define file(s) freopen(s".in", "r", stdin), freopen(s".out", "w", stdout)

using namespace std;

int read() {
  int x = 0, f = 0; char ch = getchar();
  while (ch < '0' || ch > '9') f |= ch == '-', ch = getchar();
  while (ch >= '0' && ch <= '9') x = (x * 10) + (ch ^ 48), ch = getchar();
  return f ? -x : x;
}

typedef long long ll;

const int kMaxN = 205, kMaxM = 5e4 + 5;
const ll kInf = 1e18;

int n, m;
int u[kMaxM], v[kMaxM], w[kMaxM], d[kMaxM];

struct Graph {
  struct Node {
    int v; ll w; int id;

    Node() {}
    Node(int _v, ll _w, int _id) : v(_v), w(_w), id(_id) {}
    ~Node() {}
  };

  vector<Node> G[kMaxN];
  int s, rv;
  ll dis1[kMaxN], dis2[kMaxN], ed[kMaxN];
  bool vis[kMaxN], tr[kMaxM];

  void addE(int u, int v, int w, int id) {
    G[u].emplace_back(v, w, id);
  }
  void dijkstra1() {
    fill(dis1, dis1 + 1 + n, kInf), fill(vis, vis + 1 + n, 0);
    dis1[s] = 0;
    for (int i = 1; i <= n; ++i) {
      int u = 0;
      for (int j = 1; j <= n; ++j) {
        if (!vis[j] && dis1[j] < dis1[u]) {
          u = j;
        }
      }
      if (!u) break ;
      vis[u] = 1;
      for (auto [v, w, id] : G[u]) {
        if (dis1[v] > dis1[u] + w) {
          dis1[v] = dis1[u] + w, ed[v] = id;
        }
      }
    }
    for (int i = 1; i <= n; ++i) {
      if (i != s && dis1[i] != kInf) tr[ed[i]] = 1;
    }
  }
  void dijkstra2() {
    fill(dis2, dis2 + 1 + n, kInf), fill(vis, vis + 1 + n, 0);
    dis2[s] = 0;
    for (int i = 1; i <= n; ++i) {
      int u = 0;
      for (int j = 1; j <= n; ++j) {
        if (!vis[j] && dis2[j] < dis2[u]) {
          u = j;
        }
      }
      if (!u) break ;
      vis[u] = 1;
      for (auto [v, w, id] : G[u]) {
        if (id == rv) continue ;
        if (dis2[v] > dis2[u] + w) {
          dis2[v] = dis2[u] + w;
        }
      }
    }
  }

  ll solve(int t, int rev) {
    if (!tr[rev]) return dis1[t];
    rv = rev;
    dijkstra2();
    return dis2[t];
  }

} g1, g2, g3, g4; // g1, g3 正图， g2, g4 反图

signed main() {
  n = read(), m = read();
  g1.s = 1, g2.s = n, g3.s = n, g4.s = 1;
  for (int i = 1; i <= m; ++i) {
    u[i] = read(), v[i] = read(), w[i] = read(), d[i] = read();
    g1.addE(u[i], v[i], w[i], i), g3.addE(u[i], v[i], w[i], i);
    g2.addE(v[i], u[i], w[i], i), g4.addE(v[i], u[i], w[i], i);
  }
  g1.dijkstra1(), g2.dijkstra1(), g3.dijkstra1(), g4.dijkstra1();
  ll ans = g1.dis1[n] + g3.dis1[1];
  for (int i = 1; i <= m; ++i) {
    ll dis1 = min(g1.solve(n, i), g1.solve(v[i], i) + w[i] + g2.solve(u[i], i)),
       dis2 = min(g3.solve(1, i), g3.solve(v[i], i) + w[i] + g4.solve(u[i], i));
    ans = min(ans, dis1 + dis2 + d[i]);
  }
  if (ans >= kInf) ans = -1;
  cout << ans << endl;
  return 0;
}
```

</details>