---
title: '[AGC038E] Gachapon 题解'
date: 2025-02-19 15:23:00
---

## Description

有一个随机数生成器，生成 $[0,n-1]$ 之间的整数，其中生成 $i$ 的概率为 $\frac{A_i}{S}$，其中，$S=\sum A_i$。

这个随机数生成器不断生成随机数，当 $\forall i\in [0,n-1]$，$i$ 至少出现了 $B_i$ 次时，停止生成，否则继续生成。

求期望生成随机数的次数，输出答案对 $998244353$ 取模的结果。

$A_i,B_i\geq 1$，$\sum A_i,\sum B_i,n\leq 400$。

## Solution

显然先要 min-max 容斥。

对于集合 $T$，有 $P=\frac{\sum_{i\in T}{A_i}}{S}$ 的概率选到 $T$ 内的点，所以期望 $\frac{1}{P}$ 次选到 $T$ 内，$T$ 对答案的贡献即为让 $T$ 中存在一个 $i$ 至少出现 $B_i$ 次的期望操作数乘 $\frac{1}{P}$。

考虑枚举还没满足条件的每个时刻每个位置被选的次数，设分别选了 $C_1,C_2,\ldots,C_m$ 次。

首先需要满足 $C_i<B_i$，然后用总方案数除以得到这种状态的方案数得到获得此状态的概率，即 $\frac{\left(\sum C_i\right)!}{\prod C_i!}\cdot \prod\left(\frac{A_i}{\sum_{i\in T}A_i}\right)^{C_i}$。

所以最终答案为：

$$
\begin{aligned}
ans&=\sum_{T\subseteq\left\{1,2,\ldots,n\right\}}{(-1)^{|T|-1}\cdot\frac{S}{\sum_{i\in T}{A_i}}\cdot \sum_{\forall i\in T,C_i<B_i}\frac{(\sum C_i)!}{\prod C_i!}\cdot \prod\left(\frac{A_i}{\sum_{i\in T}{A_i}}\right)^{C_i}}
\end{aligned}
$$

dp 时记录选的 $\sum A_i$ 和 $\sum C_i$ 即可。

时间复杂度：$O\left(\sum A_i\cdot\left(\sum B_i\right)^2\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 405, kMod = 998244353;

int n, sa, sb;
int a[kMaxN], b[kMaxN], fac[kMaxN], ifac[kMaxN], f[kMaxN][kMaxN];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

void prework(int n = 400) {
  fac[0] = ifac[0] = 1;
  for (int i = 1; i <= n; ++i) {
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = qpow(fac[i]);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i)
    std::cin >> a[i] >> b[i];
  prework();
  f[0][0] = kMod - 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = sa; ~j; --j) {
      for (int k = sb; ~k; --k) {
        if (!f[j][k]) continue;
        int pw = 1;
        for (int c = 0; c <= b[i] - 1; ++c) {
          dec(f[j + a[i]][k + c], 1ll * f[j][k] * ifac[c] % kMod * pw % kMod);
          pw = 1ll * pw * a[i] % kMod;
        }
      }
    }
    sa += a[i], sb += b[i];
  }
  int ans = 0;
  for (int i = 1; i <= sa; ++i) {
    for (int j = 0; j <= sb; ++j)
      inc(ans, 1ll * sa * qpow(i) % kMod * fac[j] % kMod * qpow(qpow(i), j) % kMod * f[i][j] % kMod);
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