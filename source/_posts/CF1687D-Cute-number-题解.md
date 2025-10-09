---
title: CF1687D Cute number 题解
date: 2024-09-13 09:39:00
---

## Description

定义 $f(x)$ 表示严格大于 $x$ 的最小的完全平方数，定义 $g(x)$ 为小于等于 $x$ 的最大的完全平方数。例如，$f(1)=f(2)=g(4)=g(8)=4$。

蓝认为，一个正整数是“可爱”的，当且仅当 $x-g(x)<f(x)-x$，例如，$1,5,11$ 是可爱的正整数，而 $3,8,15$ 不是。

蓝给了你一个长度为 $n$ 的正整数数列 $a_i$，你需要帮她找到最小的非负整数 $k$，使得对于 $\forall i$，$a_i+k$ 是可爱的。

$1\leq n\leq 10^6,1\leq a_1\leq a_2\leq\ldots\leq a_n\leq 2\cdot 10^6$。

## Solution

容易发现一个可爱的数构成的连续段一定形如 $[x^2,x^2+x]$ 且当 $a_1+k=a_n^2$ 时一定合法。

考虑钦定 $a_1$ 属于第 $x$ 个好段，先让 $a_1$ 平移到 $x^2$，那么整个序列的可移动空间就只有 $x$ 了。

注意到对于一个 $a_i$，在这 $x$ 的移动空间内最多会改变一次状态，因为后面无论是好段还是不好段的长度都大于 $x$。所以一个目前不好的 $a_i$ 可以用于更新移动空间的左端点，好的 $a_i$ 可以更新右端点。

但是直接暴力做是 $O(nV)$ 的，过不了。

由于当 $a_1$ 平移到 $x^2$ 时，整个序列的数只会分布于 $O\left(\frac{V}{x}\right)$ 个不同的段，所以对于每个段一起考虑即可。

时间复杂度：$O(V\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e6 + 5;

int n, ans;
int a[kMaxN], pre[kMaxN];

int getpre(int x) { return x <= a[n] ? (x >= 0 ? pre[x] : 0) : n; }

void solve(int x) {
  int d = x * x - a[1], L = std::max<int>(d, 0), R = 1e18;
  for (int i = x, p = 0; p < n; ++i) {
    int np = getpre(i * i + i - d);
    if (np != p) R = std::min(R, i * i + i - a[np]);
    p = np;

    np = getpre((i + 1) * (i + 1) - d - 1);
    if (np != p) L = std::max(L, (i + 1) * (i + 1) - a[p + 1]);
    p = np;
  }
  if (L <= R) ans = std::min(ans, L);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    pre[a[i]] = i;
  }
  for (int i = 1; i <= a[n]; ++i) {
    if (!pre[i]) pre[i] = pre[i - 1];
  }
  ans = a[n] * a[n] - a[1];
  for (int i = 1; i < a[n]; ++i) solve(i);
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