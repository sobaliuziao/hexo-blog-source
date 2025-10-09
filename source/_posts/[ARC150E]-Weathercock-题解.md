---
title: '[ARC150E] Weathercock 题解'
date: 2025-04-05 16:00:00
---

## Description

有 $n\times k$ 个人排成一行，从左往右按 $0,1,\ldots nk−1$ 编号。每个人初始都面对着一个方向 `L` 或 `R`。给出一个字符串 $s_{0\dots n-1}$，则第 $i$ 个人的方向为 $s_{i\bmod n}$。

接下来进行若干轮操作，每一轮所有人**同时进行如下操作**：

1. 若当前某人面对左边，且他左边的人中面对右边的人数超过一半，则他转头面向右边。
2. 若当前某人面对右边，且他右边的人中面对左边的人数超过一半，则他转头面向左边。

操作进行 $10^{100}$ 轮，请求出所有轮中每个人转头的次数之和。

$n,k\leq 2\times 10^5$。

## Solution

考虑 $k=1$ 怎么做。

先将 `L` 看成 $-1$，`R` 看成 $1$，并求前缀和。设 $s_i$ 表示 $[1,i]$ 的前缀和。

这里钦定 $s_n\geq 0$，如果不满足则可以全局取反并翻转。

那么操作分两种：

1. $i$ 向左且 $s_i\geq 0$。
2. $i$ 向右且 $s_n-s_i<0$。

把折线图画出来（图源 atcoder）：

![](https://img.atcoder.jp/arc150/5fcbe5621030f2c37008e4ad25e106f3.png)

经过手玩可以发现图中的所有红蓝边都会翻转，因为把所有在 $y=s_n$ 上方的折线拿出来，在 $y=s_n+1$ 及以上的部分显然都会翻转，而连续段两端分别是 `R` 和 `L`，都分别满足条件。

同时所有在 $y=0$ 和 $y=s_n$ 之间的黄色折线中的向左段也会翻转。

由于在 $y=s_n$ 上方的折线都会翻转到下面，所以 $s_n$ 在一次操作后一定会变成全局最大值。

所以进行一次操作后所有向右的线段都不会再翻转，只有部分向左的线段可能翻转。

对于一个向左的线段 $i$，其会翻转的条件显然为 $s_1,s_2,\dots s_i$ 中存在一个正数。这个可以归纳证明：找到第一个正数位置 $x$，显然 $x$ 之前都不会翻转，而 $x$ 一定会变为向右，对于后面的第一个向左的位置 $y$，由于 $[x+1,y-1]$ 都是向右，所以 $s_y$ 也会是正数，所以 $y$ 最终也会向右。每次找到后面的第一个向左的位置就一定能操作完。

注意到 $s_n=0$ 时找不到第一个 $x$，所以需要特判。

对于 $s_n>0$ 的情况，一个位置被操作的条件为：

1. $i$ 初始向左且 $s_i\geq 0$，操作 $1$ 次。
2. $i$ 初始向右且 $\displaystyle\max_{j=1}^{i}{s_j}\geq 0$，操作 $2$ 次。

$k>1$ 时解个不等式即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5, kMod = 998244353;

int n, k;
int s[kMaxN], f[kMaxN];
std::string str;

int cei(int x, int y) {
  if (!y) return x <= 0 ? 0 : k;
  if (y < 0) x = -x, y = -y;
  if (x >= 0) return (x + y - 1) / y;
  else return 0;
}

void dickdreamer() {
  std::cin >> n >> k >> str;
  if (std::count(str.begin(), str.end(), 'R') <= (n - 1) / 2) {
    for (auto &c : str) c = 'L' + 'R' - c;
    std::reverse(str.begin(), str.end());
  }
  str = " " + str;
  for (int i = 1; i <= n; ++i) {
    s[i] = s[i - 1] + (str[i] == 'L' ? -1 : 1);
  }
  if (!s[n]) {
    int ans = 0;
    for (int i = 1; i <= n; ++i) {
      if (str[i] == 'L' && s[i] >= 0 || str[i] == 'R' && s[i] > 0)
        ++ans;
    }
    std::cout << 1ll * ans * k % kMod << '\n';
    return;
  }
  f[0] = (*std::max_element(s + 1, s + 1 + n) > 0 ? 1 : k);
  for (int i = 1, mx = 0; i <= n; ++i) {
    mx = std::max(mx, s[i]);
    if (mx > 0) f[i] = 0;
    else f[i] = f[i - 1];
  }
  int ans = 0;
  for (int i = 1; i <= n; ++i) {
    if (str[i] == 'L') {
      if (f[i] < k) ans += k - f[i];
    } else {
      int lim = s[n] * k;
      // s[i] + cnt * s[n] >= lim + 1
      int cnt = cei(lim + 1 - s[i], s[n]);
      // if (s[n]) 
      // else if (s[i] >= lim + 1) cnt = 0;
      // std::cerr << s[i] << ' ' << s[n] << ' ' << lim + 1 - s[i] << '\n';
      if (cnt <= k - 1) ans += 2 * (k - cnt);
    }
  }
  std::cout << ans % kMod << '\n';
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