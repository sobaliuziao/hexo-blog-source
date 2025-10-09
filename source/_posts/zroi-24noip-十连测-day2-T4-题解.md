---
title: zroi 24noip 十连测 day2 T4 题解
date: 2024-09-08 20:13:00
---

## Description

小凯有两个长度为 $N$ 的整数序列 $A_1,A_2,\cdots,A_N$ 和 $B_1,B_2,\cdots,B_N$。

小凯现在越来越喜欢对称的东西了，当他看到两个序列 $C,D$ 时，他会找到序列 $C$ 的最小值 $Cmin$ 和 $D$ 的最小值 $Dmin$，他认为这两个最小值相差越小越好，所以他定义 $f(C,D)=|Cmin-Dmin|$。

更进一步的，他定义 $w(l,r)$ 表示当 $C=\{A_l,A_{l+1},\cdots,A_r\},D=\{B_l,B_{l+1},\cdots,B_r\} $ 时 $f(C,D)$ 的值，即 $\{A_l,A_{l+1},\cdots,A_r\}$ 的最小值和 $\{B_l,B_{l+1},\cdots,B_r\}$ 的最小值的差的绝对值。

对于每个 $k=1,2,\cdots,N$，小凯想求出所有长度为 $k$  的区间 $[l,r]$ 中，$w(l,r)$ 的最小值，即求 $\min_{r-l+1=k} w(l,r)$。

$1\leq N\leq 2\times 10^5,1\leq A_i,B_i\leq 10^9$。

## Solution

首先直接做显然是没有任何性质的，考虑分治。

假设当前处理的是区间 $[L,R]$，$mid=(L+R)/2$，考虑跨越 $[L,mid]$ 和 $[mid+1,R]$ 的贡献。

设

- $a_i=\min\left\{A_i,A_{i+1},\ldots,A_{mid}\right\}$
- $b_i=\min\left\{B_i,B_{i+1},\ldots,B_{mid}\right\}$
- $c_i=\min\left\{A_{mid+1},A_{mid+2},\ldots,A_{i}\right\}$
- $d_i=\min\left\{A_{mid+1},A_{mid+2},\ldots,A_{i}\right\}$

那么对于一个跨越 $mid$ 的区间 $[l,r]$ 的答案就是 $\left|\min\left\{a_l,c_r\right\}-\min\left\{b_l,d_r\right\}\right|$。

枚举 $r-l$，令 $k=r-l$，$w(l,r)$ 转化为 $\left|\min\left\{a_l,c_{l+k}\right\}-\min\left\{b_l,d_{l+k}\right\}\right|$。由于 $a,b$ 是不降的，$c,d$ 是不增的，所以可以二分出 $w(l,r)=|a_l-b_l|,|a_l-d_r|,|c_r-b_l|,|c_r-d_r|$ 分别对应的连续的区间。

对于 $w(l,r)=|a_l-b_l|\ 或\ |c_r-d_r|$ 的情况可以用线段树维护区间最小值。

而对于 $w(l,r)=|a_l-d_r|$ 的情况，因为 $a_l$ 不降且 $d_r$ 不增，所以固定区间长度后 $w(l,r)$ 关于 $l$ 是个单谷函数，于是二分出 $a_l\geq d_r$ 的最大 $l$ 和 $a_l<d_r$ 的最小 $l$ 即可。$w(l,r)=|c_r-b_l|$ 的情况同理。

时间复杂度：$O(n\log^2n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN], b[kMaxN], ans[kMaxN], mila[kMaxN], milb[kMaxN], mira[kMaxN], mirb[kMaxN];

struct SGT {
  int N, mi[kMaxN * 4];

  void build(int n) {
    memset(mi, 0x3f, sizeof(mi));
    for (N = 1; N <= n + 2; N <<= 1) {}
  }

  void update(int x, int v) {
    mi[x += N] = v;
    for (x >>= 1; x; x >>= 1) mi[x] = std::min(mi[x << 1], mi[x << 1 | 1]);
  }

  int query(int l, int r) {
    int ret = 1e9;
    for (l += N - 1, r += N + 1; l ^ r ^ 1; l >>= 1, r >>= 1) {
      if (~l & 1) ret = std::min(ret, mi[l ^ 1]);
      if (r & 1) ret = std::min(ret, mi[r ^ 1]);
    }
    return ret;
  }
} sgt;

int func(int x, int k) {
  return abs(std::min(mila[x], mira[x + k]) - std::min(milb[x], mirb[x + k]));
}

void solve(int l, int r) {
  if (l == r) return void(ans[1] = std::min(ans[1], abs(a[l] - b[l])));
  int mid = (l + r) >> 1;
  solve(l, mid), solve(mid + 1, r);
  mila[mid] = a[mid], milb[mid] = b[mid], mira[mid + 1] = a[mid + 1], mirb[mid + 1] = b[mid + 1];
  for (int i = mid - 1; i >= l; --i) {
    mila[i] = std::min(mila[i + 1], a[i]);
    milb[i] = std::min(milb[i + 1], b[i]);
  }
  for (int i = mid + 2; i <= r; ++i) {
    mira[i] = std::min(mira[i - 1], a[i]);
    mirb[i] = std::min(mirb[i - 1], b[i]);
  }
  for (int i = l; i <= r; ++i) {
    if (i <= mid) sgt.update(i, abs(mila[i] - milb[i]));
    else sgt.update(i, abs(mira[i] - mirb[i]));
  }
  for (int k = 1; k <= r - l; ++k) {
    int ll = std::max(l, mid + 1 - k), rr = std::min(mid, r - k);
    if (ll > rr) continue;
    int L = ll - 1, R = rr + 1, p1 = ll - 1, p2 = ll - 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (mila[mid] <= mira[mid + k]) L = p1 = mid;
      else R = mid;
    }
    L = ll - 1, R = rr + 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (milb[mid] <= mirb[mid + k]) L = p2 = mid;
      else R = mid;
    }
    if (ll <= std::min(p1, p2)) ans[k + 1] = std::min(ans[k + 1], sgt.query(ll, std::min(p1, p2)));
    if (std::max(p1, p2) < rr) ans[k + 1] = std::min(ans[k + 1], sgt.query(std::max(p1, p2) + 1 + k, rr + k));
    if (p1 == p2) continue;
    if (p1 < p2) {
      int L = p1 + 1, R = p2 + 1, res = p1 + 1;
      while (L + 1 < R) {
        int mid = (L + R) >> 1;
        if (mira[mid + k] >= milb[mid]) L = res = mid;
        else R = mid;
      }
      ans[k + 1] = std::min(ans[k + 1], func(res, k));
      if (res < p2) ans[k + 1] = std::min(ans[k + 1], func(res + 1, k));
    } else {
      int L = p2 + 1, R = p1 + 1, res = p2 + 1;
      while (L + 1 < R) {
        int mid = (L + R) >> 1;
        if (mirb[mid + k] >= mila[mid]) L = res = mid;
        else R = mid;
      }
      ans[k + 1] = std::min(ans[k + 1], func(res, k));
      if (res < p1) ans[k + 1] = std::min(ans[k + 1], func(res + 1, k));
    }
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= n; ++i) std::cin >> b[i];
  memset(ans, 0x3f, sizeof(ans));
  sgt.build(n);
  solve(1, n);
  for (int i = 1; i <= n; ++i) std::cout << ans[i] << '\n';
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