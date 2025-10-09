---
title: 'CF1270H Number of Components 题解'
date: 2024-09-23 15:16:00
---

## Description

给一个长度为 $n$ 的数组 $a$，$a$ 中的元素两两不同。

对于每个数对 $(i,j)(i<j)$，若 $a_i<a_j$，则让 $i$ 向 $j$ 连一条边。求图中连通块个数。

支持 $q$ 次修改数组某个位置的值，每次修改后输出图中连通块个数。

$n,q\le 5\times 10^5,1\le a_i\le 10^6$，保证任意时刻数组中元素两两不同。

## Solution

考虑怎么求一个序列有几个连通块。

首先有个性质是每个连通块一定是一个区间，证明就考虑钦定 $i<k<j$ 且 $i$ 和 $j$ 连通。如果 $a_i<a_j$，则 $a_i<a_k$ 和 $a_k<a_j$ 必定满足至少一个。

如果 $a_i>a_j$，由于 $i,j$ 连通，所以一定存在 $x<i$ 且 $a_i>a_j>a_x$ 或 $x>j$ 且 $a_x>a_i>a_j$。这样就规约到了 $a_i<a_j$ 的情况。故结论得证。

所以连通块数就是满足 $\min_{i=1}^{k}{a_i}>\max_{i=k+1}^{n}{a_i}$ 的 $k$ 的数量。

考虑枚举前缀的最小值 $x$，将 $a$ 数组中大于等于 $x$ 的位置设成 $1$，小于 $x$ 的位置设成 $0$，则合法的 $x$ 一定满足 $01$ 序列为 $11110000$ 的形式，即 $10$ 的出现次数为 $1$。

设 $cnt_x$ 表示 $x$ 的 $01$ 序列中 $10$ 的出现次数。于是题目转化为求对于所有在 $a$ 数组中出现了的 $x$ 中 $cnt_x=1$ 的 $x$ 的数量，维护一个值域的线段树即可。

时间复杂度：$O\left((n+q)\log n\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e6 + 5;

int n, q, m;
int a[kMaxN], pos[kMaxN], x[kMaxN], unq[kMaxN];

struct SGT {
  int mi[kMaxN * 4], tag[kMaxN * 4], tot[kMaxN * 4], cnt[kMaxN * 4];

  void pushup(int x) {
    mi[x] = std::min(tot[x << 1] ? mi[x << 1] : 1e9, tot[x << 1 | 1] ? mi[x << 1 | 1] : 1e9);
    tot[x] = tot[x << 1] + tot[x << 1 | 1];
    cnt[x] = 0;
    if (tot[x << 1] && mi[x] == mi[x << 1]) cnt[x] += cnt[x << 1];
    if (tot[x << 1 | 1] && mi[x] == mi[x << 1 | 1]) cnt[x] += cnt[x << 1 | 1];
  }

  void addtag(int x, int v) {
    mi[x] += v, tag[x] += v;
  }

  void pushdown(int x) {
    if (tag[x])
      addtag(x << 1, tag[x]), addtag(x << 1 | 1, tag[x]), tag[x] = 0;
  }

  void build(int x, int l, int r) {
    if (l == r) return void(cnt[x] = 1);
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }

  void update1(int x, int l, int r, int ql, int v) {
    if (l == r) return void(tot[x] = v);
    pushdown(x);
    int mid = (l + r) >> 1;
    if (ql <= mid) update1(x << 1, l, mid, ql, v);
    else update1(x << 1 | 1, mid + 1, r, ql, v);
    pushup(x);
  }

  void update2(int x, int l, int r, int ql, int qr, int v) {
    if (l > qr || r < ql) return;
    else if (l >= ql && r <= qr) return addtag(x, v);
    pushdown(x);
    int mid = (l + r) >> 1;
    update2(x << 1, l, mid, ql, qr, v), update2(x << 1 | 1, mid + 1, r, ql, qr, v);
    pushup(x);
  }

  int query() { return tot[1] && mi[1] == 1 ? cnt[1] : 0; }
} sgt;

void discrete() {
  for (int i = 0; i <= n + 1; ++i) unq[++m] = a[i];
  for (int i = 1; i <= q; ++i) unq[++m] = x[i];
  std::sort(unq + 1, unq + 1 + m);
  m = std::unique(unq + 1, unq + 1 + m) - unq;

  for (int i = 0; i <= n + 1; ++i)
    a[i] = std::lower_bound(unq + 1, unq + 1 + m, a[i]) - unq;
  for (int i = 1; i <= q; ++i)
    x[i] = std::lower_bound(unq + 1, unq + 1 + m, x[i]) - unq;
}

void update(int x, int y, int v) {
  if (x > y) sgt.update2(1, 1, m, y + 1, x, v);
}

void dickdreamer() {
  std::cin >> n >> q;
  a[0] = 1e9, a[n + 1] = -1e9;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= q; ++i) std::cin >> pos[i] >> x[i];
  discrete();
  sgt.build(1, 1, m);
  for (int i = 1; i <= n; ++i) sgt.update1(1, 1, m, a[i], 1);
  for (int i = 0; i <= n; ++i) update(a[i], a[i + 1], 1);
  for (int i = 1; i <= q; ++i) {
    update(a[pos[i] - 1], a[pos[i]], -1), update(a[pos[i]], a[pos[i] + 1], -1);
    sgt.update1(1, 1, m, a[pos[i]], 0);
    a[pos[i]] = x[i];
    update(a[pos[i] - 1], a[pos[i]], 1), update(a[pos[i]], a[pos[i] + 1], 1);
    sgt.update1(1, 1, m, a[pos[i]], 1);
    std::cout << sgt.query() << '\n';
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