---
title: CF1672I PermutationForces 题解
date: 2025-03-24 08:47:00
---

## Description

给定一个长度为 $n$ 的排列 $p_1,p_2,\ldots,p_n$，你可以进行如下操作若干次：

- 选择 $1\leq i\leq |p|$ 满足 $|i-p_i|\leq m$；
- 对于所有 $1\leq j\leq |p|$ 的 $j$，若满足 $p_i<p_j$，则 $p_j\leftarrow p_j-1$；
- 之后删去 $p_i$，$p$ 后面的元素向前补位。

求最小的 $m$ 使经过 $n$ 次操作能将 $p$ 删空。

$1\leq n\leq 5\times 10^5$。

## Solution

首先会有一个想法是每次选择 $|i-p_i|$ 最小的进行操作，这么做我们可能会担心操作顺序的影响。但是可以证明这么做就是对的。

不妨设 $f_i=|i-p_i|$，且 $i<p_i$，考虑分讨 $j$ 和 $p_j$ 的取值。有如下几种可能：

1. $i<j<p_j<p_i$，$f_j$ 变为 $f_j+1$。
2. $i<p_j<j<p_i$，$f_j$ 变为 $f_j-1$。
3. $j<i<p_j<p_i$，$f_j$ 不变。
4. $p_j<i<j<p_i$，$f_j$ 变为 $f_j-1$。
5. $j<i<p_i<p_j$，$f_j$ 变为 $f_j-1$。
6. $p_j<i<p_i<j$，$f_j$ 变为 $f_j-1$。
7. $i<j<p_i<p_j$，$f_j$ 不变。
8. $i<p_j<p_i<j$，$f_j$ 不变。
9. $i<p_i<j<p_j$，$f_j$ 不变。
10. $i<p_i<p_j<j$，$f_j$ 不变。

观察这些情况可以发现对于 $f_j\leq f_i$ 的所有情况，操作后都不会大于 $f_i$。而对于 $f_j>f_i$ 的情况，操作后 $f_j$ 都不会变大。

所以每次贪心地选择 $f_i$ 最小的 $i$ 进行操作一定不劣。

暴力维护这个东西是 $O(n\log^2n)$ 或者 $O(n\sqrt n)$，不太能过。

---

考虑优化。

容易发现在操作的过程中 $f_j$ 的正负性一定不会改变，因为在 $f_j=0$ 的时候才会变，但这时一定是能选择 $f_i=0$ 的操作，所以操作完 $j$ 和 $a_j$ 的变化量一定相同，$f_j$ 也就不变了。

所以我们对于 $i\leq a_i$ 和 $i>a_i$ 单独处理。

对于 $i\leq a_i$ 的情况。将 $(i,a_i)$ 看成坐标系上的点，那么如果存在 $j>i,a_j<a_i$，即 $f_i$ 在 $j$ 删掉之前一定不会比 $f_j$ 更优。所以 $f_i$ 可能成为答案当且仅当 $(i,a_i)$ 右下方没有点。

考虑只把可能成为答案的点拿出来，那么这些点都是 $a_i$ 的后缀最小值，且构成一个从左下到右上的递增点列。

由于这个具有单调性，所以用线段树维护这个递增的点列上每个点的答案。

每次删掉一个点后还要更新后缀最小值，容易发现每次只需要暴力在前驱和后继之间找最小值，然后递归即可。

显然每个点在加入之后不会再被删除。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using pii = std::pair<int, int>;

const int kMaxN = 5e5 + 5;

int n, ans;
int a[kMaxN];
std::set<int> st1, st2;
std::set<pii> st3, st4;

struct BIT {
  int c[kMaxN];
  void upd(int x, int v) {
    for (; x <= n; x += x & -x) c[x] += v;
  }
  int qry(int x) {
    int ret = 0;
    for (; x; x -= x & -x) ret += c[x];
    return ret;
  }
} bit1, bit2;

struct SGT {
  int N;
  pii mi[kMaxN * 4];
  void pushup(int x) {
    mi[x] = std::min(mi[x << 1], mi[x << 1 | 1]);
  }
  void build(int n) {
    for (N = 1; N <= n + 1; N <<= 1) {}
    std::fill_n(mi, 2 * N, pii{1e9, 0});
  }
  void update(int x, pii v) {
    mi[x += N] = v;
    for (x >>= 1; x; x >>= 1) pushup(x);
  }
  pii query(int l, int r) {
    if (l > r) return {1e9, 0};
    pii ret = {1e9, 0};
    for (l += N - 1, r += N + 1; l ^ r ^ 1; l >>= 1, r >>= 1) {
      if (~l & 1) ret = std::min(ret, mi[l ^ 1]);
      if (r & 1) ret = std::min(ret, mi[r ^ 1]);
    }
    return ret;
  }
} sgt1, sgt2;

struct SGT_s {
  pii mi[kMaxN * 4];
  int tag[kMaxN * 4];
  void pushup(int x) {
    mi[x] = std::min(mi[x << 1], mi[x << 1 | 1]);
  }
  void addtag(int x, int v) {
    mi[x].first += v, tag[x] += v;
  }
  void pushdown(int x) {
    if (tag[x]) {
      addtag(x << 1, tag[x]), addtag(x << 1 | 1, tag[x]);
      tag[x] = 0;
    }
  }
  void build(int x, int l, int r) {
    if (l == r) return void(mi[x] = {1e9, l});
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }
  void update1(int x, int l, int r, int ql, int v) {
    if (l == r) return void(mi[x].first = v);
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
} sgt3, sgt4;

void rebuild1(int l, int r, int suf) {
  for (; l <= r;) {
    auto p = sgt1.query(l, r);
    // if (p.second) assert(p.first == a[p.second]);
    if (!p.second || p.first > suf) return;
    int x = p.second;
    st1.emplace(x), st3.emplace(a[x], x);
    sgt3.update1(1, 1, n, x, abs((x - bit1.qry(x)) - (a[x] - bit2.qry(a[x]))));
    l = x + 1;
  }
}

void rebuild2(int l, int r, int pre) {
  for (; l <= r;) {
    auto p = sgt2.query(l, r);
    // if (p.second) assert(p.first == -a[p.second]);
    if (!p.second || a[p.second] < pre) return;
    int x = p.second;
    st2.emplace(x), st4.emplace(a[x], x);
    sgt4.update1(1, 1, n, x, abs((x - bit1.qry(x)) - (a[x] - bit2.qry(a[x]))));
    r = x - 1;
  }
}

void upd(int x) {
  sgt3.update2(1, 1, n, x, n, 1), sgt4.update2(1, 1, n, x, n, -1);
  auto it1 = st3.lower_bound({a[x], x}), it2 = st4.lower_bound({a[x], x});
  if (it1 != st3.end()) sgt3.update2(1, 1, n, it1->second, n, -1);
  if (it2 != st4.end()) sgt4.update2(1, 1, n, it2->second, n, 1);
  bit1.upd(x, 1), bit2.upd(a[x], 1);
}

void work(int x) {
  ans = std::max(ans, abs((x - bit1.qry(x)) - (a[x] - bit2.qry(a[x]))));
  if (x <= a[x]) {
    sgt1.update(x, {1e9, 0});
    st1.erase(x), st3.erase({a[x], x});
    sgt3.update1(1, 1, n, x, 1e9);
    auto it = st1.lower_bound(x);
    int nxt = *it, pre = *--it;
    rebuild1(pre + 1, nxt - 1, nxt == n + 1 ? (int)1e9 : a[nxt]);
    upd(x);
  } else {
    sgt2.update(x, {1e9, 0});
    st2.erase(x), st4.erase({a[x], x});
    sgt4.update1(1, 1, n, x, 1e9);
    auto it = st2.lower_bound(x);
    int nxt = *it, pre = *--it;
    rebuild2(pre + 1, nxt - 1, a[pre]);
    upd(x);
  }
  // std::cerr << x << ' ' << ans << ' ' << st3.size() << ' ' << st4.size() << '\n';
}

void prework() {
  st1.emplace(0), st1.emplace(n + 1);
  st2.emplace(0), st2.emplace(n + 1);
  sgt1.build(n), sgt2.build(n);
  sgt3.build(1, 1, n), sgt4.build(1, 1, n);
  for (int i = 1; i <= n; ++i) {
    if (i <= a[i]) sgt1.update(i, {a[i], i});
    else sgt2.update(i, {-a[i], i});
  }
  rebuild1(1, n, 1e9), rebuild2(1, n, 0);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  prework();
  for (int i = 1; i <= n; ++i) {
    work(std::min(sgt3.mi[1], sgt4.mi[1]).second);
  }
  std::cout << ans << '\n';
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