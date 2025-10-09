---
title: [ARC166D] Interval Counts 题解
date: 2023-10-28 20:33:00
---

## Description

给定正整数 $n$ 和长度为 $n$ 的序列 $x_i,y_i$，保证 $x_i$ 单调递增。你要构造 $m$ 个区间 $[L_i,R_i]$（$m$ 由你指定），使每个 $x_i$ 恰好被 $y_i$ 个区间包含。

最大化 $\min_{i=1}^m \{R_i-L_i\}$，并求该值。无穷输出 $-1$。

$n\leq 2\times 10^5,1\leq x_i,y_i\leq 10^9$。

## Solution

考虑贪心。

假设当前已经满足了 $1\sim i-1$ 的限制，维护一个队列表示当前还没确定右端点的所有左端点。

如果 $y_i=y_{i-1}$，那么只要让原来右端点接在 $x_{i-1}$ 的区间接到 $x_i$ 即可。

如果 $y_i>y_{i-1}$，这说明原来的区间就算全部接到 $x_i$ 上还不够，需要再加 $y_i-y_{i-1}$ 个左端点为 $x_{i-1}+1$ 的区间。

如果 $y_i<y_{i-1}$，说明要删掉 $y_{i-1}-y_i$ 个区间，由于要让最小值最大，所以需要删掉左端点最小的区间。

于是只要维护一个左端点递增的区间即可，由于区间数很多，顺便记一个这个左端点的个数即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int x[kMaxN], y[kMaxN];
std::pair<int, int> q[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i)
    std::cin >> x[i];
  for (int i = 1; i <= n; ++i)
    std::cin >> y[i];
  x[0] = -1e18;
  int h = 1, t = 0, ans = 1e18;
  for (int i = 1; i <= n; ++i) {
    if (y[i] > y[i - 1]) {
      q[++t] = {x[i - 1] + 1, y[i] - y[i - 1]};
    } else if (y[i] < y[i - 1]) {
      int d = y[i - 1] - y[i];
      for (; d && h <= t;) {
        int w = std::min(q[h].second, d);
        d -= w, q[h].second -= w;
        ans = std::min(ans, x[i] - 1 - q[h].first);
        if (!q[h].second) ++h;
        else break;
      }
    }
  }
  std::cout << (ans == 1e18 ? -1 : ans) << '\n';
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