---
title: P5547 [BJ United Round #3] 三色树 题解
date: 2024-10-11 16:05:00
---

## Description

请你对满足以下要求的 $n$ 个节点的 **无标号无根树** 计数： 
 
- 每个节点是三种颜色之一：红，蓝，黄
- 红色节点度数不超过 $4$，蓝色和黄色节点度数均不超过 $3$  
- 黄色节点不能相邻

注意 **无标号无根树** 的意义是：如果两颗树可以通过重新编号的方法使得对应点颜色相同，对应连边一致，则认为是同一颗树。

答案对输入的质数 $p$ 取模。

$1\leq n\leq 3000$。

## Solution

首先对无根树计数是无法做的，考虑利用树哈希的思想把重心定做根做有根树计数，然后减去树里面恰有 $2$ 个重心的方案数。

设 $f_{i,0/1/2}$ 表示大小为 $i$ 的有根树，根的颜色为红/蓝/黄且钦定根有一个父亲的方案数，同时维护 $g_{i,j}$ ，$h_{i,j}$ 表示 $i$ 个树的大小和为 $j$ 且根的颜色不为黄的方案数。

然后从小到大枚举 $i$，通过 $g$ 和 $h$ 求出 $f_{i,0/1/2}$ 后通过 $f_{i,0/1/2}$ 更新 $g$ 和 $h$。

恰有 $2$ 个重心的方案可以通过枚举根的颜色来求。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 3e3 + 5;

int n, mod;
int f[kMaxN][3], g[kMaxN][5], h[kMaxN][5];

// 0 : 红, 1 : 蓝, 2 : 黄

constexpr int qpow(int bs, int64_t idx = mod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % mod)
    if (idx & 1)
      ret = (int64_t)ret * bs % mod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= mod ? x + y - mod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + mod); }
inline void inc(int &x, int y) { (x += y) >= mod ? x -= mod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += mod : x; }

int C(int m, int n) {
  if (n == 0) return 1;
  else if (n == 1) return m;
  else if (n == 2) return 1ll * m * (m - 1) % mod * ((mod + 1) / 2) % mod;
  else if (n == 3) return 1ll * m * (m - 1) % mod * (m - 2) % mod * qpow(6) % mod;
  else return 1ll * m * (m - 1) % mod * (m - 2) % mod * (m - 3) % mod * qpow(24) % mod;
}

void upd(int f[kMaxN][5], int sz, int cnt) {
  if (!cnt) return;
  int g[5] = {1, cnt, add(cnt, C(cnt, 2)), add(cnt, add(1ll * cnt * (cnt - 1) % mod, C(cnt, 3))),
              add(C(cnt, 4), add(1ll * cnt * C(cnt - 1, 2) % mod, add(C(cnt, 2), add(1ll * cnt * (cnt - 1) % mod, cnt))))};
  for (int i = 3; ~i; --i) {
    for (int j = n; ~j; --j) {
      for (int k = 1; k <= 4 - i; ++k)
        if (j + k * sz <= n) inc(f[j + k * sz][i + k], 1ll * f[j][i] * g[k] % mod);
    }
  }
  // std::cerr << f[1][1] << '\n';
}

void dickdreamer() {
  std::cin >> n >> mod;
  if (n == 1) return void(std::cout << "3\n");
  g[0][0] = h[0][0] = 1;
  for (int i = 1; i <= n / 2; ++i) {
    // f[i][0]
    for (int j = 0; j <= 3; ++j) inc(f[i][0], g[i - 1][j]);
    // f[i][1]
    for (int j = 0; j <= 2; ++j) inc(f[i][1], g[i - 1][j]);
    // f[i][2]
    for (int j = 0; j <= 2; ++j) inc(f[i][2], h[i - 1][j]);

    upd(g, i, f[i][0]), upd(h, i, f[i][0]);
    upd(g, i, f[i][1]), upd(h, i, f[i][1]);
    upd(g, i, f[i][2]);
    // std::cerr << f[i][0] << ' ' << f[i][1] << ' ' << f[i][2] << '\n';
  }
  int ans = 0;
  for (int i = 0; i <= 4; ++i) inc(ans, g[n - 1][i]);
  for (int i = 0; i <= 3; ++i) inc(ans, g[n - 1][i]);
  for (int i = 0; i <= 3; ++i) inc(ans, h[n - 1][i]);
  if (~n & 1) {
    for (int i = 0; i <= 2; ++i)
      for (int j = i + 1; j <= 2; ++j)
        dec(ans, 1ll * f[n / 2][i] * f[n / 2][j] % mod);
    for (int i = 0; i <= 1; ++i)
      dec(ans, C(f[n / 2][i], 2));
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