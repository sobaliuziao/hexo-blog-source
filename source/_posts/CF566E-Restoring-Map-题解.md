---
title: CF566E Restoring Map 题解
date: 2024-08-04 17:22:00
---

## Description

有一棵 $n$ 个点的树，你不知道这棵树的边是怎么连的。

你得到了 $n$ 条关于每个点信息，每条信息记录了距离某一个点 $\le 2$ 的所有点。

但你不知道每条信息具体是哪个点的。

你需要构造一棵满足这些信息的树。

$n \le 10^3$。

## Solution

首先可以发现如果存在一条路径 $x-u-v-y$，那么 $x,y$ 的信息求个交一定是 $\left\{u,v\right\}$，可以证明所有的非叶子节点之间的连边一定可以通过这种方式构造出来。

然后就只要考虑叶子节点选哪个非叶子节点做父亲了。

---

注意到非叶子节点很少的时候会比较特殊，考虑单独处理，下面先考虑非叶子节点个数 $\geq 3$ 的情况。


不妨设 $T_x$ 表示距离 $x$ 不超过 $1$ 的非叶子节点构成的集合，由于非叶子节点个数 $\geq 3$，所以 $T_x$ 互不相同。

考虑对于一个叶子 $x$，设其父亲为 $y$，则距离 $x$ 不超过 $2$ 的点构成的集合一定是 $x$ 所在的集合中最小的那个，这个容易求出来。

这时候会发现如果把 $s_x$ 中所有的叶子节点去掉后，$s_x$ 就等于 $T_y$。由于 $T_y$ 互不相同，所以暴力枚举 $y$ 即可。

---

然后考虑特殊情况。

如果没有非叶子节点，说明 $n=2$，直接输出。如果只有 $1$ 个，说明原图是个菊花图，直接输出。

如果有 $2$ 个，那么一定只有两种不同的大小不为 $n$ 的集合，对于这两种集合一种连左边的非叶子即可，另一种连另一个非叶子节点即可。

注意到直接做是 $O(n^3)$，可以用 bitset 优化上面的求交和判相等，就可以除掉一个 $\omega$ 了。

时间复杂度：$O\left(\frac{n^3}{\omega}\right)$

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e3 + 5;

int n;
bool isleaf[kMaxN];
std::bitset<kMaxN> a[kMaxN], b[kMaxN], g[kMaxN], tmp;
std::vector<int> vec[kMaxN];
std::vector<std::pair<int, int>> ed;

void dickdreamer() {
  std::cin >> n;
  bool fl = 1;
  for (int i = 1; i <= n; ++i) {
    int k, x;
    std::cin >> k;
    fl &= (k == n);
    for (int j = 1; j <= k; ++j) {
      std::cin >> x;
      a[i][x] = 1, vec[x].emplace_back(i);
    }
  }
  if (fl == 1) {
    for (int i = 2; i <= n; ++i) std::cout << 1 << ' ' << i << '\n';
    return;
  }
  std::fill_n(isleaf + 1, n, 1);
  for (int i = 1; i <= n; ++i) {
    for (int j = i + 1; j <= n; ++j) {
      tmp = (a[i] & a[j]);
      if (tmp.count() != 2) continue;
      int u = tmp._Find_first(), v = tmp._Find_next(u);
      g[u][v] = g[v][u] = 1, isleaf[u] = isleaf[v] = 0;
      ed.emplace_back(u, v);
    }
  }
  int cnt = 0;
  for (int i = 1; i <= n; ++i) cnt += (!isleaf[i]);
  if (cnt == 2) {
    auto [u1, v1] = ed[0];
    int id1 = 0, id2 = 0;
    for (int i = 1; i <= n; ++i) {
      if (a[i].count() == n) continue;
      if (!id1) {
        id1 = i;
        for (int j = 1; j <= n; ++j)
          if (isleaf[j] && a[i][j]) ed.emplace_back(j, u1);
      } else if (a[i] != a[id1]) {
        id2 = i;
        for (int j = 1; j <= n; ++j)
          if (isleaf[j] && a[i][j]) ed.emplace_back(j, v1);
      }
      if (id1 && id2) break;
    }
  } else {
    std::vector<int> notleaf;
    for (int i = 1; i <= n; ++i) {
      if (!isleaf[i]) {
        notleaf.emplace_back(i);
        g[i][i] = 1;
      }
    }
    for (int i = 1; i <= n; ++i)
      for (int j = 1; j <= n; ++j) b[i][j] = (a[i][j] & (!isleaf[j]));
    for (int i = 1; i <= n; ++i) {
      if (!isleaf[i]) continue;
      int id = 0;
      for (auto j : vec[i])
        if (!id || a[j].count() < a[id].count()) id = j;
      for (auto j : notleaf)
        if (b[id] == g[j]) ed.emplace_back(i, j);
    }
  }
  std::sort(ed.begin(), ed.end()),
      ed.erase(std::unique(ed.begin(), ed.end()), ed.end());
  for (auto [u, v] : ed) std::cout << u << ' ' << v << '\n';
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