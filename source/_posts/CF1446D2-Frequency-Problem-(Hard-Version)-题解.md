---
title: CF1446D2 Frequency Problem (Hard Version) 题解
date: 2025-02-12 20:32:00
---

## Description

给出 $n$ 个元素组成的序列 $a_1,a_2,\ldots,a_n$。

求最长的子段使得其中有至少两个出现次数最多的元素。

输出最长子段长度。

$1\leq n\leq 2\times 10^5$。

## Solution

首先有个关键性质是如果设全局的众数为 $x$，则在最终的最长子段中一定有个众数是 $x$。

证明就考虑如果 $x$ 不是当前子段的众数，则可以拓展左右端点，拓展一次不足以让 $x$ 变成唯一的众数，当拓展到 $x$ 刚好与之前的众数出现次数相等时这个子段就满足条件了，而由于 $x$ 是全局的众数，所以一定可以拓展到这个局面。

然后就可以自然地想到枚举另一个众数 $y$，求出满足 $x$ 和 $y$ 出现次数相等的最长子段（不需要保证 $x$ 和 $y$ 出现次数最多），这么做显然是对的，因为根据上面那个做法，如果不是众数就可以再继续拓展直到 $x$ 是众数。

但是上面的做法会做颜色种类次，可能会很多。

考虑根号分治。

对于出现次数大于 $\sqrt n$ 的 $y$ 跑上面的做法。剩下的就一定满足众数出现次数不超过 $\sqrt n$，则可以枚举众数出现次数 $k$，对于每个 $l$，找到满足众数出现次数不超过 $k$ 的最大 $r$，然后判断出现次数恰为 $r$ 的数是否有至少两个。这个容易用双指针维护。

时间复杂度：$O(n\sqrt n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, lim, x, ans;
int a[kMaxN], cnt[kMaxN] = {0};

void solve_big(int y) {
  static int sum[kMaxN], pos[kMaxN * 2];
  std::fill_n(pos, 2 * n + 1, 1e9);
  pos[n] = 0;
  for (int i = 1; i <= n; ++i) {
    sum[i] = sum[i - 1];
    if (a[i] == x) ++sum[i];
    else if (a[i] == y) --sum[i];
    if (pos[sum[i] + n] == 1e9) pos[sum[i] + n] = i;
    else ans = std::max(ans, i - pos[sum[i] + n]);
  }
}

void solve_big() {
  for (int i = 1; i <= n; ++i) {
    if (cnt[i] > lim && i != x) {
      solve_big(i);
    }
  }
}

void solve_small() {
  for (int c = 1; c <= lim; ++c) {
    static int cnt[kMaxN] = {0}, ccnt[kMaxN] = {0};
    std::fill_n(cnt, n + 1, 0);
    std::fill_n(ccnt, n + 1, 0);
    ccnt[0] = n;
    
    for (int l = 1, r = 0; l <= n; --ccnt[cnt[a[l++]]--]) {
      for (; r < n && !ccnt[c + 1]; ++ccnt[++cnt[a[++r]]]) {}
      if (ccnt[c + 1]) --ccnt[cnt[a[r--]]--];
      assert(!ccnt[c + 1]);
      if (ccnt[c] >= 2) ans = std::max(ans, r - l + 1);
    }
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    ++cnt[a[i]];
    if (cnt[a[i]] > cnt[x]) x = a[i];
  }
  lim = sqrtl(n);
  solve_big(), solve_small();
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