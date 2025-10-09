---
title: P11915 [PA 2025] Teleport 题解
date: 2025-03-26 11:28:00
---

## Description

给定一张 $n$ 个节点的简单无向连通图，边权全为 $1$。

在图中加入一条边权为 $0$ 的边，最小化**加边后**这张图的 $\displaystyle \max_{1\le u,v\le n} \{\operatorname{dist}(u,v)\}$。只需要求出 $\displaystyle \max_{1\le u,v\le n} \{\operatorname{dist}(u,v)\}$ 的最小值。

这里，$\operatorname{dist}(u,v)$ 定义为 $u,v$ 间最短路长度。

$n\leq 400$。

## Solution

首先有个观察是对于如果 $\text{dist}(i,x)\leq\text{dist}(i,y)$，那么走 $i\to y\to x\to j$ 一定没有意义，因为走后面的要么没有 $x\to y$ 优要么不如直接不经过 $(x,y)$。

考虑怎么判断 $ans$ 是否合法。

枚举 $i$，对于所有 $\text{dist}(i,j)>ans$ 的 $(i,j)$，如果满足 $\text{dist}(i,x)\leq\text{dist}(i,y)$ 且 $\text{dist}(i,x)+\text{dist}(y,j)>ans$ 则 $(x,y)$ 不合法。

但是这么做单次是 $O(n^4)$ 的。

考虑对于 $y$ 维护 $mx_{i,y}$ 表示所有必须经过新加入边的 $(i,j)$ 中 $\text{dist}(y,j)$ 的最大值。那么一对 $(x,y)$ 在 $i$ 处不合法就等价于 $\text{dist}(i,x)+mx_{i,y}>ans$。

时间复杂度：$O(n^3\log n)$。

还是过不了。

---

注意到我们只需要判断是否存在**一组**边满足条件，所以考虑从大到小枚举 $ans$，每次同样枚举 $i$，并对于每个 $y$ 维护 $pos_{i,y}$ 表示目前 $\text{dist}(i,x)\leq\text{dist}(i,y)$ 且 $(x,y)$ 还没被删的 $\text{dist}(i,x)$ 最大的 $x$。

加入新边后暴力枚举 $y$ 更新 $pos$ 即可。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 405;

int n, tot;
int dis[kMaxN][kMaxN], pos[kMaxN], pp[kMaxN][kMaxN], mx[kMaxN][kMaxN], id[kMaxN][kMaxN];
bool res[kMaxN][kMaxN];

void del(int x, int y) {
  tot -= res[x][y], res[x][y] = res[y][x] = 0;
}

bool work(int ans) {
  for (int i = 1; i <= n; ++i) {
    for (; pos[i] && dis[i][id[i][pos[i]]] > ans; --pos[i]) {
      int x = id[i][pos[i]];
      for (int j = 1; j <= n; ++j)
          mx[i][j] = std::max(mx[i][j], dis[x][j]);
    }
    for (int j = 1; j <= n; ++j) {
      for (; pp[i][j]; --pp[i][j]) {
        int x = id[i][pp[i][j]];
        if (!res[x][j]) continue;
        if (dis[i][x] + mx[i][j] <= ans) break;
        del(j, x);
      }
      // for (int k = 1; k <= n; ++k)
      //   if (dis[i][k] >= dis[i][j] && dis[i][j] + mx[i][k] > ans)
      //     del(j, k);
    }
  }
  // std::cerr << tot << '\n';
  // if (tot == 2) {
  //   for (int i = 1; i <= n; ++i)
  //     for (int j = 1; j <= n; ++j)
  //       if (res[i][j])
  //         std::cerr << i << ' ' << j << '\n';
  // }
  return tot != 0;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i)
    std::fill_n(dis[i] + 1, n, 1e9), dis[i][i] = 0;
  for (int i = 1; i <= n; ++i) {
    std::string s;
    std::cin >> s;
    for (int j = 1; j <= n; ++j)
      if (s[j - 1] == '1')
        dis[i][j] = 1;
  }
  for (int k = 1; k <= n; ++k)
    for (int i = 1; i <= n; ++i)
      for (int j = 1; j <= n; ++j)
        dis[i][j] = std::min(dis[i][j], dis[i][k] + dis[k][j]);
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) id[i][j] = j;
    std::sort(id[i] + 1, id[i] + 1 + n, [&] (int x, int y) { return dis[i][x] < dis[i][y]; });
    for (int j = 1; j <= n; ++j) pp[i][id[i][j]] = j - 1;
    pos[i] = n;
    std::fill_n(mx[i] + 1, n, -1e9);
    for (int j = i + 1; j <= n; ++j)
      res[i][j] = res[j][i] = 1;
  }
  tot = n * (n - 1) / 2;
  for (int i = n; i; --i) {
    if (!work(i)) return void(std::cout << i + 1 << '\n');
  }
  std::cout << "1\n";
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```