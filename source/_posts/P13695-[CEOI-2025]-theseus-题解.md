---
title: 'P13695 [CEOI 2025] theseus 题解'
date: 2025-09-16 17:16:00
---

## Description

当不在思考这些抽象哲学问题时，忒修斯会在闲暇时猎杀弥诺陶洛斯。但这一次，他必须先穿过一个黑暗而扭曲的迷宫。由于这并非易事，他请求阿里阿德涅为他引路。这个迷宫可以看作是一个连通的无向图，包含 $n$ 个节点（编号 $1$ 到 $n$）和 $m$ 条边，并且有一个特殊节点 $t$，弥诺陶洛斯就在这里。

忒修斯完全看不到图的全貌，但阿里阿德涅可以。两人会先商定一个策略，使他能安全到达弥诺陶洛斯所在的节点：阿里阿德涅会在 $m$ 条边的每一条上贴上 $0$ 或 $1$ 的标签。之后，忒修斯会从某个节点 $s$ 进入迷宫，而阿里阿德涅事先并不知道 $s$ 的位置。

由于迷宫极为黑暗，任何时刻他只能看到当前所在节点的编号、相邻节点的编号以及相邻边的标签。此外，由于迷宫结构扭曲，他**永远无法记住**自己之前到过的节点的任何信息。

为了安全到达弥诺陶洛斯，忒修斯必须在不超过 $\min+C$ 次移动内完成，其中 $\min$ 是从 $s$ 到 $t$ 的最短路径上的边数，$C$ 是一个常数。

$1 \leq n \leq 10000,1 \leq m \leq 50000,C = 14$。

## Solution

首先如果知道边的两端点 $u,v$ 和边权 $w$ 后，我们可以把它看成一条有向边，即如果 $w=0$，则方向为 $\min(u,v)\to\max(u,v)$，否则 $\max(u,v)\to\min(u,v)$。

那么我们求出 $dis_i$ 表示 $i\to t$ 的最短路长度。然后对于每条无向边 $u,v$，如果 $dis_u\neq dis_v$，则让大的指向小的，否则让编号大的指向编号小的。

这是个答案正确的做法，但是最劣的步数是 $\min$ 加上所有层点数减一的和，过不了。

由于层与层之间的边是必须要走的，所以这里要控制层内走的总边数在 $\log n$ 范围内。

---

考虑利用启发式合并的思想，给每个点一个点权 $a_i$，初始为 $1$，每次如果确定了一条边的方向 $u\to v$ 后，就让 $a_v\leftarrow a_v+a_u,a_u\leftarrow 0$。

具体地，如果一条边 $(u,v)$ 是层与层之间的边，则把其挂在层数较深的点上。否则挂在编号较大的点上。

然后从深往浅去枚举每一层，对于层内按照编号从大到小枚举每个点和挂在它上面的边，边的另一端也是从大到小枚举。

如果两端点层数不同，则层数深的指向浅的，并更新点权。如果层数相同，则点权小的指向点权大的，并更新点权。

走的时候每次走 $u$ 的出边编号最大的点即可，这么做至多走 $\min+\log n$ 步。

证明就考虑每次走出去的出边一定是第一次让 $u$ 的点权变为 $0$ 的边，层内的排序保证了这一点。不妨设 $b_i$ 为 $i$ 达到过的最大点权，那么 $u$ 对于走出去的点 $v$，如果是层与层之间的边，则 $b_v\geq b_u$；如果是层内的边，则 $b_v\geq 2b_u$，这样的边最多走 $\log n$ 次。

总步数也就是 $\min+\log n$。

## Code

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include "grader.cpp"
#endif

const int kMaxN = 1e4 + 5;

int n, dep[kMaxN], val[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];
std::vector<int> id[kMaxN];

void dijkstra(int s) {
  static bool vis[kMaxN] = {0};
  std::priority_queue<std::pair<int, int>> q;
  for (int i = 1; i <= n; ++i) dep[i] = 1e9;
  q.emplace(dep[s] = 0, s);
  for (; !q.empty();) {
    int u = q.top().second; q.pop();
    if (vis[u]) continue;
    vis[u] = 1;
    for (auto [v, id] : G[u]) {
      if (dep[v] > dep[u] + 1) {
        dep[v] = dep[u] + 1, q.emplace(-dep[v], v);
      }
    }
  }
}

int geted(int u, int v) { // u -> v
  for (int i = 0; i <= 19; ++i) {
    if ((u ^ v) >> i & 1) return v >> i & 1;
  }
  return -1;
}

std::vector<int> paint(int n, std::vector<std::pair<int, int>> edges, int t) {
  ::n = n;
  int m = edges.size();
  std::vector<int> colors(m);
  for (int i = 0; i < m; ++i) {
    auto [u, v] = edges[i];
    G[u].emplace_back(v, i), G[v].emplace_back(u, i);
  }
  dijkstra(t);
  for (int i = 1; i <= n; ++i) {
    id[dep[i]].emplace_back(i), val[i] = 1;
    std::sort(G[i].begin(), G[i].end(), std::greater<>());
  }
  for (int d = n; d; --d) {
    std::sort(id[d].begin(), id[d].end(), std::greater<>());
    for (auto u : id[d]) {
      for (auto [v, id] : G[u]) {
        if (dep[v] < dep[u]) {
          colors[id] = geted(u, v), val[v] += val[u], val[u] = 0;
        } else if (dep[v] == dep[u]) {
          if (val[u] <= val[v]) colors[id] = geted(u, v), val[v] += val[u], val[u] = 0;
          else colors[id] = geted(v, u), val[u] += val[v], val[v] = 0;
        }
      }
    }
  }
  return colors;
}

int travel(int n, int u, std::vector<std::pair<int, int>> neighbours) {
  int nxt = 0;
  for (auto [v, w] : neighbours) {
    if (geted(u, v) == w) nxt = std::max(nxt, v);
  }
  return nxt;
}
```