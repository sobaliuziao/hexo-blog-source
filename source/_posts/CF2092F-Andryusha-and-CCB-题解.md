---
title: CF2092F Andryusha and CCB 题解
date: 2025-05-10 20:54:00
---

## Description

我们定义一个二进制字符串 $z$ 的**美感值**为满足 $1 \le i < |z|$ 且 $z_i \neq z_{i+1}$ 的索引 $i$ 的数量。

在等待 CCB 的朋友们到来时，Andryusha 烤了一个馅饼，表示为一个长度为 $n$ 的二进制字符串 $s$。为了避免冒犯任何人，他想要将这个字符串分割成 $k$ 个子字符串，使得每个字符属于恰好一个子字符串，且所有子字符串的美感值相同。

Andryusha 不知道会有多少 CCB 的朋友来他家，因此他希望找出满足条件的所有 $k$ 值的数量。然而，他的兄弟 Tristan 认为这个问题的表述过于简单。因此，他要求你为字符串的每个前缀找出这样的 $k$ 值的数量。换句话说，对于每个 $i$（从 $1$ 到 $n$），你需要找出满足可以将前缀 $s_1 s_2 \ldots s_i$ 分割成恰好 $k$ 个具有相同美感值的子字符串的 $k$ 值的数量。

$1\leq n\leq 10^6$。

## Solution

设 $cnt$ 表示分出来的每个段的美感值，容易发现 $cnt=\displaystyle\left\lfloor\frac{1 的个数}{k}\right\rfloor$。

所以对于一个 $k$，其对应的 $cnt$ 是唯一的，于是枚举 $(k,cnt)$，再计算其对哪些前缀造成贡献即可。

由于 $k\times cnt\leq n$，所以这样的数对总数是 $O(n\log n)$ 级别的。

然后考虑怎么计算其对哪些前缀造成贡献。

先把每个 $01$ 极长连续段缩起来，设长度为 $a_1,a_2,\ldots,a_m$。

如果 $k=1$，则 $i$ 在 $a_{cnt+1}$ 对应的区间内。如果 $k=2$，贡献在 $a_{2\times cnt+2}\sim a_{2\times cnt+2}$。但是如果 $a_{cnt+1}>1$，那么让第一个分界点在 $a_{cnt+1}$ 内部就能让 $a_{2\times cnt+1}$ 内也能有贡献。

容易发现每个数对的贡献一定是一段区间，不妨设 $(k-1,cnt)$ 对应的区间为 $a_l\sim a_r$，那么 $(k,cnt)$ 的右端点为 $r+cnt+1$；如果 $a_l>1$，则左端点为 $a_{l+cnt}$，否则为 $a_{l+cnt+1}$。

对于 $cnt=0$ 需要单独计算，因为上面那个做法基于必须跨段，而 $cnt=0$ 为不能跨段，上面做法就不对了。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e6 + 5;

int n, m;
int a[kMaxN], ans[kMaxN], pos[kMaxN];
std::string str;

void dickdreamer() {
  std::cin >> n >> str;
  str = " " + str, m = 0;
  std::fill_n(ans + 1, n, 0);
  for (int i = 1, lst = 0; i <= n; ++i) {
    if (i == n || str[i] != str[i + 1]) {
      a[++m] = i - lst;
      for (int j = lst + 1; j <= i; ++j) pos[j] = m;
      lst = i;
    }
  }
  for (int i = 1; i <= n - 1; ++i) {
    int l = i + 1, r = i + 1;
    for (; l <= n;) {
      ++ans[l], --ans[std::min(r, n) + 1];
      r += i + 1;
      if (a[l] == 1) l += i + 1;
      else l += i;
    }
  }
  for (int i = 1; i <= m; ++i) ans[i] += ans[i - 1];
  for (int i = 1; i <= n; ++i) {
    std::cout << ans[pos[i]] + i - pos[i] + 1 << " \n"[i == n];
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