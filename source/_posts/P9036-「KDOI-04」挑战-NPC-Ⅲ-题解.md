---
title: P9036 「KDOI-04」挑战 NPC Ⅲ 题解
date: 2025-08-26 11:54:00
---

## Description

给出一个含有 $n$ 个顶点，$m$ 条边的无向图 $G$，求 $G$ 中大小恰好为 $n-k$ 的独立集的数量。由于答案可能很大，请将其对 $998~244~353$ 取模。

$1\leq n\leq10^5$，$0\le m\le 10^5$，$0\leq k\leq \min(n-1,18)$，$1\leq T\leq 10^{4}$，$\sum n,\sum m\leq10^6$。

## Solution

注意到 $k$ 很小，取独立集的补集则可将问题转化为求有多少个大小为 $k$ 的点覆盖。

这类问题有个很普遍的技巧是考虑删点，这题就是如果存在一个点度数大于 $k$，则这个点一定会选，否则需要选所有它邻域的点就超了。在删点的同时把边也删掉。

如果剩下的边数超过 $k^2$ 则一定无解，因为剩下的点度数都不超过 $k$，选 $k$ 个最多只能覆盖 $k^2$ 条边。

那么问题转化为在一个 $O(k^2)$ 个点和边的图上做这个问题。

仍然考虑删点，任意拿出一个点，分讨它选不选。如果选，则把这个点和与这个点相连的边删掉。如果不选，则这个点邻域没被删掉的所有点都要选，这些邻域的点和边也能删掉。

那么复杂度为 $T(k)=T(k-1)+T(k-deg_x-1)+O(k^2)$，容易发现每次选度数最大的一定最优。如果最大的度数小于等于 $2$ 就能停止了，因为剩下的一定是一些环和一些链，dp 即可。

现在复杂度为 $T(k)=T(k-1)+T(k-3)+O(k^2)$，能轻松跑过 $k=18$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5, kMod = 998244353;

int n, m, k, cnt, ans;
int u[kMaxN], v[kMaxN], deg[kMaxN], pos[kMaxN], id[605], g[605][605];
int ff[605][25], gg[605][25], hh[25];
bool del[kMaxN], exi[kMaxN];

// ff[i][j] : 长度为 i 的链，选 j 个点覆盖方案数
// gg[i][j] : 长度为 i 的环，选 j 个点覆盖方案数

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

void prework(int n = 600, int k = 18) {
  static int tmp[605][25] = {0};
  memset(tmp, 0, sizeof(tmp));
  tmp[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= k; ++j) {
      // i 选
      if (j) {
        inc(ff[i][j], tmp[i - 1][j - 1]);
        if (i >= 2) inc(ff[i][j], tmp[i - 2][j - 1]);
      }
      tmp[i][j] = ff[i][j];
      // i 不选
      inc(ff[i][j], tmp[i - 1][j]);
    }
  }
  for (int op = 0; op < 2; ++op) {
    memset(tmp, 0, sizeof(tmp));
    if (!op) tmp[0][0] = 1;
    else tmp[1][1] = 1;
    gg[1][op] = 1;
    for (int i = 2; i <= n; ++i) {
      for (int j = 0; j <= k; ++j) {
        // i 选
        if (j) {
          inc(tmp[i][j], tmp[i - 1][j - 1]);
          if (i >= 2) inc(tmp[i][j], tmp[i - 2][j - 1]);
        }
        inc(gg[i][j], tmp[i][j]);
        // i 不选
        if (op) inc(gg[i][j], tmp[i - 1][j]);
      }
    }
  }
}

void upd() {
  assert(k >= 0);
  static int fa[605], sz[605], cnte[605];
  for (int i = 1; i <= cnt; ++i) fa[i] = i, sz[i] = 1, cnte[i] = 0;
  std::function<int(int)> find = [&] (int x) { return x == fa[x] ? x : fa[x] = find(fa[x]); };
  std::function<void(int, int)> unionn = [&] (int x, int y) {
    int fx = find(x), fy = find(y);
    if (fx != fy) fa[fx] = fy, sz[fy] += sz[fx], cnte[fy] += cnte[fx];
    ++cnte[fy];
  };
  for (int i = 1; i <= cnt; ++i) {
    if (del[id[i]]) continue;
    for (int j = i + 1; j <= cnt; ++j)
      if (!del[id[j]] && g[i][j])
        unionn(i, j);
  }
  static int f[25], tmp[25];
  memset(f, 0, sizeof(f));
  f[0] = 1;
  int tc = 0;
  for (int i = 1; i <= cnt; ++i) {
    if (!del[id[i]] && i == find(i)) {
      tc += sz[i];
      for (int j = 0; j <= k; ++j) tmp[j] = f[j], f[j] = 0;
      if (cnte[i] == sz[i] - 1) {
        for (int j = 0; j <= k; ++j)
          for (int s = 0; s <= k - j; ++s)
            inc(f[j + s], 1ll * tmp[j] * ff[sz[i]][s] % kMod);
      } else {
        for (int j = 0; j <= k; ++j)
          for (int s = 0; s <= k - j; ++s)
            inc(f[j + s], 1ll * tmp[j] * gg[sz[i]][s] % kMod);
      }
    }
  }
  for (int i = 0; i <= k; ++i) inc(ans, 1ll * f[i] * hh[k - i] % kMod);
}

void delet(int x) {
  assert(pos[x]);
  del[x] = 1;
  for (int i = 1; i <= cnt; ++i)
    if (!del[id[i]] && g[pos[x]][i])
      --deg[x], --deg[id[i]];
}

void rollback(int x) {
  assert(pos[x]);
  del[x] = 0;
  for (int i = 1; i <= cnt; ++i)
    if (!del[id[i]] && g[pos[x]][i])
      ++deg[x], ++deg[id[i]];
}

void dfs() {
  if (k < 0) return;
  int x = 0;
  for (int i = 1; i <= cnt; ++i) {
    if (!del[id[i]] && deg[id[i]] > deg[x]) x = id[i];
  }
  if (!x || deg[x] <= 2) return upd();
  delet(x), --k, dfs(), ++k, rollback(x);

  std::vector<int> vid;
  del[x] = 1;
  for (int i = 1; i <= cnt; ++i)
    if (!del[id[i]] && g[pos[x]][i])
      --k, delet(id[i]), vid.emplace_back(i);
  dfs();
  for (auto i : vid) ++k, rollback(id[i]);
  del[x] = 0;
}

void dickdreamer() {
  static std::unordered_map<int, bool> mp[kMaxN];
  std::cin >> n >> m >> k;
  for (int i = 1; i <= n; ++i) deg[i] = del[i] = pos[i] = 0, mp[i].clear();
  for (int i = 1; i <= m; ++i) {
    std::cin >> u[i] >> v[i];
    if (!mp[u[i]].count(v[i])) ++deg[u[i]], ++deg[v[i]], mp[u[i]][v[i]] = mp[v[i]][u[i]] = exi[i] = 1;
    else exi[i] = 0;
  }
  int now = 0;
  for (int i = 1; i <= n; ++i)
    if (deg[i] > k)
      del[i] = 1, ++now;
  if (now > k) return void(std::cout << "0\n");
  int cnte = 0;
  std::vector<int> vec;
  std::fill_n(deg + 1, n, 0);
  for (int i = 1; i <= m; ++i) {
    if (exi[i] && !del[u[i]] && !del[v[i]]) {
      ++cnte, vec.emplace_back(u[i]), vec.emplace_back(v[i]);
    }
  }
  if (cnte > k * k) return void(std::cout << "0\n");
  k -= now;
  std::sort(vec.begin(), vec.end());
  vec.erase(std::unique(vec.begin(), vec.end()), vec.end());
  cnt = vec.size();
  for (int i = 1; i <= cnt; ++i) {
    pos[id[i] = vec[i - 1]] = i, deg[id[i]] = 0;
    for (int j = 1; j <= cnt; ++j) g[i][j] = 0;
  }
  for (int i = 1; i <= m; ++i) {
    if (!del[u[i]] && !del[v[i]]) {
      g[pos[u[i]]][pos[v[i]]] = g[pos[v[i]]][pos[u[i]]] = 1;
    }
  }
  for (int i = 1; i <= cnt; ++i) {
    deg[id[i]] = 0;
    for (int j = 1; j <= cnt; ++j)
      deg[id[i]] += g[i][j];
  }
  int noww = 0;
  for (int i = 1; i <= n; ++i)
    if (!del[i] && !pos[i])
      ++noww;
  for (int i = 0; i <= k; ++i) {
    int cnt = 1;
    for (int j = noww; j > noww - i; --j) cnt = 1ll * cnt * j % kMod;
    for (int j = 1; j <= i; ++j) cnt = 1ll * cnt * qpow(j) % kMod;
    hh[i] = cnt;
  }
  ans = 0, dfs();
  std::cout << ans << '\n';
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T; prework();
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```