---
title: P9062 [Ynoi2002] Adaptive Hsearch&amp;Lsearch 题解
date: 2025-04-13 16:16:00
---

## Description

有 $n$ 个点 $p_1,p_2,\dots,p_n$ 在二维平面上。

有 $q$ 次询问，在第 $i$ 个询问中，给定两个数 $l_i,r_i$ ($1\leq l_i< r_i\leq n$)，你需要找到一对 $(u,v)$ 满足 $l_i\leq u<v\leq r_i$，$p_u$ 和 $p_v$ 之间的欧几里得距离 $\sqrt{(x_u-x_v)^2+(y_u-y_v)^2}$ 最小。

$n,q\leq 2.5\times 10^5$。

## Solution

平面最近点对有一个做法是分别按照 $d^0\times d^0,d^1\times d^1,\ldots,d^c\times d^c$ 对二维平面进行分块，每次新加入一个点 $i$，对所有 $0\leq k\leq c$，选择所有 $i$ 所在块周围的 $3\times 3$ 个相邻块中的点更新。

更新后把这些相邻块中与 $i$ 距离小于 $d^{k-1}$ 的点删掉。

这个做法保证了每个对于所有 $k$，每个块中的点数都是一个比较小的量级。正确性就考虑设 $x<y<z$，假设 $(x,z)$ 对答案有贡献，就说明所有 $y\in[x+1,z-1]$，都满足 $dis(x,y)\geq dis(x,z)$。

但是有可能对于一个 $k$，如果 $dis(x,z)\leq dis(x,y)<d^{k-1}$，此时 $x$ 会在 $y$ 加入后被删掉，在 $z$ 插入时就找不到 $x$ 了。

对于这种情况，可以发现将 $k$ 缩小到 $dis(x,y)\geq d^{k-1}$ 时 $x$ 就不会被删掉了，由于这些 $dis$ 都大于等于 $1$，所以一定能找到这样的 $k$，也就说明每个可能的有效点对都会被计算到。

容易发现总共有 $O(n\log V)$ 个点对，用分块+扫描线维护答案即可。

时间复杂度：$O(n\log V+q\sqrt n)$。

## Code

```cpp
#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/hash_policy.hpp>

// #define int int64_t

using i64 = int64_t;

struct custom_hash {
  static uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
    x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
    return x ^ (x >> 31);
  }
  size_t operator()(uint64_t x) const {
    static const uint64_t FIXED_RANDOM = std::chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x + FIXED_RANDOM);
  }
  size_t operator()(std::pair<uint64_t, uint64_t> x) const {
    static const uint64_t FIXED_RANDOM = std::chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x.first + FIXED_RANDOM) ^
           (splitmix64(x.second + FIXED_RANDOM) >> 1);
  }
  size_t operator()(std::tuple<uint64_t, uint64_t, uint64_t> x) const {
    static const uint64_t FIXED_RANDOM = std::chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(std::get<0>(x) + FIXED_RANDOM) ^
           (splitmix64(std::get<1>(x) + FIXED_RANDOM) >> 1) ^
           (splitmix64(std::get<2>(x) + FIXED_RANDOM) >> 2);
  }
};

const int kMaxN = 2.5e5 + 5, kMaxB = 505;

int n, q;
int x[kMaxN], y[kMaxN];
i64 ans[kMaxN];
std::vector<int> vv[kMaxN];
std::vector<std::pair<int, int>> qq[kMaxN];

void chkmin(i64 &x, i64 y) { x = (x < y ? x : y); }

struct Block {
  int b, tot, bel[kMaxN], L[kMaxB], R[kMaxB];
  i64 mi1[kMaxB], mi2[kMaxN];
  void init(int n) {
    b = sqrtl(n);
    if (!b) ++b;
    tot = (n + b - 1) / b;
    for (int i = 1; i <= tot; ++i) {
      L[i] = (i - 1) * b + 1, R[i] = std::min(i * b, n);
      mi1[i] = 1e18;
      for (int j = L[i]; j <= R[i]; ++j)
        bel[j] = i, mi2[j] = 1e18;
    }
  }
  void update(int x, i64 v) {
    chkmin(mi1[bel[x]], v), chkmin(mi2[x], v);
  }
  i64 query(int x) {
    i64 ret = 1e18;
    for (int i = bel[x] + 1; i <= tot; ++i) chkmin(ret, mi1[i]);
    for (int i = x; i <= R[bel[x]]; ++i) chkmin(ret, mi2[i]);
    return ret;
  }
} t;

i64 getdis(int i, int j) {
  return (i64)(x[i] - x[j]) * (x[i] - x[j]) + (i64)(y[i] - y[j]) * (y[i] - y[j]);
}

void getans() {
  t.init(n);
  for (int i = 1; i <= n; ++i) {
    for (auto j : vv[i]) t.update(j, getdis(i, j));
    for (auto [j, id] : qq[i]) ans[id] = t.query(j);
  }
}

void dickdreamer() {
  std::cin >> n >> q;
  for (int i = 1; i <= n; ++i) std::cin >> x[i] >> y[i];
  for (int k = 0, d = 4, pw = 1; pw <= 2e8; ++k, pw *= d) {
    __gnu_pbds::gp_hash_table<std::pair<int, int>, std::vector<int>, custom_hash> mp;
    for (int i = 1; i <= n; ++i) {
      int bx = x[i] / pw, by = y[i] / pw;
      for (int px = bx - 1; px <= bx + 1; ++px) {
        for (int py = by - 1; py <= by + 1; ++py) {
          if (px < 0 || py < 0) continue;
          if (mp.find({px, py}) == mp.end()) continue;
          auto &vec = mp[{px, py}];
          std::vector<int> dv;
          for (auto j : vec) {
            vv[i].emplace_back(j);
            if (getdis(i, j) >= std::max<i64>(1, 1ll * pw * pw / d / d)) dv.emplace_back(j);
          }
          vec = dv;
        }
      }
      mp[{bx, by}].emplace_back(i);
    }
  }
  for (int i = 1; i <= q; ++i) {
    int l, r;
    std::cin >> l >> r;
    qq[r].emplace_back(l, i);
  }
  getans();
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