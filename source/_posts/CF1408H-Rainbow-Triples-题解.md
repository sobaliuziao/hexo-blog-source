---
title: CF1408H Rainbow Triples 题解
date: 2024-02-28 20:56:00
---

## Description

给定长度为 $n$ 的序列 $p$

找出尽可能多的三元组 $(a_i,b_i,c_i)$ 满足：

- $1\le a_i<b_i<c_i\le n$
- $p_{a_i}=p_{c_i}=0$，$p_{b_i}\ne 0$
- $p_{b_i}$ 互不相同。
- 所有的 $a_i,b_i,c_i$ 互不相同。

输出最多可以选出多少个三元组，多组数据。

$\sum n\le 5\cdot 10^5$

## Solution

设总共有 $c$ 个 $0$，容易发现答案的上界是 $\left\lfloor\frac{c}{2}\right\rfloor$，并且对于每个三元组，$a_i$ 一定在前 $\left\lfloor\frac{c}{2}\right\rfloor$ 个，$c_i$ 一定在最后 $\left\lfloor\frac{c}{2}\right\rfloor$ 个。

因为如果不满足那么调整成这个情况一定更优。

然后考虑一个 $b_i$，如果在前 $\left\lfloor\frac{c}{2}\right\rfloor$ 个 $0$ 的区间里，那么如果它能够与 $\left\lfloor\frac{c}{2}\right\rfloor$ 匹配那么一定能和右边的 $0$ 匹配，如果在右边则一定能与左边的 $0$ 匹配。

所以只要把 $mid$ 左边和右边的分开考虑然后把答案相加与 $\left\lfloor\frac{c}{2}\right\rfloor$ 取 min。

容易发现对于一个颜色，只有 $<mid$ 的最大位置和 $>mid$ 的最小位置有意义，所以把这个颜色与 $<mid$ 的位置之前的 $0$ 和 $>mid$ 的位置之后的 $0$ 连边跑网络流即可，显然过不了。

注意到一个颜色匹配的一定是一个前缀+一个后缀，所以把 $mid$ 之前的 $0$ 移到最后面，那么每个颜色匹配的就是一个区间 $[l,r]$，于是只要先按 $r$ 排序然后贪心即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>
 
// #define int int64_t
 
const int kMaxN = 5e5 + 5;
 
int n;
int a[kMaxN];
std::vector<int> vec[kMaxN];
 
void dickdreamer() {
  std::cin >> n;
  for (int i = 0; i <= n; ++i) vec[i].clear();
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    vec[a[i]].emplace_back(i);
  }
  // if (vec[0].size() & 1) vec[0].erase(vec[0].begin() + vec[0].size() / 2);
  if (!vec[0].size()) return void(std::cout << "0\n");
  int cnt = vec[0].size(), L, R;
  if (vec[0].size() & 1) L = R = vec[0][(vec[0].size() - 1) / 2];
  else L = vec[0][vec[0].size() / 2 - 1], R = vec[0][vec[0].size() / 2];
  std::vector<std::pair<int, int>> rg;
  for (int i = 1; i <= n; ++i) {
    if (!vec[i].size()) continue;
    int id1 = -1, id2 = n + 1;
    for (auto x : vec[i]) {
      if (x < R) id1 = x;
      if (x > L && id2 == n + 1) id2 = x;
    }
    id1 = std::lower_bound(vec[0].begin(), vec[0].end(), id1) - vec[0].begin() - 1;
    id2 = std::lower_bound(vec[0].begin(), vec[0].end(), id2) - vec[0].begin();
    rg.emplace_back(id2, cnt + id1);
  }
  auto cmp = [](const std::pair<int, int> &p1, const std::pair<int, int> &p2) {
    return std::make_pair(p1.second, p1.first) < std::make_pair(p2.second, p2.first);
  };
  std::sort(rg.begin(), rg.end(), cmp);
  std::set<int> st;
  for (int i = 0; i < 2 * cnt; ++i) st.emplace(i);
  int ans = 0;
  for (auto p : rg) {
    auto it = st.lower_bound(p.first);
    if (it != st.end() && *it <= p.second) ++ans, st.erase(it);
  }
  std::cout << std::min(ans, cnt / 2) << '\n';
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