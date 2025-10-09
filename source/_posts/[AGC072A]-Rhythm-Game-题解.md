---
title: '[AGC072A] Rhythm Game 题解'
date: 2025-04-21 09:44:00
---

## Description

有 $N$ 个按钮。第 $i$ 个按钮 $(1 \le i \le N)$ 在游戏开始后 $T_i$ 秒出现在坐标 $X_i$ 处。每个按钮在出现 $D + 0.5$ 秒后消失。

玩家从坐标 $0$ 开始，时间为 $0$ ，必须按下所有 $N$ 按钮才能赢得游戏。按键的顺序不限。但是，在按下一个按钮后和按下另一个按钮前，玩家必须至少访问一次坐标 $0$ 。违反此规则将被取消游戏资格。

AtCoder 女士可以在线路上以 $1$ 的速度移动。她能赢得比赛吗？按下按钮所需的时间可以忽略不计。

解决 $\mathrm{TESTCASES}$ 个测试案例。

$n\leq 5000,\sum n^2\leq 2.5\times 10^7$。

## Solution

首先可以对问题做个转化：第 $i$ 个任务在 $T_i-X_i$ 时刻出现，做任务需要 $2X_i$ 的时间，并要求必须要在 $T_i+X_i+D$ 时刻之前**完成**任务。设 $L_i=T_i-X_i$，$R_i=T_i+X_i+D$。

先考虑没有 $L$ 的限制的情况。

容易发现此时按照 $R_i$ 排序一定更优，证明就考虑邻项交换，如果 $R_i>R_{i+1}$，则完成 $i-1$ 号任务的最晚时刻为 $\min(R_i-2X_i,R_{i+1}-2X_i-2X_{i+1})=\min(R_i+2X_{i+1},R_{i+1})-2X_i-2X_{i+1}$，交换后为 $\min(R_{i+1}+2X_i,R_i)-2X_i-2X_{i+1}$，显然交换后更优。

加上 $L$ 的限制后就不能直接按照 $R$ 排序了，因为可能出现 $L_2<L_1<R_1<R_2$ 的情况，此时如果先做 $1$ 任务需要先等待到 $L_1$ 时刻，可能会有浪费，先做 $2$ 再做 $1$ 则会更优。

不过如果 $L$ 和 $R$ 分别有单调性的话原来的做法是没问题的。

注意到如果先做了 $R$ 更大的任务 $i$，则所有 $R_j<R_i$ 的任务 $j$ 就都已经激活，因为做 $i$ 任务的最小结束时间为 $L_i+2X_i=T_i+X_i\geq T_j+X_j>L_j$。此时可以把 $L_j$ 看成 $0$，由于这些 $R_j<R_i$ 的任务的 $L$ 和 $R$ 都满足单调不降的性质，所以先按照 $R$ 的大小顺序做这些 $R$ 小于 $R_i$ 的任务一定更优。

具体来说，按照 $R_i$ 排序后的可能操作顺序长这样：$(1)$, $(2)$, $(6,3,4,5)$, $(8,7)$, $(9)$, $(10)$。

设 $f_i$ 表示做完前 $i$ 个任务的最小时间，然后枚举下一个做的任务即可。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;

const int kMaxN = 5e3 + 5;
const i64 kInf = 1e18;

int n;
i64 d, t[kMaxN], x[kMaxN], id[kMaxN], l[kMaxN], r[kMaxN];
i64 f[kMaxN], s[kMaxN], g[kMaxN][kMaxN];

void getg() {
  for (int i = 1; i <= n; ++i) {
    i64 sum = 0;
    g[i][i - 1] = kInf;
    for (int j = i; j <= n; ++j) {
      sum += 2 * x[id[j]];
      g[i][j] = std::min(g[i][j - 1], r[j] - sum);
    }
  }
}

void dickdreamer() {
  std::cin >> n >> d;
  for (int i = 1; i <= n; ++i) {
    std::cin >> t[i] >> x[i];
    id[i] = i;
  }
  std::sort(id + 1, id + 1 + n, [&] (int i, int j) { return t[i] + x[i] < t[j] + x[j]; });
  for (int i = 1; i <= n; ++i) {
    l[i] = t[id[i]] - x[id[i]], r[i] = t[id[i]] + x[id[i]] + d;
    s[i] = s[i - 1] + 2 * x[id[i]];
    // std::cerr << id[i] << ' ' << l[i] << ' ' << r[i] << '\n';
  }
  getg();
  f[0] = 0, std::fill_n(f + 1, n, kInf);
  for (int i = 0; i < n; ++i) {
    // std::cerr << i << ' ' << f[i] << '\n';
    for (int j = i + 1; j <= n; ++j) {
      i64 now = std::max(f[i], l[j]) + 2 * x[id[j]];
      // if (i == 0 && j == 2) std::cerr << "??? " << now << '\n';
      if (now <= r[j] && now <= g[i + 1][j - 1]) f[j] = std::min(f[j], now + s[j - 1] - s[i]);
    }
  }
  std::cout << (f[n] != kInf ? "Yes\n" : "No\n");
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