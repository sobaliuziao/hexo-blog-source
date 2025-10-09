---
title: [ABC259Ex] Yet Another Path Counting 题解
date: 2024-02-22 14:12:00
---

## Description

有 $N$ 行 $N$ 列的网格图，只能向下或向右走，合法路径的开端和结尾的格子上数字一样

找到合法路径条数，对 $998244353$ 取模

$1\leq N\leq 400,1\leq a_{i,j}\leq N^2$。

## Solution

有一个 $O(n^4)$ 的做法是每次枚举起点和终点然后用组合数计算答案，但是由于同一颜色的点可能很多所以这个做法过不了。

注意到出现次数 $\leq n$ 的颜色显然这样做是可以的，而出现次数 $>n$ 的颜色最多 $n$ 个，所以对于这些出现次数很多的颜色在网格图上进行 dp 即可。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 405, kMaxS = kMaxN * kMaxN, kMod = 998244353;

int n;
int col[kMaxN][kMaxN], fac[kMaxS], ifac[kMaxS], inv[kMaxS];
std::vector<std::pair<int, int>> vec[kMaxS];

int C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = inv[1] = 1;
  for (int i = 2; i <= 2 * n; ++i) {
    inv[i] = 1ll * (kMod - kMod / i) * inv[kMod % i] % kMod;
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = 1ll * inv[i] * ifac[i - 1] % kMod;
  }
}

int solve1(int x) {
  int ret = 0;
  for (auto p1 : vec[x]) {
    ret = (ret + 1) % kMod;
    for (auto p2 : vec[x]) {
      if (p1.first <= p2.first && p1.second <= p2.second && p1 != p2) {
        ret = (ret + C(p2.first - p1.first + p2.second - p1.second, p2.first - p1.first)) % kMod;
      }
    }
  }
  return ret;
}

int solve2(int x) {
  static int f[kMaxN][kMaxN] = {0};
  int ret = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      f[i][j] = ((col[i][j] == x) + f[i - 1][j] + f[i][j - 1]) % kMod;
      if (col[i][j] == x) ret = (ret + f[i][j]) % kMod;
    }
  }
  return ret;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      std::cin >> col[i][j];
      vec[col[i][j]].emplace_back(i, j);
    }
  }
  prework();
  int ans = 0;
  for (int i = 1; i <= n * n; ++i) {
    if (vec[i].size() <= n) ans = (ans + solve1(i)) % kMod;
    else ans = (ans + solve2(i)) % kMod;
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