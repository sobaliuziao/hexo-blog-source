---
title: 'P10139 [USACO24JAN] Nap Sort G 题解'
date: 2024-02-23 22:00:00
---

## Description

Bessie 正在尝试使用她自己的排序算法对一个整数数组进行排序。她有一堆共 $N$（$1\le N\le 2\cdot 10^5$）个整数 $a_1,a_2,\ldots,a_N$（$1\le a_i\le 10^{11}$），她将会按排序顺序将这些数放入一个单独的数组中。她反复查找这堆数中的最小数，将其删除，同时将其添加到数组的末尾。Bessie 在 $p$ 个数的堆中找到最小数需要花费 $p$ 秒。

Farmer John 命令了农场中其他一些奶牛帮助 Bessie 完成任务，她们很懒，然而 Bessie 利用了这一点。她将整数分成两堆：Bessie 堆和助手堆。对于 Bessie 堆中的每个整数，她会正常执行她的算法。对于助手堆中的每个整数，她将其分配给不同的助手奶牛。Farmer John 有一个很大的农场，所以 Bessie 可以找来任意多的助手奶牛。如果助手收到整数 $a_i$，Bessie 会指示该牛小睡 $a_i$ 秒，并在她们醒来时立即将该整数添加到数组末尾。如果 Bessie 和一个助手同时向数组添加整数，Bessie 的整数将优先被添加，因为她是领导者。如果多个助手被分配了相同的整数，她们会同时将多个该整数添加到数组中。

请帮助 Bessie 划分她的数，使得最终得到的数组是排序的，并使得排序该数组所需的时间最少。

## Solution

先把 $a$ 数组排序，不妨设 Bessie 分配到了 $k$ 头牛，那么答案一定是 $a_{n}$ 或 $\frac{k\times(k+1)}{2}$。容易发现答案为 $a_n$ 的情况一定能满足，考虑求后面那个的最小值。

先考虑对于一个 $k$ 如何求其是否可行，钦定最后一个一定是 Bessie。那么从后往前扫显然剩下的 Bessie 数一定越多越好，但是如果 $a_i$ 大于后面的最小 sum，则 $a_i$ 一定要选 Bessie，否则维持现状一定更优。但是如果 $a_i=sum$ 根据题意同一时间 Bessie 选的牛回放前面，则这个时候 $a_i$ 会被放到后面的牛的后面，显然不合法。所以 $a_i$ 选 Bessie 的条件为 $a_i\geq sum$。如果最后选了的数量 $>k$ 就一定可行，否则不可行。

容易发现这个对于 $k$ 具有单调性，所以二分即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN];

bool check(int k) {
  int now = 1, sum = k * (k + 1) / 2;
  for (int i = n - 1; i; --i) {
    if (a[i] >= sum) sum -= (now++);
    if (now > k) return 0;
  }
  return 1;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  std::sort(a + 1, a + 1 + n);
  int L = 0, R = n, res = n;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (check(mid)) R = res = mid;
    else L = mid;
  }
  std::cout << std::min(res * (res + 1) / 2, a[n]) << '\n';
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