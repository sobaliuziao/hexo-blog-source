---
title: P6109 [Ynoi2009] rprmq1 题解
date: 2024-08-16 14:40:00
---

## Description

有一个 $n \times n$ 的矩阵 $a$，初始全是 $0$，有 $m$ 次修改操作和 $q$ 次查询操作，先进行所有修改操作，然后进行所有查询操作。

一次修改操作会给出 $l_1,l_2,r_1,r_2,x$，代表把所有满足 $l_1 \le i \le r_1$ 且 $l_2 \le j \le r_2$ 的 $a_{i,j}$ 元素加上一个值 $x$。

一次查询操作会给出 $l_1,l_2,r_1,r_2$，代表查询所有满足 $l_1 \le i \le r_1$ 且 $l_2 \le j \le r_2$ 的 $a_{i,j}$ 元素的最大值。

$1\leq n,m\leq 5\times 10^4$，$1\leq q \leq 5\times 10^5$，$1\leq x\leq 2147483647$，$1\leq l_1\leq r_1\leq n$，$1\leq l_2\leq r_2\leq n$。

## Solution

容易发现可以扫描线，但是直接做的话查询时需要维护任意一段时刻内的区间最大值，这显然是做不了的。

但是如果所有的查询 $l_1$ 均相等的话就可以从小到大枚举修改操作和查询的 $r_1$，这样只需要通过[区间加、历史最大值线段树](https://www.cnblogs.com/Scarab/p/18355696)维护当前所有操作的区间历史最大值。

这可以启发我们进行类似猫树分治的做法，从浅到深枚举线段树的每一层，找到所有横跨当前层不同节点的询问放在当前层做，剩下的放到更深层做。

由于横跨当前层不同节点的询问 $[l_1,r_1]$ 一定只跨过两个节点，所以这两个节点可以把它切割成 $[l_1,k]$ 和 $[k+1,r_1]$，对于 $[k+1,r_1]$ 这部分只需要维护一个历史最大值线段树，然后从小到大做修改操作，在每个线段树节点的开头重置历史最大值为当前最大值即可。$[l_1,k]$ 的部分同理。

时间复杂度：$O(n\log^2n+q\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 5e4 + 5, kMaxQ = 5e5 + 5;

int n, m, q;
int l1[kMaxQ], r1[kMaxQ], l2[kMaxQ], r2[kMaxQ], ans[kMaxQ];
bool vis[kMaxQ];
std::vector<std::tuple<int, int, int, int, int>> ud;
std::vector<std::tuple<int, int, int>> qq[kMaxN], vec[kMaxN];

struct SGT {
  int maxa[kMaxN * 8], maxb[kMaxN * 8], tag1[kMaxN * 8], tag2[kMaxN * 8], tagr[kMaxN * 8];

  void pushup(int x) {
    maxa[x] = std::max(maxa[x << 1], maxa[x << 1 | 1]);
    maxb[x] = std::max(maxb[x << 1], maxb[x << 1 | 1]);
  }

  void addtag(int x, int v1, int v2) {
    maxb[x] = std::max(maxb[x], maxa[x] + v2);
    tag2[x] = std::max(tag2[x], tag1[x] + v2);
    maxa[x] += v1, tag1[x] += v1;
  }

  void reset(int x) {
    addtag(x << 1, tag1[x], tag2[x]), addtag(x << 1 | 1, tag1[x], tag2[x]);
    maxb[x] = maxa[x], tagr[x] = 1;
    tag1[x] = tag2[x] = 0;
  }

  void pushdown(int x) {
    if (tagr[x]) {
      reset(x << 1), reset(x << 1 | 1);
      tagr[x] = 0;
    }
    if (tag1[x] || tag2[x]) {
      addtag(x << 1, tag1[x], tag2[x]), addtag(x << 1 | 1, tag1[x], tag2[x]);
      tag1[x] = tag2[x] = 0;
    }
  }

  void build(int x, int l, int r) {
    maxa[x] = maxb[x] = tag1[x] = tag2[x] = tagr[x] = 0;
    if (l == r) return;
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
  }

  void update(int x, int l, int r, int ql, int qr, int v) {
    if (l > qr || r < ql) return;
    else if (l >= ql && r <= qr) return addtag(x, v, std::max<int>(v, 0));
    pushdown(x);
    int mid = (l + r) >> 1;
    update(x << 1, l, mid, ql, qr, v), update(x << 1 | 1, mid + 1, r, ql, qr, v);
    pushup(x);
  }

  int query(int x, int l, int r, int ql, int qr) {
    if (l > qr || r < ql) return 0;
    else if (l >= ql && r <= qr) return maxb[x];
    pushdown(x);
    int mid = (l + r) >> 1;
    return std::max(query(x << 1, l, mid, ql, qr), query(x << 1 | 1, mid + 1, r, ql, qr));
  }
} sgt;

void solve(int d) {
  for (int i = 1; i <= n; ++i) vec[i].clear(), qq[i].clear();
  for (auto [l1, r1, l2, r2, x] : ud)
    vec[l1].emplace_back(l2, r2, x), vec[r1 + 1].emplace_back(l2, r2, -x);
  for (int i = 1; i <= q; ++i) {
    if (!vis[i] && ((l1[i] >> d) != (r1[i] >> d) || !d)) {
      if (l1[i] != r1[i]) assert((l1[i] >> d) == (r1[i] >> d) - 1);
      qq[r1[i]].emplace_back(i, l2[i], r2[i]);
    }
  }
  sgt.build(1, 1, n);
  for (int i = 1; i <= n; ++i) {
    for (auto [l, r, v] : vec[i]) {
      if (v < 0) sgt.update(1, 1, n, l, r, v);
    }
    for (auto [l, r, v] : vec[i]) {
      if (v >= 0) sgt.update(1, 1, n, l, r, v);
    }
    if (i % (1 << d) == 0) sgt.reset(1);
    for (auto [id, l, r] : qq[i]) ans[id] = std::max(ans[id], sgt.query(1, 1, n, l, r));
  }

  for (int i = 1; i <= n; ++i) vec[i].clear(), qq[i].clear();
  for (auto [l1, r1, l2, r2, x] : ud)
    vec[r1].emplace_back(l2, r2, x), vec[l1 - 1].emplace_back(l2, r2, -x);
  for (int i = 1; i <= q; ++i) {
    if (!vis[i] && ((l1[i] >> d) != (r1[i] >> d) || !d)) {
      if (l1[i] != r1[i]) assert((l1[i] >> d) == (r1[i] >> d) - 1);
      vis[i] = 1;
      qq[l1[i]].emplace_back(i, l2[i], r2[i]);
    }
  }
  sgt.build(1, 1, n);
  for (int i = n; i; --i) {
    for (auto [l, r, v] : vec[i]) {
      if (v < 0) sgt.update(1, 1, n, l, r, v);
    }
    for (auto [l, r, v] : vec[i]) {
      if (v >= 0) sgt.update(1, 1, n, l, r, v);
    }
    if (i % (1 << d) == (1 << d) - 1) sgt.reset(1);
    for (auto [id, l, r] : qq[i]) ans[id] = std::max(ans[id], sgt.query(1, 1, n, l, r));
  }
}

void dickdreamer() {
  std::cin >> n >> m >> q;
  for (int i = 1; i <= m; ++i) {
    int l1, l2, r1, r2, x;
    std::cin >> l1 >> l2 >> r1 >> r2 >> x;
    ud.emplace_back(l1, r1, l2, r2, x);
  }
  for (int i = 1; i <= q; ++i)
    std::cin >> l1[i] >> l2[i] >> r1[i] >> r2[i];
  for (int i = std::__lg(n) + 1; ~i; --i) {
    solve(i);
  }
  for (int i = 1; i <= q; ++i) std::cout << ans[i] << '\n';
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