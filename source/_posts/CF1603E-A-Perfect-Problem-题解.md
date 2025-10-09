---
title: 'CF1603E A Perfect Problem 题解'
date: 2024-09-13 21:16:00
---

## Description

称一个序列为**好序列**当且仅当这个序列的 $\max\times \min\ge sum$，其中 $sum$ 是序列元素和。

给定 $n,M$，求长度为 $n$，每个数在 $[1,n+1]$ 范围内，每个**非空子序列**（包含序列本身）都是好序列的整数序列个数，对 $M$ 取模。

$1\le n\le 200$，$10^8\le M\le 10^9$，保证 $M$ 为素数。

## Solution

容易发现可以将序列排序后转化为判断所有前缀是否合法。这样就可以暴力 dp 了，时间复杂度：$O(n^6)$。

考虑优化。下面有合法序列的几条性质：

1. $\forall k,a_k\geq k$，因为如果 $a_k<k$，则 $a_1a_k<k\cdot a_1\leq \sum_{i=1}^{k}{a_i}$，矛盾了。

2. 若 $a_k=k$，则 $a_1=a_2=\ldots=a_k=k$。因为 $a_1a_k=k\cdot a_1\geq\sum_{i=1}^{k}{a_i}$，所以 $a_1=a_2=\ldots=a_k=k$。

3. 若 $a_n=n+1$，则 $\forall a_k\geq k+1$，$[1,k]$ 合法。因为 $a_1a_n=(n+1)a_1\geq\sum_{i=1}^{n}{a_i}$，则 $a_1\geq\sum_{i=1}^{n}{(a_i-a_1)}\geq\sum_{i=1}^{k}{(a_i-a_1)}$，所以 $a_1a_k\geq (k+1)a_1\geq\sum_{i=1}^{k}{a_i}$。

---

对于 $a_n=n$ 的情况很容易。

对于 $a_n=n+1$，一个序列合法的条件即为：

- $\forall 1\leq i\leq a_1,a_1\leq a_i\leq n+1$。

- $\forall a_1+1\leq i\leq n,i+1\leq a_i\leq n+1$。

- $\sum_{i=1}^{n}{(a_i-a_1)}\geq a_1$。

设 $b_i=a_i-a_1$，则：

- $\forall 1\leq i\leq a_1,0\leq b_i\leq n+1-a_1$。

- $\forall a_1+1\leq i\leq n,i+1-a_1\leq b_i\leq n+1-a_1$。

- $\sum_{i=1}^{n}{b_i}\geq a_1$。

这样就可以 dp 了。先枚举 $a_1$ 的值，可以设 $f_{i,j,k}$ 填了 $b$ 的前 $i$ 位，和为 $j$，当前的最大值为 $k$ 的方案数。

转移时可以枚举 $0\sim k-1$ 的总个数 $i$，$b$ 的前 $i$ 项的和 $j$，$k$ 的出现次数 $cnt$，则当 $i+cnt+1-a_1\leq k\leq n+1-a_1$ 时，即可让 $f_{i+cnt,j+cnt\cdot k,k}\leftarrow \frac{f_{i,j,k-1}}{cnt!}$。

时间复杂度：$O(n^4\log n)$，过不了。

---

注意到 $a_1$ 的值不会很大，并且 $a_1\geq n-2\sqrt n$。证明就考虑 $a_1\geq\sum b_i\geq\sum_{i=a_1+1}^{n}{(i-a_1+1)}=\frac{(n+a_1+3)(n-a_1)}{2}-a_1(n-a_1)$，可以得到 $a_1\geq n-2\sqrt n$。

这样 $a_1$ 的枚举数量就只有 $O(\sqrt n)$ 级别了。

时间复杂度：$O(n^3\sqrt n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 205;

int n, mod;
int fac[kMaxN], ifac[kMaxN], f[kMaxN][kMaxN][kMaxN];

constexpr int qpow(int bs, int64_t idx = mod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % mod)
    if (idx & 1)
      ret = (int64_t)ret * bs % mod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= mod ? x + y - mod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + mod); }
inline void inc(int &x, int y) { (x += y) >= mod ? x -= mod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += mod : x; }

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = 1;
  for (int i = 2; i <= n + 1; ++i) {
    fac[i] = 1ll * i * fac[i - 1] % mod;
    ifac[i] = qpow(fac[i]);
  }
}

void dickdreamer() {
  std::cin >> n >> mod;
  prework();
  int ans = 1;
  for (int a1 = std::max<int>(n - 18, 1); a1 <= n; ++a1) {
    for (int i = 0; i <= n; ++i)
      for (int j = 0; j <= a1; ++j)
        for (int k = 0; k <= n - a1 + 1; ++k)
          f[i][j][k] = 0;
    for (int i = 1; i <= a1; ++i) {
      f[i][0][0] = 1ll * fac[n] * ifac[i] % mod;
    }
    for (int k = 1; k <= n - a1 + 1; ++k) {
      for (int i = 1; i <= n; ++i) {
        for (int j = 0; j <= a1; ++j) {
          for (int cnt = 0; cnt <= std::min(n - i, (a1 - j) / k); ++cnt) {
            if (k >= i + cnt - a1 + 1) {
              inc(f[i + cnt][j + cnt * k][k], 1ll * f[i][j][k - 1] * ifac[cnt] % mod);
            }
          }
        }
      }
    }
    for (int i = 0; i <= a1; ++i) inc(ans, f[n][i][n - a1 + 1]);
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