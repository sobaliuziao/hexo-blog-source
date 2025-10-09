---
title: P9669 [ICPC2022 Jinan R] DFS Order 2 题解
date: 2023-12-23 23:14:00
---

## Description

P 哥有一棵树，根节点是 $1$，总共有 $n$ 个节点，从 $1$ 到 $n$ 编号。

他想从根节点开始进行深度优先搜索。他想知道对于每个节点 $v$，在深度优先搜索中，它出现在第 $j$ 个位置的方式有多少种。深度优先搜索的顺序是在搜索过程中访问节点的顺序。节点出现在第 $j\ (1 \leq j \le n)$ 个位置表示它在访问了 $j - 1$个其他节点之后才被访问。因为节点的子节点可以以任意顺序访问，所以有多种可能的深度优先搜索顺序。

P 哥想知道对于每个节点 $v$，有多少种不同的深度优先搜索顺序，使得 $v$ 出现在第 $j$ 个位置。对于每个 $v$ 和 $j\ (i \le v,j \le n)$ 计算答案。

答案可能很大，所以输出时要取模 $998244353$。

$1\leq n\leq 500$。

以下是深度优先搜索的伪代码，用于处理树。在调用 `main()` 函数后，`dfs_order` 将会包含深度优先搜索的顺序。

```
void dfs(u):
  dfs_order.push_back(u)
  for (auto v : son(u))
    dfs(v)

void main():
  dfs_order = {}
  dfs(1)
```

## Solution

考虑树形 DP。

设 $f_{i}$ 表示 $i$ 的子树任意排列的方案数，这个东西是很好求的，$g_{i,j}$ 表示走到了 $i$，并且 $i$ 当前在第 $j$ 个的方案数。

假设当前是从 $u\to v$，然后会发现这个 $g$ 的转移会受到 $u$ 子树以外的点的影响，这个是不好搞的。

容易发现只要把 $g_{i,j}$ 改成表示走到了 $i$，并且 $i$ 当前在第 $j$ 个的**概率**，那么这个时候就只要考虑 $u$ 子树里对 $v$ 的影响了。

设 $h_{i,j}$ 表示 $u$ 的子树里去掉 $v$，选 $i$ 个无序儿子使得他们的子树大小和为 $j$ 的方案数。容易发现 $h_{i,j}$ 可以先用考虑所有儿子的答案，然后利用 01 背包的可撤销性求得。

所以这里 $v$ 的编号比 $u$ 的编号大 $i+1$ 的概率就是 

$$\frac{\sum\limits_{j=0}^{cnt-1}{h_{j,i}\times j!\times (cnt-1-j)!}}{cnt!}$$

其中 $cnt$ 表示 $u$ 的儿子个数。

然后只要枚举 $u$ 的编号为 $k$ 的概率和 $v$ 比 $u$ 大 $i$ 的概率即可得到 $v$ 的编号为 $k+i$ 的概率。

最后只要把所有的概率乘 $f_1$ 就是答案。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

namespace Modular {
template<class T>
T qpow(T bs, T idx, T kMod) {
  bs %= kMod;
  int ret = 1;
  for (; idx; idx >>= 1, bs = 1ll * bs * bs % kMod)
    if (idx & 1)
      ret = 1ll * ret * bs % kMod;
  return ret;
}
int inv(int x, int kMod) {
  x %= kMod;
  if (!x) { std::cerr << "inv error\n"; return 0; }
  return qpow(x, kMod - 2, kMod);
}
template<class T, const T kMod>
T add(T x, T y) {
  if (x + y >= kMod) return x + y - kMod;
  else return x + y;
}

template<class T, const T kMod>
T minu(T x, T y) {
  if (x - y < 0) return x - y + kMod;
  else return x - y;
}

template<class T, const T kMod>
struct Mint {
  T x;

  Mint() { x = 0; }
  template<class _T> Mint(_T _x) { x = _x; }

  friend Mint operator +(Mint m1, Mint m2) { return Mint(Modular::add<T, kMod>(m1.x, m2.x)); }
  friend Mint operator -(Mint m1, Mint m2) { return Mint(Modular::minu<T, kMod>(m1.x, m2.x)); }
  friend Mint operator *(Mint m1, Mint m2) { return Mint(1ll * m1.x * m2.x % kMod); }
  friend Mint operator /(Mint m1, Mint m2) { return Mint(1ll * m1.x * inv(m2.x, kMod) % kMod); }
  Mint operator +=(Mint m2) { return x = Modular::add<T, kMod>(x, m2.x); }
  Mint operator -=(Mint m2) { return x = Modular::minu<T, kMod>(x, m2.x); }
  Mint operator *=(Mint m2) { return x = 1ll * x * m2.x % kMod; }
  Mint operator /=(Mint m2) { return x = 1ll * x * inv(m2.x, kMod) % kMod; }

  template<class _T> friend Mint operator +(Mint m1, _T m2) { return Mint(Modular::add<T, kMod>(m1.x, m2 % kMod)); }
  template<class _T> friend Mint operator -(Mint m1, _T m2) { return Mint(Modular::minu<T, kMod>(m1.x, m2 % kMod)); }
  template<class _T> friend Mint operator *(Mint m1, _T m2) { return Mint(1ll * m1.x * m2 % kMod); }
  template<class _T> friend Mint operator /(Mint m1, _T m2) { return Mint(1ll * m1.x * inv(m2, kMod) % kMod); }
  template<class _T> Mint operator +=(_T m2) { return x = Modular::add<T, kMod>(x, m2); }
  template<class _T> Mint operator -=(_T m2) { return x = Modular::minu<T, kMod>(x, m2); }
  template<class _T> Mint operator *=(_T m2) { return x = 1ll * x * m2 % kMod; }
  template<class _T> Mint operator /=(_T m2) { return x = 1ll * x * inv(m2, kMod) % kMod; }
  template<class _T> friend Mint operator +(_T m1, Mint m2) { return Mint(Modular::add<T, kMod>(m1 % kMod, m2.x)); }
  template<class _T> friend Mint operator -(_T m1, Mint m2) { return Mint(Modular::minu<T, kMod>(m1 % kMod, m2)); }
  template<class _T> friend Mint operator *(_T m1, Mint m2) { return Mint(1ll * m1 * m2.x % kMod); }
  template<class _T> friend Mint operator /(_T m1, Mint m2) { return Mint(1ll * m1 * inv(m2.x, kMod) % kMod); }
  friend Mint operator -(Mint &m1) { return Mint(m1.x == 0 ? (kMod - 1) : (m1.x - 1)); }
  friend Mint operator --(Mint &m1) { return m1 = Mint(m1.x == 0 ? (kMod - 1) : (m1.x - 1)); }
  friend Mint operator ++(Mint &m1) { return m1 = Mint(m1.x == (kMod - 1) ? 0 : (m1.x + 1)); }
  friend bool operator ==(Mint m1, Mint m2) { return m1.x == m2.x; }

  friend std::istream &operator >>(std::istream &is, Mint &m) {
    int x;
    is >> x;
    m = Mint(x);
    return is;
  }
  friend std::ostream &operator <<(std::ostream &os, Mint m) {
    os << m.x;
    return os;
  }
};
} // namespace Modular

using mint = Modular::Mint<int, 998244353>;

const int kMaxN = 505;

int n;
int sz[kMaxN];
std::vector<int> G[kMaxN];
mint f[kMaxN], g[kMaxN][kMaxN], fac[kMaxN], ifac[kMaxN]; // f[i] : i 的子树的方案数, g[i][j] : i 排在第 j 个的概率

mint C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return fac[m] * ifac[n] * ifac[m - n];
}

void dfs1(int u, int fa) {
  f[u] = sz[u] = 1;
  int ct = 0;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    f[u] *= f[v] * (++ct);
  }
}

void dfs2(int u, int fa) {
  static mint ff[kMaxN][kMaxN], tmp[kMaxN];
  for (int i = 0; i <= n; ++i)
    for (int j = 0; j <= n; ++j)
      ff[i][j] = 0;
  ff[0][0] = 1;
  int now = 0, cnt = 0;
  mint mul = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    mul *= f[v];
    ++cnt;
    for (int i = cnt; i; --i)
      for (int j = sz[v]; j <= n; ++j)
        ff[i][j] += ff[i - 1][j - sz[v]];
    now += sz[v];
  }
  for (auto v : G[u]) {
    if (v == fa) continue;
    for (int i = 0; i <= n; ++i)
      tmp[i] = 0;
    for (int i = 1; i <= cnt; ++i)
      for (int j = sz[v]; j <= n; ++j)
        ff[i][j] -= ff[i - 1][j - sz[v]];
    for (int i = 0; i <= cnt - 1; ++i) {
      for (int j = 0; j <= n; ++j) {
        tmp[j] += ff[i][j] * fac[i] * fac[cnt - 1 - i] * mul;
      }
    }
    for (int i = cnt; i; --i)
      for (int j = sz[v]; j <= n; ++j)
        ff[i][j] += ff[i - 1][j - sz[v]];
    mint val = 1 / f[u];
    for (int i = 0; i <= n; ++i)
      for (int j = 0; j <= n - 1 - i; ++j)
        g[v][i + j + 1] += g[u][i] * tmp[j] * val;
  }
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs2(v, u);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  fac[0] = ifac[0] = 1;
  for (int i = 1; i <= n; ++i) {
    fac[i] = fac[i - 1] * i;
    ifac[i] = 1 / fac[i];
  }
  dfs1(1, 0);
  g[1][1] = 1;
  dfs2(1, 0);
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j)
      std::cout << g[i][j] * f[1] << ' ';
    std::cout << '\n';
  }
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