---
title: 'P4183 [USACO18JAN] Cow at Large P 题解'
date: 2024-02-10 23:13:00
---

## Description

贝茜被农民们逼进了一个偏僻的农场。农场可视为一棵有 $N$   个结点的树，结点分别编号为 $1,2,\ldots, N$  。每个叶子结点都是出入口。开始时，每个出入口都可以放一个农民（也可以不放）。每个时刻，贝茜和农民都可以移动到相邻的一个结点。如果某一时刻农民与贝茜相遇了（在边上或点上均算），则贝茜将被抓住。抓捕过程中，农民们与贝茜均知道对方在哪个结点。

请问：对于结点 $i\,(1\le i\le N)$  ，如果开始时贝茜在该结点，最少有多少农民，她才会被抓住。

$2\leq N\leq 7\times 10^4$。

## Solution

先考虑固定起点怎么做。

首先每个叶子一定是每次往父亲跳，那么设 $len_i$ 表示 $i$ 到 $i$ 子树里叶子的最短距离。

那么如果 $len_i>dis_i$，则无论 $i$ 的子树怎么放都无法在 $i$ 点拦截贝茜。否则只要在离 $i$ 最近的点放一个奶牛就能在 $i$ 点拦截且贝茜不可能走到 $i$ 子树里的其他点。

容易发现这些放的奶牛是不重的。

所以答案就是所有 $len_i\leq dis_i$ 且 $len_{fa_{i}}>dis_{fa_i}$ 的 $i$ 的个数。

这样做是 $O(n^2)$ 的。

---

考虑优化。

继续固定起点。容易发现这个题目等价于问有多少个子树，子树的根 $i$ 满足 $len_i\leq dis_i$ 且 $len_{fa_{i}}>dis_{fa_i}$。

设 $deg_i$ 表示 $i$ 的度数。

则对于一个大小为 $m$ 的子树 $S$，且子树的根不为原树的根，那么 $\sum_{u\in S}{deg_u}=2m-1$，转化一下就是：$\sum_{u\in S}{(2-deg_u)}=1$。

所以这个子树的价值可以换为子树里 $(2-deg_i)$ 的和。

又注意到如果子树的根 $r$ 满足 $len_r\leq dis_r$ 那么整个子树都满足这个条件。

所以整个树的答案就是：$\sum_{i=1}^{n}{[len_i\leq dis_i]\times (2-deg_i)}$。

然后把这个式子用点分治做即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 7e4 + 5;

int n, rt;
int ans[kMaxN], f[kMaxN], deg[kMaxN], sz[kMaxN], mx[kMaxN];
bool del[kMaxN];
std::vector<std::pair<int, int>> vec;
std::vector<int> G[kMaxN];

struct BIT {
  int c[kMaxN * 2];

  void upd(int x, int v) {
    x += n + 1;
    for (; x <= 2 * n + 1; x += x & -x) c[x] += v;
  }

  int qry(int x) {
    x += n + 1;
    int ret = 0;
    for (; x; x -= x & -x) ret += c[x];
    return ret;
  }
  int qry(int l, int r) { return qry(r) - qry(l - 1); }
} bit;

void pre_dfs1(int u, int fa) {
  if (G[u].size() == 1) f[u] = 0;
  else f[u] = 1e9;
  deg[u] = G[u].size();
  for (auto v : G[u]) {
    if (v == fa) continue;
    pre_dfs1(v, u);
    f[u] = std::min(f[u], f[v] + 1);
  }
}

void pre_dfs2(int u, int fa) {
  for (auto v : G[u]) {
    if (v == fa) continue;
    f[v] = std::min(f[v], f[u] + 1);
    pre_dfs2(v, u);
  }
}

void getsz(int u, int fa) {
  sz[u] = 1, mx[u] = 0;
  for (auto v : G[u]) {
    if (v == fa || del[v]) continue;
    getsz(v, u);
    sz[u] += sz[v], mx[u] = std::max(mx[u], sz[v]);
  }
}

void getrt(int u, int fa, int tot) {
  mx[u] = std::max(mx[u], tot - sz[u]);
  for (auto v : G[u]) {
    if (v == fa || del[v]) continue;
    getrt(v, u, tot);
  }
  if (mx[u] < mx[rt]) rt = u;
}

void dfs2(int u, int fa, int dis) {
  ans[u] += bit.qry(-n, dis);
  vec.emplace_back(f[u] - dis, 2 - deg[u]);
  for (auto v : G[u]) {
    if (v == fa || del[v]) continue;
    dfs2(v, u, dis + 1);
  }
}

void dfs1(int u, int fa) {
  bit.upd(f[u], 2 - deg[u]);
  vec = {{f[u], 2 - deg[u]}};
  int lst = 1;
  for (int i = 0; i < G[u].size(); ++i) {
    int v = G[u][i];
    if (v == fa || del[v]) continue;
    dfs2(v, u, 1);
    for (int i = lst; i < vec.size(); ++i) bit.upd(vec[i].first, vec[i].second);
    lst = vec.size();
  }
  for (auto [x, v] : vec) bit.upd(x, -v);
  vec.clear(), lst = 0;
  for (int i = (int)G[u].size() - 1; ~i; --i) {
    int v = G[u][i];
    if (v == fa || del[v]) continue;
    dfs2(v, u, 1);
    for (int i = lst; i < vec.size(); ++i) bit.upd(vec[i].first, vec[i].second);
    lst = vec.size();
  }
  ans[u] += bit.qry(-n, 0);
  for (auto [x, v] : vec) bit.upd(x, -v);
  vec.clear();

  del[u] = 1;
  for (auto v : G[u]) {
    if (v == fa || del[v]) continue;
    rt = 0, getsz(v, u), getrt(v, u, sz[v]), dfs1(rt, 0);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  pre_dfs1(1, 0), pre_dfs2(1, 0);
  mx[0] = 1e9, getsz(1, 0), getrt(1, 0, n), dfs1(rt, 0);
  for (int i = 1; i <= n; ++i) {
    std::cout << (deg[i] != 1 ? ans[i] : 1) << '\n';
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