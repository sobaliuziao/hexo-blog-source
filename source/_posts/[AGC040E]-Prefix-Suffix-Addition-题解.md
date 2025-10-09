---
title: '[AGC040E] Prefix Suffix Addition 题解'
date: 2025-02-20 11:30:00
---

## Description

你有一个长为 $N$ 的序列 $x_1,x_2,\ldots,x_N$，一开始全部为 $0$，你现在可以以任意顺序进行任意次以下两种操作：

1. 选定整数 $k(1\leq k\leq N)$ 与不下降非负序列 $c_1,c_2,\ldots,c_k$，对所有 $1\leq i\leq k$，令 $x_i$ 加上 $c_i$。
2. 选定整数 $k(1\leq k\leq N)$ 与不上升非负序列 $c_1,c_2,\ldots,c_k$，对所有 $1\leq i\leq k$，令 $x_{N-k+i}$ 加上 $c_i$。

问最少进行多少次操作使得最后对任意 $i$ 有 $x_i=A_i$。

$1\leq N\leq 2\times 10^5,1\leq A_i\leq 10^9$。

## Solution

首先如果只能做 $1$ 操作，答案就是极长不降段的个数。只有 $2$ 操作答案就是极长不升段的个数。

这启发我们将每个 $A_i$ 拆成 $a_i$ 和 $b_i$，分别表示来自 $1$ 操作和 $2$ 操作的贡献，答案即为：$\sum_{i=1}^{\color{red}{N+1}}{\left([a_i<a_{i-1}]+[b_i>b_{i-1}]\right)}$。

考虑 dp。

设 $f_{i,j}$ 表示考虑了前 $i$ 个数，满足 $a_i=j,b_i=A_i-j$ 的最小操作数。

直接转移是 $O(nV)$ 的，但是注意到 $f_{i,j}$ 不升，且 $f_{i,a_i}\geq f_{i,0}-2$，所以用记录一下三种值对应的区间即可。

时间复杂度：$O(n)/O(n\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  // int val = 2, f0 = a[1], f1 = a[1] + 1, f2 = a[1] + 1;
  int val = 0, f0 = 0, f1 = 1, f2 = 1;
  std::function<int(int)> getreal = [&] (int x) -> int {
    if (x >= f2) return 1e9;
    if (x <= f0) return val;
    else if (x <= f1) return val - 1;
    else return val - 2;
  };
  for (int i = 1; i <= n + 1; ++i) {
    int _val, _f0, _f1;
    std::function<int(int, int)> getcoef = [&] (int v1, int v2) -> int {
      return (v1 > v2) + (a[i - 1] - v1 < a[i] - v2);
    };
    std::function<int(int)> calc = [&] (int x) -> int {
      return std::min({getreal(0) + getcoef(0, x), getreal(f0 + 1) + getcoef(f0 + 1, x), getreal(f1 + 1) + getcoef(f1 + 1, x)});
    };
    _val = calc(0), _f0 = 0;
    int L = 0, R = a[i] + 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (calc(mid) >= _val) L = _f0 = mid;
      else R = mid;
    }
    L = _f1 = _f0, R = a[i] + 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (calc(mid) >= _val - 1) L = _f1 = mid;
      else R = mid;
    }
    // std::cerr << i << ' ' << _val << ' ' << _f0 << ' ' << _f1 << " : \n";
    // for (int j = 0; j <= a[i]; ++j) std::cerr << calc(j) << ' ';
    // std::cerr << '\n';
    // if (_f0 <= a[i]) assert(calc(_f0) == _val && calc(_f0 + 1) != _val);
    // if (_f1 <= a[i]) assert(calc(_f1) == _val + 1);
    val = _val, f0 = _f0, f1 = _f1, f2 = a[i] + 1;
  }
  std::cout << val << '\n';
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