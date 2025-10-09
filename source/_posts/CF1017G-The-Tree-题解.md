---
title: CF1017G The Tree 题解
date: 2024-12-20 14:48:00
---

## Description

给定一棵树，维护以下 $3$ 个操作：

1. `1 x` 表示如果节点 $x$ 为白色，则将其染黑。否则对这个节点的所有儿子递归进行相同操作。

2. `2 x` 表示将以节点 $x$ 为根的子树染白。

3. `3 x` 表示查询节点 $x$ 的颜色。

$n,q\leq 10^5$。

## Solution

首先考虑没有操作二怎么做。

容易发现在点 $x$ 进行的操作能够影响到 $y$，当且仅当 $y$ 在 $x$ 的子树里且 $x\to y$ 的路径上进行一操作的总次数不小于路径长度。

那么先将每个点的权值设为 $-1$，进行一次一操作就将操作点点权加 $1$，则一个点 $x$ 为黑色的条件即为根到 $x$ 的最大后缀和大于等于 $0$，树剖+线段树维护即可。

加上操作二后，相当于是每次需要将 $x$ 子树内的点权重置为 $-1$，并且还要去除根到 $x$ 这条路径上对 $x$ 子树的影响，前面重置为 $-1$ 可以用线段树进行区间覆盖，而去除祖先影响则可以直接求出根到 $x$ 的最大后缀和 $s$，然后将 $x$ 的点权加上 $-1-s$，这样祖先对 $x$ 的贡献就只有 $-1$ 了。

时间复杂度：$O(n+q\log^2n)$。

## Code

```C++
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

struct Info {
  int sum, res;
  Info(int _sum = 0, int _res = 0) : sum(_sum), res(_res) {}
  friend Info operator +(Info a, Info b) {
    return {a.sum + b.sum, std::max(a.res + b.sum, b.res)};
  }
};

int n, q;
int p[kMaxN], sz[kMaxN], wson[kMaxN], dfn[kMaxN], top[kMaxN];
std::vector<int> G[kMaxN];

struct SGT {
  Info t[kMaxN * 4];
  bool tag[kMaxN * 4];

  void pushup(int x) {
    t[x] = t[x << 1] + t[x << 1 | 1];
  }
  void addtag(int x, int l, int r) {
    tag[x] = 1, t[x] = {-(r - l + 1), -1};
  }
  void pushdown(int x, int l, int r) {
    if (tag[x]) {
      int mid = (l + r) >> 1;
      addtag(x << 1, l, mid), addtag(x << 1 | 1, mid + 1, r);
      tag[x] = 0;
    }
  }
  void build(int x, int l, int r) {
    if (l == r) return void(t[x] = {-1, -1});
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }
  void update1(int x, int l, int r, int ql, int v) {
    if (l == r) {
      t[x].sum += v, t[x].res += v;
      return;
    }
    pushdown(x, l, r);
    int mid = (l + r) >> 1;
    if (ql <= mid) update1(x << 1, l, mid, ql, v);
    else update1(x << 1 | 1, mid + 1, r, ql, v);
    pushup(x);
  }
  void update2(int x, int l, int r, int ql, int qr) {
    if (l > qr || r < ql) return;
    else if (l >= ql && r <= qr) return addtag(x, l, r);
    pushdown(x, l, r);
    int mid = (l + r) >> 1;
    update2(x << 1, l, mid, ql, qr), update2(x << 1 | 1, mid + 1, r, ql, qr);
    pushup(x);
  }
  Info query(int x, int l, int r, int ql, int qr) {
    if (l > qr || r < ql) return {0, -(int)1e9};
    else if (l >= ql && r <= qr) return t[x];
    pushdown(x, l, r);
    int mid = (l + r) >> 1;
    return query(x << 1, l, mid, ql, qr) + query(x << 1 | 1, mid + 1, r, ql, qr);
  }
} sgt;

void dfs1(int u, int fa) {
  sz[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}
void dfs2(int u, int fa, int t) {
  static int cnt = 0;
  dfn[u] = ++cnt, top[u] = t;
  if (wson[u]) dfs2(wson[u], u, t);
  for (auto v : G[u]) {
    if (v == fa || v == wson[u]) continue;
    dfs2(v, u, v);
  }
}

int query(int x) {
  if (!x) return 0;
  Info ret = {0, -(int)1e9};
  for (; x; x = p[top[x]]) ret = sgt.query(1, 1, n, dfn[top[x]], dfn[x]) + ret;
  return ret.res;
}

void dickdreamer() {
  std::cin >> n >> q;
  for (int i = 2; i <= n; ++i) {
    std::cin >> p[i];
    G[i].emplace_back(p[i]), G[p[i]].emplace_back(i);
  }
  dfs1(1, 0), dfs2(1, 0, 1), sgt.build(1, 1, n);
  for (int i = 1; i <= q; ++i) {
    int op, x;
    std::cin >> op >> x;
    if (op == 1) {
      sgt.update1(1, 1, n, dfn[x], 1);
    } else if (op == 2) {
      sgt.update2(1, 1, n, dfn[x], dfn[x] + sz[x] - 1);
      sgt.update1(1, 1, n, dfn[x], -1 - query(x));
    } else {
      std::cout << (query(x) >= 0 ? "black\n" : "white\n");
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