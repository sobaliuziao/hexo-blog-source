---
title: 'CF1268E Happy Cactus 题解'
date: 2024-09-29 15:23:00
---

## Description

给定一张仙人掌图，第 $i$ 条边连接 $u,v$，边权为 $i$

定义路径为 "Happy Path" 当且仅当其满足沿途边权递增。

定义点对 $(u,v)$ Happy 当且仅当存在一条 Happy Path 以 $u$ 为起点，$v$ 为终点。

对于 $u=1,2...n$，求满足 $(u,v)$ Happy 的 $v$ 的数量。

$n,m\le 5\times 10^5$。

## Solution

先考虑树的情况怎么做。

由于这里建圆方树跑 dp 非常复杂，考虑按照编号从大到小加边。

设 $f_i$ 表示 $i$ 走已经加入的边能到多少个点。那么假设加入了 $(u,v)$，因为 $(u,v)$ 是当前边权最小的边，所以 $u$ 和 $v$ 跨过这条边后可以随便走，即让 $f_u=f_v=f_u+f_v$。

对于一般仙人掌的情况，直接照搬上面那个做法会出现一个问题，就是 $(u,v)$ 在加入这条边之前就已经存在共同能够到达的点了，会算重。

注意到这是个仙人掌，所以如果算重，就一定要满足 $(u,v)$ 是其所在环的最小边，且 $u,v$ 分别能够到达所在环的最大边 $(u_0,v_0)$，这时 $u$ 和 $v$ 同时能到达 $u_0,v_0$ 和通过 $(u_0,v_0)$ 能到的所有点。

算重的部分在加入 $(u_0,v_0)$ 的时候记录 $f_{u_0}+f_{v_0}$ 即可，所有环可以在 dfs 树上求出。

时间复杂度：$O(n+m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e5 + 5;

int n, m;
int u[kMaxN], v[kMaxN], dep[kMaxN], p[kMaxN], mat[kMaxN];
int f[kMaxN], g[kMaxN];
std::vector<int> G[kMaxN];

void dfs(int u, int pid) {
  p[u] = pid;
  for (auto id : G[u]) {
    int v = ::u[id] ^ ::v[id] ^ u;
    if (!dep[v]) {
      dep[v] = dep[u] + 1, dfs(v, id);
    } else if (dep[v] > dep[u]) {
      std::vector<int> ver, ed;
      for (int i = v; i != u; i = ::u[p[i]] ^ ::v[p[i]] ^ i)
        ver.emplace_back(i), ed.emplace_back(p[i]);
      ver.emplace_back(u), ver.emplace_back(v), ed.emplace_back(id);
      int mx = std::max_element(ed.begin(), ed.end()) - ed.begin(), mi = std::min_element(ed.begin(), ed.end()) - ed.begin();
      if ((int)ed.size() == 2) {
        mat[ed[mi]] = ed[mx];
        continue;
      }
      bool fl = 1;
      for (int i = (mx + 1) % ed.size(); i != mi; i = (i + 1) % ed.size()) {
        fl &= (ed[i] < ed[(i + (int)ed.size() - 1) % ed.size()]);
      }
      for (int i = (mx + (int)ed.size() - 1) % ed.size(); i != mi; i = (i + (int)ed.size() - 1) % ed.size()) {
        fl &= (ed[i] < ed[(i + 1) % ed.size()]);
      }
      if (fl) mat[ed[mi]] = ed[mx];
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    std::cin >> u[i] >> v[i];
    G[u[i]].emplace_back(i), G[v[i]].emplace_back(i);
  }
  dep[1] = 1, dfs(1, 0);
  std::fill_n(f + 1, n, 1);
  for (int i = m; i; --i) {
    g[i] = f[u[i]] = f[v[i]] = f[u[i]] + f[v[i]] - g[mat[i]];
  }
  for (int i = 1; i <= n; ++i) std::cout << f[i] - 1 << ' ';
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