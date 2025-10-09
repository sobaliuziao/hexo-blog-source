---
title: 'Public Round #14 A 安顿 题解'
date: 2025-02-06 20:24:00
---

## Description

对于一个数组 $A$ 和数字 $X$，让我们定义 $f(A,X)$ 如下：

如果不能将 $A$ 拆分为几个子段使得每个子数组中所有元素的异或不等于 $X$，则 $f(A,X)=0$。

否则，$f(A,X)$ 等于这种拆分中最大可能的子段数。

给定整数 $N,K$ 和 $X$，其中 $0\leq X<2^K$。 考虑长度为 $N$ 的数组 $A$，如果每个元素都是从 $0$ 到 $2^K-1$ 均匀生成的整数。 求 $f(A,X)$ 的期望值对 $998244353$ 取模的值。

$1 \le N \le 10^6, 1 \le K \le 60, 0 \leq X < 2^K$。

## Solution

考虑将 $A$ 的前缀异或和数组 $S$ 拿出来，题目转化为选出最多的断点，满足 $i_0=0<i_1<i_2<\ldots<i_k=n$，且 $S_{i_j}\oplus S_{i_{j-1}}\neq X$。

首先如果 $X=0$，那么显然 $f(A,X)$ 等于 $S$ 中极长连续段的个数减一。

如果 $X\neq 0$，考虑用类似 $X=0$ 的做法，将 $v$ 和 $v\oplus X$ 看成一种数去缩连续段，那么不同连续段之间显然不互相影响。而对于连续段内，如果当前是开始或者末尾连续段，个数即为开始或者末尾对应的数的个数，否则个数为这个连续段内两种数的出现次数最大值。容易发现这么做是最优的。

然后考虑怎么计数。

设 $f_i$ 表示长度为 $i$ 的连续段（不在开始或者末尾）的贡献。可以得到：

$$f_i=\sum_{j=0}^{i}{\binom{i}{j}\max\{j,i-j\}}$$

这个东西可以分类讨论 $\max\{j,i-j\}$ 的类型然后递推求。

对于前缀和后缀串的贡献容易得到。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e6 + 5, kMod = 998244353;

int n, k, x, cnt;
int fac[kMaxN], ifac[kMaxN], f[kMaxN], g[kMaxN];

int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int fix(int x) { return (x % kMod + kMod) % kMod; }
inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }
inline int getop(int x) { return (~x & 1) ? 1 : (kMod - 1); }

int C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

void prework(int n = 1e6) {
  fac[0] = 1;
  for (int i = 1; i <= n; ++i) fac[i] = 1ll * i * fac[i - 1] % kMod;
  ifac[n] = qpow(fac[n]);
  for (int i = n; i; --i) ifac[i - 1] = 1ll * i * ifac[i] % kMod;
}

int getcnt(int n) {
  if (n == 0) return 0;
  else if (n == 1) return 1;
  else return add(1ll * (n - 1) * qpow(2, n - 2) % kMod, qpow(2, n - 1));
}

void dickdreamer() {
  std::cin >> n >> k >> x;
  prework();
  int ans = 0, cnt = fix(1ll << k), cntg = fix(1ll << (k - 1));
  if (x == 0) return void(std::cout << sub(n, 1ll * n * qpow(cnt) % kMod) << '\n');
  for (int i = 2; i <= n; ++i) {
    g[i] = add(2ll * g[i - 1] % kMod, 1ll * getop(i) * C(i - 2, i / 2 - 1) % kMod);
  }
  for (int i = 1; i <= n; ++i) {
    f[i] = sub(2ll * i % kMod * g[i] % kMod, (i % 2 == 0) * (i / 2) * C(i, i / 2) % kMod);
    f[i] = sub(1ll * i * qpow(2, i) % kMod, f[i]);
    if (i <= n - 2) inc(ans, 1ll * (n - i - 1) * f[i] % kMod * cntg % kMod * (cnt - 2) % kMod * (cnt - 2) % kMod * qpow(cnt, n - i - 2) % kMod);
  }
  // std::cerr << f[4] << '\n';
  for (int i = 1; i <= n - 1; ++i)
    inc(ans, 1ll * f[i] * (cntg - 1) % kMod * (cnt - 2) % kMod * qpow(cnt, n - i - 1) % kMod);
  // std::cerr << ans << '\n';
  for (int i = 1; i <= n - 1; ++i) { // 后缀
    inc(ans, 1ll * getcnt(i) * cnt % kMod * (cnt - 2) % kMod * qpow(cnt, n - i - 1) % kMod);
  }
  // std::cerr << ans << '\n';
  inc(ans, 1ll * getcnt(n) % kMod * (cnt - 2) % kMod);
  // std::cerr << ans << '\n';
  // std::cerr << 124780545ll * 16 % kMod << '\n';
  for (int i = 1; i <= n - 1; ++i) {
    inc(ans, 1ll * i * qpow(2, i - 1) % kMod * (cnt - 2) % kMod * qpow(cnt, n - i - 1) % kMod);
  }
  // std::cerr << ans << '\n';
  for (int i = 1; i <= n; ++i) inc(ans, 1ll * i * C(n - 1, i - 1) % kMod);
  // std::cerr << ans << '\n';
  std::cout << 1ll * ans * qpow(qpow(cnt), n) % kMod << '\n';
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