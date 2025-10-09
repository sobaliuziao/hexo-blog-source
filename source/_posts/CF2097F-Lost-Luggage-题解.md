---
title: 'CF2097F Lost Luggage 题解'
date: 2025-07-28 17:25:00
---

## Description

众所周知，航空公司"Trouble"经常丢失行李，为此关心的记者们决定计算可能无法归还给旅客的行李最大数量。

航空公司"Trouble"在编号从 $1$ 到 $n$ 的 $n$ 个机场间运营航班。记者们的实验将持续 $m$ 天。已知在实验第一天午夜前，第 $j$ 个机场有 $s_j$ 件遗失行李。在第 $i$ 天会发生以下事件：

- 早晨，同时起飞 $2n$ 个航班，包括 $n$ 个第一类航班和 $n$ 个第二类航班：
  - 第一类第 $j$ 个航班从机场 $j$ 飞往机场 $(((j-2) \bmod n )+ 1)$（前一个机场，第一个机场的前一个是最后一个），最多可运输 $a_{i,j}$ 件遗失行李；
  - 第二类第 $j$ 个航班从机场 $j$ 飞往机场 $((j \bmod n) + 1)$（后一个机场，最后一个机场的后一个是第一个），最多可运输 $c_{i,j}$ 件遗失行李；
- 下午，机场会进行遗失行李检查。如果当天航班起飞后，第 $j$ 个机场剩余 $x$ 件行李且 $x \ge b_{i, j}$，则至少会有 $x - b_{i, j}$ 件行李被找到，不再视为遗失；
- 晚上，当天所有 $2n$ 个航班结束，运输的遗失行李抵达对应机场。

对于每个 $k$ 从 $1$ 到 $m$，记者们想知道在前 $k$ 天的检查中可能未被找到的遗失行李最大数量。注意每个 $k$ 的计算都是独立的。

$1\leq n\leq 12,1\leq m\leq 2000$。

## Solution

首先这个显然是网络流，有一个比较显然的最大流建模是建给第 $i(0\leq i\leq m)$ 天建一个点 $(i,j)$ 表示这一天晚上机场 $j$ 的行李数量，同时第 $i$ 天有个汇点 $T_i$。连边就是 $(i-1,j)$ 向 $(i,j)$ 连流量为 $b_{i,j}$ 的边，$(i-1,j)$ 向 $(i,j-1)$ 连流量为 $a_{i,j}$ 的边，$(i-1,j)$ 向 $(i,j+1)$ 连流量为 $c_{i,j}$ 的边，$(i,j)$ 向 $T_i$ 连流量为 $+\infty$ 的边。第 $i$ 天的答案就是 $S\to T_i$ 的最大流。

但是直接跑肯定是不行的。考虑转最小割。

由于 $n\leq 12$ 且只有相邻层数之间的边，所以可以直接按照天数把和 $S$ 连通的点压入状态。

设 $f_{i,S}$ 表示前 $i$ 天，钦定第 $i$ 层和源点相连的点为集合 $S$ 内的点，其余的全和汇点相连。

转移为：

$$
f_{i,S}=\min_{T}{\left\{f_{i-1,S}+\sum_{j\in T}\sum_{k\notin S}{e_{i-1,j,k}}\right\}}
$$

注意：这里转移的边必须满足前面的点属于 $T$，后面的不属于 $S$，不能加入前面属于 $S$ 后面不属于 $T$ 的贡献，因为这样的边根本不会被经过！！！

直接转移是 $O(m\cdot 4^n)$，过不了。优化就考虑先把初始状态设为上一层的状态，然后从前往后逐位修改状态，设 $g_{i,S,0/1}$ 表示修改了前 $i$ 位，目前状态为 $S$，且第 $i$ 位在修改前是 $0/1$ 的最小答案。容易转移。

单次转移是 $O(2^nn)$。

时间复杂度：$O(nm\cdot 2^n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 15, kMaxM = 2e3 + 5, kMaxS = (1 << 13) + 5;

int n, m;
int cnt[kMaxN], a[kMaxM][kMaxN], b[kMaxM][kMaxN], c[kMaxM][kMaxN];
int f[kMaxS];

inline void chkmax(int &x, int y) { x = (x > y ? x : y); }
inline void chkmin(int &x, int y) { x = (x < y ? x : y); }

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i) std::cin >> cnt[i];
  for (int i = 1; i <= m; ++i) {
    for (int j = 1; j <= n; ++j) std::cin >> a[i][j];
    for (int j = 1; j <= n; ++j) std::cin >> b[i][j];
    for (int j = 1; j <= n; ++j) std::cin >> c[i][j];
  }
  for (int s = 0; s < (1 << n); ++s) {
    f[s] = 0;
    for (int i = 1; i <= n; ++i)
      if (s >> (i - 1) & 1)
        f[s] += cnt[i];
  }
  for (int i = 1; i <= m; ++i) {
    static int g[kMaxS][2], tmp[kMaxS][2];
    for (int s = 0; s < (1 << (n + 1)); ++s) g[s][0] = g[s][1] = 1e18;
    for (int s = 0; s < (1 << n); ++s) g[s | ((s & 1) << n)][s >> (n - 1) & 1] = f[s];
    for (int j = 0; j < n; ++j) {
      for (int s = 0; s < (1 << (n + 1)); ++s)
        for (int o = 0; o < 2; ++o)
          tmp[s][o] = g[s][o], g[s][o] = 1e18;
      for (int s = 0; s < (1 << (n + 1)); ++s) {
        for (int o1 = 0; o1 < 2; ++o1) {
          for (int o2 = 0; o2 < 2; ++o2) {
            int val = tmp[s][o1], t = s;
            if (o2 ^ (s >> j & 1)) t ^= (1 << j);
            val += ((o1 == 0) && (o2 == 1)) * c[i][(j + n - 1) % n + 1];
            val += (((s >> j & 1) == 0) && (o2 == 1)) * b[i][j + 1];
            val += (((s >> (j + 1) & 1) == 0) && (o2 == 1)) * a[i][(j + 1) % n + 1];
            chkmin(g[t][s >> j & 1], val);
          }
        }
      }
    }
    std::fill_n(f, 1 << n, 1e18);
    for (int s = 0; s < (1 << (n + 1)); ++s) chkmin(f[s & ((1 << n) - 1)], std::min(g[s][0], g[s][1]));
    std::cout << f[(1 << n) - 1] << '\n';
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