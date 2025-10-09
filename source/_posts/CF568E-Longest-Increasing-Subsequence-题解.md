---
title: 'CF568E Longest Increasing Subsequence 题解'
date: 2024-08-06 08:59:00
---

## Description

给定一个长度为 $n$ 的有 $k$ 个空缺的序列。

你有 $m$ 个数可以用于填补空缺。

要求最大化最长上升子序列的长度。

$n, m \le 10^5$，$k \le 10^3$。

## Solution

容易发现只需要先构造出 LIS 上的位置的值，对于其余未填位置随便填，所以构造 LIS 时就不需要考虑出现重复的问题。

考虑先求出最长上升子序列长度。

有一个显然的做法是维护一个数据结构，对于已经填了的位置就正常转移，对于没填的位置暴力枚举填的数然后转移，可以做到 $O\left((n+m)k\right)$，但是常数会比较大。

有另一个求 LIS 的方法是维护 $f_i$ 表示当前长度为 $i$ 的上升子序列的最小末尾值，$g_i$ 表示这个末尾的位置。每次加入一个 $x$，就二分求出 $f_j<x$ 的最大的 $j$，说明以 $x$ 结尾的 LIS 长度为 $j+1$。又由于 $f_{j+1}\geq x$，就用 $x$ 更新 $f_{j+1}$ 。对于没填的位置可以维护一个指针，从大往小枚举填的数同时更新指针即可。这样做常数就很小了。

然后考虑构造方案。

先在求 LIS 的过程中求出 $len_i$ 表示以 $i$ 结尾的 LIS 长度，$pre_i$ 表示以 $i$ 结尾的 LIS 中 $i$ 的前驱的位置。这时会发现对于 $a_i=-1$ 的位置这两个东西是维护不了的，构造方案时需要特殊处理。

为了方便构造方案，先在数组末尾加入 $+\infty$。然后找到 LIS 的末尾位置 $n+1$，每次往前跳，可以在跳的过程中更新 $-1$ 的位置的 $len$ 值。设当前在 $i$，如果 $a_i$ 初始不为 $-1$，有两种情况：

1. $a_{pre_i}$ 为 $-1$，就让 $a_{pre_i}$ 填 $<a_i$ 的最大可填值。
2. $a_{pre_i}$ 不为 $-1$，就不用管。

然后就是 $a_i$ 初始为 $-1$（由于是从后往前构造的，所以 $a_i$ 此时已经填了数了），如果前面存在一个位置 $j$，使得 $a_j\neq -1,a_j<a_i,len_j=len_i-1$，那么 $i$ 的前驱就为 $j$。否则一定是一个 $-1$ 的位置，这里贪心选取最靠近 $i$ 的那个 $-1$，同时填上 $<a_i$ 的最大可填值。填完往前跳即可。

时间复杂度：$O\left((n+m)k\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, m;
int a[kMaxN], b[kMaxN], pre[kMaxN], len[kMaxN], f[kMaxN], g[kMaxN];
bool vis[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  std::cin >> m;
  for (int i = 1; i <= m; ++i) std::cin >> b[i];
  std::sort(b + 1, b + 1 + m);
  a[n + 1] = 1e9 + 1;
  memset(f, 0x3f, sizeof(f)), memset(pre, -1, sizeof(pre));
  f[0] = g[0] = 0;
  for (int i = 1; i <= n + 1; ++i) {
    if (~a[i]) {
      int j = std::lower_bound(f, f + 2 + n, a[i]) - f - 1;
      len[i] = j + 1, pre[i] = g[j], f[j + 1] = a[i], g[j + 1] = i;
    } else {
      for (int j = m, k = n + 1; j; --j) {
        for (; ~k && f[k] >= b[j]; --k) {}
        f[k + 1] = b[j], g[k + 1] = i;
      }
    }
  }
  for (int i = n + 1; len[i] > 1;) {
    if (!~pre[i]) {
      for (int j = i - 1; j; --j) {
        if (~a[j] && len[j] == len[i] - 1 && a[j] < a[i]) {
          pre[i] = j; break;
        }
      }
      if (!~pre[i]) {
        for (int j = i - 1; j; --j) {
          if (!~a[j]) {
            pre[i] = j; break;
          }
        }
      }
    }
    if (!~a[pre[i]]) {
      int j = std::lower_bound(b + 1, b + 1 + m, a[i]) - b - 1;
      a[pre[i]] = b[j], vis[j] = 1, len[pre[i]] = len[i] - 1;
    }
    i = pre[i];
  }
  for (int i = 1, j = 1; i <= n; ++i) {
    if (!~a[i]) {
      for (; vis[j]; ++j) {}
      a[i] = b[j], vis[j] = 1;
    }
  }
  for (int i = 1; i <= n; ++i) std::cout << a[i] << ' ';
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