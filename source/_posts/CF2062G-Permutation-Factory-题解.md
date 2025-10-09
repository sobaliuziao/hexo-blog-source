---
title: 'CF2062G Permutation Factory 题解'
date: 2025-08-12 15:49:00
---

## Description

给定两个长度为 $n$ 的排列 $p_1, p_2, \ldots, p_n$ 和 $q_1, q_2, \ldots, q_n$。每次操作中，你可以选择两个不同的整数 $1 \leq i, j \leq n$ 并交换 $p_i$ 和 $p_j$。该操作的成本为 $\min(|i - j|, |p_i - p_j|)$。

请找到使 $p_i = q_i$ 对所有 $1 \leq i \leq n$ 成立的最小总成本，并输出达成该目标的交换操作序列。

一个长度为 $n$ 的排列是由 $1$ 到 $n$ 的不同整数按任意顺序组成的数组。例如，$[2, 3, 1, 5, 4]$ 是排列，但 $[1, 2, 2]$ 不是排列（$2$ 重复出现），$[1, 3, 4]$ 也不是排列（当 $n=3$ 时出现 $4$）。

$n\leq 100$。

## Solution

首先每次操作的成本是两个东西的 $\min$，而最后又要最小化总成本，所以这两维可以拆开。

考虑把排列看成 $n$ 个点，每个为 $(i,p_i)$，每次有两种操作：

1. 选择 $i,j$，用 $|i-j|$ 的代价将 $(i,p_i)$ 移到 $(j,p_i)$，$(j,p_j)$ 移到 $(i,p_j)$。
2. 选择 $i,j$，用 $|p_i-p_j|$ 的代价将 $(i,p_i)$ 移到 $(i,p_j)$，$(j,p_j)$ 移到 $(j,p_i)$。

容易发现一次操作的代价就是移动的曼哈顿距离除以二，所以我们只关心移动的总曼哈顿距离。

由于最终所有 $(j,q_j)$ 上需要有点，所以一定是一一匹配的，不妨设最终是初始的 $(i,p_i)$ 移动到了 $(m_i,q_{m_i})$，那么有一个显然的下界是 $\sum_{i=1}^{n}{\left(|i-m_i|+|p_i-q_{m_i}|\right)}$，可以证明这个下界是可以取到的。

先用费用流求出 $m_i$。

构造就考虑两位实际上是独立的，而每一维等价于是有一个大小为 $n$ 的排列 $p$，可以通过 $|i-j|$ 的代价交换 $p_i$ 和 $p_j$，要求最后 $p_i=p_j$。

这个是比较经典的问题，每次选择最小的 $i$ 使得 $p_i\neq i$，然后找到 $p_j=i$ 的这个 $j$，容易发现 $p_i,p_{i+1},\ldots,p_{j-1}$ 一定存在一个数大于等于 $j$，找到这个位置交换即可，总共做至多 $\frac{n(n-1)}{2}$ 次，因为每次会至少减少两个逆序对。

时间复杂度：$O(n^4)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 105;

int n;
int p[kMaxN], q[kMaxN], match1[kMaxN], match2[kMaxN];
std::vector<std::pair<int, int>> vec;

namespace Dinic {
const int kMaxN = 205, kMaxM = kMaxN * kMaxN * 4, kInf = 1e9;

struct Node {
  int v, w, c, pre;
} e[kMaxM];

int tot = 1, n, s, t, cost;
int tail[kMaxN], dis[kMaxN], cur[kMaxN], eid[kMaxN][kMaxN];
bool inq[kMaxN], vis[kMaxN];

void init(int _n, int _s, int _t) {
  for (int i = 1; i <= n; ++i) tail[i] = 0;
  tot = 1, n = _n, s = _s, t = _t;
}

void adde(int u, int v, int w, int c) { e[++tot] = {v, w, c, tail[u]}, tail[u] = eid[u][v] = tot; }
void add(int u, int v, int w, int c) { adde(u, v, w, c), adde(v, u, 0, -c); }

bool spfa() {
  std::queue<int> q;
  for (int i = 1; i <= n; ++i) {
    dis[i] = kInf, cur[i] = tail[i], inq[i] = vis[i] = 0;
  }
  q.emplace(s), dis[s] = 0, inq[s] = 1;
  for (; !q.empty();) {
    int u = q.front(); inq[u] = 0, q.pop();
    for (int i = tail[u]; i; i = e[i].pre) {
      int v = e[i].v, w = e[i].w, c = e[i].c;
      if (w && dis[v] > dis[u] + c) {
        dis[v] = dis[u] + c;
        if (!inq[v]) q.emplace(v), inq[v] = 1;
      }
    }
  }
  return dis[t] != kInf;
}

int dfs(int u, int lim) {
  if (u == t || !lim) {
    cost += lim * dis[t];
    return lim;
  }
  vis[u] = 1;
  int flow = 0;
  for (int &i = cur[u]; i; i = e[i].pre) {
    int v = e[i].v, w = e[i].w;
    if (!vis[v] && w && dis[v] == dis[u] + e[i].c) {
      int tmp = dfs(v, std::min(w, lim));
      if (!tmp) dis[v] = kInf;
      e[i].w -= tmp, e[i ^ 1].w += tmp;
      lim -= tmp, flow += tmp;
      if (!lim) break;
    }
  }
  vis[u] = 0;
  return flow;
}

void solve() {
  for (; spfa(); dfs(s, kInf)) {}
}
} // namespace Dinic

void getmatch() {
  int s = 2 * n + 1, t = 2 * n + 2;
  Dinic::init(t, s, t);
  for (int i = 1; i <= n; ++i) {
    Dinic::add(s, i, 1, 0), Dinic::add(i + n, t, 1, 0);
    for (int j = 1; j <= n; ++j)
      Dinic::add(i, j + n, 1, abs(i - j) + abs(p[i] - q[j]));
  }
  Dinic::solve();
  for (int i = 1; i <= n; ++i) {
    match1[i] = 0;
    for (int j = 1; j <= n; ++j)
      if (!Dinic::e[Dinic::eid[i][j + n]].w)
        assert(!match1[i]), match1[i] = j;
    match2[p[i]] = q[match1[i]];
  }
}

void work(int x, int y) {
  vec.emplace_back(x, y), std::swap(p[x], p[y]);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> p[i];
  for (int i = 1; i <= n; ++i) std::cin >> q[i];
  getmatch();
  vec.clear();
  { // 把 x 变对
    for (int i = 1; i <= n; ++i) {
      int pos = 0;
      while (true) {
        for (int j = 1; j <= n; ++j)
          if (match1[j] == i)
            pos = j;
        if (pos == i) break;
        for (int j = i; j < pos; ++j) {
          if (match1[j] >= pos) {
            work(pos, j), std::swap(match1[pos], match1[j]);
            break;
          }
        }
      }
    }
  }
  { // 把 y 变对
    static int pp[kMaxN];
    for (int i = 1; i <= n; ++i) pp[p[i]] = i;
    for (int i = 1; i <= n; ++i) {
      int pos = 0;
      while (true) {
        for (int j = 1; j <= n; ++j)
          if (match2[j] == i)
            pos = j;
        if (pos == i) break;
        for (int j = i; j < pos; ++j) {
          if (match2[j] >= pos) {
            work(pp[pos], pp[j]), std::swap(match2[pos], match2[j]), std::swap(pp[pos], pp[j]);
            break;
          }
        }
      }
    }
  }
  // for (int i = 1; i <= n; ++i) std::cerr << p[i] <<  " \n"[i == n];
  std::cout << vec.size() << '\n';
  for (auto [x, y] : vec) std::cout << x << ' ' << y << '\n';
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