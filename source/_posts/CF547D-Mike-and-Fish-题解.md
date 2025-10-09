---
title: 'CF547D Mike and Fish 题解'
date: 2024-07-24 11:30:00
---

## Description

- 给定 $n$ 个整点。
- 你要给每个点染成红色或蓝色。
- 要求同一水平线或垂直线上两种颜色的数量最多相差 $1$。
- $n,x_i, y_i \le 2 \times 10^5$。

## Solution

考虑给每条水平线和垂直线建一个点，对于每个整点就把它对应的两条线连一条边。

题目就转化为了给每条边定向，使得每个点入度和出度不超过 $1$。这是个经典的问题，由于度数为奇数的点只有偶数个，所以新建一个点和这个奇度数的点连边，然后跑欧拉回路定向即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 6e5 + 5;

int n;
int x[kMaxN], y[kMaxN], ans[kMaxN], cur[kMaxN];
bool vis[kMaxN], vx[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u) {
  vx[u] = 1;
  for (int i = cur[u]; i < (int)G[u].size(); i = cur[u]) {
    auto [v, id] = G[u][i];
    cur[u] = i + 1;
    if (vis[id]) continue;
    vis[id] = 1;
    dfs(v);
    if (u >= 1 && u <= 2e5 && v > 2e5) ans[id] = 0;
    else if (v >= 1 && v <= 2e5 && u > 2e5) ans[id] = 1;
    else assert(!u || !v);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> x[i] >> y[i];
    G[x[i]].emplace_back(y[i] + (int)2e5, i), G[y[i] + (int)2e5].emplace_back(x[i], i);
  }
  int tmp = n;
  for (int i = 1; i <= 4e5; ++i)
    if (G[i].size() & 1)
      G[0].emplace_back(i, ++tmp), G[i].emplace_back(0, tmp);
  for (int i = 0; i <= 4e5; ++i) dfs(i);
  for (int i = 1; i <= n; ++i)
    std::cout << (ans[i] ? 'r' : 'b');
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