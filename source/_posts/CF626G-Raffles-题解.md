---
title: CF626G Raffles 题解
date: 2024-07-28 17:37:00
---

## Description

- 有 $n$ 个奖池，第 $i$ 个奖池的奖金是 $p_i$，已经有 $l_i$ 张彩票押在上面。
- 现在你有 $t$ 张彩票，你需要将你的彩票分配到这些奖池中，并且保证你在每个奖池中押的彩票数**不能超过该奖池原有的彩票数**。
- 若你在第 $i$ 个奖池中押了 $t_i$ 张彩票，则你中奖的概率为 $\frac{t_i}{t_i + l_i}$，若你中奖，你可以获得这个奖池的全部奖金 $p_i$。
- 一共有 $q$ 次事件，每次事件会使某个 $l_i$ 加 $1$ 或减 $1$。
- 你需要在每个事件后求出在最佳方案下你获得的奖金总数的最大期望值。
- $n,t,q \le 2 \times 10^5$，$p_i,l_i \le 10^3$，答案精度误差 $\le 10^{-6}$。

## Solution

首先单次 $O(t\log n)$ 是很容易的，就先假设所有 $t_i=0$，每次取出让 $t_i\to t_i+1$ 的增量的最大值，由于对于每个 $i$，$t_i$ 越大增量越小，所以每次贪心取最大值是对的。

考虑怎么支持修改。

不妨设修改了 $x$，让 $l_x\leftarrow l_x+1$。

有一个结论是每次选出当前已经选择的 $\Delta$ 里的最小值和没选的 $\Delta$ 的最大值，如果这个最小值小于最大值就贪心地替换，替换的次数不超过 $1$ 次。

证明就考虑设 $\Delta E(k)=\dfrac{p_xl_x}{(l_x+k)(l_x+k+1)},\Delta E'(k)=\dfrac{p_x(l_x+1)}{(l_x+k+1)(l_x+k+2)}$。

注意到 $\Delta E'(k)=\dfrac{p_x(l_x+1)}{(l_x+k+1)(l_x+k+2)}>\Delta E(k+1)=\dfrac{p_xl_x}{(l_x+k+1)(l_x+k+2)}$，所以 $x$ 只有可能是选了的最小的增量被替换，所以最多只有一次。

对于 $l_x\leftarrow l_x-1$ 的情况同理可证结论仍成立。

时间复杂度：$O((n+q+t)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using f64 = long double;

const int kMaxN = 2e5 + 5;

int n, m, q;
f64 ans;
int l[kMaxN], p[kMaxN], t[kMaxN];
std::multiset<std::pair<f64, int>> st[2];

f64 getdet(int x, int v) {
  return (f64)p[x] * l[x] / (l[x] + t[x]) / (l[x] + t[x] + v);
}

void add(int x) {
  --m;
  st[1].erase({getdet(x, 1), x});
  if (t[x]) st[0].erase({getdet(x, -1), x});
  ans += getdet(x, 1), ++t[x];
  st[0].emplace(getdet(x, -1), x);
  if (t[x] < l[x]) st[1].emplace(getdet(x, 1), x);
}

void del(int x) {
  ++m;
  if (t[x] < l[x]) st[1].erase({getdet(x, 1), x});
  st[0].erase({getdet(x, -1), x});
  ans -= getdet(x, -1), --t[x];
  if (t[x]) st[0].emplace(getdet(x, -1), x);
  st[1].emplace(getdet(x, 1), x);
}

void dickdreamer() {
  std::cin >> n >> m >> q;
  for (int i = 1; i <= n; ++i) std::cin >> p[i];
  for (int i = 1; i <= n; ++i) std::cin >> l[i];
  for (int i = 1; i <= n; ++i) st[1].emplace(getdet(i, 1), i);
  for (; m && !st[1].empty();) add(st[1].rbegin()->second);
  for (int i = 1; i <= q; ++i) {
    int op, x;
    std::cin >> op >> x;
    if (op == 1) {
      if (t[x]) st[0].erase({getdet(x, -1), x});
      if (t[x] < l[x]) st[1].erase({getdet(x, 1), x});
      ans -= (f64)p[x] * t[x] / (t[x] + l[x]);
      ++l[x];
    } else {
      if (t[x] == l[x]) del(x);
      if (t[x]) st[0].erase({getdet(x, -1), x});
      if (t[x] < l[x]) st[1].erase({getdet(x, 1), x});
      ans -= (f64)p[x] * t[x] / (t[x] + l[x]);
      --l[x];
    }
    ans += (f64)p[x] * t[x] / (t[x] + l[x]);
    if (t[x]) st[0].emplace(getdet(x, -1), x);
    if (t[x] < l[x]) st[1].emplace(getdet(x, 1), x);
    for (; m && !st[1].empty();) add(st[1].rbegin()->second);
    if (!st[0].empty() && !st[1].empty()) {
      auto [det1, j1] = *st[0].begin();
      auto [det2, j2] = *st[1].rbegin();
      if (det1 < det2) del(j1), add(j2);
    }
    std::cout << std::fixed << std::setprecision(10) << ans << '\n';
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