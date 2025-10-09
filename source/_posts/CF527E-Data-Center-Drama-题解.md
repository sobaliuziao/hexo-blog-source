---
title: CF527E Data Center Drama 题解
date: 2024-07-24 09:51:00
---

## Description

- 给定一张 $n$ 个点 $m$ 条边的连通无向图。
- 你需要加尽可能少的边，然后给所有边定向，使得每一个点的出入度都是偶数。
- 边可以是自环，也可以有重边。
- $n \le 10^5$，$m \le 2 \times 10^5$。

## Solution

看到定向考虑欧拉回路。

注意到题目里每个点出入度都是偶数说明定向前每个点的度数均为偶数，正好符合欧拉回路的条件。

那么先把度数为奇数的点拿出来，相邻两个连边就让每个点度数为偶数了。

但是这里还需满足每个点出入度都是偶数，所以总边数也应为偶数，如果为奇数就随便找个点连自环即可。

定向就考虑在欧拉回路上交错定向，类似：$v_1\rightarrow v_2\leftarrow v_3\rightarrow v_4\leftarrow v_5\ldots$。

容易发现这样的定向方案合法且添加的边数最少。

时间复杂度：$O(n+m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, m;
int cur[kMaxN];
bool vis[kMaxN * 2];
std::vector<int> path;
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u) {
  for (int i = cur[u]; i < (int)G[u].size(); i = cur[u]) {
    cur[u] = i + 1;
    auto [v, id] = G[u][i];
    if (vis[id]) continue;
    vis[id] = 1;
    dfs(v);
  }
  if (path.size()) {
    if (path.size() & 1) std::cout << path.back() << ' ' << u << '\n';
    else std::cout << u << ' ' << path.back() << '\n';
  }
  path.emplace_back(u);
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v, i), G[v].emplace_back(u, i);
  }
  std::vector<int> v;
  for (int i = 1; i <= n; ++i)
    if (G[i].size() & 1)
      v.emplace_back(i);
  for (int i = 0; i + 1 < v.size(); i += 2)
    ++m, G[v[i]].emplace_back(v[i + 1], m), G[v[i + 1]].emplace_back(v[i], m);
  if (m & 1) G[1].emplace_back(1, ++m), G[1].emplace_back(1, m);
  std::cout << m << '\n';
  dfs(1);
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