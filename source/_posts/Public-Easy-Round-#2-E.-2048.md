---
title: 'Public Easy Round #2 E. 2048'
date: 2024-04-01 18:57:00
---

## Description

pb 大师喜欢玩 2048。

pb 大师在一个 $1\times n$ 的网格上玩 2048，初始 $n$ 个格子都是空的。

游戏会进行若干轮，每轮将发生如下事件：

1. 如果没有空位，游戏结束。否则随机一个 $1$ 到 $m$ 的数，随机到 $i$ 的概率是 $p_i$，再等概率随机一个空位，在空位中填入 $2^i−1$。

2. 将所有数顺序不变移到最左侧。例如 `_ _ x _ y z` 会变成 `x y z _ _ _`。

3. 如果没有相邻相同的数，这一轮结束。否则从左往右最后一对相同的数变成他们的和以及一个空位，并且他的得分会加上产生的和，例如 `x y y z _ _` 会变成 `x 2y _ z _ _`，并且 pb 大师会得到 $2y$ 分，接下来回到第二步。

pb 大师想要知道：他的期望总得分是多少。

## Solution

显然每次 1 操作之前所有已填的数构成一个前缀，所以那个选位置的操作是没意义的，于是每次相当于就是在栈的末尾添加一个数。

考虑 dp。

设 $f_{i,j}$ 表示栈的大小为 $i$，第一步填了 $j$ 的期望得分。

这时会发现后面总共有三种可能：

1. 后面比他小并且填到末尾。
2. 后面能消成 $j$ 然后与第一个 $j$ 合并。
3. 后面的第一个数比 $j$ 大。

所以需要记 $g_{i,j}$ 表示栈的大小为 $i$，最终开头为 $j$ 的期望得分，$h_{i,j}$ 表示栈的大小为 $i$，由空栈填成只有一个 $j$ 的概率，$s_{i,j}$ 表示栈的大小为 $i$，由空栈填成只有一个 $j$ 的期望得分。

那么可以得到转移方程：

$$
\begin{aligned}
h_{i,j}&=p_j+h_{i,j-1}\cdot h_{i-1,j-1}\\
s_{i,j}&=h_{i,j-1}s_{i-1,j-1}+h_{i-1,j-1}s_{i,j-1}+h_{i,j-1}h_{i-1,j-1}2^j\\
g_{i,j}&=s_{i,j}+h_{i,j}\left(\sum_{k=0}^{j-1}g_{i-1,k}+\sum_{k=j+1}^{m}{p_kf_{i-1,k}}\right)-s_{i,j}h_{i-1,j}\\
f_{i,j}&=\sum_{k=0}^{j-1}{g_{i-1,k}}+\sum_{k=j+1}^{m}{p_kf_{i-1,k}}+h_{i-1,j}\left(2^{j+1}+f_{i,j+1}\right)+s_{i-1,j}
\end{aligned}
$$

注意栈里的数可能达到 $n+m$。

时间复杂度：$O\left(n(n+m)\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e3 + 5, kMod = 998244353;

int n, m;
int p[kMaxN * 2], pw[kMaxN * 2], f[kMaxN][kMaxN * 2], g[kMaxN][kMaxN * 2],
    h[kMaxN][kMaxN * 2], s[kMaxN][kMaxN * 2];
int pre[kMaxN * 2], suf[kMaxN * 2];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1) ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

void dickdreamer() {
  std::cin >> n >> m;
  int sum = 0;
  for (int i = 1; i <= m; ++i) {
    std::cin >> p[i];
    inc(sum, p[i]);
  }
  sum = qpow(sum);
  for (int i = 1; i <= m; ++i) p[i] = 1ll * p[i] * sum % kMod;
  pw[0] = 1;
  for (int i = 1; i <= n + m + 1; ++i) pw[i] = add(pw[i - 1], pw[i - 1]);
  // get h, s
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n + m; ++j) {
      h[i][j] = add(p[j], 1ll * h[i][j - 1] * h[i - 1][j - 1] % kMod);
      s[i][j] =
          add(1ll * h[i][j - 1] * s[i - 1][j - 1] % kMod,
              add(1ll * h[i - 1][j - 1] * s[i][j - 1] % kMod,
                  1ll * h[i][j - 1] * h[i - 1][j - 1] % kMod * pw[j - 1] % kMod));
    }
  }
  // get f, g
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= n + m; ++j) {
      if (j) pre[j] = pre[j - 1];
      else pre[j] = 0;
      inc(pre[j], g[i - 1][j]);
    }
    for (int j = n + m; ~j; --j) {
      suf[j] = add(suf[j + 1], 1ll * p[j] * f[i - 1][j] % kMod);
      f[i][j] = add((j ? pre[j - 1] : (int)0), suf[j + 1]);
      g[i][j] = 1ll * h[i][j] * f[i][j] % kMod;
      inc(f[i][j], add(1ll * h[i - 1][j] * add(pw[j], f[i][j + 1]) % kMod, s[i - 1][j]));
      inc(g[i][j], 1ll * s[i][j] * sub(1, h[i - 1][j]) % kMod);
    }
  }
  int ans = 0;
  for (int i = 1; i <= m; ++i)
    inc(ans, 1ll * f[n][i] * p[i] % kMod);
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