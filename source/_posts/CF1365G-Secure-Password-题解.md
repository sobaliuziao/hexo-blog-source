---
title: CF1365G Secure Password 题解
date: 2024-02-17 19:38:00
---

## Description

本题是**交互题**。

有一个固定的数组 $A$，同时通过数组 $A$ 构造出数组 $P$，具体来讲，$P_i$ 是 $A$ 中除 $A_i$ 外的所有元素的按位或。

你需要在最多 $13$ 次询问中得到最后的 $P$ 数组。

$2\leq n\leq 1000$。

## Solution

首先有一个 $2\log n$ 的是注意到对于任意两个不同的数 $i,j$，则必有至少一位满足 $i$ 和 $j$ 不同，所以只要维护 $val_{i,0/1}$ 表示第 $i$ 位为 $0/1$ 的数的或，那么每次只要把与 $i$ 不同的位的 $val$ 值或起来即可。

考虑怎么优化到 $\log n$。

容易发现要想优化掉那个 $2$，就必定要构造出一种方案，使得 $id_i$ 存在一位为 $1$，$id_j$ 存在一位为 $0$。

所以只要给每个 $i$ 分配 popcount 相同的 $id$ 即可满足条件。

经过计算，这些 $id$ 最小位数是 $13$，因为 $\binom{13}{6}>1000$。

总询问次数：$13$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e3 + 5;

int n;
int id[kMaxN], val[13];

int ask(std::vector<int> vec) {
  if (!vec.size()) return 0;
  std::cout << "? " << vec.size() << ' ';
  for (auto x : vec) std::cout << x << ' ';
  std::cout << std::endl;
  int x;
  std::cin >> x;
  return x;
}

void dickdreamer() {
  std::cin >> n;
  int cnt = 0;
  for (int i = 0; i < (1 << 13); ++i) {
    if (__builtin_popcount(i) == 6) {
      id[++cnt] = i;
      if (cnt == n) break;
    }
  }
  for (int i = 0; i < 13; ++i) {
    std::vector<int> vec;
    for (int j = 1; j <= n; ++j)
      if (~id[j] >> i & 1)
        vec.emplace_back(j);
    val[i] = ask(vec);
  }
  std::cout << "! ";
  for (int i = 1; i <= n; ++i) {
    int res = 0;
    for (int j = 0; j < 13; ++j)
      if (id[i] >> j & 1)
        res |= val[j];
    std::cout << res << ' ';
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