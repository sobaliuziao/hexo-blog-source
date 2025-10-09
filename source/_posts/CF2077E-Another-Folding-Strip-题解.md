---
title: CF2077E Another Folding Strip 题解
date: 2025-08-01 16:08:00
---

## Description

对于一个长度为 $m$ 的数组 $b$，定义 $f(b)$ 如下：

考虑一个 $1 \times m$ 的纸带，所有单元格初始暗度为 $0$。你需要通过以下操作将其转化为第 $i$ 个位置的暗度为 $b_i$ 的纸带。每次操作包含两个步骤：

1. 在任意两个单元格之间的线上折叠纸带。你可以进行任意次折叠（包括不折叠）。
2. 选择一个位置滴下黑色染料。染料会从顶部渗透并向下流动，使其路径上所有单元格的暗度增加 $1$。滴完染料后展开纸带。

令 $f(b)$ 为达成目标配置所需的最小操作次数。可以证明总能通过有限次操作达成目标。

给定一个长度为 $n$ 的数组 $a$，计算

$$ \sum_{l=1}^n\sum_{r=l}^n f(a_l a_{l+1} \ldots a_r) $$

模 $998\,244\,353$ 的结果。

## Solution

首先一次操作的意义是选择一个相邻下标奇偶性不同的子序列减一，问最少多少次能把序列中的数全变为 $0$。

对于这种跟奇偶性有关的题目有个思路是设 $b_i=(-1)^i$，问题就变为每次选择一个子序列，做下面两种操作：

1. $+1,-1,+1,-1,\ldots,+1,-1$
2. $-1,+1,-1,+1,\ldots,-1,+1$

注意到对于所有区间 $[l,r]$，每次操作只会让 $[l,r]$ 的区间和变化不超过 $1$，所以可以得到一个答案的下界是 $\displaystyle\max\left|\sum_{i=l}^{r}{b_i}\right|$。

下面证明这个下界是可以取到的。

首先有个正确性显然的贪心是维护一个集合 $S$，每次从前往后扫 $i$，如果 $b_i\neq 0$ 且 $i$ 和 $S$ 末尾元素的奇偶性不同就把 $i$ 加入 $S$，每次对 $S$ 进行操作。

我们找到所有满足 $\left|\sum_{i=l}^{r}{b_i}\right|$ 最大的区间 $[l,r]$，结论是 $l$ 一定在集合 $S$ 中，且 $[l,r]$ 内选择的元素数量一定是奇数。

这是因为如果 $l$ 不在集合 $S$ 中，则一定存在一个 $i$，满足 $i$ 和 $l$ 奇偶性相同，且 $b_{[i+1,l-1]}$ 这个区间内全和 $b_l$ 符号相同，这样的话把 $l$ 设为 $i$ 一定能让区间和绝对值更大，就矛盾了。

后面那个结论就是首先 $b_l$ 和 $b_r$ 符号相同，否则删掉一个绝对值会更大。然后如果 $[l,r]$ 中只有偶数个元素，则最后一个元素一定和 $l$ 奇偶性不同，也和 $r$ 不同，$r$ 一定会加入，就矛盾了。

所以所有 $[l,r]$ 区间和绝对值最大的区间在一次操作后绝对值一定会减少 $1$，总次数也就刚好是区间和绝对值的最大值。

求答案直接单调栈即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5, kMod = 998244353;

int n;
int a[kMaxN], s[kMaxN];

int solve(int *a) {
  static int stk[kMaxN], L[kMaxN], R[kMaxN];
  int top = 0, ret = 0;
  a[0] = 1e18;
  for (int i = 1; i <= n + 1; ++i) {
    for (; top && a[i] > a[stk[top]]; R[stk[top--]] = i) {}
    L[i] = stk[top], stk[++top] = i;
  }
  for (; top; R[stk[top--]] = n + 2) {}
  for (int i = 1; i <= n + 1; ++i) ret = (ret + 1ll * a[i] % kMod * (i - L[i]) % kMod * (R[i] - i) % kMod + kMod) % kMod;
  return ret;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    s[i + 1] = s[i] + ((i & 1) ? a[i] : -a[i]);
  }
  int ans = solve(s);
  for (int i = 1; i <= n + 1; ++i) s[i] = -s[i];
  ans += solve(s);
  std::cout << (ans % kMod + kMod) % kMod << '\n';
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