---
title: CF512D Fox And Travelling 题解
date: 2024-07-22 23:01:00
---

## Description

- 给定一张 $n$ 个点 $m$ 条边的无向图。
- 一个点只有当与它直接相连的点中最多只有一个点未被选择过时才可被选择。
- 询问对于每个 $k \in [0,n]$，有序选择 $k$ 个点的方案数。
- $n \le 100$，$m \le \frac{n(n-1)}2$，答案对 $10^9+9$ 取模。

## Solution

容易发现一个环上的任意一个点一定不能被选，因为只要不动这些点那么它们一定不会变，也就永远没选。并且如果两个环之间存在一条路径，则这个路径上的也不能选。

用拓扑排序去掉这些不能选的点后原图就变为一个森林，并且有两类点：周围有不能删的和周围没有不能删的。

容易发现一棵树里最多有一个周围不能删的，如果有则这个点一定是最后一个选，就把这个点作为根，跑 dp。

设 $f_{i,j}$ 表示以 $i$ 为根的子树里选 $j$ 个点的方案数，容易 $O(n^2)$ 转移。

由于 $i$ 要选的话一定是最后一个，所以 $f_{i,sz_i}=f_{i,sz_i-1}$。

---

考虑树没有根的情况。

先让每个点作为根求一遍答案加起来，但是会有算重，容易发现对于一个大小为 $i$ 的方案，会在不在这 $i$ 个点里的点作为根时被算到，所以会算 $sz-i$ 次，除去这个就行了。特别的对于 $i=sz$ 则显然不会算重，就不用除。

然后类似 dp 过程合并答案即可。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 105, kMod = 1e9 + 9;

int n, m, rt;
int f[kMaxN][kMaxN], g[kMaxN], tmp[kMaxN], ans[kMaxN], sz[kMaxN], C[kMaxN][kMaxN];
bool vis[kMaxN], del[kMaxN], exi[kMaxN];
std::vector<int> G[kMaxN], vec;

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1) ret = (int64_t)ret * bs % kMod;
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
    for (int j = 1; j <= i; ++j) C[i][j] = add(C[i - 1][j], C[i - 1][j - 1]);
  }
}

void _dfs(int u, int fa, int rt) {
  vis[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    if (!vis[v])
      _dfs(v, u, rt);
    else
      del[rt] |= (v == rt);
  }
}

void check(int x) {
  std::fill_n(vis + 1, n, 0);
  _dfs(x, 0, x);
  exi[x] = del[x];
}

void dfs1(int u, int fa) {
  vec.emplace_back(u);
  exi[u] = 1;
  bool fl = 0;
  for (auto v : G[u]) {
    fl |= del[v];
    if (v == fa || exi[v]) continue;
    dfs1(v, u);
  }
  if (fl) {
    if (~rt && !rt)
      rt = u;
    else if (~rt)
      rt = -1;
  }
}

void dfs2(int u, int fa) {
  sz[u] = 0, f[u][0] = 1;
  for (auto v : G[u]) {
    if (v == fa || del[v]) continue;
    dfs2(v, u);
    std::fill_n(g, n + 1, 0);
    for (int i = 0; i <= sz[u]; ++i)
      for (int j = 0; j <= sz[v]; ++j)
        inc(g[i + j], 1ll * f[u][i] * f[v][j] % kMod * C[i + j][i] % kMod);
    sz[u] += sz[v];
    for (int i = 0; i <= sz[u]; ++i) f[u][i] = g[i];
  }
  ++sz[u];
  f[u][sz[u]] = f[u][sz[u] - 1];
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  prework();
  for (int i = 1; i <= n; ++i) check(i);
  ans[0] = 1;
  for (int i = 1; i <= n; ++i) {
    if (!exi[i]) {
      vec.clear();
      rt = 0, dfs1(i, 0);
      if (!~rt) continue;
      if (rt) {
        dfs2(rt, 0);
        std::fill_n(g, n + 1, 0);
        for (int j = 0; j <= n; ++j) {
          for (int k = 0; k <= n - j; ++k)
            inc(g[j + k], 1ll * f[rt][j] * ans[k] % kMod * C[j + k][j] % kMod);
        }
        for (int j = 0; j <= n; ++j) ans[j] = g[j];
      } else {
        std::fill_n(tmp, n + 1, 0);
        for (auto x : vec) {
          dfs2(x, 0);
          for (int j = 0; j <= n; ++j)
            inc(tmp[j], f[x][j]);
        }
        std::fill_n(g, n + 1, 0);
        for (int j = 0; j <= (int)vec.size(); ++j) {
          tmp[j] = 1ll * tmp[j] * (j == vec.size() ? 1 : qpow((int)vec.size() - j)) % kMod;
          for (int k = 0; k <= n - j; ++k)
            inc(g[j + k], 1ll * tmp[j] * ans[k] % kMod * C[j + k][j] % kMod);
        }
        for (int j = 0; j <= n; ++j) ans[j] = g[j];
      }
    }
  }
  for (int i = 0; i <= n; ++i) std::cout << ans[i] << '\n';
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