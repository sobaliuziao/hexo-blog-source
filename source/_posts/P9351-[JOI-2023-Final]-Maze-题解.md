---
title: P9351 [JOI 2023 Final] Maze 题解
date: 2024-10-18 10:51:00
---

## Description

给定一张 $R\times C$ 的地图，其中 ```.``` 可以走，而 ```#``` 不能走。一次操作可以将 $N \times N$ 的正方形范围内所有点变成 ```.```，给定起点和终点，求最少需要几次操作使得起点和终点连通（只能上下左右移动）。

$R\times C\le 6\times 10^6$，$N\le R\le C$。

## Solution

先考虑怎么暴力求出答案。

假设当前从起点走到了 $(x,y)$，那么 $(x,y)$ 此时一定为白点，下一步可以花 $0$ 的代价走到一个初始就是白色的点。

或者花费 $1$ 的代价在 $(x,y)$ 周围涂白一个大小为 $N$ 的正方形并走到这个正方形里的任何一个点 $(x_0,y_0)$，容易发现 $(x,y)$ 能走到 $(x_0,y_0)$ 当且仅当 $|x-x_0|,|y-y_0|\leq N$ 且 $\min\left\{|x-x_0|,|y-y_0|\right\}\leq N-1$。

建图跑 01bfs 可以得到一个 $O(RCN^2)$ 的做法。过不了。

由于算法慢在二操作的边数过多，所以考虑把二操作的长距离走法优化成多次走相邻格子的过程。

因为 $(x,y)$ 能走到 $(x_0,y_0)$ 当且仅当 $|x-x_0|,|y-y_0|\leq N$ 且 $\min\left\{|x-x_0|,|y-y_0|\right\}\leq N-1$，所以 $(x,y)\to (x_0,y_0)$ 可以看成先走到四联通格子，再走至多 $N-1$ 步八联通。

于是把步数作为第一关键字，走的八联通步数看作第二关键字跑最短路即可。

dijkstra 直接做可以做到 $O(RC\log RC)$，但是可能能用 01bfs 做到 $O(RC)$。

时间复杂度：$O(RC\log RC)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxT = 6e6 + 5, kMaxN = 3e3 + 5;
const int kD4[][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
const int kD8[][2] = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}, {0, 1}, {0, -1}, {1, 0}, {-1, 0}};

int n, m, k;
int sx, sy, tx, ty;
std::vector<int> G[kMaxT];
std::string s[kMaxN];

void dijkstra() {
  std::vector<std::vector<std::pair<int, int>>> dis(n + 1, std::vector<std::pair<int, int>>(m + 1));
  std::vector<std::vector<bool>> vis(n + 1, std::vector<bool>(m + 1));
  std::priority_queue<std::tuple<int, int, int, int>> q;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= m; ++j)
      dis[i][j] = {1e9, 1e9};
  dis[sx][sy] = {0, k - 1};
  q.emplace(0, -(k - 1), sx, sy);
  for (; !q.empty();) {
    auto [d, w, x, y] = q.top();
    q.pop();
    if (vis[x][y]) continue;
    vis[x][y] = 1;
    for (auto [dx, dy] : kD4) {
      int tx = x + dx, ty = y + dy;
      if (tx < 1 || tx > n || ty < 1 || ty > m) continue;
      if (s[tx][ty] == '.') {
        std::pair<int, int> p = {dis[x][y].first, k - 1};
        if (dis[tx][ty] > p) {
          dis[tx][ty] = p;
          q.emplace(-p.first, -p.second, tx, ty);
        }
      }
      std::pair<int, int> p = {dis[x][y].first + 1, 0};
      if (dis[tx][ty] > p) {
        dis[tx][ty] = p;
        q.emplace(-p.first, -p.second, tx, ty);
      }
    }
    if (dis[x][y].second < k - 1) {
      for (auto [dx, dy] : kD8) {
        int tx = x + dx, ty = y + dy;
        if (tx < 1 || tx > n || ty < 1 || ty > m) continue;
        std::pair<int, int> p = {dis[x][y].first, dis[x][y].second + 1};
        if (dis[tx][ty] > p) {
          dis[tx][ty] = p;
          q.emplace(-p.first, -p.second, tx, ty);
        }
      }
    }
  }
  std::cout << dis[tx][ty].first << '\n';
}

void dickdreamer() {
  std::cin >> n >> m >> k >> sx >> sy >> tx >> ty;
  for (int i = 1; i <= n; ++i) {
    std::cin >> s[i];
    s[i] = " " + s[i];
  }
  dijkstra();
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