---
title: CF2089C2 Key of Like (Hard Version)
date: 2025-07-31 14:45:00
---

## Description

有 $n$ 名成员参与游戏，他们按顺序轮流尝试解锁 $l$ 把锁。

每名成员在每轮中会根据历史信息选择最佳的钥匙和锁组合，选择的目标是最大化成功匹配的概率。成员们每次尝试时，只会使用尚未被尝试过的钥匙和锁。

这里除了能匹配锁的真实钥匙外，还有一些仿制钥匙（总数为 $k$），它们不能打开任何锁。

$1 \leq n \leq 100, 1 \leq l \leq 5000, 0 \leq k \leq 25$。

## Solution

首先如果 $k=0$，询问策略一定是对于任意一个锁，按顺序询问目前没有配对的所有钥匙，直到能配对。

如果存在仿制钥匙，可以虚拟出 $k$ 个锁，依次对应每个仿制钥匙。

设目前有 $x$ 个锁（不算虚拟的），$y$ 个仿制钥匙，第一次询问的是 $a$ 号锁，和 $b$ 号钥匙。

那么如果下一次询问的 $a$ 不变，改变询问的钥匙，概率则为 $\frac{1}{x+y-1}$。

如果下一次询问的 $b$ 不变，改变询问的锁，由于与 $a$ 配对的钥匙一定在去掉 $b$ 的所有钥匙中，所以 $b$ 是真钥匙的概率是 $\frac{x-1}{x+y-1}$，再随机一个锁和 $b$ 配对的概率是 $\frac{1}{x-1}$，所以下次询问正确的概率是 $\frac{x-1}{x+y-1}\cdot\frac{1}{x-1}=\frac{1}{x+y-1}$。

两个都改变显然不优，所以策略是以 $\frac{x-1}{2x+y-2}$ 的概率固定 $b$，依次询问所有的锁；以 $\frac{x+y-1}{2x+y-2}$ 的概率固定 $a$，依次询问所有的钥匙。

现在就可以 dp 了。设 $f_{i,j,k}$ 表示目前剩余 $i$ 个锁，$j$ 个仿制钥匙，做到了第 $k$ 个人的概率。

设 $p_r$ 表示$\bmod n=r$ 的所有轮数的概率。

对于第一种情况，询问到第 $p$ 个锁才找到配对的概率是 $\frac{1}{x+y}$，由于这个固定所以可以 $O(n)$ 计算 $p_r$，找不到的情况概率是 $\frac{y}{x+y}$。

第二种情况是同理的。

但是直接转移是 $O(n^2lk)$，注意到 $p_r$ 只有 $O(1)$ 个极长连续段，所以可以前缀和优化。

时间复杂度：$O(nlk)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 105, kMaxM = 5e3 + 35, kMaxK = 30, kMod = 1e9 + 7;

int n, m, k;
int f[kMaxM][kMaxK][kMaxN], inv[kMaxM * 2], res[kMaxN];

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

void prework(int n = 10030) {
  for (int i = 1; i <= n; ++i) inv[i] = qpow(i);
}

int getp(int x, int y) { return 1ll * x * inv[y] % kMod; }

void dickdreamer() {
  std::cin >> n >> m >> k;
  std::fill_n(res + 1, n, 0);
  for (int i = 0; i <= m; ++i)
    for (int j = 0; j <= k; ++j)
      std::fill_n(f[i][j], n + 1, 0);
  f[m][k][n] = 1;
  for (int i = m; i; --i) {
    for (int j = k; ~j; --j) {
      static int val[kMaxN], sum[kMaxN];
      std::fill_n(val, n, 0);
      // 换锁，钥匙不变
      int coef = getp(i - 1, 2 * i + j - 2);
      if (!j) coef = (kMod + 1) / 2;
      for (int s = 0; s < std::min(n, i); ++s) inc(val[(s + 1) % n], 1ll * ((i - 1 - s) / n + 1) * coef % kMod * getp(1, i + j) % kMod);
      // for (int s = 0; s < i; ++s) {
      //   inc(val[(s + 1) % n], 1ll * coef * getp(1, i + j) % kMod);
      //   // inc(val[(s + 1) % n], 1ll * coef * getp(1, i + j - s) % kMod);
      //   // coef = 1ll * coef * getp(i + j - s - 1, i + j - s) % kMod;
      // }
      coef = 1ll * coef * getp(j, i + j) % kMod;
      for (int lst = 1; lst <= n; ++lst) {
        if (j) inc(f[i][j - 1][(lst + i - 1) % n + 1], 1ll * f[i][j][lst] * coef % kMod);
      }
      coef = getp(i + j - 1, 2 * i + j - 2);
      if (!j) coef = (kMod + 1) / 2;
      for (int s = 0; s < std::min(n, i + j); ++s) inc(val[(s + 1) % n], 1ll * ((i + j - 1 - s) / n + 1) * coef % kMod * getp(1, i + j) % kMod);
      // for (int s = 0; s < i + j; ++s) {
      //   inc(val[(s + 1) % n], 1ll * coef * getp(1, i + j - s) % kMod);
      //   coef = 1ll * coef * getp(i + j - s - 1, i + j - s) % kMod;
      // }
      for (int s = 1; s <= n; ++s) sum[s] = add(sum[s - 1], f[i][j][s]);
      std::function<int(int, int)> getsum = [&] (int l, int r) {
        if (l <= r) return sub(sum[r], sum[l - 1]);
        else return add(sum[r], sub(sum[n], sum[l - 1]));
      };
      for (int l = 0, r = -1; l < n; l = r + 1) {
        for (; r + 1 < n && val[r + 1] == val[l]; ++r) {}
        for (int s = 1; s <= n; ++s) {
          inc(f[i - 1][j][s], 1ll * val[l] * getsum((s - r + n - 1) % n + 1, (s - l + n - 1) % n + 1) % kMod);
          inc(res[s], 1ll * val[l] * getsum((s - r + n - 1) % n + 1, (s - l + n - 1) % n + 1) % kMod);
        }
      }
      // for (int lst = 1; lst <= n; ++lst) {
      //   for (int s = 0; s < n; ++s) {
      //     inc(f[i - 1][j][(lst + s - 1) % n + 1], 1ll * f[i][j][lst] * val[s] % kMod);
      //     inc(res[(lst + s - 1) % n + 1], 1ll * f[i][j][lst] * val[s] % kMod);
      //     // if (1ll * f[i][j][lst] * val[s] % kMod) std::cerr << "??? " << (lst + s - 1) % n + 1 << ' ' << 1ll * f[i][j][lst] * val[s] % kMod << '\n';
      //   }
      // }
    }
  }
  for (int i = 1; i <= n; ++i) std::cout << res[i] << " \n"[i == n];
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  prework();
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```