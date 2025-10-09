---
title: 'CF613E Puzzle Lover 题解'
date: 2024-07-27 22:09:00
---

## Description

给定一个 $2 \times n$ 的矩阵，每个位置上有一个小写字母。

有一个长度为 $k$ 的小写字符串 $w$，询问矩阵中有多少条有向路径满足以下条件：
  - 路径上的字母连起来恰好为 $w$。
  - 不多次经过同一个位置。
  - 只能向上下左右四个方向走。

$n,k \le 2 \times 10^3$，答案对 $10^9+7$ 取模。

## Solution

注意到矩阵的宽只有 $2$，所以最终的行走路线一定是这样：

![](https://cdn.luogu.com.cn/upload/image_hosting/fkecjfml.png)

即两边为一个 U 形，中间为一个不走回头路的路径和两边的 U 形拼接起来。

不妨先考虑起点在终点左边或者起点和终点在同一列并且起点先往左走的情况，另一种情况就把 w 反转再做一遍即可。

显然可以 dp，设 $f_{i,j,s}$ 表示目前走到 $(i,j)$，且匹配到了 $w$ 的第 $s$ 位的方案数，这个方案是考虑了左边的 U + 不回头路径或者只有不回头路径的方案。

那么如果 $(i,j)$ 右边能找到一个长度为 $k-s$ 的 U 就可以让 $f_{i,j,s}$ 更新答案。

实现时要注意如果起点和终点在同一列时答案会算重，需要把这一部分减掉。

时间复杂度：$O(nk)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using u64 = uint64_t;

const int kMaxN = 2e3 + 5, kMod = 1e9 + 7;

int n, m;
int f[kMaxN][2][kMaxN];
bool g[kMaxN][2][kMaxN];
u64 pw[kMaxN], hss[2][kMaxN], hst[kMaxN], rhst[kMaxN];
std::string s[2], t;

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

u64 gethash(u64 *hs, int l, int r) { return hs[r] - hs[l - 1] * pw[r - l + 1]; }
u64 gethash_rev(int l, int r) { return gethash(rhst, m - r + 1, m - l + 1); }

void prework() {
  memset(hss, 0, sizeof(hss));
  memset(hst, 0, sizeof(hst));
  memset(rhst, 0, sizeof(rhst));
  memset(pw, 0, sizeof(pw));
  pw[0] = 1;
  for (int i = 1; i <= 2e3; ++i) pw[i] = 13331ull * pw[i - 1];
  for (int o = 0; o < 2; ++o) {
    for (int i = 1; i <= n; ++i) hss[o][i] = 13331ull * hss[o][i - 1] + s[o][i];
  }
  for (int i = 1; i <= m; ++i) {
    hst[i] = 13331ull * hst[i - 1] + t[i];
    rhst[i] = 13331ull * rhst[i - 1] + t[m - i + 1];
  }
}

int solve(int o) {
  prework();
  memset(f, 0, sizeof(f)), memset(g, 0, sizeof(g));
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j < 2; ++j) {
      for (int k = 1; k <= std::min(m / 2, n - i + 1); ++k) {
        g[i][j][2 * k] =
            (gethash(hss[j], i, i + k - 1) ==
                 gethash(hst, m - 2 * k + 1, m - k) &&
             gethash(hss[j ^ 1], i, i + k - 1) == gethash_rev(m - k + 1, m));
      }
    }
  }
  int ret = 0, cnt = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j < 2; ++j) {
      for (int k = 1; k <= std::min(m / 2, i); ++k) {
        inc(f[i][j][2 * k],
            gethash(hss[j ^ 1], i - k + 1, i) == gethash_rev(1, k) &&
                gethash(hss[j], i - k + 1, i) == gethash(hst, k + 1, 2 * k));
      }
      if (o) dec(ret, f[i][j][m] + g[i][j][m]);
      for (int k = 1; k <= m; ++k) {
        if (s[j][i] != t[k]) continue;
        int sum = f[i][j][k];
        if (k == 1) {
          inc(f[i][j][k], 1);
        } else {
          inc(f[i][j][k], f[i - 1][j][k - 1]);
          inc(sum, f[i - 1][j][k - 1]);
          if (s[j ^ 1][i] == t[k - 1] && k > 2) {
            inc(f[i][j][k], f[i - 1][j ^ 1][k - 2]);
          }
        }
        if (k == m) inc(ret, sum);
        else if (g[i + 1][j][m - k]) inc(ret, f[i][j][k]);
      }
      inc(ret, g[i][j][m]);
    }
  }
  return ret;
}

void dickdreamer() {
  std::cin >> s[0] >> s[1] >> t;
  n = s[0].size(), m = t.size();
  s[0] = " " + s[0], s[1] = " " + s[1], t = " " + t;
  if (m == 1) {
    int ans = 0;
    for (int i = 1; i <= n; ++i) ans += (s[0][i] == t[1]) + (s[1][i] == t[1]);
    return void(std::cout << ans << '\n');
  } else if (m == 2) {
    int ans = 0;
    for (int i = 1; i <= n; ++i) {
      ans += (s[0][i] == t[1] && s[1][i] == t[2]) +
             (s[1][i] == t[1] && s[0][i] == t[2]);
      if (i < n) {
        ans += (s[0][i] == t[1] && s[0][i + 1] == t[2]);
        ans += (s[0][i + 1] == t[1] && s[0][i] == t[2]);
        ans += (s[1][i] == t[1] && s[1][i + 1] == t[2]);
        ans += (s[1][i + 1] == t[1] && s[1][i] == t[2]);
      }
    }
    return void(std::cout << ans << '\n');
  }
  int ans = solve(0);
  std::reverse(t.begin() + 1, t.begin() + 1 + m);
  inc(ans, solve(1));
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