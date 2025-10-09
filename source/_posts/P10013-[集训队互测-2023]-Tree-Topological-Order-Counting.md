---
title: 'P10013 [集训队互测 2023] Tree Topological Order Counting'
date: 2024-08-29 23:19:00
---

## Description

给定一颗 $n$ 个点的有根树，$1$ 是根，记 $u$ 的父亲是 $fa_u$。另给出一长度为 $n$ 的权值序列 $b$。

称一个长度为 $n$ 的排列 $a$ 为这颗树的合法拓扑序，当且仅当 $\forall 2 \le u \le n,a_u > a_{fa_u}$。

对每个点 $u$，定义 $f(u)$ 为，在所有这颗树的合法拓扑序中，$b_{a_u}$ 之和。

现在对 $1 \le u \le n$，求 $f(u) \bmod 10^9+7$。

$2 \le n \le 5000$，$1 \le fa_i < i$，$0 \le b_i < 10^9+7$。

## Solution

先考虑对于每个 $x$ 怎么求出答案。

假设当前处理到了节点 $u$（要求 $u$ 是 $x$ 的祖先），$v$ 为 $u$ 的儿子中子树包含 $x$ 的儿子。

设 $f_u$ 表示 $u$ 的子树的合法拓扑序数量，$g_{u,i}$ 表示 $u$ 的子树里已经钦定恰好有 $i$ 个点 dfs 序小于 $x$ 的方案数，$h_u$ 表示 $u$ 的子树去掉包含 $x$ 的子树剩下的点的合法拓扑序数。可以得到转移：

$$
\begin{aligned}
f_u&=(sz_u-1)!\prod_{w\in \text{son}_u}{f_w/(sz_w!)}\\
h_u&=\prod_{w\in \text{son}_u,w\neq v}{f_w/(sz_w!)}\\
g_{u,i+j+1}&=\sum_{0\leq i\leq sz_v-1,0\leq j\leq sz_u-sz_v-1}{\binom{i+j}{j}\binom{sz_u-i-j-2}{sz_v-i-1}h_ug_{v,i}}
\end{aligned}
$$

最终的答案即为 $\sum_{i=1}^{n}{g_{1,i-1}b_i}$。

时间复杂度：$O(n^3)$。

---

考虑怎么优化。

容易发现这题主要慢在每次要处理从一个点到根的路径上的 dp，而不是从根到某个点的路径，这样会导致每个点之间的信息没有任何交集。

注意到这题转移的终点是一定的，就是根，而起点不一样。所以可以类似[这题](https://www.cnblogs.com/Scarab/p/18383703)的思路把转移倒过来做。

具体的，将 $g_{u,i}$ 的状态改为当前状态为 $(u,i)$，到最终状态对答案的贡献。转移改为：

$$
g_{v,i}=\sum_{0\leq i\leq sz_v-1,0\leq j\leq sz_u-sz_v-1}{\binom{i+j}{j}\binom{sz_u-i-j-2}{sz_v-i-1}h_ug_{u,i+j+1}}
$$

最终 $x$ 的答案就是 $f_xg_{x,0}$。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 5e3 + 5, kMod = 1e9 + 7;

int n;
int a[kMaxN], C[kMaxN][kMaxN], sz[kMaxN], f[kMaxN], g[kMaxN][kMaxN];
std::vector<int> G[kMaxN];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
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

void prework() {
  C[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    C[i][0] = 1;
    for (int j = 1; j <= i; ++j)
      C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
}

void dfs1(int u) {
  f[u] = 1, sz[u] = 0;
  for (auto v : G[u]) {
    dfs1(v);
    f[u] = 1ll * f[u] * f[v] % kMod * C[sz[u] += sz[v]][sz[v]] % kMod;
  }
  ++sz[u];
}

void dfs2(int u) {
  for (auto v : G[u]) {
    int coef = 1, now = 0;
    for (auto w : G[u]) {
      if (w != v) coef = 1ll * coef * f[w] % kMod * C[now += sz[w]][sz[w]] % kMod;
    }
    for (int i = 0; i <= sz[v] - 1; ++i)
      for (int j = 0; j <= sz[u] - sz[v] - 1; ++j)
        inc(g[v][i], 1ll * coef * C[i + j][j] % kMod * C[sz[u] - i - j - 2][sz[v] - i - 1] % kMod * g[u][i + j + 1] % kMod);
    dfs2(v);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 2; i <= n; ++i) {
    int p;
    std::cin >> p;
    G[p].emplace_back(i);
  }
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  prework();
  for (int i = 1; i <= n; ++i) g[1][i - 1] = a[i];
  dfs1(1), dfs2(1);
  for (int i = 1; i <= n; ++i) std::cout << 1ll * f[i] * g[i][0] % kMod << ' ';
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