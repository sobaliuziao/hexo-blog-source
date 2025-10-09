---
title: CF526G Spiders Evil Plan 题解
date: 2024-07-28 23:32:00
---

## Description

给定一棵 $n$ 个节点的无根树，每条边有边权。

有 $q$ 次询问，每次询问给出 $x,y$，你需要选择 $y$ 条树上的路径，使这些路径形成一个包含 $x$ 的连通块，且连通块中包含的边权和最大。

$n, q \le 10^5$，强制在线。

## Solution

考虑只有一组询问怎么快速求答案。

容易发现树上路径的两端点一定是叶子，并且如果给定了这些叶子那么一定存在一组方案使得这些路径覆盖了这些叶子构成的虚树。

对于询问 $x,y$，考虑把 $x$ 提到根，需要找到一些叶子使得这些叶子的虚树包含 $x$ 并且虚树权值和最大。

如果只要求权值和最大就只需要找到权值最大的 $2y$ 条长链即可，这就是贪心选，但是此时选择的虚树可能不包含 $x$ 而导致这种以 $x$ 为根贪心取长链算出来的答案会算上一些虚树没有的边。

由于这是暴力就不考虑怎么调整了。

注意到选择叶子的最优解一定满足至少选了树的直径的两端点之一，所以考虑让直径的两端点作为根跑上面那个贪心做法，这样就不用换根了。

具体的，假设直径的一端点为 $p$，询问为 $(x,y)$，就以 $p$ 为根选择最长的 $2y-1$ 条长链加入答案。可能出现选的方案虚树不包含 $x$ 的情况，这时需要调整。容易发现只有两种调整方案：

1. 找到 $x$ 祖先里第一个被选的点然后把这个点到叶子的路径替换为这个点走到 $x$ 那边的路径。
2. 让 $x$ 所在的长链替换原来第 $2y-1$ 长的长链。

至于为什么是这两种就考虑 $x$ 的长链替换哪个原长链即可。

时间复杂度：$O\left((n+q)\log n\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, q, s, t, cntl;
int dis[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u, int fa) {
  if (!fa) dis[u] = 0;
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    dis[v] = dis[u] + w;
    dfs(v, u);
  }
}

struct Tree {
  int rt, cnt, tot;
  int lg[kMaxN], len[kMaxN], dis[kMaxN], mxd[kMaxN], lson[kMaxN], p[kMaxN][18];
  int rnk[kMaxN], id[kMaxN], sum[kMaxN], minrnk[kMaxN], top[kMaxN];
  
  void dfs1(int u, int fa) {
    mxd[u] = u, p[u][0] = fa;
    for (int i = 1; i <= lg[n]; ++i)
      p[u][i] = p[p[u][i - 1]][i - 1];
    for (auto [v, w] : G[u]) {
      if (v == fa) continue;
      dis[v] = dis[u] + w;
      dfs1(v, u);
      if (len[v] + w > len[u])
        len[u] = len[v] + w, mxd[u] = mxd[v], lson[u] = v;
    }
  }

  void dfs2(int u, int fa) {
    minrnk[u] = rnk[u];
    for (auto [v, w] : G[u]) {
      if (v == fa) continue;
      dfs2(v, u);
      minrnk[u] = std::min(minrnk[u], minrnk[v]);
    }
  }

  void init(int s) {
    rt = s, lg[0] = -1;
    for (int i = 1; i <= n; ++i) lg[i] = lg[i >> 1] + 1;
    dfs1(rt, 0);
    for (int i = 1; i <= n; ++i) {
      if (i == rt || i != lson[p[i][0]]) {
        for (int j = i; j; j = lson[j]) top[j] = i;
      }
    }
    std::vector<std::pair<int, int>> vec;
    for (int i = 1; i <= n; ++i) {
      rnk[i] = 1e9;
      if (i == rt || i != lson[p[i][0]]) {
        vec.emplace_back(dis[mxd[i]] - dis[p[i][0]], mxd[i]);
      }
    }
    std::sort(vec.begin(), vec.end(), std::greater<std::pair<int, int>>());
    tot = vec.size();
    for (int i = 0; i < (int)vec.size(); ++i) {
      rnk[vec[i].second] = i + 1;
      id[i + 1] = vec[i].second, sum[i + 1] = sum[i] + vec[i].first;
    }
    dfs2(rt, 0);
  }

  int ask1(int x, int y) {
    int now = x;
    for (int i = lg[n]; ~i; --i)
      if (p[now][i] && minrnk[p[now][i]] > y)
        now = p[now][i];
    if (minrnk[now] > y) now = p[now][0];
    return sum[y] - len[now] + dis[mxd[x]] - dis[now];
  }

  int ask2(int x, int y) {
    int now = x;
    for (int i = lg[n]; ~i; --i)
      if (p[now][i] && minrnk[p[now][i]] >= y)
        now = p[now][i];
    if (minrnk[now] >= y) now = p[now][0];
    return sum[y - 1] + dis[mxd[x]] - dis[now];
  }

  int solve(int x, int y) {
    y = 2 * y - 1;
    if (y >= tot) return sum[tot];
    else if (minrnk[x] <= y) return sum[y];
    return std::max(ask1(x, y), ask2(x, y));
  }
} tr[2];

void dickdreamer() {
  std::cin >> n >> q;
  int sumw = 0;
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
    sumw += w;
  }
  for (int i = 1; i <= n; ++i) cntl += (G[i].size() == 1);
  dfs(1, 0);
  s = std::max_element(dis + 1, dis + 1 + n) - dis;
  dfs(s, 0);
  t = std::max_element(dis + 1, dis + 1 + n) - dis;
  tr[0].init(s), tr[1].init(t);
  for (int i = 1, lstans = 0; i <= q; ++i) {
    int x, y;
    std::cin >> x >> y;
    x = (x + lstans - 1) % n + 1, y = (y + lstans - 1) % n + 1;
    if (2 * y >= cntl)std::cout << (lstans = sumw) << '\n';
    else std::cout << (lstans = std::max(tr[0].solve(x, y), tr[1].solve(x, y))) << '\n';
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