---
title: 'CF1991F Triangle Formation 题解'
date: 2024-09-07 16:33:00
---

## Description

你有 $n$ 根棍子，从 $1$ 到 $n$ 编号。第 $i$ 根棍子的长度是 $a_i$。

你需要回答 $q$ 个问题。在每个查询中，你会得到两个整数 $l$ 和 $r$（$1 \le l < r \le n，r − l + 1 \ge 6$）。确定是否可以从编号为 $l$ 到 $r$ 的棒中选择 $6$ 个不同的棒，形成 $2$ 个非退化三角形。

边长为 $a$、$b$ 和 $c$ 的三角形称为非退化三角形，当且仅当 $a<b+c,b<a+c,c<a+b$。

## Solution

先考虑什么样的序列存在至少一个三角形。容易发现把序列排序后，如果存在三角形，则必存在一个长度为 $3$ 的连续区间满足条件。

而如果不存在，则一定满足 $a_i\geq a_{i-1}+a_{i-2}$。经过计算，这样的序列长度一定不超过 $45$，即长度不小于 $45$ 的序列一定存在至少一个三角形。

回到这个题。利用上面那个结论可以得出序列长度 $\geq 48$ 时一定存在答案，因为这里至少存在一个三角形，去掉这个三角形后还剩 $45$ 个数，所以存在第二个。

于是 $r-l+1\geq 48$ 时必然有解，现在需要判断 $r-l+1\leq 47$ 时是否有解。

同样是先排序，把所有形如 $(i,i+1,i+2)$ 且满足 $a_i+a_{i+1}>a_{i+2}$ 的数对拿出来，如果存在两个数对不相交则一定有解。

如果不存在则说明最终的两个三角形是相交的，就像 $(1,2,4),(3,5,6)$ 这种。注意到这时选的 $6$ 个数如果不是连续的 $6$ 个则调整成连续的一定更优，所以只需要对于所有连续的 $6$ 个数暴力判断即可。

时间复杂度：$O(n\log V\log\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, q;
int a[kMaxN];

bool check(int64_t x, int64_t y, int64_t z) {
  return x + y > z && x + z > y && y + z > x;
}

bool check(int l, int r) {
  std::vector<int> vec;
  for (int i = l; i <= r; ++i) vec.emplace_back(a[i]);
  std::sort(vec.begin(), vec.end());
  int mi = 1e9;
  for (int i = 2; i < (int)vec.size(); ++i) {
    if (check(vec[i - 2], vec[i - 1], vec[i])) {
      if (i - 2 > mi) return 1;
      if (mi == 1e9) mi = i;
    }
  }
  for (int i = 0; i + 5 < (int)vec.size(); ++i) {
    if (check(vec[i], vec[i + 1], vec[i + 2]) && check(vec[i + 3], vec[i + 4], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 1], vec[i + 3]) && check(vec[i + 2], vec[i + 4], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 1], vec[i + 4]) && check(vec[i + 2], vec[i + 3], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 1], vec[i + 5]) && check(vec[i + 2], vec[i + 3], vec[i + 4])) return 1;
    if (check(vec[i], vec[i + 2], vec[i + 3]) && check(vec[i + 1], vec[i + 4], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 2], vec[i + 4]) && check(vec[i + 1], vec[i + 3], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 2], vec[i + 5]) && check(vec[i + 1], vec[i + 3], vec[i + 4])) return 1;
    if (check(vec[i], vec[i + 3], vec[i + 4]) && check(vec[i + 1], vec[i + 2], vec[i + 5])) return 1;
    if (check(vec[i], vec[i + 3], vec[i + 5]) && check(vec[i + 1], vec[i + 2], vec[i + 4])) return 1;
    if (check(vec[i], vec[i + 4], vec[i + 5]) && check(vec[i + 1], vec[i + 2], vec[i + 3])) return 1;
  }
  return 0;
}

void dickdreamer() {
  std::cin >> n >> q;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= q; ++i) {
    int l, r;
    std::cin >> l >> r;
    if (r - l + 1 >= 48) std::cout << "YES\n";
    else std::cout << (check(l, r) ? "YES\n" : "NO\n");
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