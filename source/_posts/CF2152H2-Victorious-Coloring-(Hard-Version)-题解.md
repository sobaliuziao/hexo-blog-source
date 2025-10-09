---
title: CF2152H2 Victorious Coloring (Hard Version) 题解
date: 2025-10-07 20:59:00
---

## Description

给定一棵有 $n$ 个顶点的树，每个顶点编号为 $1$ 到 $n$。每条边都被赋予一个正整数权值 $w_1, w_2, \ldots, w_{n-1}$。

一种“胜利染色”指的是将所有顶点染成红色或黄色两种颜色，其中必须至少有一个顶点染成红色（这象征着队伍 T1 的象征）。

设对每个顶点分配了一个非负整数权值 $x_1, x_2, \ldots, x_n$。胜利染色的代价被定义为：所有红色顶点权值之和，加上所有连接不同颜色顶点（即红色和黄色）之间的边的权值之和。定义 $f([x_1, x_2, \ldots, x_n])$ 为所有胜利染色下可能的最小代价。

Gumayusi 考虑了在给定序列 $x_1, x_2, \ldots, x_n$ 时计算 $f([x_1, x_2, \ldots, x_n])$ 的问题。但对他而言这个问题太简单了，于是他改进了这个问题：给定一个整数 $l$，求一组非负整数顶点权值 $[x_1, x_2, \ldots, x_n]$，使得 $f([x_1, x_2, \ldots, x_n]) \ge l$ 且顶点权值总和 $\sum_{i=1}^n x_i$ 最小。

Gumayusi 感到满意，但还存在一个严重问题——这个问题没有任何询问，对于任何不是“坏的”题目来说是不可接受的。因此，他给这个问题增加了询问。每给定一个 $l$ 作为询问，你需要输出相应的最小总顶点权值。

$1\leq n,q\leq 2.5\times 10^5$。

## Solution

设 $g(S)$ 表示选择 $S$ 点集内的点染红的边权代价和，那么问题实际上等价于选择一些互不相交的集合 $S_1,S_2,\ldots,S_k$，最大化 $\sum(l-g(s_i))$。

首先容易发现最优划分中 $S$ 一定构成一个连通块，否则随便选择任意一个连通块 $T$ 的 $g(T)$ 值一定小于 $g(S)$，最终的结果也就更大。

还有一个结论是如果存在两条边 $e_1$ 和 $e_2$，满足 $e_1$ 两个端点都在 $S$ 中，$e_2$ 恰有一个端点在 $S$ 中，则一定满足 $w(e_1)>w(e_2)$。否则把 $e_1$ 断掉会把 $S$ 划分成两个集合 $S_1$ 和 $S_2$，选择不包含 $e_2$ 的端点的那个集合，那么 $g$ 值一定会至少减少 $w(e_2)-w(e_1)\geq 0$，矛盾。

注意到如果我们固定最优划分集合 $S$ 邻域中边权最小的边是 $e$ 后，只会有至多两个集合满足条件！这是因为 $e$ 只有两个端点，这两个集合就是两边分别走边权大于 $w(e)$ 的边后能走到的连通块。

---

由于这个很类似最大生成树，所以考虑建出边权从大到小的 kruskal 重构树。那么每次选择的集合一定构成一个子树。

每个子树的 $g$ 值容易树上差分求，设 $s_u$ 表示 $u$ 选择子树的 $g$ 值，$f_u$ 表示 $u$ 子树能选择的最大 $\sum(k-s_u)$。

容易得到转移：$f_u\leftarrow \max(f_{ls_u}+f_{rs_u},k-s_u)$，直接转移是 $O(nq)$ 的。

优化就考虑最终的答案一定是由 $k\cdot i+w$ 的形式构成的，设 $g_{u,i}$ 表示 $u$ 的子树中系数为 $i$ 的最大 $w$ 值。

转移变为 $g_{u,i+j}\leftarrow g_{ls_u,i}+g_{rs_u,j},g_{u,1}\leftarrow -s_u$，很遗憾这个东西不是凸的，但是由于我们只需要求 $k\cdot i+g_{u,i}$ 的最大值，所以维护出凸包然后闵可夫斯基和合并即可，$g_{u,1}$ 的转移需要单独处理一下。

时间复杂度：$O(n\log^2n+q\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

template<class T>
struct Vector {
  T x, y;

  Vector() {}
  Vector(T _x, T _y) : x(_x), y(_y) {}

  friend bool operator ==(Vector a, Vector b) { return a.x == b.x && a.y == b.y; }
  friend bool operator !=(Vector a, Vector b) { return a.x != b.x || a.y != b.y; }
  friend Vector operator -(Vector a) { return {-a.x, -a.y}; }
  friend Vector operator +(Vector a, Vector b) { return {a.x + b.x, a.y + b.y}; }
  friend Vector operator -(Vector a, Vector b) { return {a.x - b.x, a.y - b.y}; }
  friend T operator *(Vector a, Vector b) { return a.x * b.y - a.y * b.x; }
  template<class _T> friend Vector operator *(Vector a, _T b) { return {a.x * b, a.y * b}; }
  template<class _T> friend Vector operator *(_T a, Vector b) { return {a * b.x, a * b.y}; }
  template<class _T> friend Vector operator /(Vector a, _T b) { return {a.x * 1.0 / b, a.y * 1.0 / b}; }
  friend Vector operator +=(Vector &a, Vector b) { return a = {a.x + b.x, a.y + b.y}; }
  friend Vector operator -=(Vector &a, Vector b) { return a = {a.x - b.x, a.y - b.y}; }
  template<class _T> friend Vector operator *=(Vector &a, _T b) { return a = {a.x * b, a.y * b}; }
  template<class _T> friend Vector operator /=(Vector &a, _T b) { return a = {a.x * 1.0 / b, a.y * 1.0 / b}; }
  friend bool operator <(Vector a, Vector b) { return a * b > 0; }
};

using i64 = int64_t;
using Vec = Vector<i64>;

const int kMaxN = 5e5 + 5;

int n, q, cnt, k, m;
int u[kMaxN], v[kMaxN], w[kMaxN], fa[kMaxN], id[kMaxN], s[kMaxN];
int ls[kMaxN], rs[kMaxN], f[kMaxN], g[kMaxN];
std::priority_queue<Vec> qq[kMaxN];

inline void chkmax(int &x, int y) { x = (x > y ? x : y); }
inline void chkmin(int &x, int y) { x = (x < y ? x : y); }

int find(int x) {
  return x == fa[x] ? x : fa[x] = find(fa[x]);
}

void unionn(int x, int y, int w) {
  int fx = find(x), fy = find(y);
  if (fx != fy) {
    ++cnt, ls[cnt] = id[fx], rs[cnt] = id[fy], s[cnt] = s[id[fx]] + s[id[fy]] - 2 * w;
    fa[fx] = fy, id[fy] = cnt;
  }
}

void build() {
  cnt = n;
  for (int i = 1; i <= n; ++i) fa[i] = id[i] = i;
  std::vector<std::tuple<int, int, int>> ed;
  for (int i = 1; i < n; ++i) ed.emplace_back(w[i], u[i], v[i]);
  std::sort(ed.begin(), ed.end(), std::greater<>());
  for (auto [w, u, v] : ed) {
    unionn(u, v, w);
  }
}

void dfs(int u) {
  for (; qq[u].size(); qq[u].pop()) {}
  if (u <= n) {
    qq[u].emplace(1, -s[u]);
  } else {
    dfs(ls[u]), dfs(rs[u]);
    if (qq[ls[u]].size() < qq[rs[u]].size()) qq[ls[u]].swap(qq[rs[u]]);
    qq[u].swap(qq[ls[u]]);
    for (; qq[rs[u]].size(); qq[rs[u]].pop()) qq[u].emplace(qq[rs[u]].top());
    Vec p = {1, -s[u]};
    if (qq[u].top() < p) {
      for (; qq[u].size() >= 2;) {
        auto p1 = qq[u].top(); qq[u].pop();
        auto p2 = qq[u].top();
        if ((p1 - p) * p2 >= 0) qq[u].pop(), qq[u].emplace(p1 + p2);
        else { qq[u].emplace(p1); break;}
      }
      if (qq[u].size()) {
        auto pp = qq[u].top(); qq[u].pop();
        if ((pp - p).x > 0) qq[u].emplace(pp - p);
      }
      qq[u].emplace(p);
    }
  }
}

int solve(int k) {
  int L = 0, R = m + 1, res = 0;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (k * f[mid] + g[mid] > k * f[mid - 1] + g[mid - 1]) L = res = mid;
    else R = mid;
  }
  return k * f[res] + g[res];
}

void dickdreamer() {
  std::cin >> n;
  std::fill_n(s + 1, n, 0);
  for (int i = 1; i < n; ++i)
    std::cin >> u[i] >> v[i] >> w[i], s[u[i]] += w[i], s[v[i]] += w[i];
  build();
  dfs(cnt);
  for (m = 0; qq[cnt].size();) {
    ++m;
    auto [x, y] = qq[cnt].top(); qq[cnt].pop();
    f[m] = f[m - 1] + x, g[m] = g[m - 1] + y;
  }
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int k;
    std::cin >> k;
    std::cout << solve(k) << '\n';
  }
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