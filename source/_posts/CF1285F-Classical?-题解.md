---
title: 'CF1285F Classical? 题解'
date: 2025-03-24 10:05:00
---

## Description

有 $n$ 个整数 $a_1,a_2,\ldots,a_n$，求 $\displaystyle\max_{1\leq i<j\leq n}(\text{lcm}(a_i,a_j))$。

$n,a_i\leq 10^5$。

## Solution

先枚举 $d=\gcd(a_i,a_j)$，题目转化求序列中互质的一对数的乘积的最大值。

考虑从大到小枚举 $a_i$，同时维护一个单调栈表示可能成为答案的互质数对的数。

如果当前栈里面存在一个数 $x$ 和 $a_i$ 互质，则所有小于 $x$ 的数一定不可能成为答案，暴力弹栈找到最大的 $x$ 即可。

但是如果里面不存在的话暴力弹栈复杂度是错的。

考虑怎么判断里面是否存在和 $a_i$ 互质的数。

这等价于求 $\sum{\varepsilon(\gcd(a_i,a_j))}=\sum_{d|a_i}\mu(d)\sum[d|a_j]$，维护单调栈时对于所有 $a_j$ 的因数修改即可。

时间复杂度：$O(n\log^2V)$。

---

但是还可以更优。注意到 $\text{lcm}(a_i,a_j)=a_i\times\frac{a_j}{\gcd(a_i,a_j)}$，由于 $a_i$ 和 $a_j/\gcd(a_i,a_j)$ 互质，所以把所有 $a_i$ 的因数加入序列再做上面的做法答案也是对的。

时间复杂度：$O(V\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, mx; int64_t ans;
int a[kMaxN], mu[kMaxN], s[kMaxN];
bool exi[kMaxN];
std::vector<int> d[kMaxN];

void prework(int n = mx) {
  static int prime[kMaxN];
  static bool vis[kMaxN];
  for (int i = 1; i <= n; ++i)
    for (int j = i; j <= n; j += i)
      d[j].emplace_back(i);
  int m = 0;
  mu[1] = 1;
  for (int i = 2; i <= n; ++i) {
    if (!vis[i]) {
      mu[i] = -1, prime[++m] = i;
    }
    for (int j = 1; j <= m && i * prime[j] <= n; ++j) {
      int x = i * prime[j];
      vis[x] = 1;
      if (i % prime[j]) mu[x] = -mu[i];
      else break;
    }
  }
}

void upd(int x, int v) {
  for (auto i : d[x]) s[i] += v * mu[i];
}

int get(int x) {
  int ret = 0;
  for (auto i : d[x]) ret += s[i];
  return ret;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    mx = std::max(mx, a[i]);
    if (exi[a[i]]) ans = std::max<int64_t>(ans, a[i]);
    exi[a[i]] = 1;
  }
  prework();
  for (int i = mx; i; --i)
    for (int j = 2 * i; j <= mx; j += i)
      exi[i] |= exi[j];
  static int stk[kMaxN];
  int top = 0;
  for (int i = mx; i; --i) {
    if (!exi[i]) continue;
    if (get(i)) {
      while (true) {
        for (; top && std::__gcd(i, stk[top]) != 1; --top) upd(stk[top], -1);
        assert(top);
        ans = std::max<int64_t>(ans, 1ll * i * stk[top]);
        upd(stk[top], -1);
        if (get(i)) {
          --top;
        } else {
          upd(stk[top], 1);
          break;
        }
      }
    }
    stk[++top] = i, upd(i, 1);
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