---
title: 'CF1209G2 Into Blocks (hard version) 题解'
date: 2024-02-28 17:16:00
---

## Description

给你 $n$ , $q$，$n$ 表示序列长度，$q$ 表示操作次数。

我们需要达成这么一个目标状态：
如果存在 $x$ 这个元素，那么必须满足所有 $x$ 元素都必须在序列中连续。

然后你可以进行这么一种操作，将所有的 $x$ 元素的变为任意你指定的 $y$ 元素，并且花费 $cnt[x]$ 的花费，$cnt[x]$ 代表 $x$ 元素的个数。

现在有 $q$ 次询问，每次询问单点修改一个位置的值，求修改完之后最小花费使得序列满足目标状态。

注意：更新不是独立的，之前的更新会保留。

$1\leq n\leq 2\times 10^5,0\leq q\leq 2\times 10^5$

## Solution

先考虑对于一个序列怎么求答案。

显然是把整个序列先划分成若干个最短的区间使得区间内部里出现过的颜色的所有位置都在这个区间里，答案就是 $n$ 减每个区间颜色出现次数的最大值。

考虑怎么去刻画这个区间。

先不考虑长度是 $1$ 的区间，不妨设 $l_i$ 表示颜色 $i$ 第一次出现的位置，$r_i$ 表示颜色 $i$ 最后一次出现的位置，$b_i$ 表示位置 $i$ 被多少个区间 $[l_j,r_j)$ 覆盖，$w_i$ 表示 $a_i$ 这个颜色的出现次数。

那么每个合法的区间 $[l,r]$ 一定满足 $b_l,b_{l+1},\dots,b_{r-1}$ 都不为 $0$，所以每个 $[l,r]$ 都可以用 $b$ 数组的最长非零区间表示，由于必定会有一个颜色在 $[l,r]$ 中出现至少 $2$ 次，所以 $[l,r]$ 对答案的贡献就是 $\max\{w_l,w_{l+1},\dots,w_{r-1}\}$。

现在考虑用线段树维护这个东西。

设 $minb_i$ 表示 $i$ 这个区间 $b$ 的最小值，$maxw_i$ 表示区间内 $w$ 的最大值，$sum_i$ 表示区间内的贡献之和。

容易发现 $b_n=0$，所以 $minb_1=0$，那么总贡献就是 $sum_1$。

但是线段树需要支持合并，所以只要再维护区间前缀还没确定的贡献和后缀还没确定的贡献（这个贡献不能包含左端点）。

修改相当于就是删除或加入 $[l_c,r_c)$，并且每次只要修改每个颜色第一次出现的位置的 $w$，因为求区间 max 时一定会在第一次出现的位置贡献到。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5;

int n, q;
int a[kMaxN];
std::set<int> st[kMaxN];

struct SGT {
  int mi[kMaxN * 4], lmx[kMaxN * 4], rmx[kMaxN * 4], mx[kMaxN * 4], sum[kMaxN * 4], tag[kMaxN * 4];

  void pushup(int x) {
    mi[x] = std::min(mi[x << 1], mi[x << 1 | 1]);
    mx[x] = std::max(mx[x << 1], mx[x << 1 | 1]);
    if (mi[x << 1] < mi[x << 1 | 1]) {
      lmx[x] = lmx[x << 1], rmx[x] = std::max(rmx[x << 1], mx[x << 1 | 1]);
      sum[x] = sum[x << 1];
    } else if (mi[x << 1] > mi[x << 1 | 1]) {
      rmx[x] = rmx[x << 1 | 1], lmx[x] = std::max(lmx[x << 1 | 1], mx[x << 1]);
      sum[x] = sum[x << 1 | 1];
    } else {
      lmx[x] = lmx[x << 1], rmx[x] = rmx[x << 1 | 1];
      sum[x] = sum[x << 1] + sum[x << 1 | 1] + std::max(rmx[x << 1], lmx[x << 1 | 1]);
    }
  }

  void addtag(int x, int v) {
    tag[x] += v, mi[x] += v;
  }

  void pushdown(int x) {
    if (!tag[x]) return;
    addtag(x << 1, tag[x]), addtag(x << 1 | 1, tag[x]);
    tag[x] = 0;
  }

  void update1(int x, int l, int r, int ql, int qr, int v) {
    if (l > qr || r < ql) {
      return;
    } else if (l >= ql && r <= qr) {
      return addtag(x, v);
    }
    pushdown(x);
    int mid = (l + r) >> 1;
    update1(x << 1, l, mid, ql, qr, v), update1(x << 1 | 1, mid + 1, r, ql, qr, v);
    pushup(x);
  }

  void update2(int x, int l, int r, int ql, int v) {
    if (l == r) return void(mx[x] = lmx[x] = v);
    pushdown(x);
    int mid = (l + r) >> 1;
    if (ql <= mid) update2(x << 1, l, mid, ql, v);
    else update2(x << 1 | 1, mid + 1, r, ql, v);
    pushup(x);
  }
} sgt;

void upd(int x, int v) {
  int val = a[x];
  if (!st[val].empty()) {
    sgt.update1(1, 1, n, *st[val].begin(), *prev(st[val].end()) - 1, -1);
    sgt.update2(1, 1, n, *st[val].begin(), 0);
  }
  if (v == 1) st[val].emplace(x);
  else st[val].erase(x);
  if (!st[val].empty()) {
    sgt.update1(1, 1, n, *st[val].begin(), *prev(st[val].end()) - 1, 1);
    sgt.update2(1, 1, n, *st[val].begin(), st[val].size());
  }
}

void dickdreamer() {
  std::cin >> n >> q;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    st[a[i]].emplace(i);
  }
  for (int i = 1; i <= 2e5; ++i) {
    if (!st[i].size()) continue;
    sgt.update1(1, 1, n, *st[i].begin(), *prev(st[i].end()) - 1, 1);
    sgt.update2(1, 1, n, *st[i].begin(), st[i].size());
  }
  std::cout << n - sgt.lmx[1] - sgt.rmx[1] - sgt.sum[1] << '\n';
  for (int i = 1; i <= q; ++i) {
    int x, y;
    std::cin >> x >> y;
    upd(x, -1), a[x] = y, upd(x, 1);
    std::cout << n - sgt.lmx[1] - sgt.rmx[1] - sgt.sum[1] << '\n';
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