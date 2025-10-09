---
title: 'P13693 [CEOI 2025] Equal Mex 题解'
date: 2025-09-16 15:44:00
---

## Description

罗马尼亚贵族们普遍认为，一个整数数组 $a[0], a[1], a[2], \ldots, a[m - 1]$ 的**美丽值**定义为：满足以下条件的正整数 $k$ 的个数——你可以将该数组划分为 $k$ 个互不重叠的子数组（即连续元素的序列），使得：

1. 每个元素恰好属于一个子数组；
2. 所有子数组具有相同的**最小缺失元素**。

这里，一个整数数组的**最小缺失元素**是指数组中没有出现的、严格大于 $0$ 的最小正整数。

给定一个整数数组 $v[0], v[1], \ldots, v[n - 1]$，以及 $q$ 个询问，每个询问的形式为 $(l_i, r_i)$，其中对所有 $0 \leq i < q$，均有 $1 \leq l_i \leq r_i \leq n$。

对于每个询问，你需要求出数组 $v[l_i - 1], v[l_i ], \ldots, v[r_i - 1]$ 的美丽值。

## Solution

单次询问等价于问 $[l_i,r_i]$ 可以划分成至多多少个区间，满足每个区间的 $\text{mex}$ 为 $\text{mex}[l_i,r_i]$。

有个经典结论是“极短 mex 区间”只有 $O(n)$  个，这里的“极短 mex 区间”指的是所有的区间 $[l,r]$，满足 $\text{mex}[l,r]\neq\text{mex}[l,r-1]$ 且 $\text{mex}[l,r]\neq \text{mex}[l+1,r]$。

证明考虑构造性证明，我们去找到所有的这样的区间 $[l,r]$。先预处理出所有 $\text{mex}[1,i]$ 的值，然后从小到大枚举左端点 $l$，用 ODT 维护所有 $\text{mex}[l,r]$ 的值。

每次删掉 $a_l$ 时，相当于是对于 $val_i\leftarrow\max(val_i,a_l)(l+1\leq i\leq nxt_l-1)$，$nxt_i$ 为 $i$ 后面第一个和 $a_i$ 相等的位置。由于 $val_i$ 具有单调性，所以在 ODT 上 split 出来后直接暴力枚举区间修改即可。而对于所有修改区间 $[l',r',v](v>a_l)$，都对应了唯一一个极短区间 $[l,l']$。

也就是说极短区间数量和 ODT 的复杂度是一样的，都是 $O(n)$。

由于所有极短区间不存在包含关系，所以对于 $\text{mex}$ 相同的直接倍增跳即可。

时间复杂度：$O((n+q)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include "grader.cpp"
#endif

const int kMaxN = 6e5 + 5;

int n, q, b;
int a[kMaxN], l[kMaxN], r[kMaxN], res[kMaxN], mex[kMaxN];
std::vector<int> qq[kMaxN];
std::vector<std::pair<int, int>> seg[kMaxN];
std::vector<std::array<int, 20>> nxt[kMaxN];

struct ODT {
  std::set<std::pair<int, int>> st;
  void init(int n, int *a) {
    st.clear();
    for (int i = 1; i <= n; ++i)
      if (i == 1 || a[i] != a[i - 1])
        st.emplace(i, a[i]);
  }
  void split(int x) {
    if (x < 1 || x > n) return;
    auto [p, v] = *--st.lower_bound({x + 1, 0});
    if (p != x) st.emplace(x, v);
  }
  void fix(int x) {
    return;
    auto it = st.lower_bound({x, 0});
    std::vector<std::pair<int, int>> vec;
    int c = 0;
    for (auto i = it; i != st.end() && c <= 3; ++i, ++c) {
      if (i != st.begin() && i->second == prev(i)->second) vec.emplace_back(*i);
    }
    c = 0;
    if (it != st.begin()) {
      for (auto i = prev(it); i != st.begin() && c <= 3; --i, ++c) {
        if (i ->second == prev(i)->second) vec.emplace_back(*it);
      }
    }
    for (auto p : vec) st.erase(p);
  }
  std::vector<std::pair<int, int>> chkmin(int x, int v) {
    // 对 [1, x] chkmin v
    split(x + 1);
    auto it = --st.lower_bound({x + 1, 0});
    std::vector<std::pair<int, int>> vec;
    for (;; --it) {
      if (it->second > v) vec.emplace_back(*it);
      else break;
      if (it == st.begin()) break;
    }
    if (!vec.size()) return fix(x + 1), vec;
    std::reverse(vec.begin(), vec.end());
    for (auto p : vec) st.erase(p);
    st.emplace(vec[0].first, v);
    fix(x + 1);
    return vec;
  }
  int query(int x) {
    auto it = --st.lower_bound({x + 1, 0});
    return it->second;
  }
} odt;

void getseg() {
  static int cnt[kMaxN] = {0}, now[kMaxN], lst[kMaxN], nxt[kMaxN] = {0};
  for (int i = 1; i <= n; ++i) ++cnt[a[i]];
  for (int i = 1; i <= 4e5 + 1; ++i) {
    lst[i] = n + 1;
    if (!cnt[i]) {
      now[n] = i; break;
    }
  }
  for (int i = n; i > 1; --i) {
    now[i - 1] = now[i];
    if (!--cnt[a[i]]) now[i - 1] = std::min(now[i - 1], a[i]);
  }
  for (int i = n; i; --i) nxt[i] = lst[a[i]], lst[a[i]] = i;
  // for (int i = 1; i <= n; ++i) std::cerr << now[i] << " \n"[i == n];
  odt.init(n, now);
  for (int i = 1; i <= n; ++i) {
    for (auto id : qq[i]) mex[id] = odt.query(r[id]);
    std::vector<std::pair<int, int>> vec = odt.chkmin(nxt[i] - 1, a[i]);
    for (auto [p, v] : vec) seg[v].emplace_back(i, p);
  }
  // for (auto [l, r] : seg[4]) std::cerr << l << ' ' << r << '\n';
}

void getnxt() {
  for (int i = 1; i <= n + 1; ++i) {
    std::sort(seg[i].begin(), seg[i].end());
    nxt[i].resize(seg[i].size());
    for (int j = (int)seg[i].size() - 1; ~j; --j) {
      nxt[i][j][0] = std::lower_bound(seg[i].begin(), seg[i].end(), std::pair<int, int>{seg[i][j].second + 1, 0}) - seg[i].begin();
      for (int k = 1; k <= std::__lg(n); ++k) {
        if (nxt[i][j][k - 1] == seg[i].size()) nxt[i][j][k] = seg[i].size();
        else nxt[i][j][k] = nxt[i][nxt[i][j][k - 1]][k - 1];
      }
    }
  }
}

void solve() {
  for (int i = 1; i <= q; ++i) {
    if (mex[i] == 1) {
      res[i] = r[i] - l[i] + 1;
      continue;
    }
    int mex = ::mex[i], p = std::lower_bound(seg[mex].begin(), seg[mex].end(), std::pair<int, int>{l[i], 0}) - seg[mex].begin();
    int ans = 0;
    if (p < seg[mex].size()) {
      for (int j = std::__lg(n); ~j; --j) {
        assert(p < nxt[mex].size());
        // std::cerr << seg[mex].size() << ' ' << j << ' ' << p << ' ' << nxt[mex][p][j] << '\n';
        if (nxt[mex][p][j] != seg[mex].size() && seg[mex][nxt[mex][p][j]].second <= r[i]) {
          p = nxt[mex][p][j], ans += (1 << j);
        }
      }
    }
    res[i] = ans + 1;
  }
}

std::vector<int> solve(int n, std::vector<int> &v, int q, std::vector<std::pair<int, int>> &queries) {
  ::n = n, ::q = q;
  for (int i = 1; i <= n; ++i) a[i] = v[i - 1];
  for (int i = 1; i <= q; ++i) {
    std::tie(l[i], r[i]) = queries[i - 1];
    ++l[i], ++r[i];
    qq[l[i]].emplace_back(i);
    // std::cerr << l[i] << ' ' << r[i] << '\n';
  }
  getseg(), getnxt(), solve();
  std::vector<int> ans;
  for (int i = 1; i <= q; ++i) ans.emplace_back(res[i]);
  return ans;
}
```