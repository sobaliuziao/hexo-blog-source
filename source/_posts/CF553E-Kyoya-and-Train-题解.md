---
title: CF553E Kyoya and Train 题解
date: 2024-08-01 21:17:00
---

## Description

给定一张 $n$ 个点 $m$ 条边的无重边无自环的有向图，你要从 $1$ 号点到 $n$ 号点去。

如果你在 $t$ 时刻之后到达 $n$ 号点，你要交 $x$ 元的罚款。

每条边从 $a_i$ 到 $b_i$，走过它需要花费 $c_i$ 元，多次走过同一条边需要多次花费。

走过每条边所需的时间是随机的，对于 $k \in [1,t]$，$\frac{p_{i,k}}{10^5}$ 表示走过第 $i$ 条边需要时间 $k$ 的概率。因此如果多次走过同一条边，所需的时间也可能不同。

你希望花费尽可能少的钱（花费与罚款之和）到达 $n$ 号点，因此每到达一个点，你可能会更改原有的计划。

求在最优决策下，你期望花费的钱数。

$n \le 50$，$m \le 100$，$t \le 2 \times 10^4$，$x,c_i \le 10^6$，$\sum_{k=1}^t p_{i,k} = 10^5$，答案精度误差 $\le 10^{-6}$。

## Solution

考虑 dp。

设 $f_{i,j}$ 表示在 $j$ 时刻走到 $i$ 的期望花费，那么转移如下：

$$
f_{i,j}=
\begin{cases}
0\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ &(i=n, j\leq t)\\
x\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ &(i=n, j> t)\\
x+\text{dist}(i,n)\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ &(i\neq n, j\geq t)\\
\min_{a_k=i}{\left\{\sum_{len=1}^{t}{p_{k,len}f_{b_k,j+len}+c_k}\right\}}\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ &(i\neq n, j<t)
\end{cases}
$$

直接暴力做是 $O(mt^2)$ 的，过不了。

注意到最后一个转移是差卷积的形式，可以用分治 fft 进行优化。具体的，设 $g_{i,k}=\sum_{len=1}^{t}{p_{k,len}f_{b_k,j+len}}$，那么分治到 $[k,k]$ 时就让 $f_{i,k}\leftarrow g_{i,k}+c_k$。

转移就考虑假设当前区间为 $[l,r]$，先递归处理 $[mid+1,r]$，然后处理时间 $[mid+1,r]$ 对 $[l,mid]$ 的 $g$ 值的贡献，最后递归 $[l,mid]$。

注意对于 $[t,2t-1]$ 这个区间由于不能内部进行转移所以不需要递归。

时间复杂度：$O(mt\log^2 t)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using f64 = double;

const int kMaxN = 105, kMaxM = 105, kMaxT = 4e4 + 5;

struct Complex {
  f64 a, b;

  Complex(f64 _a = 0, f64 _b = 0) : a(_a), b(_b) {}
  friend Complex operator +(const Complex &c1, const Complex &c2) { return {c1.a + c2.a, c1.b + c2.b}; }
  friend Complex operator -(const Complex &c1, const Complex &c2) { return {c1.a - c2.a, c1.b - c2.b}; }
  friend Complex operator *(const Complex &c1, const Complex &c2) { return {c1.a * c2.a - c1.b * c2.b, c1.a * c2.b + c2.a * c1.b}; }
};

using cp = Complex;

int n, m, t, x;
int u[kMaxM], v[kMaxM], w[kMaxM];
f64 dis[kMaxN][kMaxN], p[kMaxM][kMaxT * 2], f[kMaxN][kMaxT * 2], g[kMaxM][kMaxT * 2];

namespace FFT {
int n, m, c, len, rev[kMaxT * 50];
cp a[kMaxT * 50], b[kMaxT * 50], omg[kMaxT * 50], inv[kMaxT * 50];

int getlen(int n) {
  int ret = 1;
  for (c = 0; ret <= n + 1; ret <<= 1, ++c) {}
  return ret;
}

void prework() {
  const double kPi = acos(-1.0);
  len = getlen(n + m + 5);
  cp og = {cos(2 * kPi / len), sin(2 * kPi / len)}, ig = {cos(2 * kPi / len), -sin(2 * kPi / len)};
  omg[0] = inv[0] = {1, 0};
  for (int i = 1; i < len; ++i) {
    omg[i] = omg[i - 1] * og;
    inv[i] = inv[i - 1] * ig;
    for (int j = 0; j < c; ++j)
      if (i >> j & 1)
        rev[i] |= (1 << (c - j - 1));
  }
}

void fft(cp *a, int n, cp *omg) {
  for (int i = 0; i < n; ++i)
    if (i < rev[i])
      std::swap(a[i], a[rev[i]]);
  for (int l = 2; l <= n; l <<= 1) {
    int m = l / 2;
    for (int i = 0; i < n; i += l) {
      for (int j = 0; j < m; ++j) {
        auto tmp = a[i + j + m] * omg[n / l * j];
        a[i + j + m] = a[i + j] - tmp;
        a[i + j] = a[i + j] + tmp;
      }
    }
  }
}

void clear() {
  for (int i = 0; i < len; ++i)
    a[i] = b[i] = omg[i] = inv[i] = {0, 0}, rev[i] = 0;
  n = m = c = len = 0;
}

void set(int _n, int _m) {
  n = _n, m = _m;
}

void mul() {
  prework();
  fft(a, len, omg), fft(b, len, omg);
  for (int i = 0; i < len; ++i) a[i] = a[i] * b[i];
  fft(a, len, inv);
  for (int i = 0; i < len; ++i) a[i].a /= len;
}
} // namespace FFT

void solve(int l, int r) {
  if (l == r) {
    for (int i = 1; i < n; ++i) f[i][l] = 1e18;
    for (int i = 1; i <= m; ++i)
      if (u[i] != n) f[u[i]][l] = std::min(f[u[i]][l], g[i][l] + w[i]);
    return;
  }
  int mid = (l + r) >> 1;
  if (r - l + 1 != 2 * t) solve(mid + 1, r);
  for (int i = 1; i <= m; ++i) {
    if (u[i] == n) continue;
    FFT::set(r - l, r - mid);
    for (int j = 1; j <= r - l; ++j) FFT::a[j] = {p[i][j], 0};
    for (int j = 1; j <= r - mid; ++j) FFT::b[j] = {f[v[i]][r - j + 1], 0};
    FFT::mul();
    for (int j = r - mid + 1; j <= r - l + 1; ++j) {
      g[i][r - j + 1] += FFT::a[j].a;
    }
    FFT::clear();
  }
  solve(l, mid);
}

void dickdreamer() {
  std::cin >> n >> m >> t >> x;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= n; ++j)
      dis[i][j] = (i != j) * 1e18;
  for (int i = 1; i <= m; ++i) {
    std::cin >> u[i] >> v[i] >> w[i];
    dis[u[i]][v[i]] = w[i];
    for (int j = 1; j <= t; ++j) {
      int x;
      std::cin >> x;
      p[i][j] = x / 1e5;
    }
  }
  for (int k = 1; k <= n; ++k)
    for (int i = 1; i <= n; ++i)
      for (int j = 1; j <= n; ++j)
        dis[i][j] = std::min(dis[i][j], dis[i][k] + dis[k][j]);
  for (int i = 0; i < 2 * t; ++i) f[n][i] = x * (i > t);
  for (int i = 1; i < n; ++i)
    for (int j = t; j < 2 * t; ++j)
      f[i][j] = x + dis[i][n];
  solve(0, 2 * t - 1);
  std::cout << std::fixed << std::setprecision(10) << f[1][0] << '\n';
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