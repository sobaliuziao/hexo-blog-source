---
title: CF2115D Gellyfish and Forget-Me-Not 题解
date: 2025-07-22 20:15:00
---

## Description

Gellyfish 和 Flower 正在玩一个游戏。

该游戏包含两个长度为 $n$ 的整数数组 $a_1,a_2,\ldots,a_n$ 和 $b_1,b_2,\ldots,b_n$，以及一个长度为 $n$ 的二进制字符串 $c_1c_2\ldots c_n$。

还有一个整数 $x$，初始值为 $0$。

游戏进行 $n$ 回合。对于 $i = 1,2,\ldots,n$，每一回合如下进行：

1. 如果 $c_i = 0$，那么 Gellyfish 是该回合的操作者。否则，如果 $c_i = 1$，那么 Flower 是该回合的操作者。
2. 当前操作者必须执行以下两个操作之一：

   * 将 $x := x \oplus a_i$；
   * 将 $x := x \oplus b_i$。

这里，$⊕$ 表示[按位异或操作](https://en.wikipedia.org/wiki/Bitwise_operation#XOR)。

Gellyfish 希望使 $x$ 的最终值尽可能小，而 Flower 则希望使它尽可能大。

如果双方都采取最优策略，求 $n$ 回合后 $x$ 的最终值。

$n\leq 10^5,0\leq a_i,b_i<2^{60}$。

## Solution

先让 $b_i$ 和 $res$ 异或上 $a_i$，现在相当于是选择一些 $b_i$ 给 $res$ 异或上。

首先考虑只有一位怎么做。

容易发现最大的一个 $b_i=1$ 的 $i$ 可以控制这一位的最终取值，这一个 $i$ 的最终取值取决于 $1\sim i-1$ 的所有 $b_j=1$ 的位置选择数量的奇偶性。

对于位数不止 $1$ 的情况，先找到 $i$，由于 $b_i$ 的选择只跟其余 $b_j=1$ 的选择数量奇偶性有关，所以让 $b_j\leftarrow b_j\oplus b_i$ 后对答案的没有影响，同时最高位就只有 $i$ 是 $1$ 了，可以通过 $c_i$ 和 $res$ 在这一位的取值来确定现在的 $b_i$ 需不需要选。

由于 $b_i$ 的选法是固定的了，所以让 $res$ 异或上 $b_i$ 的选择后把 $b_i$ 删掉即可，然后对后面的位做同样的事情。

时间复杂度：$O(n\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

int n;
int a[kMaxN], b[kMaxN], c[kMaxN];

void dickdreamer() {
  std::cin >> n;
  int res = 0;
  for (int i = 1; i <= n; ++i) std::cin >> a[i], res ^= a[i];
  for (int i = 1; i <= n; ++i) std::cin >> b[i], b[i] ^= a[i];
  std::string str;
  std::cin >> str;
  for (int i = 1; i <= n; ++i) c[i] = str[i - 1] - '0';
  for (int c = 60; ~c; --c) {
    int x = 0;
    for (int i = n; i; --i) {
      if (b[i] >> c & 1) {
        if (x) {
          b[i] ^= x;
        } else {
          if ((res >> c & 1) != ::c[i]) res ^= b[i];
          x = b[i], b[i] = 0;
        }
      }
    }
  }
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