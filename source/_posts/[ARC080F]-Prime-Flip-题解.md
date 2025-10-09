---
title: '[ARC080F] Prime Flip 题解'
date: 2024-07-10 20:53:00
---

## Description

有无限枚硬币，其中有 $n$ 枚硬币 $x_{1\ldots n}$。初始时正面朝上，其余均为背面朝上，每次可以选择一段区间 $[l,r]$，将区间内所有硬币翻转，其中 $r-l+1$ 为一个奇质数。

问最少多少次能将所有硬币全部翻为背面朝上。

$1\leq n\leq 100, 1\leq x_1\leq x_2\leq\ldots\leq x_n\leq 10^7$。

## Solution

考虑差分，每次操作显然是选择两个数 $i,j$，使得 $|i-j|\in \text{prime}$ 然后把 $a_i$ 和 $a_j$ 异或 $1$，最后要使得所有的 $a_i$ 变为 $0$。

容易发现两两消去是最优的，证明见[这里](https://www.luogu.com.cn/article/t73a800r)。

考虑对于 $i,j(i<j)$ 求出最少需要多少次操作才能把它们消掉。

1. $j-i\in \text{prime}$，显然能一次消掉。

2. $2|j-i$。

那么对于 $j-i=2$，就操作 $(i,i+5),(i+2,i+5)$ 即可。对于 $j-i=4$，则操作 $(i,i+7),(i+4,i+7)$，对于 $j-i\geq 6$，由哥德巴赫猜想在 $n\leq 10^7$ 时的正确性知一定能通过 $2$ 次构造出。

3. $2∤j-i,j-i\notin\text{prime}$

如果 $j-i=1$，操作 $(i,i+7),(i+1,i+4),(i+4,i+7)$。如果 $j-i\geq 5$，就转化为 $3+偶数$ 的情况，可以 $3$ 次构造出。

由于匹配的总数量一定，所以一定是先匹配一次消掉的，再两次，最后三次。

对于一次的跑最大匹配，后面的分奇偶考虑即可。

时间复杂度：$O(n^2\sqrt{V}+n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e3 + 5, kMaxV = 1e7 + 5;

int n, m, _m, ans;
int a[kMaxV], b[kMaxN], match[kMaxN];
bool vis[kMaxN], exi[kMaxN];
std::vector<int> G[kMaxN];

bool isprime(int n) {
  if (n <= 2) return 0;
  for (int i = 2; i * i <= n; ++i)
    if (n % i == 0)
      return 0;
  return 1;
}

bool dfs(int u) {
  for (auto v : G[u]) {
    if (vis[v]) continue;
    vis[v] = 1;
    if (!match[v] || dfs(match[v])) {
      match[v] = u; return 1;
    }
  }
  return 0;
}

void solve1() {
  for (int i = 1; i <= m; ++i) {
    if (b[i] & 1) {
      for (int j = 1; j <= m; ++j)
        if ((~b[j] & 1) && isprime(abs(b[i] - b[j])))
          G[i].emplace_back(j);
    }
  }
  for (int i = 1; i <= m; ++i) {
    if (b[i] & 1) {
      std::fill_n(vis + 1, m, 0);
      dfs(i);
    }
  }
  for (int i = 1; i <= m; ++i) {
    if (match[i]) {
      exi[i] = exi[match[i]] = 1;
      ++ans, _m -= 2;
    }
  }
}

void solve2() {
  int cnt[2] = {0};
  for (int i = 1; i <= m; ++i) {
    if (!exi[i]) ++cnt[b[i] & 1];
  }
  ans += 2 * (cnt[0] / 2 + cnt[1] / 2), _m -= 2 * (cnt[0] / 2 + cnt[1] / 2);
}

void solve3() {
  if (_m) ans += 3;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    int x;
    std::cin >> x;
    a[x] = 1;
  }
  for (int i = 1; i <= 1e7 + 1; ++i)
    if (a[i] ^ a[i - 1])
      b[++m] = i;
  _m = m;
  solve1(), solve2(), solve3();
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