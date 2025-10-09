---
title: [ABC310Ex] Negative Cost 题解
date: 2025-08-05 09:39:00
---

## Description

一头怪兽挡在你的面前，它有 $H$ 的血量。

你有 $n$ 种技能，每个技能都可以**以任意合法顺序无限次使用**。

你有一个魔力值，初始为  $0$ 。

第 $i$ 种技能会消耗 $C_i$ 的魔力值，并对怪兽造成 $D_i$ 的伤害。你要时刻保证魔力值非负。

特别的， $C_i$ 可能为负数，此时该技能会增加 $-C_i$ 的魔力值。

当怪物血量不为正数时，怪物就死了。

问：最少发动多少次技能，能杀死这只怪物？

$n\leq 300,-300\leq c_i\leq 300,1\leq d_i\leq 10^9,H\leq 10^{18}$。

## Solution

先把 $c_i$ 都变为 $-c_i$，也就是魔力值的增量。

由于操作序列可能很长，所以有个感觉就是所有长操作序列都可以划分成很多个比较小的序列。事实也是如此。

首先定义一个好的合法操作序列为所有前缀和都在 $[0,2V]$ 之间的序列，下面证明所有的合法序列都可以变为好的操作序列。

>设 $S$ 表示当前的魔力值，那么如果 $S\leq V$，就随便选择一个 $c_i\geq 0$ 的加上，如果 $S>V$，选择 $c_i<0$ 的加上。
>
>如果不存在 $c_i\geq 0$ 的，就说明所有的 $c_i$ 都小于 $0$，所以剩下的 $S$ 只会变小，由于现在一定不超过 $2V$，所以一定满足条件。
>
>如果不存在 $c_i>0$ 的，剩下的单独放一个序列即可。

有了这个结论后可以发现有用的操作序列一定不长，因为如果长度大于 $2V$，则一定存在一个和为 $0$ 的区间，把这个区间删掉仍然合法。

所以所有有效区间的长度不超过 $2V$，最大前缀和也不超过 $2V$。

这个可以通过一次 dp 求出 $f_i$ 表示做 $i$ 次操作的最大权值，由于性价比不是最高的物品只会选不超过 $2V$ 次，再做一遍背包即可。

时间复杂度：$O(nV^2+V^3)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 305;

int n, t;
int a[kMaxN], b[kMaxN], f[2][kMaxN * 2], g[kMaxN * 2], h[kMaxN * kMaxN * 4];

void chkmax(int &x, int y) { x = (x > y ? x : y); }
void chkmin(int &x, int y) { x = (x < y ? x : y); }

void dickdreamer() {
  std::cin >> n >> t;
  for (int i = 1; i <= n; ++i) std::cin >> a[i] >> b[i], a[i] = -a[i];
  int o = 0;
  memset(f[o], 0xcf, sizeof(f[o]));
  f[o][0] = 0;
  for (int i = 1; i <= 600; ++i) {
    o ^= 1;
    memset(f[o], 0xcf, sizeof(f[o]));
    for (int j = 0; j <= 600; ++j) {
      for (int k = 1; k <= n; ++k)
        if (j + a[k] >= 0 && j + a[k] <= 600)
          chkmax(f[o][j + a[k]], f[o ^ 1][j] + b[k]);
    }
    for (int j = 0; j <= 600; ++j) chkmax(g[i], f[o][j]);
  }
  int p = 1;
  for (int i = 2; i <= 600; ++i)
    if (g[i] * p > g[p] * i)
      p = i;
  for (int i = 1; i <= 600; ++i) {
    for (int j = i; j <= 600 * 600; ++j)
      chkmax(h[j], h[j - i] + g[i]);
  }
  int ans = 1e18;
  for (int j = 0; j <= std::min<int>(t, 600 * 600); ++j) {
    if (h[j] <= t) {
      chkmin(ans, j + (t - h[j] + g[p] - 1) / g[p] * p);
    } else {
      chkmin(ans, j);
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