---
title: 'Pjudge #21728. 【CTS Round #1 Day 1】地雷 题解'
date: 2025-09-28 11:15:00
---

## Description

给定一棵 $n$ 个顶点的树，其中第 $i$（$1 \le i \le n-1$）条边连接了顶点 $u_i$ 与 $v_i$（$1 \le u_i, v_i \le n$），其长度为 $w_i$。

在每个顶点上均埋藏着一棵地雷。第 $i$（$1 \le i \le n$）个顶点上的地雷的爆炸半径为 $R_i$ ，伤害值为 $h_i$ 。

我们定义 $\mathrm{dist}(i, j)$ 表示在树上顶点 $i$ 与顶点 $j$ 的最短距离。即，$\mathrm{dist}(i, j)$ 为顶点 $i$ 与 $j$ 之间唯一的简单路径的边权之和。

当顶点 $i$ 处的地雷爆炸时，所有距离其不超过 $R_i$ 的地雷都会一起爆炸。即，对于所有满足 $\mathrm{dist}(i, j) \le R_i$ 的地雷 $j$，如果其还没有爆炸，那么他也会被引爆。

对于每个 $i$（$i = 1, 2, \cdots, n$），你希望求出，如果在起始时引爆了顶点 $i$ 处的地雷，则最终所有被引爆的地雷的伤害值之和。

$1 \le n \le 10^5$，$1\le h_i\le 10^9$，$0 \le R_i \le 10^{18}$，$1 \le u_i, v_i \le n$，$1 \le w_i \le 10^{12}$。

## Solution

首先这题爆炸的过程会跳来跳去，没有一个固定的转移过程，考虑用点分治把跳的过程限定在点分树子树里。

先递归处理子树。设 $f_{rt,x}$ 表示从 $x$ 炸到 $rt$ 的最大剩余长度（只考虑 $rt$ 的子树），炸不到就设为 $-\infty$；$g_{rt,x}$ 表示要想从 $rt$ 炸到 $x$ 的最小初始剩余长度。那么 $x$ 能炸到 $y$ 的条件是存在一个 $rt$，使得 $f_{rt,x}\geq g_{rt,y}$。

先求 $g_{rt,x}$，在 $rt$ 点分树子树里的每个点 $k$ 维护一个 vector，表示 $k$ 的子树没有被炸到的点，并按照其与 $k$ 的距离从小到大排序。

然后直接从小到大枚举初始长度，同时维护一个队列表示新炸到的点，如果队列非空就拿出队首，枚举它炸到的下一个点的 LCA，在 LCA 的 vector 里从前往后枚举还没被炸到的点更新即可。

这部分时间复杂度是 $O(n\log^2n)$。

---

再求 $f_{rt,x}$。这里先求出从 $x$ 开始**第一次**炸到 $rt$ 最大剩余长度，枚举 $x$ 在炸到 $rt$ 之前炸到的最后一个点 $y$，由于 $x$ 和 $y$ 的 LCA 在 $rt$ 的子树内，就转化为了已经求出来的 dp 值了。

具体地，设枚举的 LCA 是 $k$，则如果 $f_{k,x}\geq g_{k,x}$ 就说明可以让 $dis_{k,x}+dis_{k,y}$ 更新 $f_{rt,x}$，这个可以双指针处理。

求出第一次炸到的结果后，利用新求出来的 $g_{rt,x}$ 再双指针算即可。

这部分时间复杂度也是 $O(n\log^2n)$。

---

现在求出了每个子树里的 dp 结果了，由于 $x$ 能炸到 $y$ 的条件是存在一个 $rt$，使得 $f_{rt,x}\geq g_{rt,y}$，这个 $rt$ 不唯一，直接枚举 $rt$ 会算重。

我们钦定 $x$ 和 $y$ 在 LCA 处计算，但是它们跳到的深度最浅的地方不一定是 LCA，所以还需要修改 dp 状态。

设 $f_{rt,x}$ 表示从 $x$ 炸到 $rt$ 的最大剩余长度（可以炸到整棵树），$g_{rt,x}$ 表示要想从 $rt$ 炸到 $x$ 的最小初始剩余长度（可以炸到整棵树）。

对于整棵点分树的根的 dp 数组已经通过刚才的过程得到了，考虑从上往下转移。

假设已经求出当前 $rt$ 的所有祖先 $rt'$ 的 dp 数组。

---

先求新的 $f_{rt,x}$。枚举 $x$ 跳到 rt 之前的最后一个点 $y$，设经过的深度最浅的 LCA $rt'$。那么在 $rt'$ 的子树内 $x$ 能跳到 $y$ 的条件是 $f_{rt',x}\geq g_{rt',y}$，满足了这个条件即可对 $f_{rt,x}$ 造成 $r_y-dis_{y,rt}$ 的贡献。

这个贡献可以在 $rt'$ 处处理，但是由于 $y$ 和 $rt$ 的 LCA 不固定，所以需要对于每个可能的 LCA $k$ 维护出 $r_y-dis_{k,x}$ 的最优值，更新 $f_{rt,x}$ 时再枚举 $rt$ 的祖先即可。

这部分时间复杂度是 $O(n\log^3n)$。

---

最后求 $g_{rt,x}$。枚举 $rt$ 跳到的第一个点 $y$，设最终跳到 $x$ 的最浅点是 $rt'$，则 $y$ 能对 $g_{rt,x}$ 造成贡献的条件为 $f_{rt',y}\geq g_{rt',x}$，贡献为 $dis_{rt,y}$。

跟求 $f$ 的做法一样在可能的 $LCA(rt,y)$ 处维护 $dis_{k,y}$ 的最优值即可。

这部分时间复杂度是 $O(n\log^3n)$。

总的时间复杂度是：$O(n\log^3n)$。

细节见代码以及[官方题解](https://pjudge.ac/blog/qingyu/blog/633)。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using i64 = int64_t;

const int kMaxN = 1e5 + 5;

int n, rt;
int a[kMaxN], p[kMaxN], dep[kMaxN], res[kMaxN];
i64 r[kMaxN], f[kMaxN][25], g[kMaxN][25], dis[kMaxN][25];
std::vector<std::pair<int, i64>> G[kMaxN];
std::vector<int> T[kMaxN], vid[kMaxN];
std::vector<int> v1[kMaxN], v2[kMaxN];

template<class T> inline void chkmax(T &x, T y) { x = (x > y ? x : y); }
template<class T> inline void chkmin(T &x, T y) { x = (x < y ? x : y); }

namespace Build {
int rt, sz[kMaxN], mx[kMaxN];
bool del[kMaxN], vis[kMaxN];

void getsz(int u, int fa) {
  sz[u] = 1, mx[u] = 0;
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    getsz(v, u);
    sz[u] += sz[v], mx[u] = std::max(mx[u], sz[v]);
  }
}

void getrt(int u, int fa, int tot) {
  mx[u] = std::max(mx[u], tot - sz[u]);
  if (!rt || mx[u] < mx[rt]) rt = u;
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    getrt(v, u, tot);
  }
}

void dfs2(int u, int fa, int rt, i64 d) {
  dis[u][dep[u] - dep[rt]] = d;
  for (auto [v, w] : G[u]) {
    if (v == fa || !vis[v]) continue;
    dfs2(v, u, rt, d + w);
  }
}

void dfs1(int u) {
  del[u] = 1;
  for (int i = u; i; i = p[i]) vid[i].emplace_back(u);
  for (auto [v, w] : G[u]) {
    if (del[v]) continue;
    rt = 0, getsz(v, 0), getrt(v, 0, sz[u]);
    T[u].emplace_back(rt), p[rt] = u, dep[rt] = dep[u] + 1;
    dfs1(rt);
  }
  for (auto x : vid[u]) vis[x] = 1;
  dfs2(u, 0, u, 0);
  for (auto x : vid[u]) vis[x] = 0;
}

void build() {
  mx[rt = 0] = 1e9, getsz(1, 0), getrt(1, 0, n), dep[rt] = 1, dfs1(::rt = rt);
  for (int i = 1; i <= n; ++i)
    std::sort(vid[i].begin(), vid[i].end(), [&] (int x, int y) { return dis[x][dep[x] - dep[i]] < dis[y][dep[y] - dep[i]]; });
}
} // namespace Build

namespace Part1 {

void dfs(int t) {
  for (auto v : T[t]) dfs(v);
  { // get g
    static bool vis[kMaxN] = {0};
    static std::vector<int> vec[kMaxN];
    for (auto i : vid[t]) {
      vec[i] = vid[i], std::reverse(vec[i].begin(), vec[i].end());
      vis[i] = 0;
    }
    for (auto v : vid[t]) {
      std::queue<int> q;
      q.emplace(v);
      int val = dis[v][dep[v] - dep[t]];
      for (; !q.empty();) {
        int i = q.front(); q.pop();
        for (int lca = i; dep[lca] >= dep[t]; lca = p[lca]) {
          while (true) {
            for (; vec[lca].size() && vis[vec[lca].back()]; vec[lca].pop_back()) {}
            if (!vec[lca].size()) break;
            int j = vec[lca].back();
            assert(!vis[j]);
            if (dis[i][dep[i] - dep[lca]] + dis[j][dep[j] - dep[lca]] <= r[i]) {
              g[j][dep[j] - dep[t]] = val, vis[j] = 1, q.emplace(j);
            } else {
              break;
            }
          }
        }
      }
    }
    v2[t] = vid[t];
    std::sort(v2[t].begin(), v2[t].end(), [&] (int i, int j) { return g[i][dep[i] - dep[t]] < g[j][dep[j] - dep[t]]; });
  }
  //
  { // get f
    for (auto v : vid[t]) {
      if (v == t) continue;
      i64 mx = -1e18;
      for (int i = 0, j = 0; i < v1[v].size(); ++i) {
        int x = v1[v][i];
        for (; j < v2[v].size(); ++j) {
          int y = v2[v][j];
          if (f[x][dep[x] - dep[v]] < g[y][dep[y] - dep[v]]) break;
          chkmax(mx, r[y] - dis[y][dep[y] - dep[t]]);
        }
        if (mx >= 0) chkmax(f[x][dep[x] - dep[t]], mx);
      }
    }
    f[t][0] = r[t];
    v1[t] = vid[t];
    std::sort(v1[t].begin(), v1[t].end(), [&] (int i, int j) { return f[i][dep[i] - dep[t]] < f[j][dep[j] - dep[t]]; });
    i64 mx = -1e18;
    for (int i = 0, j = 0; i < v1[t].size(); ++i) {
      int x = v1[t][i];
      for (; j < v2[t].size(); ++j) {
        int y = v2[t][j];
        if (f[x][dep[x] - dep[t]] < g[y][dep[y] - dep[t]]) break;
        chkmax(mx, r[y] - dis[y][dep[y] - dep[t]]);
      }
      if (mx >= 0) chkmax(f[x][dep[x] - dep[t]], mx);
    }
    std::sort(v1[t].begin(), v1[t].end(), [&] (int i, int j) { return f[i][dep[i] - dep[t]] < f[j][dep[j] - dep[t]]; });
  }
}

void solve() {
  memset(f, 0xcf, sizeof(f));
  memset(g, 0x3f, sizeof(g));
  dfs(rt);
}
} // namespace Part1

namespace Part2 {
void dfs(int t) {
  std::sort(v1[t].begin(), v1[t].end(), [&] (int i, int j) { return f[i][dep[i] - dep[t]] < f[j][dep[j] - dep[t]]; });
  std::sort(v2[t].begin(), v2[t].end(), [&] (int i, int j) { return g[i][dep[i] - dep[t]] < g[j][dep[j] - dep[t]]; });
  { // get f
    static int mx[kMaxN];
    for (auto i : vid[t]) mx[i] = -2e18;
    for (int i = 0, j = 0; i < v1[t].size(); ++i) {
      int x = v1[t][i];
      for (; j < v2[t].size(); ++j) {
        int y = v2[t][j];
        if (f[x][dep[x] - dep[t]] < g[y][dep[y] - dep[t]]) break;
        for (int pp = y; dep[pp] >= dep[t]; pp = p[pp]) chkmax(mx[pp], r[y] - dis[y][dep[y] - dep[pp]]);
      }
      std::vector<int> vec;
      for (int pp = x; dep[pp] > dep[t]; pp = p[pp]) {
        for (int qq = pp; dep[qq] >= dep[t]; qq = p[qq])
          if (mx[qq] - dis[pp][dep[pp] - dep[qq]] >= 0)
            chkmax(f[x][dep[x] - dep[pp]], mx[qq] - dis[pp][dep[pp] - dep[qq]]);
      }
    }
  }
  // 
  { // get g
    static int mi[kMaxN];
    for (auto i : vid[t]) mi[i] = 2e18;
    for (int i = (int)v2[t].size() - 1, j = (int)v1[t].size() - 1; ~i; --i) {
      int x = v2[t][i];
      for (; ~j; --j) {
        int y = v1[t][j];
        if (g[x][dep[x] - dep[t]] > f[y][dep[y] - dep[t]]) break;
        for (int pp = y; dep[pp] >= dep[t]; pp = p[pp]) chkmin(mi[pp], dis[y][dep[y] - dep[pp]]);
      }
      for (int pp = x; dep[pp] > dep[t]; pp = p[pp]) {
        for (int qq = pp; dep[qq] >= dep[t]; qq = p[qq])
          chkmin(g[x][dep[x] - dep[pp]], mi[qq] + dis[pp][dep[pp] - dep[qq]]);
      }
    }
  }
  //
  { // get res
    int sum = 0;
    for (int i = 0, j = 0; i < v1[t].size(); ++i) {
      int x = v1[t][i];
      for (; j < v2[t].size(); ++j) {
        int y = v2[t][j];
        if (f[x][dep[x] - dep[t]] < g[y][dep[y] - dep[t]]) break;
        sum += a[y];
      }
      res[x] += sum;
    }
    for (auto v : T[t]) {
      int sum = 0;
      std::vector<int> v1 = ::v1[v], v2 = ::v2[v];
      std::sort(v1.begin(), v1.end(), [&] (int i, int j) { return f[i][dep[i] - dep[t]] < f[j][dep[j] - dep[t]]; });
      std::sort(v2.begin(), v2.end(), [&] (int i, int j) { return g[i][dep[i] - dep[t]] < g[j][dep[j] - dep[t]]; });
      for (int i = 0, j = 0; i < v1.size(); ++i) {
        int x = v1[i];
        for (; j < v2.size(); ++j) {
          int y = v2[j];
          if (f[x][dep[x] - dep[t]] < g[y][dep[y] - dep[t]]) break;
          sum += a[y];
        }
        res[x] -= sum;
      }
    }
  }
  for (auto v : T[t]) dfs(v);
}

void solve() {
  dfs(rt);
}
} // namespace Part2

int LCA(int x, int y) {
  if (dep[x] < dep[y]) std::swap(x, y);
  for (; dep[x] > dep[y]; x = p[x]) {}
  for (; x != y; x = p[x], y = p[y]) {}
  return x;
}

bool check(int x, int y) {
  int lca = LCA(x, y);
  return f[x][dep[x] - dep[lca]] >= g[y][dep[y] - dep[lca]];
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  // for (int i = 1; i <= n; ++i) a[i] = 1;
  for (int i = 1; i <= n; ++i) std::cin >> r[i];
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
  }
  Build::build(), Part1::solve(), Part2::solve();
  for (int i = 1; i <= n; ++i) std::cout << res[i] << " \n"[i == n];
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