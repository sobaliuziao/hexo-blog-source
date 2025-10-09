---
title: P13690 [CEOI 2025] boardgames 题解
date: 2025-09-15 17:04:00
---

## Description

每年在克卢日-纳波卡都会举办一次大型桌游博览会，展示各种新推出的游戏。今年的主要亮点是一款名为 **BoardOina** 的游戏。

队伍中排有 $n$ 名玩家，等待体验该游戏。玩家按排队顺序编号为 $0$ 到 $n - 1$。编号 $0$ 的玩家在队首，编号 $n - 1$ 的玩家在队尾。

队伍中共有 $m$ 对不同的好友关系。具体而言，对于每个 $i$（$0 \leq i \leq m - 1$），玩家 $x[i]$ 与玩家 $y[i]$ 是好友，且满足 $0 \leq x[i] < y[i] < n$。好友关系是对称的。

考虑从玩家 $s$ 开始的、长度为 $k$ 的连续玩家序列（$0 \leq s < n$ 且 $1 \leq k \leq n - s$）。如果在该序列中，任意两名玩家之间都可以通过该组内的好友关系链相互到达，那么这组玩家构成一个规模为 $k$ 的好友组。具体来说，玩家 $s, s + 1, \ldots, s + k - 1$ 构成规模为 $k$ 的好友组，当且仅当对于任意满足 $s \leq u < v < s + k$ 的玩家 $u$ 和 $v$，存在一列玩家 $p[0], \ldots, p[l - 1]$，使得：

- $l \geq 2$；
- 对于所有 $j \in [0, l - 1]$，都有 $s \leq p[j] < s + k$；
- $p[0] = u$ 且 $p[l - 1] = v$；
- 对于所有 $j \in [0, l - 2]$，玩家 $p[j]$ 与 $p[j + 1]$ 是好友。

特别地，当 $k = 1$ 时，玩家 $s$ 自身就构成一个规模为 $1$ 的好友组。

**BoardOina** 可供任意人数游玩，但为了让游戏更受欢迎，组织者只允许好友组参与游戏。

同一时间只能有一个组进行游戏。每次从队首玩家开始组建一个好友组，该组开始游戏，随后从队伍中移除。如此反复，直到队伍为空。形式化地说，如果存在一个数组 $K = [K[0], K[1], \ldots, K[g - 1]]$，使得：

- $g > 0$ 且对于所有 $j$（$0 \leq j < g$），都有 $K[j] > 0$；
- $K[0] + K[1] + \ldots + K[g - 1] = n$；
- 对于每个 $j \in [0, g - 1]$，玩家 $s[j], s[j] + 1, \ldots, s[j] + K[j] - 1$ 构成一个规模为 $K[j]$ 的好友组，其中 $s[0] = 0$，其他情况下 $s[j] = K[0] + K[1] + \ldots + K[j - 1]$；

则称队伍可以被划分为 $g$ 个好友组。

组织者希望 **最小化** 进行游戏的好友组数量。即，他们希望将队伍划分为 $g$ 个好友组，并且无法再划分为 $g - 1$（或更少）个好友组。

你的任务是找到一种将队伍划分为最少好友组的方案，并输出该划分中各组的规模数组。

$2 \leq n \leq 10^5,0 \leq m \leq 2\times 10^5$。

## Solution

首先有个很容易想到的暴力是如果当前需要对 $[l,r]$ 进行划分，则将所有区间内部的边加进去后选择随便一个区间内满足 $i$ 和 $i+1$ 不在同一个连通块的 $i$，然后将区间分治成 $[l,i]$ 和 $[i+1,r]$。如果找不到则说明 $[l,r]$ 是一个答案中的区间。

直接做是 $O(nm)$ 的，考虑优化。

考虑如果已经得到在 $[l,r]$ 内的边，那么根据启发式分裂的思想，从前面和后面同时枚举，找到第一个满足条件的断点 $k$。

然后我们对 $[l,k]$ 和 $[k+1,r]$ 中较长的区间继承当前连的边，较短的直接重构，容易发现这个和重链剖分是一样的，复杂度仍然正确。

对于区间中的边可以直接 LCT 维护，但是有一个更加厉害的做法。

考虑用可撤销并查集维护，维护的数据结构需要支持：往开头加边、往末尾加边、删除最开头加的边、删除最末尾加的边。

做法是直接维护一个栈，栈中的每个元素需要维护一个 $0/1$ 值，表示当前加的边是往开头加的还是往末尾加的。

对于加边操作就直接加入。对于删边则从栈顶往下暴力找到需要删的边，假设是从上往下数第 $x$ 个。

那么如果 $x=0$ 或者 $2x-top\leq 0$ 就重构整个栈，将加入的元素按照顺序从 $mid$ 劈开，前面的看成从开头加，后面的看成从末尾加，然后把栈变成 $01$ 交替的形式。如果 $2x-top\geq 1$，则重构 $[2x-top,top]$ 内的元素，同样是尽量变成 $01$ 交替的形式，但是不改变栈中元素的 $0/1$ 值。

可以证明如果操作数量是 $t$，加边和撤销的总次数是 $O(t\log t)$ 级别。

时间复杂度：$O(m\log^2n\log m)$。

## Code

```cpp
#include <bits/stdc++.h>
#include "boardgames.h"

#ifdef ORZXKR
#include "grader.cpp"
#endif

const int kMaxN = 4e5 + 5, kMaxM = 4e5 + 5;

int n, m, t;
int u[kMaxM], v[kMaxM], L[kMaxN], R[kMaxN];
std::pair<int, int> e[kMaxM * 2];
std::vector<std::pair<int, int>> seg;

struct DSU {
  int fa[kMaxN], rnk[kMaxN];
  std::vector<std::tuple<int, int, bool>> stk;
  void init(int n) {
    stk.clear();
    for (int i = 1; i <= n; ++i) fa[i] = i, rnk[i] = 0;
  }
  int find(int x) {
    for (; x != fa[x]; x = fa[x]) {}
    return x;
  }
  void unionn(int x, int y) {
    int fx = find(x), fy = find(y);
    if (fx == fy) return void(stk.emplace_back(-1, -1, 0));
    if (rnk[fx] > rnk[fy]) std::swap(fx, fy);
    stk.emplace_back(fx, fy, rnk[fx] == rnk[fy]);
    fa[fx] = fy, rnk[fy] += (rnk[fx] == rnk[fy]);
  }
  void undo() {
    assert(stk.size());
    auto [fx, fy, det] = stk.back(); stk.pop_back();
    if (fx == -1) return;
    fa[fx] = fx, rnk[fy] -= det;
  }
} dsu;

struct Deque {
  int top;
  std::array<int, 2> stk[kMaxM * 2];
  void undo() { --top, dsu.undo(); }
  void clear() { while (top) undo(); }
  void link(int id, int op) {
    dsu.unionn(e[id].first, e[id].second), stk[++top] = {id, op};
  }
  void rebuild(int op) {
    static int top1, stk1[kMaxM * 2];
    int del = 0;
    for (int i = top; i; --i) {
      if (!del && stk[i][1] == op) del = i;
    }
    if (!del) del = 1;
    top1 = 0;
    for (int i = top; i; --i) {
      if (i != del && stk[i][1] == 0) stk1[++top1] = stk[i][0];
    }
    for (int i = 1; i <= top; ++i) {
      if (i != del && stk[i][1] == 1) stk1[++top1] = stk[i][0];
    }
    clear();
    int mid = top1 / 2;
    for (int i = 1, p1 = mid, p2 = mid + 1; i <= top1; ++i) {
      if (i & 1) link(stk1[p2++], 1);
      else link(stk1[p1--], 0);
    }
  }
  void rebuild(int x, int op) {
    static int top1, stk1[kMaxM * 2];
    static int top2, stk2[kMaxM * 2];
    int del = 0;
    for (int i = top; i >= x; --i) {
      if (!del && stk[i][1] == op) del = i;
    }
    top1 = top2 = 0;
    for (int i = top; i >= x; --i) {
      if (i != del) {
        if (stk[i][1] == 0) stk1[++top1] = stk[i][0];
        else stk2[++top2] = stk[i][0];
      }
    }
    while (top >= x) undo();
    while (top1 > top2) link(stk1[top1--], 0);
    while (top2 > top1) link(stk2[top2--], 1);
    int tot = top1 + top2;
    for (int i = 1; i <= tot; ++i) {
      if (i & 1) link(stk1[top1--], 0);
      else link(stk2[top2--], 1);
    }
  }
  void push_front(int id) { link(id, 0); }
  void push_back(int id) { link(id, 1); }
  void pop_front() {
    assert(top);
    int x = top;
    for (; x && stk[x][1] != 0; --x) {}
    // rebuild(0);
    if (!x || top - 2 * (top - x) <= 0) rebuild(0);
    else rebuild(top - 2 * (top - x), 0);
  }
  void pop_back() {
    assert(top);
    int x = top;
    for (; x && stk[x][1] != 1; --x) {}
    // rebuild(1);
    if (!x || top - 2 * (top - x) <= 0) rebuild(1);
    else rebuild(top - 2 * (top - x), 1);
  }
} q;

void solve(int l, int r) {
  int id = -1;
  for (int i = 0; i <= r - l - 1; ++i) {
    if (dsu.find(l + i) != dsu.find(l + i + 1)) { id = l + i; break; }
    if (dsu.find(r - i - 1) != dsu.find(r - i)) { id = r - i - 1; break; }
  }
  if (id == -1) return void(seg.emplace_back(l, r));
  if (R[id] <= (L[l] + R[r]) / 2) {
    for (int i = L[l]; i <= R[id]; ++i) q.pop_front();
    solve(id + 1, r);
    q.clear();
    for (int i = L[l]; i <= R[id]; ++i) q.push_back(i);
  // std::cerr << "fuck " << l << ' ' << r << ' ' << id << ' ' << dsu.find(1) << ' ' << dsu.find(2) << '\n';
    solve(l, id);
  } else {
    for (int i = R[r]; i > R[id]; --i) q.pop_back();
    solve(l, id);
    q.clear();
    // for (int i = R[r]; i > R[id]; --i) q.push_front(i);
    for (int i = R[id] + 1; i <= R[r]; ++i) q.push_back(i);
    solve(id + 1, r);
  }
}

std::vector<int> partition_players(int n, int m, std::vector<int> X, std::vector<int> Y) {
  ::n = n, ::m = m;
  dsu.init(n + m);
  for (int i = 1; i <= m; ++i) {
    u[i] = X[i - 1] + 1, v[i] = Y[i - 1] + 1;
    e[++t] = {u[i], i + n}, e[++t] = {v[i], i + n};
  }
  std::sort(e + 1, e + 1 + t);
  for (int i = 1; i <= n; ++i) {
    L[i] = std::lower_bound(e + 1, e + 1 + t, std::pair<int, int>{i, 0}) - e;
    R[i] = std::lower_bound(e + 1, e + 1 + t, std::pair<int, int>{i + 1, 0}) - e - 1;
  }
  for (int i = 1; i <= t; ++i) q.push_back(i);
  solve(1, n);
  std::sort(seg.begin(), seg.end());
  std::vector<int> len;
  for (auto [l, r] : seg) len.emplace_back(r - l + 1);
  return len;
}
```