---
title: 'P8998 [CEOI2022] Prize 题解'
date: 2024-12-13 19:35:00
---

## Description

**这是一道交互题。**

Tomislav 在睡梦中想到了一个问题：给定两棵大小为 $N$ 的树，树上的节点按 $1\sim N$ 分别编号，树则分别编号为树 $1$，树 $2$，树有边权，但是边权被隐藏了起来。

Tomislav 需要向交互库提供一个大小为 $K$ 的编号的子集 $S$，在选择了这个集合后，小 C 可以问 $Q$ 个格式为 $(a,b)$ 的问题，定义 $d_t(x,y)$ 表示树 $t$ 上节点 $x$ 与节点 $y$ 的距离，$l_t$ 表示树 $t$ 上节点 $a$ 与节点 $b$ 的 LCA，交互库会依次回答 $d_1(l_1,a),d_1(l_1,b),d_2(l_2,a),d_2(l_2,b)$。

紧接着交互库会询问 $T$ 个格式为 $(p,q)$ 的问题，其中 $p,q\in S$，Tomislav 必须依次回答 $d_1(p,q)$ 和 $d_2(p,q)$。

可怜的 Tomislav 并不会做，请你帮帮他。

$1\le N\le 10^6$，$2\le K\le \min(N,10^5)$，$1\le T\le \min(K^2,10^5)$。

## Solution

考虑对于一棵树和给定的 $S$ 集合怎么做。

显然我们需要通过 $k-1$ 次询问得到 $S$ 的虚树上每条边的权值，这个可以转化为求出每个点到根的距离 $dis$。

于是可以用类似建虚树的过程，按照 dfs 序后询问 dfs 序相邻的数，询问出来后可以分别得到 $(dis_u,dis_{lca})$ 和 $(dis_v,dis_{lca})$ 的数量关系，由于虚树上最多 $2k-2$ 条边，所以这样做可以得到虚树上的点的 $dis$ 的关系。

如果有两棵树的话两棵树的 dfs 序排序后不一定相同，上面那个做法就不行了。

考虑对于第一棵树选择 dfs 序上的前缀，由于这些点在第一棵树上构成连通块，所以按照第二棵树的 dfs 序排序后仍能询问出第一棵树的关系。

时间复杂度：$O(N\log N+K+T)$。

## Code

```C++
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e6 + 5;

int n, k, q, t, rt1, rt2;
int p1[kMaxN], p2[kMaxN], dfn1[kMaxN], dfn2[kMaxN], idx1[kMaxN], idx2[kMaxN];
int lg[kMaxN], st1[kMaxN][20], st2[kMaxN][20], id[kMaxN];
int dis1[kMaxN], dis2[kMaxN];
std::vector<int> G1[kMaxN], G2[kMaxN];
std::vector<std::pair<int, int>> T1[kMaxN], T2[kMaxN];

int get(int *dfn, int x, int y) { return dfn[x] < dfn[y] ? x : y; }

void dfs1(int u, int fa) {
  static int cnt = 0;
  st1[dfn1[u] = ++cnt][0] = fa, idx1[cnt] = u;
  for (auto v : G1[u]) {
    if (v == fa) continue;
    dfs1(v, u);
  }
}

void dfs2(int u, int fa) {
  static int cnt = 0;
  st2[dfn2[u] = ++cnt][0] = fa, idx2[cnt] = u;
  for (auto v : G2[u]) {
    if (v == fa) continue;
    dfs2(v, u);
  }
}

int LCA1(int x, int y) {
  if (x == y) return x;
  if (dfn1[x] > dfn1[y]) std::swap(x, y);
  int k = lg[dfn1[y] - dfn1[x]];
  return get(dfn1, st1[dfn1[x] + 1][k], st1[dfn1[y] - (1 << k) + 1][k]);
}

int LCA2(int x, int y) {
  if (x == y) return x;
  if (dfn2[x] > dfn2[y]) std::swap(x, y);
  int k = lg[dfn2[y] - dfn2[x]];
  return get(dfn2, st2[dfn2[x] + 1][k], st2[dfn2[y] - (1 << k) + 1][k]);
}

void dfs3(int u) {
  static bool vis[kMaxN] = {0};
  vis[u] = 1;
  for (auto [v, w] : T1[u]) {
    if (vis[v]) continue;
    dis1[v] = dis1[u] + w;
    dfs3(v);
  }
}

void dfs4(int u) {
  static bool vis[kMaxN] = {0};
  vis[u] = 1;
  for (auto [v, w] : T2[u]) {
    if (vis[v]) continue;
    dis2[v] = dis2[u] + w;
    dfs4(v);
  }
}

void prework() {
  dfs1(rt1, 0), dfs2(rt2, 0);
  lg[0] = -1;
  for (int i = 1; i <= n; ++i) lg[i] = lg[i >> 1] + 1;
  for (int i = 1; i <= lg[n]; ++i) {
    for (int j = 1; j <= n - (1 << i) + 1; ++j) {
      st1[j][i] = get(dfn1, st1[j][i - 1], st1[j + (1 << (i - 1))][i - 1]);
      st2[j][i] = get(dfn2, st2[j][i - 1], st2[j + (1 << (i - 1))][i - 1]);
    }
  }
}

void dickdreamer() {
  std::cin >> n >> k >> q >> t;
  for (int i = 1; i <= n; ++i) {
    std::cin >> p1[i];
    if (~p1[i]) G1[p1[i]].emplace_back(i), G1[i].emplace_back(p1[i]);
    else rt1 = i;
  }
  for (int i = 1; i <= n; ++i) {
    std::cin >> p2[i];
    if (~p2[i]) G2[p2[i]].emplace_back(i), G2[i].emplace_back(p2[i]);
    else rt2 = i;
  }
  prework();
  for (int i = 1; i <= k; ++i) {
    id[i] = idx1[i];
    std::cout << id[i] << ' ';
  }
  std::cout << std::endl;
  std::sort(id + 1, id + 1 + k, [&] (int x, int y) { return dfn2[x] < dfn2[y]; });
  for (int i = 1; i < k; ++i)
    std::cout << "? " << id[i] << ' ' << id[i + 1] << '\n';
  std::cout << "!" << std::endl;
  for (int i = 1; i < k; ++i) {
    int x = id[i], y = id[i + 1], lca1 = LCA1(x, y), lca2 = LCA2(x, y);
    int d1, d2, d3, d4;
    std::cin >> d1 >> d2 >> d3 >> d4;
    T1[lca1].emplace_back(x, d1), T1[x].emplace_back(lca1, -d1);
    T1[lca1].emplace_back(y, d2), T1[y].emplace_back(lca1, -d2);
    T2[lca2].emplace_back(x, d3), T2[x].emplace_back(lca2, -d3);
    T2[lca2].emplace_back(y, d4), T2[y].emplace_back(lca2, -d4);
  }
  dfs3(id[1]), dfs4(id[1]);
  std::vector<std::pair<int, int>> res;
  for (int i = 1; i <= t; ++i) {
    int x, y;
    std::cin >> x >> y;
    int lca1 = LCA1(x, y), lca2 = LCA2(x, y);
    res.emplace_back(dis1[x] + dis1[y] - 2 * dis1[lca1], dis2[x] + dis2[y] - 2 * dis2[lca2]);
  }
  for (auto [x, y] : res) std::cout << x << ' ' << y << '\n';
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