---
title: 'P10280 [USACO24OPEN] Cowreography G 题解'
date: 2024-07-23 21:20:00
---

## Description

奶牛们组了一支舞蹈队，Farmer John 是她们的编舞！舞蹈队最新而最精彩的舞蹈有 $N$ 头奶牛（$2\le N\le 10^6$）排成一行。舞蹈中的每次动作都涉及两头奶牛，至多相距 $K$ 个位置（$1\le K < N$），优雅地跳起并降落在对方的位置上。

队伍中有两种奶牛——更赛牛（Guernsey）和荷斯坦牛（Holstein）。因此，Farmer John 将这一舞蹈记录为一系列**长为 $N$ 的 `01` 字符串**，其中 `0` 代表更赛牛，`1` 代表荷斯坦牛，整个字符串表示奶牛在这一行中是如何排列的。

不幸的是，Farmer Nhoj（对手团队的编舞）蓄意破坏了这一舞蹈，并清除了除第一个和最后一个 `01` 字符串之外的所有内容！由于一场大型比赛即将开始，Farmer John 必须抓紧每一秒重建这一舞蹈。

给定这两个 `01` 字符串，帮助 Farmer John 求出舞蹈中的最小动作数量！

## Solution

考虑交换一对 $i,j(a_i\neq a_j)$ 所用的代价，结论是 $\left\lceil\frac{|i-j|}{k}\right\rceil$。

证明就考虑数学归纳法，不妨设 $i<j$ 且长度小于 $j-i$ 的已经满足结论，容易发现对于 $j-i\leq k$ 的 $(i,j)$ 一定满足条件。

对于 $i<s<j$，如果 $a_i=a_s$ 则先交换 $(j,s)$ 再交换 $(i,s)$，否则先交换 $(i,s)$ 在交换 $(j,s)$，对应的代价为 $\left\lceil\frac{s-i}{k}\right\rceil+\left\lceil\frac{j-s}{k}\right\rceil$，容易发现当 $s$ 取 $i+k$ 时可以取到最小值，即为 $\left\lceil\frac{|i-j|}{k}\right\rceil$。

有了这个结论就可发现这里的交换一定是两两匹配，即在一张二分图上匹配。

如果没有取上整就从前往后扫，如果 $a_i\neq b_i$ 就找到任意一个还没匹配的 $j$ 使得 $a_i\neq a_j$ 匹配，容易发现这个一定是最小值。

如果有了取上整，感性理解可以发现这里需要让 $(i-j)\bmod k$ 的和尽可能小，所以只要把上面选任意一个匹配变为选使得 $(i-j)\bmod k$ 最小的 $j$ 匹配即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

int n, k;
std::string a, b;

void dickdreamer() {
  std::cin >> n >> k >> a >> b;
  a = " " + a, b = " " + b;
  std::set<std::pair<int, int>> st[2];
  int64_t ans = 0;
  for (int i = 1; i <= n; ++i) {
    if (a[i] == b[i]) continue;
    int oa = a[i] - '0', ob = b[i] - '0';
    if (!st[ob].empty()) {
      auto it = st[ob].lower_bound({i % k, 0});
      if (it == st[ob].end()) it = st[ob].begin();
      ans += (i - it->second + k - 1) / k;
      st[ob].erase(it);
    } else {
      st[oa].emplace(i % k, i);
    }
  }
  std::cout << ans << '\n';
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