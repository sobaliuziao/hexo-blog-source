---
title: [AGC061C] First Come First Serve 题解
date: 2024-10-08 10:26:00
---

## Description

有 $n$ 个人来过，第 $i$ 个人在 $a_i$ 时刻来在 $b_i$ 时刻走，每个人可以在来时或走时登记，问可能的登记顺序有多少种。

$n\leq 5\times 10^5$，$a_i,b_i$ 互不相同，$\forall i<n,a_i<a_{i+1},b_{i}<b_{i+1}$。

## Solution

首先如果每个人随便选，有 $2^n$ 种方案。但这显然会算重。考虑构造一种方案使得选的方案和最终排列一一对应。

按照排列从小到大的顺序，如果当前 $(a_i,b_i)$ 中有数，则选 $a_i$，否则选 $b_i$，容易发现这样做一定能够一一对应。

这时一个选择不合法当且仅当对于某个 $i$，$(a_i,b_i)$ 中没数但 $i$ 选了 $b_i$，可以对不合法的位置数进行容斥。

具体的，如果选了 $a_i$ 或 $b_i$，则系数为 $1$，$(a_i,b_i)$ 中没数且选 $b_i$，则系数为 $-1$。

容易发现对于任意两个钦定了不合法的位置 $i,j$，$[a_i,b_i]$ 和 $[a_j,b_j]$ 一定不相交。并且如果设 $pre_i$ 表示最大的 $b_j<a_i$ 的 $j$，$nxt_i$ 表示最小的 $a_j>b_i$ 的 $j$，那么如果 $i$ 不合法，$(pre_i,i)$ 和 $(i,nxt_i)$ 选择一定是固定的。这样就可以 dp 了。

设 $f_i$ 表示前 $i$ 个数的系数之和。那么 $f_i=2f_{i-1}-\sum_{nxt_j+1=i}{f_{pre_j}}$。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e5 + 5, kMod = 998244353;

int n;
int a[kMaxN], b[kMaxN], pre[kMaxN], nxt[kMaxN], f[kMaxN];
std::vector<int> vec[kMaxN];

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
  for (int i = 1; i <= n; ++i) std::cin >> a[i] >> b[i];
  for (int i = 1, j = 0; i <= n; ++i) {
    for (; b[j] < a[i]; ++j) {}
    pre[i] = j;
  }
  a[n + 1] = b[n + 1] = 2 * n + 1;
  for (int i = n, j = n + 1; i; --i) {
    for (; a[j] > b[i]; --j) {}
    nxt[i] = j;
  }
  for (int i = 1; i <= n; ++i) vec[nxt[i]].emplace_back(pre[i] - 1);
  f[0] = 1;
  for (int i = 1; i <= n; ++i) {
    f[i] = 2ll * f[i - 1] % kMod;
    for (auto j : vec[i]) dec(f[i], f[j]);
  }
  std::cout << f[n] << '\n';
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