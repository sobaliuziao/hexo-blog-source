---
title: CF505E Mr. Kitayuta vs. Bamboos 题解
date: 2024-07-04 20:40:00
---

## Description
- 给定 $n$ 个数 $h_{1 \dots n}$。
- 你需要进行 $m$ 轮操作，每轮操作为 $k$ 次修改，每次修改可以选择一个数 $h_i$ 修改为 $\max(h_i - p, 0)$。
- 每轮操作后每个 $h_i$ 将会被修改为 $h_i + a_i$。
- 你需要最小化最终 $h_{1 \dots n}$ 中的最大值。
- $n \le 10^5$，$m \le 5 \times 10^3$，$k \le 10$。

## Solution

注意到要最小化最大值，显然是二分。假设当前二分的答案为 $x$，那么就要判断能否满足最后的高度都不超过 $x$。

但是题目里有一个 $h_i\leftarrow \max(h_i-p,0)$ 的操作，这个取 max 是难以处理的，考虑倒过来做。

不妨设 $b_i$ 表示 $i$ 当前的高度，初始值为 $x$。

那么对于每轮操作，相当于是先让所有的 $b_i$ 减去 $a_i$，如果 $b_i<0$ 则不合法，然后选择 $k$ 个 $b_i$ 加上 $p$（这里的 $i$ 可以重复）。

然后如果最后所有 $b_i\geq h_i$ 则满足条件，否则不满足。这是因为显然最后的 $b_i$ 为在这个操作下满足最后 $h_i\leq x$ 的最大初始值，如果比这个还大显然不合法。

容易发现这个东西可以用优先队列维护，队列维护不新加 $p$ 的情况下没法满足最后的 $b_i\geq h_i$ 的所有 $i$，按照 $\left\lfloor\frac{b_i}{a_i}\right\rfloor$ 排序，每次选择最小的加 $p$，如果能满足最后 $b_i\geq h_i$ 了就不再放进队列，否则继续放进去。

时间复杂度：$O\left((n+mk)\log n\log V\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

int n, m, k, p;
int h[kMaxN], a[kMaxN], now[kMaxN];

bool check(int x) {
  std::priority_queue<std::pair<int, int>> q;
  for (int i = 1; i <= n; ++i) {
    now[i] = x;
    if (x - a[i] * m < h[i]) q.emplace(-(now[i] / a[i]), i);
  }
  for (int c = 1; c <= m; ++c) {
    for (int j = 1; j <= k && !q.empty(); ++j) {
      auto [d, i] = q.top(); q.pop();
      if (now[i] - c * a[i] < 0) return 0;
      now[i] += p;
      if (now[i] - a[i] * m < h[i]) q.emplace(-(now[i] / a[i]), i);
    }
  }
  return q.empty();
}

void dickdreamer() {
  std::cin >> n >> m >> k >> p;
  for (int i = 1; i <= n; ++i) std::cin >> h[i] >> a[i];
  int L = -1, R = 1e18, res = 1e18;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (check(mid)) R = res = mid;
    else L = mid;
  }
  std::cout << res << '\n';
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