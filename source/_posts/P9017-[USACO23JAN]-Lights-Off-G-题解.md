---
title: 'P9017 [USACO23JAN] Lights Off G 题解'
date: 2023-07-27 16:27:00
---

## Description

给定正整数 $N$，和两个长为 $N$ 的 $01$ 序列 $a$ 和 $b$。定义一次操作为：

1. 将 $b$ 序列中的一个值翻转（即 $0$ 变成 $1$，$1$ 变成 $0$，下同）。
2. 对于 $b$ 序列中每个值为 $1$ 的位置，将 $a$ 序列中对应位置的值翻转。
3. 将 $b$ 序列向右循环移位 $1$ 位。即若当前 $b$ 序列为 $b_1b_2\cdots b_{n}$，则接下来变为 $b_{n}b_1b_2\cdots b_{n-1}$。

有 $T$ 次询问，对每一次询问，你需要回答出至少需要几次操作，才能使 $a$ 序列中每一个位置的值都变为 $0$。

[link](https://www.luogu.com.cn/problem/P9017)

## Solution

显然可以把 $a,b$ 数组看成两个数，操作一就是对 $b$ 的某一位取反，操作二就是让 $a$ 异或 $b$，操作三是让 $b\leftarrow \left\lfloor \frac{b}{2} \right\rfloor$。

容易发现操作数不超过 $3n$，因为可以先用至多 $n$ 次操作把 $b$ 变成 $0$。然后每连续两次操作就让 $b$ 的某一位变成 $1$，把 $a$ 的这一位消掉，然后 $b$ 清空。

然而这样做是 $O(T\cdot n^n)$ 的，过不了且没法优化。

---

观察可知，如果第 $i$ 次操作将第 $j$ 位异或 $1$，总共进行 $s$ 次操作，那么这次操作对最终 $a$ 的贡献就是 $j\sim j+s-i$ 这些位取反（在模 $n$ 意义下）。

这样就可以 dp 了。

设 $f_{i,j}$ 表示进行恰好 $i$ 次操作，能否让 $a$ 变成 $j$，设 $x$ 为任意一个模 $n$ 意义下连续的长度为 $1$ 的数组所对应的状态，那么就让 $f_{i,j}\leftarrow f_{i-1,j\oplus x\oplus b}$。

初始 $f_{0,a}=1$，时间复杂度：$O(T\cdot n\cdot 2^{n})$，过不了。

---

考虑把操作一的贡献和操作二、三的贡献拆开算。操作一所做的贡献就相当于初始 $b=0$ 进行若干次操作对 $a$ 的贡献，显然可以预处理，即设 $f_{i,j}$ 表示 $b$ 初始值为 $0$，对 $a$ 能否做出 $j$ 的贡献。

设 $x$ 为任意一个模 $n$ 意义下连续的长度为 $1$ 的数组所对应的状态，那么就让 $f_{i,j}\leftarrow f_{i-1,j\oplus x}$。

而操作二、三就是对 $b$ 进行这么多操作的异或和，枚举操作次数即可求得。

时间复杂度：$O(n^2\cdot 2^n+Tn)$。

具体实现细节见代码

## Code

```cpp
#include <cstdio>
#include <iostream>
#include <map>

// #define int int64_t

int n, a, b;
int f[100][1 << 20];

int shift(int x) {
  return (x >> 1) + (1 << n - 1) * (x & 1);
}

int tonum(std::string s) {
  int ret = 0;
  for (int i = 0; i < static_cast<int>(s.size()); ++i)
    ret = (ret << 1) + s[i] - '0';
  return ret;
}

int calc(int a, int b) {
  for (int i = 0; i <= 3 * n; ++i, b = shift(b)) {
    if (f[i][a]) return i;
    a ^= b;
  }
  return -1;
}

void prework() {
  f[0][0] = 1;
  for (int i = 1; i <= 3 * n; ++i) {
    int s = (1 << ((i - 1) % n + 1)) - 1;
    for (int j = 0; j < n; ++j, s = shift(s)) {
      for (int k = 0; k < (1 << n); ++k)
        f[i][k] |= f[i - 1][k ^ s];
    }
  }
}

void dickdreamer() {
  int t;
  std::cin >> t >> n;
  prework();
  for (; t; --t) {
    std::string s, t;
    std::cin >> s >> t;
    a = tonum(s), b = tonum(t);
    std::cout << calc(a, b) << '\n';
  }
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