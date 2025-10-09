---
title: 'P6779 [Ynoi2009] rla1rmdq 题解'
date: 2024-12-25 10:34:00
---

## Description

给定一棵 $n$ 个节点的树，树有边权，与一个长为 $n$ 的序列 $a$。

定义节点 $x$ 的父亲为 $fa(x)$，根 $rt$ 满足 $fa(rt)=rt$。

定义节点 $x$ 的深度 $dep(x)$ 为其到根简单路径上所有边权和。

有 $m$ 次操作：

- `1 l r`：对于 $l \le i \le r$，$a_i\leftarrow fa(a_i)$。

- `2 l r`：查询对于 $l \le i \le r$，最小的 $dep(a_i)$。

$1\le n,m\le 2\times 10^5$，$1\le a_i\le n$。

## Solution

显然是分块。

对于散块暴力重构，整块打标记一起跳，考虑这两部分分别怎么做。

暴力重构可以看成只有单点操作，且能跳多步，则可以对树做重链剖分，每次跳的时候如果跳不出所在重链就用 dfs 序 $O(1)$ 求出祖先，否则就暴力跳出重链，容易发现总复杂度为 $O(n\log n)$。

整块打标记可以看成每次操作都是全局操作一起跳。容易发现如果一个点 $x$ 跳到别的点跳过的点上，则点 $x$ 就一定没用了，所以可以删掉，这里将没删的点看成关键点。每次修改时暴力跳关键点做上面的操作，每次要么删一个点要么多打一个标记，所以这部分是 $O(n)$。

回到原题，修改时整块的部分就按照全局操作的做法每次暴力跳所有没删的点。散块的话由于只有一部分跳，这一部分如果原来被删了，这次可能就能加回去，所以只要用单点跳多步的做法跳，如果跳完所在位置仍未被标记就加回所在块的关键点。

容易发现每个块的时间复杂度为 $O(n)$，所以总时间复杂度为 $O(n\sqrt n)$。

## Code

```C++
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;

const int kMaxN = 2e5 + 5, kMaxB = 450;

int n, m, b, tot, rt;
int a[kMaxN], p[kMaxN], sz[kMaxN], wson[kMaxN], top[kMaxN], dfn[kMaxN], idx[kMaxN];
int L[kMaxB], R[kMaxB], bel[kMaxN], cnt[kMaxN], id[kMaxB][kMaxB], tag[kMaxB];
i64 dis[kMaxN], res[kMaxB];
std::bitset<kMaxN> vis[kMaxB], in;
std::vector<std::pair<int, int>> G[kMaxN];

void dfs1(int u, int fa) {
  p[u] = (!fa ? u : fa);
  sz[u] = 1;
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    dis[v] = dis[u] + w;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

void dfs2(int u, int fa, int t) {
  static int cnt = 0;
  idx[dfn[u] = ++cnt] = u, top[u] = t;
  if (wson[u]) dfs2(wson[u], u, t);
  for (auto [v, w] : G[u]) {
    if (v == fa || v == wson[u]) continue;
    dfs2(v, u, v);
  }
}

int getfa(int x, int k) {
  // std::cerr << x << ' ' << k << '\n';
  if (!x || x == rt) return rt;
  else if (!k) return x;
  else if (dfn[x] - k >= dfn[top[x]]) return idx[dfn[x] - k];
  else return getfa(p[top[x]], k - (dfn[x] - dfn[top[x]] + 1));
  // for (int i = 1; i <= k; ++i) x = p[x];
  // return x;
}

void prework() {
  dis[rt] = 1;
  dfs1(rt, 0), dfs2(rt, 0, rt);
  b = sqrtl(n);
  if (!b) b = 1;
  tot = (n + b - 1) / b;
  for (int i = 1; i <= tot; ++i) {
    L[i] = (i - 1) * b + 1, R[i] = std::min(i * b, n);
    res[i] = LLONG_MAX;
    for (int j = L[i]; j <= R[i]; ++j) {
      bel[j] = i, vis[i][a[j]] = 1;
      res[i] = std::min(res[i], dis[a[j]]);
      id[i][++id[i][0]] = j, in[j] = 1;
    }
  }
}

void addtag(int x) {
  ++tag[x];
  static int tmp[kMaxN];
  int c = 0;
  for (int k = 1; k <= id[x][0]; ++k) {
    int i = id[x][k];
    in[i] = 0;
    --cnt[i];
    if (a[i] == rt || !vis[x][a[i] = p[a[i]]]) {
      vis[x][a[i]] = 1;
      tmp[++c] = i, in[i] = 1, res[x] = std::min(res[x], dis[a[i]]);
    }
  }
  id[x][0] = c;
  for (int i = 1; i <= c; ++i) id[x][i] = tmp[i];
  // for (int i = L[x]; i <= R[x]; ++i) res[x] = std::min(res[x], dis[a[i] = p[a[i]]]);
}

void rebuild(int x) {
  for (int i = L[x]; i <= R[x]; ++i) {
    assert(tag[x] + cnt[i] >= 0);
    if (tag[x] + cnt[i]) {
      a[i] = getfa(a[i], tag[x] + cnt[i]);
      res[x] = std::min(res[x], dis[a[i]]);
      vis[x][a[i]] = 1;
    }
    cnt[i] = 0;
  }
  tag[x] = 0;
}

void update(int l, int r) {
  int x = bel[l], y = bel[r];
  if (x == y) {
    for (int i = l; i <= r; ++i) {
      a[i] = getfa(a[i], tag[x] + cnt[i] + 1);
      res[x] = std::min(res[x], dis[a[i]]);
      cnt[i] = -tag[x];
      if (!vis[x][a[i]]) {
        vis[x][a[i]] = 1;
        if (!in[i]) id[x][++id[x][0]] = i, in[i] = 1;
      }
    }
  } else {
    // for (int i = l; i <= R[x]; ++i) ++cnt[i];
    for (int i = l; i <= R[x]; ++i) {
      a[i] = getfa(a[i], tag[x] + cnt[i] + 1);
      res[x] = std::min(res[x], dis[a[i]]);
      cnt[i] = -tag[x];
      if (!vis[x][a[i]]) {
        vis[x][a[i]] = 1;
        if (!in[i]) id[x][++id[x][0]] = i, in[i] = 1;
      }
    }
    // for (int i = L[y]; i <= r; ++i) ++cnt[i];
    for (int i = L[y]; i <= r; ++i) {
      a[i] = getfa(a[i], tag[y] + cnt[i] + 1);
      res[y] = std::min(res[y], dis[a[i]]);
      cnt[i] = -tag[y];
      if (!vis[y][a[i]]) {
        vis[y][a[i]] = 1;
        if (!in[i]) id[y][++id[y][0]] = i, in[i] = 1;
      }
    }
    // rebuild(x), rebuild(y);
    for (int i = x + 1; i < y; ++i) addtag(i);
  }
}

i64 query(int l, int r) {
  int x = bel[l], y = bel[r];
  i64 ret = LLONG_MAX;
  if (x == y) {
    rebuild(x);
    for (int i = l; i <= r; ++i) ret = std::min(ret, dis[a[i]]);
    return ret;
  } else {
    rebuild(x), rebuild(y);
    for (int i = l; i <= R[x]; ++i) ret = std::min(ret, dis[a[i]]);
    for (int i = L[y]; i <= r; ++i) ret = std::min(ret, dis[a[i]]);
    for (int i = x + 1; i < y; ++i) ret = std::min(ret, res[i]);
    return ret;
  }
}

void dickdreamer() {
  std::cin >> n >> m >> rt;
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
  }
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  prework();
  for (int i = 1; i <= m; ++i) {
    int op, l, r;
    std::cin >> op >> l >> r;
    if (op == 1) {
      update(l, r);
    } else {
      std::cout << query(l, r) - 1 << '\n';
    }
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