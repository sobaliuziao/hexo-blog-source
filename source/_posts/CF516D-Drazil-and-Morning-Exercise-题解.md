---
title: CF516D Drazil and Morning Exercise 题解
date: 2024-02-08 22:38:00
---

## Description

- 给定一棵 $n$ 个点的树，边有边权。
- 定义 $f_x = \max_{i=1}^n \text{dist}(x,i)$。
- $q$ 次询问最大的满足 $\max_{x \in s} f_x - \min_{x \in s} f_x \le l$ 的连通块 $s$ 包含的点数。
- $n \le 10^5$，$q \le 50$。

## Solution

这里 $f_u$ 显然可以用换根 dp 求出。

但是直接做很难搞，考虑去思考 $f_u$ 的性质。

有一个结论是 $f_u$ 一定是 $u$ 到直径两端点距离中的一个，证明就考虑反证即可。

有了这个性质，如果把树的中心当作根，那么每个点的 $f$ 一定不小于它父亲的 $f$，所以直接枚举连通块的点，那么满足条件的连通块的根一定是条链，搞个树上差分就行了。

时间复杂度：$O(nq\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

int n, q, l, rt;
int f[kMaxN], g[kMaxN], h[kMaxN][2], d[kMaxN], p[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];
std::vector<int> vec;

void dfs1(int u, int fa) {
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    int val = h[v][0] + w;
    if (val >= h[u][0]) h[u][1] = h[u][0], h[u][0] = val;
    else if (val >= h[u][1]) h[u][1] = val;
  }
}

void dfs2(int u, int fa) {
  f[u] = std::max(g[u], h[u][0]);
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    g[v] = std::max(g[u], h[u][h[v][0] + w == h[u][0]]) + w;
    dfs2(v, u);
  }
}

void dfs3(int u, int fa) {
  p[u] = fa;
  vec.emplace_back(u);
  int L = -1, R = vec.size(), res = vec.size() - 1;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (f[vec[mid]] >= f[u] - l) R = res = mid;
    else L = mid;
  }
  --d[p[vec[res]]], ++d[u];
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    dfs3(v, u);
  }
  vec.pop_back();
}

void dfs4(int u, int fa) {
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    dfs4(v, u);
    d[u] += d[v];
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
  }
  dfs1(1, 0), dfs2(1, 0);
  rt = std::min_element(f + 1, f + 1 + n) - f;
  std::cin >> q;
  for (int cs = 1; cs <= q; ++cs) {
    std::cin >> l;
    std::fill_n(d + 1, n, 0);
    dfs3(rt, 0), dfs4(rt, 0);
    std::cout << *std::max_element(d + 1, d + 1 + n) << '\n';
  }
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