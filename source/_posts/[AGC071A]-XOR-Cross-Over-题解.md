---
title: '[AGC071A] XOR Cross Over 题解'
date: 2025-04-02 09:30:00
---

## Description

有一块黑板，上面写有非负整数序列。初始时，黑板上仅写有一个长度为 $ N $ 的非负整数序列 $ A=(A_1,A_2,\dots,A_N) $。

持续进行以下操作，直到黑板上所有非负整数序列的长度均为 $ 1 $：

- 选择黑板上一个长度至少为 $ 2 $ 的非负整数序列并将其擦除。设选中的非负整数序列为 $ B=(B_1,B_2,\dots,B_n) $。接着选择一个满足 $ 1 \leq k < n $ 的整数 $ k $，计算 $X = B_1 \oplus B_2 \oplus \dots \oplus B_k $ 和 $Y = B_{k+1} \oplus B_{k+2} \oplus \dots \oplus B_n$。最后在黑板写入两个新的非负整数序列：$(B_1 \oplus Y, B_2 \oplus Y, \dots, B_k \oplus Y)$ 和 $ (B_{k+1} \oplus X, B_{k+2} \oplus X, \dots, B_n \oplus X)$。

其中，$ \oplus $ 表示按位异或（bitwise XOR）运算。

在完成所有操作后，设黑板上 $N$ 个长度为 $1$ 的非负整数序列为 $(C_1),(C_2),\dots,(C_N)$，求 $\sum_{i=1}^{N}C_i$ 可能的最小值。

$1 \leq N \leq 500$，$0 \leq A_i < 2^{40}$。

## Solution

首先有个显然的观察是每个点的权值是操作树上包含它的最短的长度为**偶数**的区间 $[l,r]$ 的区间异或和。

容易发现两个分开的偶数区间一定互不影响，所以可以设 $f_{l,r}$ 表示 $[l,r]$ 的答案（其中 $r-l+1$ 是偶数）。

设 $[l,r]$ 分成了 $[l,mid]$ 和 $[mid+1,r]$，那么如果两个都是偶数，答案即为 $f_{l,mid}+f_{mid+1,r}$。

如果两个都是奇数，则这两个区间都会有点的答案与 $[l,r]$ 的区间异或和有关，不太好做。

但是注意到一个长度为奇数的区间只会有恰好一个点的答案跟外面的区间有关，因为每次会拆成一个奇数一个偶数，偶数的只跟内部有关，奇数的那边可以继续递归到只剩一个点。

考虑改变一下状态：$f_{l,r}$ 变为只考虑 $[l,r]$ 内部的贡献的最小值。

然后转移时分讨一下 $[l,r]$ 的区间长度和分拆后的区间长度即可。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 505;

int n;
int a[kMaxN], s[kMaxN], f[kMaxN][kMaxN];

void dickdreamer() {
  std::cin >> n;
  memset(f, 0x3f, sizeof(f));
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    s[i] = s[i - 1] ^ a[i];
    f[i][i] = 0;
  }
  for (int len = 2; len <= n; ++len) {
    for (int i = 1; i <= n - len + 1; ++i) {
      int j = i + len - 1;
      if (len % 2 == 0) {
        for (int k = i; k < j; ++k) {
          if ((k - i + 1) % 2 == 0) f[i][j] = std::min(f[i][j], f[i][k] + f[k + 1][j]);
          else f[i][j] = std::min(f[i][j], f[i][k] + f[k + 1][j] + 2 * (s[j] ^ s[i - 1]));
        }
      } else {
        for (int k = i; k < j; ++k) {
          f[i][j] = std::min(f[i][j], f[i][k] + f[k + 1][j]);
        }
      }
    }
  }
  std::cout << f[1][n] + (n & 1) * s[n] << '\n';
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