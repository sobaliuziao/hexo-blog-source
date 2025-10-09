---
title: [AGC018C] Coins 题解
date: 2024-02-27 22:52:00
---

## Description

有 $x+y+z$ 个人，第 $i$ 个人有 $A_i$ 个金币，$B_i$ 个银币，$C_i$ 个铜币。

要选出 $x$ 个人获得其金币，选出 $y$ 个人获得其银币，选出 $z$ 个人获得其铜币。在不重复选某个人的情况下，最大化获得的币的总数。 

$x+y+z\le 10 ^ 5$。

## Solution

先默认每个人都选 $C$，让每个 $A_i,B_i$ 都减 $C_i$，相当于就是要选出 $x$ 个人选 $A$，$y$ 个人选 $B$，最大化总和。

注意到如果 $i$ 选 $A$，$j$ 选 $B$ 且 $A_i+B_j<A_j+B_i$ 则把 $i,j$ 互换会更优，这个条件等价于 $A_i-B_i<A_j-B_j$。

所以如果把所有人按照 $A_i-B_i$ 排序，选 $B$ 的一定是选了的人里最靠前的 $y$ 个，而选 $A$ 的一定是最靠后的 $x$ 个，搞个优先队列即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

int n, x, y, z, ans;
int a[kMaxN], b[kMaxN], c[kMaxN], pre[kMaxN], suf[kMaxN];
std::vector<std::tuple<int, int, int>> vec;

void getpre() {
  std::multiset<int> st;
  int sum = 0;
  for (int i = 1; i <= n; ++i) {
    int val = std::get<2>(vec[i]);
    if (st.size() < y) sum += val, st.emplace(val);
    else if (*st.begin() < val) sum += val - *st.begin(), st.erase(st.begin()), st.emplace(val);
    if (i >= y) pre[i] = sum;
  }
}

void getsuf() {
  std::multiset<int> st;
  int sum = 0;
  for (int i = n; i; --i) {
    int val = std::get<1>(vec[i]);
    if (st.size() < x) sum += val, st.emplace(val);
    else if (*st.begin() < val) sum += val - *st.begin(), st.erase(st.begin()), st.emplace(val);
    if (i <= n - x + 1) suf[i] = sum;
  }
}

void dickdreamer() {
  std::cin >> x >> y >> z;
  n = x + y + z;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i] >> b[i] >> c[i];
    ans += c[i], a[i] -= c[i], b[i] -= c[i];
    vec.emplace_back(a[i] - b[i], a[i], b[i]);
  }
  vec.emplace_back(-2e9, 0, 0);
  std::sort(vec.begin(), vec.end());
  getpre(), getsuf();
  int tmp = -1e18;
  for (int i = y; i <= n - x; ++i)
    tmp = std::max(tmp, pre[i] + suf[i + 1]);
  std::cout << ans + tmp << '\n';
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
  std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```