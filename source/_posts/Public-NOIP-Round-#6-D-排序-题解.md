---
title: Public NOIP Round #6 D 排序 题解
date: 2024-11-19 16:26:00
---

## Description

今天是 YQH 的生日，她得到了一个 $1\sim n$ 的排列作为礼物。
YQH 是一个有强迫症的女孩子，她希望把这个排列从小到大排序，具体的，她可以进行这样的操作：

- 把 $[1,n]$ 分成若干个区间，假如是 $m$ 段，依次为 $[l_1,r_1],[l_2,r_2],\dots,[l_m,r_m]$，其中 $l_1=1,r_m=n,l_{i+1}=r_i+1,l_i\le r_i$。

- 假如原来的排列为 $a_{1,\dots,n}$，那么把排列变为 $a_{l_m},a_{l_m+1},\dots,a_{r_m},a_{l_{m-1}},a_{l_{m-1}+1},\dots,a_{r_{m-1}},\dots,a_{l_1},a_{l_1+1},\dots,a_{r_1}$，即把每一段看作一个整体，然后把这个排列进行 reverse。
YQH 希望进行尽可能少的操作，把序列从小到大排序。但是她太笨了，所以她找到你帮忙。注意，你不需要得到最小操作数。

$n\leq 2\times 10^4$，次数限制为 $90$。

## Solution

考虑分治。

假设当前已经让 $a_{[l,r]}$ 的数值域变成 $[l,r]$ 了，设 $mid=\left\lfloor\frac{l+r}{2}\right\rfloor$，将 $a_i\leq mid$ 视作 $0$，否则视作 $1$，现在需要将这个 $01$ 序列排序，使得所有 $0$ 都在 $1$ 之前。

先把连续段缩掉，那么序列变为 $10101\ldots 010$，考虑以 $1,2,1,2\ldots$ 分段，则操作后变为 $1000111000\ldots$，连续段数变为原来的 $\frac{1}{3}$，所以将长度为 $n$ 的 $01$ 序列排序的次数为 $O(\log_3 n)$。

那么设 $f(n)$ 表示将普通序列排序的次数，用上面的方式排序可以得到：

$f(n)=f\left(\left\lceil\frac{n}{2}\right\rceil\right)+O(\log_3 n)$

于是总次数为 $1+\sum\limits_{j=0} \left\lceil\log_3\left(\left\lceil\frac{n}{2^j}\right\rceil\right)\right\rceil$，能过。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using vi = std::vector<int>;
using vvi = std::vector<std::vector<int>>;

const int kMaxN = 2e4 + 5;

int n, m;
int a[kMaxN], len[kMaxN];
bool b[kMaxN], op[kMaxN];

void prework(int l, int r) {
  int lst = l - 1;
  m = 0;
  for (int i = l; i <= r; ++i) {
    if (i == r || b[i] != b[i + 1]) {
      op[++m] = b[i], len[m] = i - lst;
      lst = i;
    }
  }
}

vvi getvec(int l, int r) {
  vvi vec;
  for (;;) {
    prework(l, r);
    if (m == 2 && op[1] == 0 && op[2] == 1) break;
    std::vector<int> v;
    for (int i = 1, now = 1; i <= m; now = 3 - now) {
      now = std::min(now, m - i + 1);
      int s = 0;
      for (int j = i; j <= i + now - 1; ++j) s += len[j];
      v.emplace_back(s);
      i += now;
    }
    vec.emplace_back(v);
    int now = l;
    std::reverse(a + l, a + 1 + r);
    std::reverse(b + l, b + 1 + r);
    std::reverse(v.begin(), v.end());
    for (auto x : v) {
      std::reverse(a + now, a + now + x);
      std::reverse(b + now, b + now + x);
      now += x;
    }
  }
  return vec;
}

vi merge(vi a, vi b) {
  vi c;
  for (auto x : a) c.emplace_back(x);
  for (auto x : b) c.emplace_back(x);
  return c;
}

vvi solve(int l, int r) {
  if (l == r) return {};
  int mid = (l + r) >> 1;
  if (r - l + 1 > 3 && (~(l + r) & 1)) ++mid;
  for (int i = l; i <= r; ++i) b[i] = (a[i] > mid);
  auto vec = getvec(l, r), L = solve(l, mid), R = solve(mid + 1, r);
  int sz = std::max(L.size(), R.size());
  if (sz & 1) ++sz;
  L.resize(sz, vi{mid - l + 1});
  R.resize(sz, vi{r - mid});
  for (int i = 0; i < sz; ++i) {
    if (~i & 1) vec.emplace_back(merge(L[i], R[i]));
    else vec.emplace_back(merge(R[i], L[i]));
  }
  return vec;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  auto res = solve(1, n);
  std::cout << res.size() << '\n';
  for (auto &vec : res) {
    std::cout << vec.size() << ' ';
    for (auto x : vec) std::cout << x << ' ';
    std::cout << '\n';
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