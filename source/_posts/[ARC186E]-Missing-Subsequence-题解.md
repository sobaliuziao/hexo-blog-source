---
title: [ARC186E] Missing Subsequence 题解
date: 2024-10-29 12:32:00
---

## Description

给定一个整数序列 $\left(X_1, \ldots, X_M\right)$ ，其长度为 $M$，元素取值为 $1, \ldots, K$。

要求找出长度为 $N$ 的序列 $(A_1, \ldots, A_N)$ 的数量，元素取值为 $1, \ldots, K$，并满足以下条件，结果取模 $998244353$：

- 在所有长度为 $M$ 的序列中，唯一不能作为 $(A_1, \ldots, A_N)$ 的（不一定连续的）子序列的序列是 $(X_1, \ldots, X_M)$。

$2\leq M,K\leq N\leq 400,1\leq X_i\leq K$。

## Solution

不妨设 $F(\{x_1,x_2,\ldots,x_m\})$ 表示所有满足除了 $x$ 的长度为 $m$ 的序列都是其子序列的序列集合。

考虑一个序列 $a$ 什么时候可以满足条件。

设 $i$ 为 $x_1$ 在 $a$ 里面第一次出现的位置，容易发现除了 $x_1$ 的颜色都在 $a_1,a_2,\ldots,a_{i-1}$ 出现了，且 $(a_{i+1},a_{i+2},\ldots,a_n)\in F(\{x_2,x_3,\ldots,x_m\})$。

然后经过手玩一下会发现这个条件在 $x_1=x_2$ 的情况下还是充分条件。

证明就考虑如果满足了这两个条件，第一位为 $x_1$ 的子序列一定都满足条件。

否则设第一位为 $s$，若第二位为 $x_1$，则第二位匹配 $i$，根据第二个条件所有长度小于 $m-1$ 的序列都出现在 $a_{i+1}$ 之后。如果第二位不为 $x_1$，根据第二个条件 $x_2,x_3,\ldots,x_m$ 也一定出现在 $a_{i+1}$ 之后。

---

对于 $x_1\neq x_2$ 的情况，设 $j$ 为 $x_2$ 在 $a_1,a_2,\ldots,a_{i+1}$ 最后一个出现位置，那么还需要满足除了 $x_1$ 的颜色都在 $a_1,a_2,\ldots,a_{j-1}$ 出现。

下面证明一下必要性。对于一个合法的序列 $a$，如果存在颜色 $c$ 使得 $c$ 第一次出现位置在 $[j+1,i-1]$ 内，则 $c,x_2,x_3,\ldots,x_m$ 这个序列的除了 $c$ 的部分只能从 $i+1$ 匹配起，而根据第二个条件这个东西一定是匹配不出来的，矛盾。

充分性证明和 $x_1=x_2$ 的情况差不多，这里就不写了。

---

求方案数时设 $f_{i,j}$ 表示长度为 $i$ 的序列满足 $x_j,x_{j+1},\ldots,x_m$ 的条件的数量，转移直接枚举 $x_j$ 第一次出现的位置和 $x_{j+1}$ 在 $x_j$ 第一次出现之前的最后位置即可。

时间复杂度：$O(n^2m+n^2k)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 405, kMod = 998244353;

int n, m, k;
int x[kMaxN], f[kMaxN][kMaxN], coef[kMaxN], C[kMaxN][kMaxN], cnt[kMaxN][kMaxN];

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

void prework() {
  C[0][0] = 1;
  for (int i = 1; i <= 400; ++i) {
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j)
      C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= k; ++j) {
      cnt[i][j] = qpow(j, i);
      for (int s = 1; s < j; ++s) dec(cnt[i][j], 1ll * cnt[i][s] * C[j][s] % kMod);
      // std::cerr << cnt[i][j] << ' ';
    }
    // std::cerr << '\n';
  }
}

void dickdreamer() {
  std::cin >> n >> m >> k;
  for (int i = 1; i <= m; ++i) std::cin >> x[i];
  prework();
  for (int i = 1; i <= n; ++i) {
    f[m][i] = cnt[i][k - 1];
    // std::cerr << f[m][i] << ' ';
  }
  // std::cerr << '\n';
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j < i; ++j)
      inc(coef[i], 1ll * cnt[j - 1][k - 1] * qpow(k - 2, i - 1 - j) % kMod);
  }
  for (int i = m - 1; i; --i) {
    for (int j = 1; j <= n; ++j) {
      if (x[i] == x[i + 1]) {
        for (int s = 1; s <= j; ++s) {
          inc(f[i][j], 1ll * cnt[s - 1][k - 1] * f[i + 1][j - s] % kMod);
          // std::cerr << "fuck " << j << ' ' << s << ' ' << cnt[s - 1][k - 1] << ' ' << f[i + 1][j - s] << '\n';
        }
      } else {
        for (int s = 1; s <= j; ++s)
          inc(f[i][j], 1ll * coef[s] * f[i + 1][j - s] % kMod);
      }
      // std::cerr << f[i][j] << ' ';
    }
    // std::cerr << '\n';
  }
  std::cout << f[1][n] << '\n';
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