---
title: 'CF1149D Abandoning Roads 题解'
date: 2024-04-06 18:43:00
---

## Description

一张 $n$ 个点 $m$ 条边的无向图，只有 $a,b$ 两种边权（$a<b$），对于每个 $i$，求图中所有的最小生成树中，从 $1$ 到 $i$ 距离的最小值。

$2\leq n\leq 70,n-1\leq m\leq 200,1\leq a<b\leq 10^7$。

## Solution

先考虑一个最小生成树是什么样的形态，显然保留边权为 $a$ 的边后形成的连通块和原图保留 $a$ 边的连通块完全相同，并且树中连接连通块之间的边都是 $b$ 边。

所以树上两点的简单路径一定是先走 $a$ 再走 $b$ 再走 $a$，以此类推，并且如果出了一个连通块就不会再回来，容易发现在原图中如果存在一条这样的 $1$ 到 $i$ 的路径，那么在新树中一定也存在。

这样就可以 dp 了，设 $f_{s,i}$ 表示已经出了 $s$ 这个集合的所有连通块，并且当前在 $j$ 的最短路。跑 dijkstra 即可。

时间复杂度：$O(2^nn)$。

考虑优化。

注意到对于一个大小不超过 $3$ 的连通块，如果出了它再走回来一定没有直接走连通块内的边优，所以这些连通块不用记到状态里，则状态数总共就只有 $2^{\frac{n}{4}}$ 个了。

时间复杂度：$O(2^{\frac{n}{4}}n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 75, kMaxS = (1 << 18);

int n, m, a, b, cnt, tot;
int g[kMaxN][kMaxN], id[kMaxN], f[kMaxN][kMaxS];
bool vis[kMaxN];
std::vector<int> vec;

void dfs(int u) {
  vec.emplace_back(u), vis[u] = 1;
  for (int i = 1; i <= n; ++i)
    if (g[u][i] == a && !vis[i])
      dfs(i);
}

void dijkstra() {
  static bool vis[kMaxN][kMaxS] = {0};
  memset(f, 0x3f, sizeof(f));
  std::priority_queue<std::tuple<int, int, int>> q;
  f[1][0] = 0, q.emplace(0, 1, 0);
  for (; !q.empty();) {
    auto [d, i, s] = q.top(); q.pop();
    if (vis[i][s]) continue;
    vis[i][s] = 1;
    for (int j = 1; j <= n; ++j) {
      if (!g[i][j]) continue;
      int t = s;
      if (id[j] < cnt) {
        if (s >> id[j] & 1) continue;
        if (id[j] == id[i]) {
          if (g[i][j] == a && f[j][t] > f[i][s] + g[i][j]) {
            f[j][t] = f[i][s] + g[i][j], q.emplace(-f[j][t], j, t);
          }
        } else {
          if (id[i] < cnt) t |= (1 << id[i]);
          if (f[j][t] > f[i][s] + g[i][j]) {
            f[j][t] = f[i][s] + g[i][j], q.emplace(-f[j][t], j, t);
          }
        }
      } else {
        if (id[j] == id[i]) {
          if (g[i][j] == a && f[j][t] > f[i][s] + g[i][j]) {
            f[j][t] = f[i][s] + g[i][j], q.emplace(-f[j][t], j, t);
          }
        } else {
          if (id[i] < cnt) t |= (1 << id[i]);
          if (f[j][t] > f[i][s] + g[i][j]) {
            f[j][t] = f[i][s] + g[i][j], q.emplace(-f[j][t], j, t);
          }
        }
      }
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m >> a >> b;
  for (int i = 1; i <= m; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    g[u][v] = g[v][u] = w;
  }
  for (int i = 1; i <= n; ++i) {
    if (vis[i]) continue;
    dfs(i);
    if (vec.size() >= 4) {
      for (auto x : vec) id[x] = tot;
      ++cnt, ++tot;
    }
    vec.clear();
  }
  std::fill_n(vis + 1, n, 0);
  for (int i = 1; i <= n; ++i) {
    if (vis[i]) continue;
    dfs(i);
    if (vec.size() <= 3) {
      for (auto x : vec) id[x] = tot;
      ++tot;
    }
    vec.clear();
  }
  dijkstra();
  for (int i = 1; i <= n; ++i)
    std::cout << *std::min_element(f[i], f[i] + (1 << cnt)) << ' ';
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