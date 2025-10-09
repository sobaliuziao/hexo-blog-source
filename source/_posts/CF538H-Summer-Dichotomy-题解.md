---
title: CF538H Summer Dichotomy 题解
date: 2024-07-30 19:55:00
---

## Description

有 $T$ 名学生，你要从中选出至少 $t$ 人，并将选出的人分成两组，可以有某一组是空的。

有 $n$ 名老师，每名老师要被分配到两个小组之一，对于第 $i$ 名老师，要求所在的小组中的学生人数 $\in [l_i, r_i]$。

此外，有 $m$ 对老师不能在同一个小组中。

你需要判断能否满足所有要求，如果可以，请给出一种方案。

$t \le T \le 10^9$，$n,m \le 10^5$。

## Solution

先不考虑人数为 $[t,T]$ 的限制，只考虑怎么取出 $n_1$ 和 $n_2$ 使答案尽可能合法。

注意到如果 $\max\{l_i\}\leq\min\{r_i\}$ 那么 $n_1$ 和 $n_2$ 取这个区间里的任意一个数均可行。

否则不妨让 $n_1=\min\{r_i\},n_2=\max\{l_i\}$，则一定有 $n_1<n_2$，此时如果让 $n_1$ 增大则必然会使 $r$ 最大的那个区间两个组都选不上，而让 $n_1$ 减少则一定会让 $n_1$ 这边能放的区间变为原来的子集，一定不优。对于 $n_2$ 同理，所以此时的 $n_1,n_2$ 一定是最优解。

现在考虑上 $[t,T]$ 的限制，如果 $n_1+n_2\in [t,T]$ 则不需要调整。如果 $n_1+n_2>T$，注意到 $n_2$ 不能减少，所以让 $n_1$ 减少，$n_2$ 不变最优。如果 $n_1+n_2<t$ 则让 $n_1$ 不变，$n_2$ 增大最优。

确定了 $n_1,n_2$ 后只需要对于每个区间判断其能放到哪个组，如果只能放一个组则已经确定，否则不管它。

然后对于不能放在一个组的两个区间连一条边，跑二分图染色即可。

时间复杂度：$O(n+m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int L, R, n, m;
int l[kMaxN], r[kMaxN], col[kMaxN];
bool vis[kMaxN];
std::vector<int> G[kMaxN];

bool dfs(int u) {
  vis[u] = 1;
  for (auto v : G[u]) {
    if (!col[v]) {
      col[v] = 3 - col[u];
      dfs(v);
    } else if (col[v] == col[u]) {
      return 0;
    }
  }
  return 1;
}

void dickdreamer() {
  std::cin >> L >> R >> n >> m;
  int n1 = 1e9, n2 = 0;
  for (int i = 1; i <= n; ++i) {
    std::cin >> l[i] >> r[i];
    n1 = std::min(n1, r[i]), n2 = std::max(n2, l[i]);
  }
  if (n1 + n2 > R) n1 = R - n2;
  if (n1 + n2 < L) n2 = L - n1;
  if (n1 < 0 || n2 < 0) return void(std::cout << "IMPOSSIBLE\n");
  for (int i = 1; i <= n; ++i) {
    int o1 = (l[i] <= n1 && n1 <= r[i]), o2 = (l[i] <= n2 && n2 <= r[i]);
    if (!o1 && !o2) return void(std::cout << "IMPOSSIBLE\n");
    if (o1 && !o2) col[i] = 1;
    else if (!o1 && o2) col[i] = 2;
  }
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  for (int i = 1; i <= n; ++i) {
    if (!vis[i] && col[i] && !dfs(i))
      return void(std::cout << "IMPOSSIBLE\n");
  }
  for (int i = 1; i <= n; ++i) {
    if (!vis[i] && !col[i]) {
      col[i] = 1;
      if (!dfs(i)) return void(std::cout << "IMPOSSIBLE\n");
    }
  }
  std::cout << "POSSIBLE\n" << n1 << ' ' << n2 << '\n';
  for (int i = 1; i <= n; ++i) std::cout << col[i];
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