---
title: 'CF1991E Coloring Game 题解'
date: 2024-09-07 14:25:00
---

## Description

有一个由 $n$ 个顶点和 $m$ 条边组成的无向图。每个顶点可以用三种颜色之一着色： $1$ 、 $2$ 或 $3$ 。初始时，所有顶点都未着色。

Alice 和 Bob 正在玩一个包含 $n$ 轮的游戏。在每一轮中，都会发生以下两个步骤：

1. Alice 选择两种**不同**的颜色。
2. Bob 选择一个未着色的结点，并用 Alice 选择的两种颜色之一为其着色。

如果存在连接两个相同颜色结点的边，则 Alice 获胜。否则 Bob 获胜。

给你这个图。您的任务是决定您想扮演哪位玩家并赢得游戏。

## Solution

首先观察样例会发现有奇环时是 Alice 胜，只有一个偶环就是 Bob 胜。

于是可以猜测图不为二分图时 Alice 胜，否则 Bob 胜。

操作就考虑不为二分图时，Alice 只要一直询问 $(1,2)$，Bob 无论怎么放颜色也无法做到让奇环上相邻的点颜色不一样。

图为二分图时，先假设左部点颜色为 $1$，右部点颜色为 $2$。Alice 每次询问 $(x,y)$ 时，如果 $x$ 和 $y$ 中有至少一个满足小于等于 $2$ 且其在原图中对应的左部/右部点没染完，就染那个满足条件的颜色。

否则一定满足左部/右部点中有至少一边被染完了，且询问的为被染完的颜色和 $3$。这样只需要让被染完的那边染 $3$ 即可。

时间复杂度：$O(n+m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e4 + 5;

int n, m;
int col[kMaxN];
bool fl = 1;
std::vector<int> G[kMaxN], id[2];

void dfs(int u) {
  id[col[u] - 1].emplace_back(u);
  for (auto v : G[u]) {
    if (!col[v]) {
      col[v] = 3 - col[u];
      dfs(v);
    } else if (col[v] == col[u]) {
      fl = 0;
    }
  }
}

bool check() {
  fl = 1, id[0].clear(), id[1].clear();
  for (int i = 1; i <= n; ++i) {
    if (!col[i]) {
      col[i] = 1, dfs(i);
    }
  }
  return fl;
}

void dickdreamer() {
  for (int i = 1; i <= n; ++i) G[i].clear(), col[i] = 0;
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  if (!check()) {
    std::cout << "Alice" << std::endl;
    for (int i = 1; i <= n; ++i) {
      std::cout << "1 2" << std::endl;
      int x, y;
      std::cin >> x >> y;
    }
  } else {
    std::cout << "Bob" << std::endl;
    for (int i = 1; i <= n; ++i) {
      int x, y;
      std::cin >> x >> y;
      if (x > y) std::swap(x, y);
      if (x <= 2 && id[x - 1].size()) {
        std::cout << id[x - 1].back() << ' ' << x << std::endl;
        id[x - 1].pop_back();
      } else if (y <= 2 && id[y - 1].size()) {
        std::cout << id[y - 1].back() << ' ' << y << std::endl;
        id[y - 1].pop_back();
      } else {
        std::cout << id[2 - x].back() << ' ' << y << std::endl;
        id[2 - x].pop_back();
      }
    }
  }
}

int32_t main() {
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```