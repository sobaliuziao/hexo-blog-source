---
title: [AGC064D] Red and Blue Chips 题解
date: 2024-10-09 11:49:00
---

## Description

你有 $N$ 个字符串，初始情况下每个字符串只有一个字符，是 $\texttt{R}$ 或  $\texttt{B}$，保证第 $N$ 个字符串是 $\texttt{B}$。

你需要对每个 $i=1,2,\cdots ,n-1$ 执行以下操作：

- 选择一个整数 $j$ 使得 $i< j\le n$，且第 $j$ 个字符串的最后一个字符是 $\texttt{B}$，然后把第 $i$ 个字符串整体拼接在第 $j$ 个字符串的**前面**。

问最后可以得到多少种本质不同的第 $N$ 个字符串，对 $998244353$ 取模。

$2\leq N\leq 300,s_N=\texttt{B}$。

## Solution

考虑怎么判断一个终止串 $t$ 是否合法。

容易发现终止串形如一棵树的后序遍历的形式，所以可以倒着为每个位置找父亲。

在找父亲的过程中把终止串挂在最后一个 `B` 上，设 $m$ 为原串 `B` 的个数，$f_i$ 表示挂在 $i$ 上的串。

设当前走到了 $i$，如果当前 $s_i$ 为 `R`，就选择一个 $f_j$ 满足 $f_j$ 开头为 `R` 并把开头的 `R` 删掉，表示 $i$ 的父亲为 $j$。否则就需要把某个 $f_j$ 在字符为 `B` 的位置分裂，并且把分裂后前面的串挂在 $i$ 上。

由于我们需要尽量让当前所有 $f_i$ 开头的 `R` 数量和最多，所以每次选择长度最大的极长 `R` 段前分裂一定最优。容易发现这么做如果存在一个时刻满足 $s_i$ 为 `R` 且所有 $f_i$ 的开头都不为 `R`，那么这个串一定不合法。

形式化的描述就是设 $a_i$ 表示**初始串**倒数第 $i$ 个极长 `R` 连续段的长度，$b_i$ 表示**终止串**倒数第 $i$ 个极长 `R` 连续段的长度。

又因为 $b_1$ 显然不能动，所以只能对 $b_2,b_3,\ldots,b_m$ 排序，排序后合法的充分必要条件为 $\forall j\in[1,m],\sum_{i=1}^{j}{a_i}\leq\sum_{i=1}^{j}{b_i}$。

方案数容易 dp 得到。

时间复杂度：$O(n^3\ln n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 305, kMod = 998244353;

int n, m;
int a[kMaxN], sum[kMaxN], f[kMaxN][kMaxN], fac[kMaxN], ifac[kMaxN];
std::string str;

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

void prework(int n = 300) {
  fac[0] = ifac[0] = 1;
  for (int i = 1; i <= n; ++i) {
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = qpow(fac[i]);
  }
}

void dickdreamer() {
  std::cin >> n >> str;
  int lst = 0;
  for (int i = 1; i <= n; ++i) {
    if (str[i - 1] == 'B') {
      a[++m] = i - lst - 1;
      lst = i;
    }
  }
  prework();
  std::reverse(a + 1, a + 1 + m);
  for (int i = 1; i <= m; ++i) sum[i] = sum[i - 1] + a[i];
  int cnt = n - m;
  for (int i = a[1]; i <= cnt; ++i) f[1][i] = fac[m - 1];
  for (int i = cnt; ~i; --i) {
    for (int j = m; j; --j) {
      for (int k = cnt; k >= sum[j]; --k) {
        for (int c = 1; c <= std::min(j, (i ? k / i : n)); ++c) {
          if (k - i * (c - 1) >= sum[j - c + 1]) inc(f[j][k], 1ll * f[j - c][k - i * c] * ifac[c] % kMod);
          else break;
        }
      }
    }
  }
  std::cout << f[m][cnt] << '\n';
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