---
title: CF2122G Tree Parking 题解
date: 2025-07-22 15:54:00
---

## Description

你得到一棵以 1 为根的树，共有 $n$ 个结点。

对于每个 $1 \leq i \leq n$，有一辆车会在时间 $l_i$ 从根结点进入。这辆车会沿着从根到结点 $i$ 的唯一路径（简单路径）瞬间行驶，并停在结点 $i$。它将在时间 $r_i$ 沿原路返回离开。

在车辆停在某个结点期间，该结点将被**占用**，不能被其他车辆通过。

当所有车辆都能在它们想要的时间进入并离开时，我们称这棵树是**合法的（valid）**。

请你计算有多少对序列 $l$、$r$ 满足以下条件：

* 对于每个 $i$，都有 $l_i < r_i$；
* 将 $l$ 和 $r$ 拼接后得到的长度为 $2n$ 的序列是 $1, 2, ..., 2n$ 的一个排列；
* 树是合法的（即所有车辆在各自的时间段可以顺利通过）。

现在的目标是：

对于所有**有 $n$ 个结点、恰好有 $k$ 个叶子结点**的**有标号树（labeled trees）**（注意：根结点 1 不算作叶子），求上述合法方案数的**总和**。

由于答案可能很大，请输出其对 $998244353$ 取模后的结果。

$1\leq k<n\leq 2\times 10^5$。

## Solution

首先考虑如果已知树的形态之后怎么求答案。

显然是按照子树从下往上考虑，假设已经知道了 $u$ 子树内除去 $u$ 的 $l$、$r$ 分配方案了，由于 $[l_u,r_u]$ 不能包含任意一个子树内点的左右端点，则 $l_u,r_u$ 只有 $2\cdot sz_u-1$ 种方案，总方案数为 $\displaystyle(2n)!\cdot\prod\frac{1}{2sz_u}=\frac{(2n)!}{2^n}\cdot\prod\frac{1}{sz_u}$。

现在只需要求出所有有标号有根树的 $\displaystyle\prod\frac{1}{sz_u}$ 即可，将这个乘上 $n!$ 就是一个有根树的拓扑序数量。

考虑先固定拓扑序，再计算可以以当前序列为拓扑序的方案数。

即设 $f(n,k)$ 表示已经确定了拓扑序 $n$ 个数的连边方案，有 $k$ 个叶子的方案数，则转移为：$f(n,k)=f(n-1,k-1)\cdot(n-k)+f(n-1,k)\cdot k$。最终答案为 $f(n,k)\cdot(n-1)!$，因为拓扑序第一项必须为 $1$，其余的可以随便排列。

现在考虑怎么快速求 $f(n,k)$。

注意到这个式子很像欧拉数 $A(n,k)$ 的转移方程，即 $A(n,k)=A(n-1,k-1)\cdot(n-k+1)+A(n-1,k)\cdot k$，打一个表会发现 $f(n,k)=A(n-1,k)$，再套用 $\displaystyle A(n,k)=\sum_{i=0}^{k-1}{(-1)^i\binom{n+1}{i}(k-i)^n}$ 即可。

最终的答案为 $\displaystyle\frac{(2n)!}{2^n\cdot n}\cdot f(n,k)$。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 4e5 + 5, kMod = 998244353;

int n, k;
int fac[kMaxN], ifac[kMaxN];

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
inline int getop(int x) { return (~x & 1) ? 1 : (kMod - 1); }

int C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

void prework(int n = 4e5) {
  fac[0] = 1;
  for (int i = 1; i <= n; ++i) fac[i] = 1ll * i * fac[i - 1] % kMod;
  ifac[n] = qpow(fac[n]);
  for (int i = n; i; --i) ifac[i - 1] = 1ll * i * ifac[i] % kMod;
}

int calc(int n, int k) {
  int ret = 0;
  for (int i = 0; i < k; ++i)
    inc(ret, 1ll * getop(i) * C(n + 1, i) % kMod * qpow(k - i, n) % kMod);
  return ret;
}

void dickdreamer() {
  std::cin >> n >> k;
  std::cout << 1ll * fac[2 * n] * qpow(1ll * qpow(2, n) * n % kMod) % kMod * calc(n - 1, k) % kMod << '\n';
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