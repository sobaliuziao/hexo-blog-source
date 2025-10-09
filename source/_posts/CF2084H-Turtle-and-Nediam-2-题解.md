---
title: 'CF2084H Turtle and Nediam 2 题解'
date: 2025-04-14 11:53:00
---

## Description

给定一个长度为 $n$ 的 01 序列 $a$，每次操作可以选择一个 $i$，满足 $1\leq i\leq n-2$，并把 $a_i,a_{i+1},a_{i+2}$ 的第一个中位数删掉，问经过若干次操作（可以为零次）能操作出多少种不同的序列。

$n\leq 2\times 10^6$。

## Solution

首先很容易想到把 01 的极长连续段拿出来，设其为 $b_1,b_2,\ldots,b_m$，那么一次操作有两种不同的选法：

1. 选择 $1\leq i\leq m$ 且 $b_i\geq 2$，让 $b_i\gets b_i-1$。
2. 选择 $2\leq i\leq m-1$ 且 $b_i=b_{i-1}=1$，将 $b_{i-1}$ 删掉，并将 $b_i$ 合并到 $b_{i-2}$ 上。

由于 $b_m$ 只能做一操作，所以先不管 $b_m$，最后将答案乘 $b_m$ 即可。

---

注意到得到的最终状态序列的每一个元素一定是**大致**是由初始 $b$ 数组的一段不相交区间操作成，考虑 dp。

设 $f_i$ 表示已经确定了最终状态的一个前缀 $c_1,c_2,\ldots,c_k$，并且最小的能将这个最终状态前缀操作出来的初始状态前缀为 $i$ 的方案数。

这里先考虑最终状态的第一个连续段的颜色和 $b_1$ 相同的情况。

枚举 $c_{k+1}$ 是由哪个区间操作成，设其为 $[i+1,j]$，容易发现 $i\bmod 2\neq j\bmod 2$。

由于需要满足 $j$ 是最小的能把 $c_{k+1}$ 操作出来的右端点，所以需要记录一个 $p_j$ 表示当前能操作的最大长度，容易证明能操作出来的是一段前缀。

如果得到了 $p_j$，就让 $f_j\leftarrow f_i\times (p_j-p_{j-2})$ 即可。

考虑 $p_j$ 怎么求。假设已经得到了 $p_{j-2}$，那么 $j$ 有两种选法：

1. 先做一操作将 $b_{j-1}$ 和 $b_j$ 都变成 $1$，再做二操作将 $b_j$ 合并到 $b_{j-2}$ 上去，此时的长度为 $p_{j-2}+1$。
2. 做操作把 $b_{i+1},b_{i+2},\ldots,b_{j-1}$ 全删掉，此时长度为 $b_j$（如果改变了 $c_k$ 就做一操作复原即可）。

所以可以得到转移方程：$p_j=\max\{p_{j-2}+1,b_j\}$。

现在可以得到一个 $O(m^2)$ 的 dp 了:

```cpp
for i := 1 to m - 1:
    x := 0
    for j := i + 1 to m - 1:
        if j mod 2 != i mod 2:
            f[j] := f[j] + f[i] * (max(x + 1, b[j]) - x)
            x := max(x + 1, b[j])
```

---

考虑优化。

容易发现当前的 $b_j$ 对 $p$ 的影响是一段区间，并且是在最小的满足 $b_k-\frac{k}{2}>b_j-\frac{j}{2}$ 的 $k$ 处结束，可以用单调栈维护出，设 $k=nxt_j$。

考虑令 $j$ 初始为 $k$，并暴力跳 $nxt$ 更新，由于一个 $k$ 只会被经过 $b_k-\frac{k}{2}$ 次，所以总复杂度为 $O(\sum b_i)=O(n)$。

现在还需要解决 $c_1$ 的颜色和 $b_1$ 不同的情况。

由于将 $b_1$ 删掉需要做二操作，所以 $b_2$ 也必须变成 $1$，将 $b_1$ 删掉并把 $b_2$ 变成 $1$ 后再做上面的 dp 即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e6 + 5, kMod = 1e9 + 7;

int n, m;
int a[kMaxN];
std::string str;

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

int solve(int m, int *a) {
  static int f[kMaxN], d[kMaxN], nxt[kMaxN];
  if (m == 1) return a[m] - 1;
  std::function<void()> getnxt = [&] () {
    for (int o = 0; o < 2; ++o) {
      static int stk[kMaxN];
      int top = 0;
      stk[0] = m + 1;
      for (int i = m - (m % 2 != o); i >= 1; i -= 2) {
        for (; top && a[i] - i / 2 >= a[stk[top]] - stk[top] / 2; --top) {}
        nxt[i] = stk[top], stk[++top] = i;
      }
    }
  };
  getnxt();
  f[1] = a[1];
  for (int i = 0; i <= m; ++i) d[i] = 0;
  for (int i = 2; i <= m; ++i) f[i] = (i & 1);
  int ret = 0;
  for (int i = 1; i <= m - 1; ++i) {
    if (i >= 3) inc(d[i], d[i - 2]);
    inc(f[i], d[i]);
    if (i % 2 == (m - 1) % 2) inc(ret, f[i]);
    for (int j = i + 1, lim = 0; j <= m - 1; lim += (nxt[j] - j) / 2 - 1, j = nxt[j]) {
      inc(f[j], 1ll * f[i] * (std::max(lim + 1, a[j]) - lim) % kMod);
      assert(a[j] >= lim + 1);
      lim = std::max(lim + 1, a[j]);
      if (j + 2 < nxt[j]) {
        inc(d[j + 2], f[i]), dec(d[nxt[j]], f[i]);
        // for (int k = j + 2; k < nxt[j]; k += 2) {
        //   assert(lim + 1 >= a[k]);
        //   inc(f[k], f[i]);
        //   lim = std::max(lim + 1, a[k]);
        // }
      }
    }
    // for (int j = i + 1, lim = 0; j <= m - 1; j += 2) {
    //   inc(f[j], 1ll * f[i] * (std::max(lim + 1, a[j]) - lim) % kMod);
    //   lim = std::max(lim + 1, a[j]);
    // }
  }
  return 1ll * ret * a[m] % kMod;
}

void dickdreamer() {
  std::cin >> n >> str;
  m = 0;
  for (int i = 0, lst = -1; i < n; ++i) {
    if (i == n - 1 || str[i] != str[i + 1])
      a[++m] = i - lst, lst = i;
  }
  int ans = solve(m, a);
  if (n >= 2) {
    a[2] = 1;
    inc(ans, solve(m - 1, a + 1));
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
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```