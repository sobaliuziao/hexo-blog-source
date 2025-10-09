---
title: CF1764H Doremy&#39;s Paint 2 题解
date: 2025-08-22 20:15:00
---

## Description

Doremy 有 $n$ 个油漆桶，用一个长度为 $n$ 的数组 $a$ 表示。第 $i$ 个桶中油漆的颜色为 $a_i$。初始时，$a_i = i$。

Doremy 有 $m$ 个区间 $[l_i, r_i]$（$1 \le l_i \le r_i \le n$）。每个区间描述一次操作。第 $i$ 次操作如下：

- 对于所有满足 $l_i < j \leq r_i$ 的 $j$，将 $a_j$ 赋值为 $a_{l_i}$。

Doremy 还会选择一个整数 $k$。她想知道，对于每个 $x$ 从 $0$ 到 $m-1$，在从初始数组出发，依次执行操作 $x \bmod m +1, (x+1) \bmod m + 1, \ldots, (x+k-1) \bmod m +1$ 后，数组中有多少种不同的颜色。你能帮她计算这些值吗？注意，对于每个 $x$，都要从初始数组重新开始，仅执行这 $k$ 次指定顺序的操作。

$1\leq n,m\leq 2\times 10^5$。

## Solution

记录一下题解的做法。

先断环为链，注意到正着做覆盖不好做，就考虑倒着做。

假设已经扫到第 $t+1$ 号区间了，我们维护 $f_i$ 表示从 $t+1$ 操作做到第 $2m$ 次操作，初始的第 $i$ 个元素的贡献消失的时刻。

现在操作第 $t$ 号区间 $[L,R]$，对数组的修改即为：

1. $\displaystyle f_L\leftarrow\max_{i=L}^{R}{f_i}$
2. $\forall i\in[L+1,R],f_i\leftarrow t$

这个东西用 odt 维护即可。

$O((n+m)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using pii = std::pair<int, int>;

const int kMaxN = 4e5 + 5;

int n, m, k;
int l[kMaxN], r[kMaxN], id[kMaxN], pre[kMaxN];

struct Tree {
  int lim, res, dfn_cnt, dfn[kMaxN], st[kMaxN][20], cnt[kMaxN];
  std::vector<int> G[kMaxN];

  int get(int x, int y) { return dfn[x] < dfn[y] ? x : y; }
  void dfs(int u, int fa) {
    st[dfn[u] = ++dfn_cnt][0] = fa;
    for (auto v : G[u]) {
      if (v == fa) continue;
      dfs(v, u);
    }
  }
  int LCA(int x, int y) {
    if (x == y) return x;
    if (dfn[x] > dfn[y]) std::swap(x, y);
    int k = std::__lg(dfn[y] - dfn[x]);
    return get(st[dfn[x] + 1][k], st[dfn[y] - (1 << k) + 1][k]);
  }
  void build() {
    for (int i = 1; i <= 2 * m; ++i) G[pre[i]].emplace_back(i);
    dfs(0, 2 * m + 1);
    for (int i = 1; i <= std::__lg(2 * m + 1); ++i)
      for (int j = 1; j <= 2 * m + 1 - (1 << i) + 1; ++j)
        st[j][i] = get(st[j][i - 1], st[j + (1 << (i - 1))][i - 1]);
  }
  void upd(int x, int v) {
    // std::cerr << "upd " << x << ' ' << v << '\n';
    if (x < lim) res += v;
    else cnt[x] += v;
    // res += v;
  }
  void setlim(int _lim) {
    for (; lim < _lim; ++lim) res += cnt[lim];
  }
  int query() { return res; }
} tr;

struct ODT {
  bool op = 0;
  std::set<std::pair<int, int>> st;
  void init(int n, bool _op) {
    st.clear(), st.emplace(1, 0), st.emplace(n + 1, 0);
    op = _op;
    if (op) tr.upd(0, n - 1);
  }
  void split(int x) {
    auto it = --st.lower_bound({x + 1, 0});
    if (x != it->first) st.emplace(x, it->second);
  }
  int getval(int x) { return (--st.lower_bound({x + 1, 0}))->second; }
  void upd(int l, int r, int v) {
    split(l), split(r + 1);
    std::vector<std::pair<int, int>> vec;
    for (auto it = st.lower_bound({l, 0}); it->first != r + 1; ++it)
      vec.emplace_back(*it);
    int pre = -1, nxt = -1;
    if (l > 1) pre = getval(l - 1);
    if (r < n) nxt = getval(r + 1);
    for (int i = 0; i < vec.size(); ++i) {
      int cnt = (i + 1 == vec.size() ? (r + 1) : vec[i + 1].first) - vec[i].first;
      if (op) {
        tr.upd(vec[i].second, -(cnt - 1));
        if (i) tr.upd(tr.LCA(vec[i].second, vec[i - 1].second), -1);
        else if (l > 1) tr.upd(tr.LCA(vec[i].second, pre), -1);
        if (i + 1 == vec.size() && r < n) tr.upd(tr.LCA(vec[i].second, nxt), -1);
      }
    }
    for (auto p : vec) st.erase(p);
    st.emplace(l, v);
    if (op) {
      tr.upd(v, r - l);
      if (l > 1) tr.upd(tr.LCA(v, pre), 1);
      if (r < n) tr.upd(tr.LCA(v, nxt), 1);
    }
  }
} odt;

void dickdreamer() {
  std::cin >> n >> m >> k;
  for (int i = 1; i <= m; ++i) {
    std::cin >> l[i] >> r[i];
    l[i + m] = l[i], r[i + m] = r[i];
  }
  odt.init(n, 0);
  for (int i = 1; i <= 2 * m; ++i) {
    pre[i] = odt.getval(l[i]);
    odt.upd(l[i], r[i], i);
  }
  tr.build(), odt.init(n, 1);
  // std::cerr << tr.query() << '\n';
  for (int i = 1; i <= 2 * m; ++i) {
  // for (int i = 1; i <= 2; ++i) {
    odt.upd(l[i], r[i], i), tr.setlim(i - k + 1);
    // std::cerr << tr.query() << '\n';
    // for (auto [x, v] : odt.st) std::cerr << "fuck " << x << ' ' << v << '\n';
    // std::cerr << "---------------\n";
    if (i >= k && i <= k + m - 1) std::cout << tr.query() + 1 << ' ';
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