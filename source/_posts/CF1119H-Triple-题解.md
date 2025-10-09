---
title: CF1119H Triple 题解
date: 2024-09-25 15:53:00
---

## Description

SK 酱送给你了一份生日礼物。礼物是 $n$ 个三元组 $(a_i,b_i,c_i)$ 和四个正整数 $x,y,z,k$。

你利用这 $n$ 个三元组填充了 $n$ 个数组，其中第 $i$ 个数组中有 $x$ 个 $a_i$，$y$ 个 $b_i$，$z$ 个 $c_i$（所以第 $i$ 个数组长度为 $(x+y+z)$。

对于 $i=0,1,\cdots,2^k-1$，回答以下询问：

- 从每个数组中选择**恰好一个**数，使得这些数的 $\mathrm{xor}$ 和为 $i$，方案数是多少？

你只需要输出方案数对 $998,244,353$ 取模后得到的结果。

对于 $100\%$ 的数据，保证：

- $1\le n\le 10^5$，$1\le k\le 17$；
- $0\le x,y,z\le 10^9$；
- $0\le a_i,b_i,c_i\lt 2^k$。

## Solution

首先先让 $b_i$ 和 $c_i$ 都异或上 $a_i$，这样就转化为了 $a_i$ 等于 $0$ 的情况。

容易发现这是个 FWT 的形式，设 $cnt(i)=popcount(i)$，$FWT_k[i]$ 表示 $(a_k,b_k,c_k)$ 的 FWT 数组，那么 $FWT_k[i]=(-1)^{cnt(i\&a_k)}x+(-1)^{cnt(i\&b_k)}y+(-1)^{cnt(i\&c_k)}z$。

由于 $a_k=0$，所以第一项为 $x$，即 $FWT_k[i]=x+(-1)^{cnt(i\&b_k)}y+(-1)^{cnt(i\&c_k)}z$。

这里的 $FWT_k[i]$ 只有 $4$ 种可能，分别是 $x+y+z,x+y-z,x-y+z,x-y-z$，设这四种分别出现了 $c_1,c_2,c_3,c_4$ 次。考虑用解方程的方式解出这四个数。

第一个式子是 $c_1+c_2+c_3+c_4=n$。

先设 $f_{1,k}[i]=(-1)^{cnt(i\&b_k)}$，则 $c_1+c_2-c_3-c_4=\sum_{k=1}^{n}{f_{1,k}[i]}$。

同理设 $f_{2,k}[i]=(-1)^{cnt(i\&c_k)}$，则 $c_1-c_2+c_3-c_4=\sum_{k=1}^{n}{f_{2,k}[i]}$。

然后设 $f_{3,k}[i]=(-1)^{cnt(i\&b_k)+cnt(i\&c_k)}$，则 $c_1-c_2-c_3+c_4=\sum_{k=1}^{n}{f_{3,k}[i]}$。

可以用 FWT 分别求出 $f_{1,k}[i],f_{2,k}[i],f_{3,k}[i]$ 的和，乘起来后再 FWT 回去就是答案。

时间复杂度：$O(n+2^kk)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5, kMaxS = (1 << 17), kMod = 998244353, kInv2 = (kMod + 1) / 2;

int n, k, x, y, z, sum;
int a[kMaxN], b[kMaxN], c[kMaxN];
int f[kMaxS], f1[kMaxS], f2[kMaxS], f3[kMaxS];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
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

void FWT(int *a, int n) {
  for (int len = 2; len <= n; len <<= 1) {
    int m = len / 2;
    for (int i = 0; i < n; i += len) {
      for (int j = i; j < i + m; ++j) {
        int tmp = a[j];
        a[j] = add(a[j], a[j + m]);
        a[j + m] = sub(tmp, a[j + m]);
      }
    }
  }
}

void IFWT(int *a, int n) {
  for (int len = 2; len <= n; len <<= 1) {
    int m = len / 2;
    for (int i = 0; i < n; i += len) {
      for (int j = i; j < i + m; ++j) {
        int tmp = a[j];
        a[j] = 1ll * kInv2 * add(a[j], a[j + m]) % kMod;
        a[j + m] = 1ll * kInv2 * sub(tmp, a[j + m]) % kMod;
      }
    }
  }
}

void dickdreamer() {
  std::cin >> n >> k >> x >> y >> z;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i] >> b[i] >> c[i];
    sum ^= a[i], b[i] ^= a[i], c[i] ^= a[i];
    ++f1[b[i]], ++f2[c[i]], ++f3[b[i] ^ c[i]];
  }
  FWT(f1, (1 << k)), FWT(f2, (1 << k)), FWT(f3, (1 << k));
  for (int i = 0; i < (1 << k); ++i) {
    int c1, c2, c3, c4;
    c1 = fix(n + f1[i] + f2[i] + f3[i]) / 4;
    c2 = fix(n + f1[i] - f2[i] - f3[i]) / 4;
    c3 = fix(n - f1[i] + f2[i] - f3[i]) / 4;
    c4 = fix(n - f1[i] - f2[i] + f3[i]) / 4;
    f[i] = 1;
    f[i] = 1ll * f[i] * qpow(fix(x + y + z), c1) % kMod;
    f[i] = 1ll * f[i] * qpow(fix(x + y - z), c2) % kMod;
    f[i] = 1ll * f[i] * qpow(fix(x - y + z), c3) % kMod;
    f[i] = 1ll * f[i] * qpow(fix(x - y - z), c4) % kMod;
  }
  IFWT(f, (1 << k));
  for (int i = 0; i < (1 << k); ++i) std::cout << f[i ^ sum] << ' ';
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