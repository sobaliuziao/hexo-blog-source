---
title: 'CF1893D Colorful Constructive 题解'
date: 2025-09-22 10:47:00
---

## Description

你有 $n$ 个有颜色的立方体，第 $i$ 个立方体的颜色为 $a_i$。

你需要将所有立方体分配到若干个架子上。总共有 $m$ 个架子，第 $i$ 个架子可以放 $s_i$ 个立方体。同时，满足 $s_1 + s_2 + \ldots + s_m = n$。

假设某个容量为 $k$ 的架子上，依次放置了颜色为 $c_1, c_2, \ldots, c_k$ 的立方体。我们定义该架子的“多彩度”为架子上相同颜色的两个立方体之间的最小距离。如果架子上的所有立方体颜色都不同，则多彩度被认为等于架子的容量 $k$。

更正式地，$c_1, c_2, \ldots, c_k$ 的多彩度定义如下：

- 如果 $c_1, c_2, \ldots, c_k$ 的颜色都不同，则多彩度为 $k$。
- 否则，多彩度为最小的整数 $x \geq 1$，使得存在下标 $i$ $(1 \leq i \leq k - x)$ 满足 $c_i = c_{i+x}$。

对于每个架子，给定了最小要求的多彩度，即给定了 $d_1, d_2, \ldots, d_m$，表示第 $i$ 个架子的多彩度必须 $\geq d_i$。

请你将所有立方体分配到各个架子上，使得每个架子的多彩度都满足要求，或者报告无法做到。

$1\leq n,m\leq 2\times 10^5$。

## Solution

对于架子 $i$ 先分 $\left\lfloor\frac{s_i}{d_i}\right\rfloor$ 个大小为 $d_i$ 的块和一个大小为 $s_i\bmod d_i$ 的块，容易发现每个块内的元素不能相同。

然后经过手玩会发现只要满足每个块内元素不相同就一定能构造。证明就考虑对于一个给定的颜色方案，求出其可能的最大的多彩度。

设 $n$ 为元素总数，$mx$ 为众数出现次数，$cnt_i$ 表示出现次数为 $i$ 的颜色数量。对于出现次数为 $mx$ 的一定是分 $mx$ 组，每组的排列顺序相同。然后让出现次数 $[1,mx-1]$ 内的数去填 $mx-1$ 个间隔，所以多彩度的理论最大值是 $cnt_{mx}+\frac{n-mx\cdot cnt_{mx}}{mx-1}=\frac{n-cnt_{mx}}{mx-1}$。构造考虑按照出现次数从大到小依次放到间隔中，且第 $i$ 个插入的颜色需要接着第 $i-1$ 个颜色的末尾往后加。

由于 $cnt_{mx}\leq s_i\bmod d_i$，所以 $\frac{s_i-cnt_{mx}}{mx-1}\geq d_i$，也就一定能构造。

---

对于把颜色放到架子上，由于所有架子的块互相独立，所以维护一个优先队列表示每个块的长度，然后每次选择当前出现次数最多的块加入当前颜色即可。

把每个架子的每种颜色出现次数求出来后按照证明中的构造即可。

时间复杂度：$O((n+m)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, m;
int a[kMaxN], cnt[kMaxN], sz[kMaxN], d[kMaxN];
std::vector<int> vec[kMaxN];

void dickdreamer() {
  std::cin >> n >> m;
  std::fill_n(cnt + 1, n, 0);
  for (int i = 1; i <= m; ++i) vec[i].clear();
  std::priority_queue<std::pair<int, int>> q;
  for (int i = 1; i <= n; ++i) std::cin >> a[i], ++cnt[a[i]];
  for (int i = 1; i <= m; ++i) std::cin >> sz[i];
  for (int i = 1; i <= m; ++i) {
    std::cin >> d[i];
    for (int j = 1; j <= sz[i] / d[i]; ++j) q.emplace(d[i], i);
    if (sz[i] % d[i]) q.emplace(sz[i] % d[i], i);
  }
  for (int i = 1; i <= n; ++i) {
    std::vector<std::pair<int, int>> vv;
    for (int j = 1; j <= cnt[i]; ++j) {
      if (!q.size()) return void(std::cout << "-1\n");
      auto [l, id] = q.top(); q.pop();
      --l, vec[id].emplace_back(i);
      if (l) vv.emplace_back(l, id);
    }
    for (auto p : vv) q.emplace(p);
  }
  for (int i = 1; i <= m; ++i) {
    static int cnt[kMaxN] = {0};
    std::vector<int> col;
    for (auto x : vec[i]) {
      if (!cnt[x]++) col.emplace_back(x);
    }
    std::sort(col.begin(), col.end(), [&] (int i, int j) { return cnt[i] > cnt[j]; });
    std::vector<std::vector<int>> res(cnt[col[0]]);
    int now = 0;
    for (auto x : col) {
      int lim = (cnt[x] == res.size() ? res.size() : res.size() - 1);
      for (int c = 1; c <= cnt[x]; ++c, now = (now + 1) % lim) {
        assert(now < res.size());
        res[now].emplace_back(x);
      }
    }
    for (auto &vec : res) {
      for (auto x : vec) std::cout << x << ' ';
    }
    std::cout << '\n';
    for (auto x : vec[i]) --cnt[x];
  }
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