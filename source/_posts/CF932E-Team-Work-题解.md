---
title: CF932E Team Work 题解
date: 2023-08-16 20:05:59
tags:
- 题解
- Codeforces
- 数学
- 斯特林数
categories:
- 题解
- 数学
- 斯特林数
---

## Description

给定 $n,k$，求：

$$\displaystyle\sum_{i=1}^{n}{\binom{n}{i}\times i^k}$$

$1\leq k\leq 5000,1\leq n\leq 10^9$。

<!--more-->

## Solution

看到那个 $i^k$ 很不爽，但是 $k$ 很小，考虑用斯特林数改写一下：

$$i^k=\sum_{j=0}^{k}{\binom{i}{j}\left \{ \begin{matrix} k\\ j \end{matrix} \right \}\cdot j!}$$

代回原式得：

$$\displaystyle
\begin{aligned}
&\sum_{i=0}^{n}{\binom{n}{i}\cdot\sum_{j=0}^{k}{\binom{i}{j}\left \{ {\begin{matrix} k\\ j \end{matrix}} \right \} j!} }\\
=&\sum_{j=0}^{k}{j!\left\{\begin{matrix}k\\j\end{matrix}\right\}\cdot\sum_{i=0}^{n}{\binom{n}{i}\binom{i}{j}}}\\
=&\sum_{j=0}^{k}{j!\left\{\begin{matrix}k\\j\end{matrix}\right\}\cdot\sum_{i=j}^{n}{\frac{n!}{i!(n-i)!}\cdot \frac{i!}{j!(i-j)!}}}\\
=&n!\sum_{j=0}^{k}{\left\{\begin{matrix}k\\j\end{matrix}\right\}\cdot\sum_{i=j}^{n}{\frac{\binom{n-j}{i-j}}{(n-j)!}}}\\
=&n!\sum_{j=0}^{k}{\frac{1}{(n-j)!}\left\{\begin{matrix}k\\j\end{matrix}\right\}\sum_{i=0}^{n-j}{\binom{n-j}{i}}}\\
=&n!\sum_{j=0}^{k}{\frac{2^{n-j}}{(n-j)!}\cdot \left\{\begin{matrix}k\\j\end{matrix}\right\}}\\
\end{aligned}$$

于是直接预处理出斯特林数即可做到 $O(k^2+k\log n)$，如果用卷积预处理的话就可以做到 $O(k\log k+k\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;

const int kMod = 1e9 + 7;

int s[5005][5005];

int qpow(int bs, int idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (i64)bs * bs % kMod)
    if (idx & 1)
      ret = (i64)ret * bs % kMod;
  return ret;
}

void dickdreamer() {
  int n, k, ans = 0;
  std::cin >> n >> k;
  s[0][0] = 1;
  for (int i = 1; i <= k; ++i) {
    for (int j = 1; j <= i; ++j) {
      s[i][j] = (s[i - 1][j - 1] + (i64)j * s[i - 1][j] % kMod) % kMod;
    }
  }
  for (int i = 0, c = 1; i <= std::min(n, k); ++i) {
    ans = (ans + (i64)s[k][i] * c % kMod * qpow(2, n - i) % kMod) % kMod;
    c = (i64)c * (n - i) % kMod;
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
