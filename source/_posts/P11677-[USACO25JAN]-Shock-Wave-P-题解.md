---
title: P11677 [USACO25JAN] Shock Wave P 题解
date: 2025-03-19 09:42:00
---

## Description

Bessie 正在试验一种能够产生巨大冲击波的强大的蹄部植入物。她有 $N$（$2 \leq N \leq 10^5$）块砖块排开在面前，分别需要至少 $p_0,p_1,\dots,p_{N-1}$ 的力量才能击破（$0 \leq p_i \leq 10^{18}$）。

Bessie 可以通过击打特定的砖块来施加力量，但由于她的植入物的奇特性质，它不会对她所击打的那块砖块施加任何力量。相反，如果她选择击打砖块 $x$ 一次，其中 $x$ 是一个 $[0,N-1]$ 范围内的整数，对所有在 $[0,N-1]$ 范围内的整数 $i$，它将对砖块 $i$ 施加 $|i-x|$ 的力量。同时这个力量是累积的，因此对一块砖块施加两次 $2$ 的力量将对该砖块施加总共 $4$ 的力量。

请求出击破所有砖块所需要的最少击打次数。

$\sum N\leq 5\times 10^5$。

## Solution

首先观察到 $1$ 和 $n$ 放到一起是很强的，所以如果存在两次操作分别在 $2\leq x\leq y\leq n-1$，则让其分别变为 $x-1$ 和 $y+1$ 一定更优。

所以最优方案一定满足只操作 $1$ 和 $n$，或者操作 $1$ 和 $n$，并在中间某个位置 $k$ 操作一次。

不妨设 $1$ 操作了 $x$ 次，$n$ 操作了 $y$ 次，并枚举中间的操作位置 $k$。

则需要满足 $\forall i\in[1,n],x\cdot(i-1)+y\cdot(n-i)+|i-k|\geq p_i$。

考虑枚举 $s=x+y$，则可以得到不等式：$(i-1)x+(n-i)(s-x)\geq p_i-|i-k|$，所以 $(2i-n-1)x\geq p_i-|i-k|-(n-i)s$。

只要解出这 $n$ 个不等式解的交即可，暴力做是 $O(n^2\log V)$。

注意到在 $k$ 移动的过程中，第 $i$ 个方程对应的解只会变化 $O\left(\frac{n}{2i-n-1}\right)$ 次，这是个调和级数的式子，所以总变化量为 $O(n\log n)$，求出这些变化点并更新即可做到 $O(n\log n\log V)$。

还是过不了。

考虑先求出中间位置没有操作的答案 $res$，这部分可做到 $O(n\log V)$。由于一次 $1$ 操作一次 $n$ 操作一定优于一次中间操作，所以中间操作得到的答案最小为 $res-1$，只 check 这一个答案即可。

时间复杂度：$O(n\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using i128 = __int128_t;

const int kMaxN = 1e5 + 5;

int n;
int a[kMaxN], d[kMaxN];
i128 b[kMaxN];

i128 cei(i128 x, int d) {
  if (d < 0) x = -x, d = -d;
  if (x >= 0) return (x + d - 1) / d;
  else return x / d;
}

i128 flr(i128 x, int d) {
  if (d < 0) x = -x, d = -d;
  if (x >= 0) return x / d;
  else return (x - d + 1) / d;
}

struct SGT1 {
  int N; i128 mx[kMaxN * 4];
  void pushup(int x) {
    mx[x] = std::max(mx[x << 1], mx[x << 1 | 1]);
  }
  void build(int n) {
    for (N = 1; N <= n + 1; N <<= 1) {}
    std::fill_n(mx, 2 * N, -2e18);
    for (int i = 1; i <= n; ++i) {
      if (d[i] > 0) mx[i + N] = cei(b[i] - (i - 1), d[i]);
    }
    for (int i = N - 1; i; --i) pushup(i);
  }
  void update(int x, i128 v) {
    mx[x += N] = v;
    for (x >>= 1; x; x >>= 1) pushup(x);
  }
  i128 query() { return mx[1]; }
} sgt1;

struct SGT2 {
  int N; i128 mi[kMaxN * 4];
  void pushup(int x) {
    mi[x] = std::min(mi[x << 1], mi[x << 1 | 1]);
  }
  void build(int n) {
    for (N = 1; N <= n + 1; N <<= 1) {}
    std::fill_n(mi, 2 * N, 2e18);
    for (int i = 1; i <= n; ++i) {
      if (d[i] < 0) mi[i + N] = flr(b[i] - (i - 1), d[i]);
    }
    for (int i = N - 1; i; --i) pushup(i);
  }
  void update(int x, i128 v) {
    mi[x += N] = v;
    for (x >>= 1; x; x >>= 1) pushup(x);
  }
  i128 query() { return mi[1]; }
} sgt2;

bool check1(int s) {
  i128 L = 0, R = s;
  for (int i = 1; i <= n; ++i) {
    b[i] = a[i] - (i128)(n - i) * s;
    int d = 2 * i - n - 1;
    if (d == 0) {
      if (b[i] > 0) R = -1;
    } else if (d > 0) {
      L = std::max(L, cei(b[i], d));
    } else {
      R = std::min(R, flr(b[i], d));
    }
  }
  return L <= R;
}

bool check2(int s) {
  static std::vector<int> vec[kMaxN];
  for (int i = 1; i <= n; ++i) vec[i].clear();
  for (int i = 1; i <= n; ++i) {
    b[i] = a[i] - (i128)(n - i) * s;
    d[i] = 2 * i - n - 1;
    if (d[i] > 0) {
      i128 mi, r = b[i] - flr(b[i], d[i]) * d[i];
      if (r >= 1) mi = r - 1;
      else mi = d[i] - 1;
      for (int j = mi; j <= n; j += d[i]) {
        if (i - j >= 1) vec[i - j].emplace_back(i);
        if (i + j <= n) vec[i + j].emplace_back(i);
        if (i - j - 1 >= 1) vec[i - j - 1].emplace_back(i);
        if (i + j + 1 <= n) vec[i + j + 1].emplace_back(i);
      }
    } else if (d[i] < 0) {
      int mi, r = -b[i] - flr(-b[i], -d[i]) * (-d[i]);
      mi = (-d[i] - r) % (-d[i]);
      for (int j = mi; j <= n; j -= d[i]) {
        if (i - j >= 1) vec[i - j].emplace_back(i);
        if (i + j <= n) vec[i + j].emplace_back(i);
        if (i - j + 1 >= 1) vec[i - j + 1].emplace_back(i);
        if (i + j - 1 <= n) vec[i + j - 1].emplace_back(i);
      }
    }
  }
  sgt1.build(n), sgt2.build(n);
  for (int i = 1; i <= n; ++i) {
    for (auto x : vec[i]) {
      if (d[x] > 0) sgt1.update(x, cei(b[x] - abs(x - i), d[x]));
      else sgt2.update(x, flr(b[x] - abs(x - i), d[x]));
    }
    i128 L = sgt1.query(), R = std::min<i128>(s, sgt2.query());
    if (n % 2 == 1) {
      int mid = (n + 1) / 2;
      if (d[mid] == 0 && b[mid] - llabs(mid - i) > 0) R = -1;
    }
    if (L <= R) return 1;
  }
  return 0;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  int mx = *std::max_element(a + 1, a + 1 + n);
  if (!mx) return void(std::cout << "0\n");
  int L = -1, R = 2 * mx, res = 2 * mx;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (check1(mid)) R = res = mid;
    else L = mid;
  }
  if (res >= 2 && check2(res - 2)) --res;
  std::cout << res << '\n';
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```