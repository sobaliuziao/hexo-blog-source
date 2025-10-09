---
title: '[ARC122E] Increasing LCMs 题解'
date: 2024-02-18 16:18:00
---

## Description

给定长度为 $N$ 的正整数序列 $\{A_i\}$，满足 $A_i$ 单调升。

问是否能将 $\{A_i\}$ 重排为序列 $\{x_i\}$，满足：

令 $y_i = \operatorname{LCM}(x_1, \dots, x_i)$，$\forall 1\le i<N, y_i<y_{i+1}$（即 $y_i$ 单调升）。

$ 1\ \leq\ N\ \leq\ 100,2\ \leq\ A_1\ <\ A_2\ \cdots\ <\ A_N\ \leq\ 10^{18} $

## Solution

直接构造显然很难，但是注意到一件事情，就是如果一个序列 $B_1,\dots,B_N$ 合法，那么如果把 $B_i$ 放到最后能使得 $y_{N-1}<y_{N}$，则整个序列依然合法。

所以每次从后往前确定数，找到能够满足 $y_{N-1}<y_N$ 的 $A_i$ 放到最后面，只要每次都能找到就一定合法。

时间复杂度：$O(N^3\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 105;

int n;
int a[kMaxN], res[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = n; i; --i) {
    for (int j = i; j; --j) {
      std::swap(a[i], a[j]);
      int lcm = 1;
      bool fl = 1;
      for (int k = 1; k < i; ++k) {
        int val = std::__gcd(a[k], a[i]);
        lcm = lcm / std::__gcd(lcm, val) * val;
        if (lcm % a[i] == 0) {
          fl = 0;
          break;
        }
      }
      if (fl) break;
      else if (j == 1) return void(std::cout << "No\n");
      std::swap(a[i], a[j]);
    }
  }
  std::cout << "Yes\n";
  for (int i = 1; i <= n; ++i) std::cout << a[i] << ' ';
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