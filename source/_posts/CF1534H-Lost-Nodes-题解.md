---
title: 'CF1534H Lost Nodes 题解'
date: 2025-06-20 16:58:00
---

## Description

这是一道**交互题**。

给你一棵包含 $n$ 个节点的树。你需要猜测出这棵树上的两个特殊节点 $a,b$（$a$ 不一定与 $b$ 不同）。

首先，你会被告知一个整数 $r$，满足节点 $r$ 是节点 $a,b$ 之间的简单路径上的一点。

接下来你可以进行询问，具体的，每次给定整数 $r$，交互器会给你当树的根节点为 $r$ 时，节点 $a,b$ 的最近公共祖先是哪个节点。

特别的，在给定树的形态之后，你需要先给出在所有 $a,b,r$ 的可能的取值中，至少需要多少次询问才能保证得出特殊节点的编号。

$1≤n≤10^5;1≤a,b,r≤n$ 且节点 $r$ 在节点 $a,b$ 之间的简单路径上（包括节点 $a,b$）。

## Solution

由于只要知道第一问的策略是什么，所以第二问和第一问差不多。

首先对于 $u$ 的子树，且 $u\neq r$，如果 $u$ 子树内所有节点的询问值都在子树内，则一定有一个特殊节点在 $u$ 的子树内，否则一定不在。

所以可以设计状态：设 $f_u$ 表示知道特殊节点是否在 $u$ 的子树内，如果在 $u$ 的子树内需要找到确切节点，否则要找到 $u$ 子树内所有点的询问值的最小次数，$g_u$ 表示如果特殊节点在 $u$ 的子树内，则为特殊节点值，否则为 $u$ 子树内所有点的询问值。

设 $v_1,v_2,\ldots,v_t$ 是 $u$ 的儿子，策略大概是从前往后枚举 $v_i$，如果按照让 $f_{v_i}$ 最小的策略询问的第一个叶子的询问值在 $v_i$ 子树内，那么特殊节点就在 $v_i$ 子树内，步数就是 $f_{v_i}$。如果询问值不在 $u$ 的子树内，则 $u$ 的子树内都没有特殊节点，步数是 $1$。否则说明特殊节点不在 $v_i$ 子树内，但在 $u$ 的子树内，继续枚举 $v_{i+1}$ 即可。

所以 $\displaystyle f_u=\max_{i=1}^{t}{\left(f_{v_i}+i-1\right)}$，最小化这个东西就让 $v_i$ 按照 $f_{v_i}$ 的值从大到小排序即可。

---

由于在根 $r$ 处可能有两个子树都有特殊节点，需要特殊处理一下，并且需要分讨 $r$ 是否是特殊节点：

1. $r$ 是特殊节点，贡献为 $\displaystyle\max_{i=1}^{t}{\left(f_{v_i}+t-1\right)}$。
2. $r$ 不是特殊节点，贡献为 $\displaystyle\max_{i=1}^{t}{\max_{j=i+1}^{t}{\left(f_{v_i}+f_{v_j}+j-2\right)}}=\max_{j=2}^{t}{\left(f_{v_1}+f_{v_j}+j-2\right)}$。

要求所有根的答案就换根即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n;
int f[kMaxN], g[kMaxN], h[kMaxN], dep[kMaxN];
int buc[kMaxN];
std::vector<int> G[kMaxN];

struct SGT {
  int mx[kMaxN * 4], tag[kMaxN * 4];
  void pushup(int x) {
    mx[x] = std::max(mx[x << 1], mx[x << 1 | 1]);
  }
  void addtag(int x, int v) {
    mx[x] += v, tag[x] += v;
  }
  void pushdown(int x) {
    if (tag[x]) {
      addtag(x << 1, tag[x]), addtag(x << 1 | 1, tag[x]);
      tag[x] = 0;
    }
  }
  void build(int x, int l, int r) {
    mx[x] = -1e9, tag[x] = 0;
    if (l == r) return;
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
  }
  void update(int x, int l, int r, int ql, int qr, int v) {
    if (l > qr || r < ql) return;
    else if (l >= ql && r <= qr) return addtag(x, v);
    pushdown(x);
    int mid = (l + r) >> 1;
    update(x << 1, l, mid, ql, qr, v), update(x << 1 | 1, mid + 1, r, ql, qr, v);
    pushup(x);
  }
} sgt;

void ins(int x) {
  if (!buc[x]++) sgt.update(1, 0, n, x, x, 1e9 + x);
  sgt.update(1, 0, n, 0, x, 1);
}

void del(int x) {
  if (!--buc[x]) sgt.update(1, 0, n, x, x, -1e9 - x);
  sgt.update(1, 0, n, 0, x, -1);
}

int query() { return std::max(sgt.mx[1] - 1, 1); }

void dfs1(int u, int fa) {
  dep[u] = dep[fa] + 1;
  bool isleaf = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
  }
  std::sort(G[u].begin(), G[u].end(), [&] (int i, int j) { return f[i] > f[j]; });
  for (auto v : G[u]) {
    if (v == fa) continue;
    ins(f[v]);
  }
  f[u] = query();
  // std::cerr << u << ' ' << f[u] << '\n';
  for (auto v : G[u]) {
    if (v == fa) continue;
    del(f[v]);
  }
}

void dfs2(int u, int fa) {
  if (fa) ins(g[u]);
  for (auto v : G[u]) {
    if (v == fa) continue;
    ins(f[v]);
  }
  for (auto v : G[u]) {
    if (v == fa) continue;
    del(f[v]), g[v] = query(), ins(f[v]);
  }
  for (auto v : G[u]) {
    if (v == fa) continue;
    del(f[v]);
  }
  if (fa) del(g[u]);
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs2(v, u);
  }

  std::vector<int> vec;
  for (auto v : G[u]) {
    if (v == fa) continue;
    vec.emplace_back(f[v]);
  }
  if (fa) vec.emplace_back(g[u]);
  std::sort(vec.begin(), vec.end(), std::greater<>());
  for (int i = 0; i < vec.size(); ++i) {
    h[u] = std::max<int>(h[u], vec[i] + vec.size() - 1);
    if (i) h[u] = std::max(h[u], vec[i] + vec[0] + i - 1);
  }
}

int ask(int x) {
  std::cout << "? " << x << std::endl;
  int v;
  std::cin >> v;
  return v;
}

int solve(int u, int fa) {
  bool isleaf = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    int val = solve(v, u);
    if (val != u) return val;
    isleaf = 0;
  }
  if (isleaf) return ask(u);
  else return u;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  sgt.build(1, 0, n);
  dfs1(1, 0), dfs2(1, 0);
  std::cout << *std::max_element(h + 1, h + 1 + n) << std::endl;
  int r, a = 0, b = 0;
  std::cin >> r;
  // std::cerr << f[4] << '\n';
  dfs1(r, 0);
  for (auto v : G[r]) {
    int val = solve(v, r);
    if (val != r) {
      if (!a) a = val;
      else b = val;
    }
    if (a && b) break;
  }
  if (!a) a = r;
  if (!b) b = r;
  std::cout << "! " << a << ' ' << b << std::endl;
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