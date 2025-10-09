---
title: CF1810G The Maximum Prefix 题解
date: 2024-08-27 22:58:00
---

## Description

构造一个长度最多为 $n$ 的数组 $a$，其每个元素均为 $1$ 或 $-1$。生成方式如下：
+ 选择任意整数 $k\in[1,n]$ 作为 $a$ 的长度。
+ 对于 $\forall i\in[1,k]$，有 $p_i$ 的概率设 $a_i=1$，有 $1-p_i$ 的概率设 $a_i=-1$。

在数列被生成后，计算 $s_i=a_1+a_2+a_3+...+a_i$。特别地，$s_0=0$。此时 $s$ 数组的最大前缀和 $S=max_{i=0}^ks_i$。

现在给定 $n+1$ 个正整数 $h_0,h_1,...,h_n$。$a$ 数组最大前缀和 $S$ 的分数为 $h_s$。现在，对于每个 $k$，你要求出一个数组长度为 $k$ 的期望分数对 $10^9+7$ 取模的结果。

$n\leq 5000$。

## Solution

先考虑给定数组怎么快速求最大前缀和。

显然可以直接求出每个前缀和，再取最大值，但是这样要记两个变量，很难放在 dp 里面。

另一个做法是倒着扫，维护 $s$ 表示当前扫过的后缀的最大前缀和，每次让 $s\leftarrow \max\{s+a_i,0\}$ 即可。

放到本题可以暴力枚举要求答案的前缀，设 $f_{i,j}$ 表示当前倒着扫到了 $i$，目前的最大前缀和为 $j$ 的概率，可以得到转移：$f_{i,j+1}\leftarrow p_if_{i+1,j},f_{i,\max\{j-1,0\}}\leftarrow (1-p_i)f_{i+1,j}$。

最后 $\sum f_{1,i}h_i$ 就是答案。

时间复杂度：$O(n^3)$。

---

这个做法慢在 dp 时要枚举前缀的后缀，dp 状态会很冗余。

考虑怎么正着扫做 dp。

先把这题状态转移的 DAG 建出来，每次相当于是求从一个点开始往后走的期望权值。由于不同前缀的 DAG 是一样的，所以可以让转移边反过来跑期望 dp。

具体的，设 $g_{i,j}$ 表示从末尾已经考虑到了 $i+1$，当前最大前缀和为 $j$ 的期望权值。可以的得到转移：$g_{i,j}=p_ig_{i-1,j+1}+(1-p_i)g_{i-1,\max\{j-1,0\}}$。

边界条件是 $g_{0,i}=h_i$，对于前缀 $[1,i]$ 的答案即为 $g_{i,0}$。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e3 + 5, kMod = 1e9 + 7;

int n;
int p[kMaxN], h[kMaxN], f[kMaxN][kMaxN];

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

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    int x, y;
    std::cin >> x >> y;
    p[i] = 1ll * x * qpow(y) % kMod;
  }
  for (int i = 0; i <= n; ++i) std::cin >> h[i];
  for (int i = 0; i <= n; ++i) f[0][i] = h[i];
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= n; ++j) {
      f[i][j] = add(1ll * p[i] * f[i - 1][j + 1] % kMod, 1ll * sub(1, p[i]) * f[i - 1][std::max(j - 1, 0)] % kMod);
    }
    std::cout << f[i][0] << ' ';
  }
  std::cout << '\n';
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