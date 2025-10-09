---
title: 'CF2115E Gellyfish and Mayflower 题解'
date: 2025-07-23 16:10:00
---

## Description

May 是 Gellyfish 的朋友，她非常喜欢玩一款名为《Inscryption》的游戏，这是一款在有向无环图（DAG）上进行的游戏，该图包含 $n$ 个顶点和 $m$ 条边。所有的边 $a \to b$ 都满足 $a < b$。

你从顶点 1 出发，携带一些金币。你需要沿着有向边从顶点 1 移动到最终 Boss 所在的顶点，并在那里与 Boss 战斗。

图中的每个顶点 $i$ 上都有一位商人（Trader），他会用 $c_i$ 枚金币出售一张攻击力为 $w_i$ 的卡牌。你可以从每位商人那里购买任意数量的卡牌，但前提是你当前处在该商人所在的顶点 $i$。

为了打败最终 Boss，你希望你手中卡牌的总攻击力尽可能大。

你将需要回答 $q$ 个查询：

每个查询给定两个整数 $p$ 和 $r$。表示最终 Boss 位于顶点 $p$，你一开始有 $r$ 枚金币。请问，当你与最终 Boss 战斗时，你最多能拥有多少总攻击力的卡牌？注意，你可以在顶点 $p$ 进行交易。

$n\leq 200,n-1\leq m\leq 2000,1\leq c_i\leq 200,1\leq w_i,r\leq 10^9$。

## Solution

定义一个点的性价比 $k_i=\frac{w_i}{c_i}$，那么如果已知从 $1$ 走到目标位置 $p$ 的路径后，除了这条路径上性价比最大的点 $i$，其余总共只会选不超过 $c_i$ 个物品。

这是因为如果选了超过 $c_i$ 个物品，根据抽屉原理，一定存在一个子集的价格之和是 $c_i$ 的倍数，由于 $i$ 的性价比最高，所以把这些物品替换成 $i$ 一定最优。

于是只要询问的 $r\leq\max c_i^2$ 就跑暴力，否则性价比不是最大的怎么选，最优解一定不会超过 $r$。

考虑枚举路径上性价比最高的物品，设 $f_{s,i,r}$ 表示从 $1$ 走到 $i$，钦定性价比最大的是 $s$，所有$\bmod c_i$ 为 $r$ 的体积 $S$ 中，除去性价比最高的物品，能够选到的最大收益和减去 $\left\lfloor\frac{S}{c_s}\right\rfloor\cdot w_s$ 的最大值。

转移这个就考虑 $(s,i,r)$ 向 $\left(s,i,(r+c_i)\bmod c_s\right)$ 连权值为 $w_i-\left\lfloor\frac{r+c_i}{c_s}\right\rfloor\cdot w_s$ 的边，这是个同余最短路的标准形式，由于已经钦定了 $s$ 是性价比最高的物品了，所以这个东西没有负环。

询问时，就枚举 $s$，答案为 $\displaystyle\max_{i=0}^{c_s-1}{\left(f_{s,p,i}-[r\bmod c_s<i]\cdot w_s+\left\lfloor\frac{r}{c_s}\right\rfloor\cdot w_s\right)}$ 的最大值，直接做是 $O(ncq)$ 的，用类似转两圈的东西再优化一下就可以做到 $O(nq)$。

时间复杂度：$O(nmc+nq)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 205;

int n, m, q, lim = 40000;
int c[kMaxN], w[kMaxN], f[kMaxN][kMaxN][kMaxN], g[kMaxN][kMaxN * kMaxN];
std::vector<int> G[kMaxN];

void chkmax(int &x, int y) { x = (x > y ? x : y); }
void chkmin(int &x, int y) { x = (x < y ? x : y); }

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i) std::cin >> c[i] >> w[i];
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[v].emplace_back(u);
  }
  for (int s = 1; s <= n; ++s) {
    for (int i = 1; i <= n; ++i) std::fill_n(f[s][i], c[s], -1e18);
    if (1ll * w[1] * c[s] > 1ll * w[s] * c[1]) continue;
    f[s][1][0] = 0;
    for (int i = 1; i <= n; ++i) {
      if (1ll * w[i] * c[s] > 1ll * w[s] * c[i]) continue;
      for (auto j : G[i]) {
        if (i > s && j < s) continue;
        for (int r = 0; r < c[s]; ++r)
          chkmax(f[s][i][r], f[s][j][r]);
      }
      for (int j = 0; j < std::__gcd(c[s], c[i]); ++j) {
        for (int r = j, cc = 0; cc < 2; cc += ((r = (r + c[i]) % c[s]) == j)) {
          int p = (r + c[i]) % c[s];
          chkmax(f[s][i][p], f[s][i][r] + w[i] - (r + c[i]) / c[s] * w[s]);
        }
      }
      for (int r = 0, cc = 0; cc < 2; cc += ((r = (r + 1) % c[s]) == 0)) {
        int p = (r + 1) % c[s];
        chkmax(f[s][i][p], f[s][i][r] - (r + 1) / c[s] * w[s]);
      }
    }
  }
  for (int i = 1; i <= n; ++i) {
    for (auto j : G[i]) {
      for (int k = 0; k <= lim; ++k)
        chkmax(g[i][k], g[j][k]);
    }
    for (int j = c[i]; j <= lim; ++j)
      chkmax(g[i][j], g[i][j - c[i]] + w[i]);
  }
  std::cin >> q;
  for (int cs = 1; cs <= q; ++cs) {
    int p, r;
    std::cin >> p >> r;
    if (r <= lim) {
      std::cout << g[p][r] << '\n';
    } else {
      int ans = 0;
      for (int s = 1; s <= p; ++s) {
        chkmax(ans, f[s][p][r % c[s]] + (r / c[s]) * w[s]);
      }
      std::cout << ans << '\n';
    }
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