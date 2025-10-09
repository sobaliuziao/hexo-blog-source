---
title: CF2096H Wonderful XOR Problem 题解
date: 2025-07-30 14:37:00
---

## Description

有 $n$ 个区间 $[l_1, r_1], [l_2, r_2], \ldots [l_n, r_n]$。对于每个 $x$ 从 $0$ 到 $2^m - 1$，求满足以下条件的序列 $a_1, a_2, \ldots a_n$ 的数量（模 $998\,244\,353$）：

- 对于所有 $i$ 从 $1$ 到 $n$，有 $l_i \leq a_i \leq r_i$；
- $a_1 \oplus a_2 \oplus \ldots \oplus a_n = x$，其中 $\oplus$ 表示[按位异或运算符](https://en.wikipedia.org/wiki/Bitwise_operation#XOR)。

$1\leq n\leq 2\times 10^5,1\leq m\leq 18$。

## Solution

显然是 fwt。考虑求出 $[l_i,r_i]$ 对应的 fwt 数组。设 $\text{pc}(x)=\text{popcount}(x)$。

先把 $[l_i,r_i]$ 变成 $[0,r_i]-[0,l_i-1]$，现在问题变为求出 $\sum_{i=0}^{n}{(-1)^{\text{pc}(x\&i)}}$。

现在把 $x$ 的 lowbit 拿出来，假设为 $2^b$，那么对于所有 $i$ 在 $b$ 位之前没有顶到 $n$ 的上界的所有数，由于 $b$ 位的存在，一定会互相抵消。

然后再分讨一下可以发现答案为 $(-1)^{\text{pc}(n\&x)}\left[n\bmod 2^b+1-(n\&2^b)\right]$，设 $v_{b,n}=n\bmod 2^b+1-(n\&2^b)$。

那么 $\displaystyle fwt_x=\prod_{i=1}^{n}{\left[(-1)^{\text{pc}(r_i\&x)}v_{b,r_i}-(-1)^{\text{pc}((l_i-1)\&x)}v_{b,l_i-1}\right]}$。

容易想到枚举 $b$，每次求上面的那个东西，再化简一下：

$$
\begin{aligned}
fwt_x=&\prod_{i=1}^{n}{\left[(-1)^{\text{pc}(r_i\&x)}v_{b,r_i}-(-1)^{\text{pc}((l_i-1)\&x)}v_{b,l_i-1}\right]}\\
=&\prod_{i=1}^{n}{\left[(-1)^{\text{pc}((l_i-1)\&x)}v_{b,l_i-1}\cdot\left(-1+\frac{v_{b,r_i}}{v_{b,l_i-1}}\cdot(-1)^{pc(r_i\&x)+pc((l_i-1)\&x)}\right)\right]}\\
=&\prod_{i=1}^{n}{\left[(-1)^{\text{pc}((l_i-1)\&x)}v_{b,l_i-1}\cdot\left(-1+\frac{v_{b,r_i}}{v_{b,l_i-1}}\cdot(-1)^{pc((r_i\oplus(l_i-1))\&x)}\right)\right]}\\
\end{aligned}
$$

那个小括号外面的部分可以直接用类似 fwt 的东西做。小括号里面的东西是形如 $\displaystyle\prod(a_i+b_ix^{c_i})$ 的东西，也是个经典技巧，设 $fwt_{x,0/1}$ 表示目前 $\displaystyle\prod\left(a_i+b_ix^{c_i}\right)$  的乘积和 $\displaystyle\prod\left(a_i-b_ix^{c_i}\right)$，具体转移看代码。

时间复杂度：$O(nm+2^m\cdot m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 3e5 + 5, kMod = 998244353;

int n, m;
int l[kMaxN], r[kMaxN], f[kMaxN];

int qpow(int bs, int64_t idx = kMod - 2) {
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
inline int getop(int x) { return (~x & 1) ? 1 : (kMod - 1); }

void ifwt(int *f, int n) {
  static const int kInv2 = (kMod + 1) / 2;
  for (int i = 0; i < n; ++i) {
    int m = (1 << i), len = 2 * m;
    for (int b = 0; b < (1 << n); b += len) {
      for (int j = b; j < b + m; ++j) {
        int val = f[j];
        f[j] = 1ll * kInv2 * add(val, f[j | m]) % kMod;
        f[j | m] = 1ll * kInv2 * sub(val, f[j | m]) % kMod;
      }
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i) std::cin >> l[i] >> r[i];
  for (int bb = 0; bb < m; ++bb) {
    static int fwt[kMaxN][2];
    int mm = m - bb;
    for (int i = 0; i < (1 << mm); ++i) fwt[i][0] = fwt[i][1] = 1;
    int coef = 1;
    for (int i = 1; i <= n; ++i) {
      int vl = 0, vr = sub((r[i] & ((1 << bb) - 1)) + 1, (r[i] & (1 << bb)));
      if (l[i]) vl = sub(((l[i] - 1) & ((1 << bb) - 1)) + 1, (l[i] - 1) & (1 << bb));
      int a, b, c;
      if (vl) {
        coef = 1ll * coef * vl % kMod;
        a = kMod - 1, b = 1ll * vr * qpow(vl) % kMod, c = ((r[i] ^ (l[i] - 1)) >> bb);
        fwt[(l[i] - 1) >> bb][1] = sub(0, fwt[(l[i] - 1) >> bb][1]);
      } else {
        a = 0, b = vr, c = (r[i] >> bb);
      }
      fwt[c][0] = 1ll * fwt[c][0] * add(a, b) % kMod;
      fwt[c][1] = 1ll * fwt[c][1] * sub(a, b) % kMod;
    }
    for (int i = 0; i < mm; ++i) {
      int m = (1 << i), len = 2 * m;
      for (int k = 0; k < (1 << mm); k += len) {
        for (int j = k; j < k + m; ++j) {
          int tmp[2] = {fwt[j][0], fwt[j][1]}, tmp1[2] = {fwt[j | m][0], fwt[j | m][1]};
          fwt[j][0] = 1ll * tmp[0] * tmp1[0] % kMod;
          fwt[j][1] = 1ll * tmp[1] * tmp1[1] % kMod;
          fwt[j | m][0] = 1ll * tmp[0] * tmp1[1] % kMod;
          fwt[j | m][1] = 1ll * tmp[1] * tmp1[0] % kMod;
        }
      }
    }
    for (int i = 1; i < (1 << mm); i += 2) {
      f[i << bb] = 1ll * coef * fwt[i][0] % kMod;
    }
  }
  f[0] = 1;
  for (int i = 1; i <= n; ++i) f[0] = 1ll * f[0] * (r[i] - l[i] + 1) % kMod;
  ifwt(f, m);
  int res = 0;
  for (int i = 0; i < (1 << m); ++i) res ^= (1ll * f[i] * qpow(2, i) % kMod);
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