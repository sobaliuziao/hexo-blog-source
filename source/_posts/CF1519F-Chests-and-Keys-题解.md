---
title: CF1519F Chests and Keys 题解
date: 2024-07-12 11:56:00
---

## Description

给定 $n,m$ 表示存在 $n$ 个宝箱和 $m$ 把钥匙，第 $i$ 把钥匙需要 $b_i$ 元，第 $i$ 个宝箱内部有 $a_i$ 元。

现在进行一场游戏，Bob 是本场游戏的玩家，而 Alice 则是场景布置者，Alice 可以给每个宝箱上一些锁（第 $j$ 种锁需要第 $j$ 种钥匙打开）

如果 Bob 可以购买一些钥匙，然后打开一些宝箱，使得 Bob 的收益大于 $0$，那么 Bob 就赢得了游戏，反之 Alice 获得了胜利。

现在 Alice 打算布置宝箱上的锁，第 $i$ 个宝箱上放置第 $j$ 种锁的花费为 $c_{i,j}$，请帮助 Alice 找到一种布置锁的方案，使得花费最小，且 Alice 将取得胜利。

特别的，一个箱子上可以放置若干把锁，Bob 需打开所有锁才能获得内部的钱。

$n,m\le 6,a_i,b_i\le 4,c_{i,j}\le 10^7$。

## Solution

考虑怎么什么样的方案是合法的。

不妨设 $T_i$ 表示第 $i$ 个宝箱选的所有钥匙，容易发现合法的充要条件是对于所有 $S\subseteq\{1,2,\ldots,n\}$，都满足：

$$
\sum_{i\in S}{a_i}\leq\sum_{j\in (\cup_{k\in S}{T_k})}b_j
$$

经过观察会发现这个东西很像[霍尔定理](https://zhuanlan.zhihu.com/p/460373184)的形式，考虑转化成二分图匹配。

原题的式子等价于对于每个箱子 $i$，拆 $a_i$ 个左部点。对于钥匙 $j$，拆 $b_j$ 个有部点，然后如果箱子 $i$ 里有钥匙 $j$ 则让所有 $i$ 对应的点与所有钥匙 $j$ 对应的点连边，然后如果对于左部点能找到完美匹配则合法。

经过转化容易发现可以 dp，设 $f_{i,s}$ 表示考虑了前 $i$ 个箱子，目前右边每个钥匙拆的点没匹配数量的状态为 $s$（$s$ 为五进制表示），每次搜出 $a_i$ 对应的点连哪些右部点，暴力转移即可。

时间复杂度：$O(n\cdot 5^{2n})$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxS = 2e4 + 5, kPw5[] = {1, 5, 25, 125, 625, 3125};

int n, m;
int a[10], b[10], c[10][10], f[10][kMaxS];

int getbit(int s, int k) { return s / kPw5[k] % 5; }

void dfs(int x, int cur, int val, int s, int cnt) {
  if (cur == m) {
    if (!cnt) f[x][s] = std::min(f[x][s], val);
    return;
  }
  int t = getbit(s, cur);
  for (int i = 0; i <= std::min(t, cnt); ++i) {
    dfs(x, cur + 1, val + (bool)i * c[x][cur], s - i * kPw5[cur], cnt - i);
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  int st = 0;
  for (int i = 0; i < m; ++i) {
    std::cin >> b[i];
    st += kPw5[i] * b[i];
  }
  for (int i = 1; i <= n; ++i)
    for (int j = 0; j < m; ++j)
      std::cin >> c[i][j];
  memset(f, 0x3f, sizeof(f));
  f[0][st] = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= st; ++j) {
      dfs(i, 0, f[i - 1][j], j, a[i]);
    }
  }
  int ans = *std::min_element(f[n], f[n] + st + 1);
  std::cout << (ans >= 1e9 ? -1 : ans) << '\n';
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