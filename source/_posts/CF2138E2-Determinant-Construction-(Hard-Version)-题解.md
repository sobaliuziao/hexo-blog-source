---
title: 'CF2138E2 Determinant Construction (Hard Version) 题解'
date: 2025-09-09 16:39:00
---

## Description

给定一个非负整数 $x$。你的任务是构造一个方阵 $M$，使其满足以下所有条件：

1. 矩阵 $M$ 的边长 **不超过 $50$**。
2. 矩阵中每个元素只能取 $-1$、$0$ 或 $1$。
3. 矩阵的行列式值等于 $x$。
4. 矩阵的每一行最多只能有 **$3$ 个非零元素**，每一列最多也只能有 **$3$ 个非零元素**。

## Solution

首先这题是不太好直接构造的，所以只能递推或者组合意义，这里考虑递推构造。

考虑每次从左上开始 $k\times k$ 的矩阵递推到 $(k+1)\times(k+1)$ 的矩阵，设 $D_k$ 为从左上开始 $k\times k$ 的矩阵的行列式。

我们钦定新加的一行一列只有 $(k+1,k+1),(k+1,k),(k,k+1)$ 非零，且 $a_{k+1,k+1}=a_{k+1,k}=1$，那么有两种可能性：

1. $a_{k,k+1}=1$：$D_{k+1}=D_k-D_{k-1}$。
2. $a_{k,k+1}=-1$：$D_{k+1}=D_k+D_{k-1}$。

边界条件是需要满足 $D_0=1,|D_1|\leq 1$。

由于正着做不好做，所以考虑倒着做，同时钦定 $D_i\geq 0$。假设我们知道了 $D_{k-1}$ 和 $D_k$，那么 $D_{k-2}=|D_k-D_{k-1}|$。

假设最终的边长是 $n$，那么 $D_n=x$，对于边长不超过 $80$ 的问题暴力枚举 $D_{n-1}$ 做上面的东西即可通过。

但是这道题暴力枚举不能过。注意到上面那个做法的本质是做辗转相减，而做辗转相减最快的序列是斐波那契数列，同时由于 $\lim_{i\to+\infty}{\frac{\text{fib}(i+1)}{\text{fib}(i)}}=\frac{\sqrt 5-1}{2}$，所以在 $\frac{\sqrt 5-1}{2}\cdot x$ 附近找 $D_{n-1}$ 即可。实测能够通过。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 55;

int n, sz;
int a[kMaxN][kMaxN];

bool check(int x, int y) {
  if (std::__gcd(x, y) != 1) return 0;
  int c = 0;
  for (c = 1; x != 1 || y != 1; ++c) {
    x = abs(x - y), std::swap(x, y);
    if (c > 50) return 0;
  }
  return x <= 1 && c <= 50;
}

void construct(int x, int y) {
  int c = 0, _x = x, _y = y;
  for (c = 1; x != 1 || y != 1; ++c) x = abs(x - y), std::swap(x, y);
  sz = c, x = _x, y = _y;
  memset(a, 0, sizeof(a));
  for (; x != 1 || y != 1; --c) {
    a[c][c] = a[c][c - 1] = 1;
    if (x >= y) a[c - 1][c] = -1;
    else a[c - 1][c] = 1;
    x = abs(x - y), std::swap(x, y);
  }
  assert(c == 1);
  a[1][1] = x;
}

void dickdreamer() {
  std::cin >> n;
  if (n == 1) return void(std::cout << "1\n1\n");
  int p = n * (sqrtl(5) - 1) / 2, m = -1;
  for (int i = 0;; ++i) {
    if (p - i >= 0 && check(n, p - i)) { m = p - i; break; }
    if (check(n, p + i)) { m = p + i; break; }
  }
  construct(n, m);
  std::cout << sz << '\n';
  for (int i = 1; i <= sz; ++i)
    for (int j = 1; j <= sz; ++j)
      std::cout << a[i][j] << " \n"[j == sz];
  // std::cerr << n << ' ' <<  << '\n';
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