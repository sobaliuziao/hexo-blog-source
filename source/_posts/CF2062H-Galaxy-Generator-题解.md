---
title: CF2062H Galaxy Generator 题解
date: 2025-08-13 10:53:00
---

## Description

在一个二维宇宙中，恒星可以用平面上的点 $(x, y)$ 表示。当且仅当两颗恒星的 $x$ 或 $y$ 坐标相同，且它们之间的线段上没有其他恒星时，这两颗恒星直接相连。定义星系为由直接或间接（通过其他恒星）相连的恒星组成的连通分量。

对于一个恒星集合，其价值定义为：经过任意次（可能为零次）以下操作后，能够得到的最小星系数量。每次操作中，你可以选择一个没有恒星的位置 $(x, y)$。如果在此处创建恒星后，该恒星能够直接连接到至少 $3$ 颗恒星，则你可以在此处创建一颗新恒星。

给定一个由 $0$ 和 $1$ 组成的 $n \times n$ 矩阵 $a$，描述一个恒星集合 $S$。当且仅当 $a_{x,y} = 1$ 时，$(x, y)$ 处存在恒星。请计算 $S$ 的所有非空子集的价值之和，结果对 $10^9 + 7$ 取模。

$n\leq 14$。

## Solution

考虑给定集合怎么求答案。

首先有个性质，就是一个连通块假设包含它的最小矩形是 $[x_1,x_2][y_1,y_2]$，那么将连完边后相邻的两个点看成一个线段对 $x$ 轴和 $y$ 轴分别进行覆盖，则 $[x_1,x_2]$ 和 $[y_1,y_2]$ 全部会被覆盖到。

证明就考虑每次加入一个点 $(x_0,y_0)$ 不妨设 $x\in[x_1,x_2]$，则这个点一定能够通过 $x$ 的边和连通块连在一起，连过去的边也就能够更新 $[y_1,y_2]$。

对于两个连通块合并就简单了，两个连通块能合并的当且仅当两个矩形的 $x$ 或 $y$ 存在交。

根据上面的过程，只求一次答案可以对于每个初始点 $(x_i,y_i)$，建立 $[x_i,x_i][y_i,y_i]$ 的矩形，每次合并矩形即可。

---

然后考虑怎么做这道题。

设 $f_{l_1,r_1,l_2,r_2}$ 表示将 $[l_1,r_1][l_2,r_2]$ 内的点合并后恰好构成 $[l_1,r_1][l_2,r_2]$ 的方案数。

转移就考虑用连通块数至少为 $1$ 的方案数减去合并后不是 $[l_1,r_1][l_2,r_2]$ 的方案数。

先枚举 $x$ 的左端点最小的矩形 $[l_1',r_1'][l_2',r_2']$，然后需要保证 $[r_1'+1,r_1][l_2,r_2]$ 构成的所有矩形的 $y$ 区间不能和 $[l_2',r_2']$ 有交，现有状态无法转移，需要设新状态。

设 $g_{l,r,S}$ 表示 $x$ 坐标在 $[l,r]$，$y$ 坐标属于 $S$ 集合的点连出的所有连通块只能在 $[l,r]S$ 这个子集里的方案数。

对于 $f$ 的转移可以直接用 $g$ 维护，而 $g$ 的转移就考虑分讨 $x=l$ 是否有点，如果没有，贡献为 $g_{l+1,r,S}$；否则就要枚举这个 $x$ 等于 $l$ 的矩形的具体形状，然后同样可以转移。

而最终要输出的是连通块数，再维护 $h_{l,r,S}$ 表示 $x$ 坐标在 $[l,r]$，$y$ 坐标属于 $S$ 集合的点连出的所有连通块只能在 $[l,r]S$ 这个子集里的所有方案的连通块数之和。转移和 $g$ 同理。

时间复杂度：$O(n^8+2^nn^4)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 16, kMaxS = (1 << 14) + 5, kMod = 1e9 + 7;

int n;
int f[kMaxN][kMaxN][kMaxN][kMaxN], g[kMaxN][kMaxN][kMaxS], h[kMaxN][kMaxN][kMaxS], cnt[kMaxN][kMaxN], pw[kMaxN * kMaxN];
bool a[kMaxN][kMaxN];

int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

void clear() {
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      cnt[i][j] = 0;
      for (int k = 1; k <= n; ++k)
        for (int l = 1; l <= n; ++l)
          f[i][j][k][l] = 0;
      std::fill_n(g[i][j], 1 << n, 0);
      std::fill_n(h[i][j], 1 << n, 0);
    }
  }
}

int getcnt(int l1, int r1, int l2, int r2) {
  return cnt[r1][r2] - cnt[l1 - 1][r2] - cnt[r1][l2 - 1] + cnt[l1 - 1][l2 - 1];
}

int getst(int l, int r) {
  if (l > r) return 0;
  else return ((1 << r) - 1) ^ ((1 << (l - 1)) - 1);
}

void dickdreamer() {
  std::cin >> n; clear();
  for (int i = 1; i <= n; ++i) {
    std::string str;
    std::cin >> str;
    for (int j = 1; j <= n; ++j) {
      a[i][j] = str[j - 1] - '0';
      cnt[i][j] = cnt[i][j - 1] + cnt[i - 1][j] - cnt[i - 1][j - 1] + a[i][j];
    }
  }
  pw[0] = 1;
  for (int i = 1; i <= n * n; ++i) pw[i] = 2ll * pw[i - 1] % kMod;
  for (int len1 = 1; len1 <= n; ++len1) {
    for (int l1 = 1; l1 <= n - len1 + 1; ++l1) {
      int r1 = l1 + len1 - 1;
      for (int len2 = 1; len2 <= n; ++len2) {
        for (int l2 = 1; l2 <= n - len2 + 1; ++l2) {
          int r2 = l2 + len2 - 1;
          f[l1][r1][l2][r2] = pw[getcnt(l1, r1, l2, r2)] - 1;
          for (int _l1 = l1; _l1 <= r1; ++_l1) {
            for (int _r1 = _l1; _r1 <= r1; ++_r1) {
              for (int _l2 = l2; _l2 <= r2; ++_l2) {
                for (int _r2 = _l2; _r2 <= r2; ++_r2) {
                  if (_l1 == l1 && _r1 == r1 && _l2 == l2 && _r2 == r2) continue;
                  if (_r1 == r1) dec(f[l1][r1][l2][r2], f[_l1][_r1][_l2][_r2]);
                  else dec(f[l1][r1][l2][r2], 1ll * f[_l1][_r1][_l2][_r2] * g[_r1 + 1][r1][getst(l2, r2) ^ getst(_l2, _r2)] % kMod);
                }
              }
            }
          }
        }
      }
      for (int s = 0; s < (1 << n); ++s) {
        if (len1 == 1) {
          inc(g[l1][r1][s], 1);
        } else {
          inc(g[l1][r1][s], g[l1 + 1][r1][s]);
          inc(h[l1][r1][s], h[l1 + 1][r1][s]);
        }
        for (int p = l1; p <= r1; ++p) {
          for (int x = 1; x <= n; ++x) {
            for (int y = x; y <= n; ++y) {
              if (~s >> (y - 1) & 1) break;
              if (p == r1) {
                inc(g[l1][r1][s], f[l1][p][x][y]);
                inc(h[l1][r1][s], f[l1][p][x][y]);
              } else {
                inc(g[l1][r1][s], 1ll * f[l1][p][x][y] * g[p + 1][r1][s ^ getst(x, y)] % kMod);
                inc(h[l1][r1][s], 1ll * f[l1][p][x][y] * add(g[p + 1][r1][s ^ getst(x, y)], h[p + 1][r1][s ^ getst(x, y)]) % kMod);
              }
            }
          }
        }
      }
    }
  }
  std::cout << h[1][n][getst(1, n)] << '\n';
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