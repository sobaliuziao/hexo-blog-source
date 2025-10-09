---
title: CF2147H Maxflow GCD Coloring 题解
date: 2025-09-22 19:35:00
---

## Description

给定一个无向图 $G$，它有 $n$ 个顶点，每条边上有一个正整数容量。我们记 $\textsf{maxflow}(u,v)$

为图中从源点 $u$ 到汇点 $v$ 的最大流值。

我们称图 $G$ 是 **好图**，如果存在一个整数 $d \geq 2$，使得对于所有不同顶点对 $(u,v)$，共有的 $n \cdot (n-1)$ 个最大流值 $\textsf{maxflow}(u,v)$ 都能被 $d$ 整除。特别地，没有边的图显然是好图。

现在给定一张图，你需要给它的顶点染色，使得 **每一种颜色对应的顶点诱导出的子图都是好图**。

请找出所需颜色数目的最小值，并给出一种这样的染色方案。

$n\leq 50,m\leq\frac{n(n-1)}{2}$。

## Solution

先套路性地把最大流转成最小割。然后把初始图就合法的情况判掉。

如果 $d$ 很大的话我们是难以去刻画所有最大流都是 $d$ 的倍数的。

所以考虑 $d=2$ 的情况。由于去钦定**最小**割是偶数是不好做的，因为我们不知道哪些边构成了最小割，那么不妨让所有割集的权值都是偶数。

然后有个结论是每个点连出来的边的边权之和是偶数就能保证所有割集权值都是偶数。证明就考虑把偶边删掉，由于一个割集可以看成给每个点赋一个 $0/1$ 的颜色 $c_i$，对于一条边 $(u,v)$，其在割集等价于 $c_x\oplus c_y=1$。由于每个点度数都是偶数，所以总割边数中每个 $c_i$ 都会异或偶数次，也就是 $0$。

---

现在我们考虑钦定每个导出子图的每个点度数都是偶数，经过打表会发现这个是一定可以在颜色数等于 $2$ 的时候做到的。

具体构造就考虑递归构造，每次先把偶数边去掉，如果不存在奇度点就直接每个点染同样的颜色。否则随便找到一个奇度点 $x$，把与其有奇数权值连边的 $y$ 拿出来，两两加一条权值为 $1$ 的边。

把 $x$ 删掉后递归构造，递归回来后把 $y$ 之间两两连的边去掉。不妨设递归构造出来后之前找到的 $y$ 中颜色为 $0$ 的集合为 $S_0$，颜色为 $1$ 的集合是 $S_1$。

由于 $|S_0|+|S_1|$ 是奇数，所以一定存在恰好一个集合目前每个点的度数都是奇数，另一个全是偶数，因为我们刚把它们两两之间的边去掉。$x$ 的颜色染每个点度数都是奇数的集合对应的颜色，染完后把边加上即可。

对于初始图合法的情况需要用最小割树判断。

时间复杂度：$O(n^5)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 55, kMaxM = 2.5e3 + 5;

int n, m;
int u[kMaxM], v[kMaxM], w[kMaxM], res[kMaxN][kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];

namespace Dinic {
const int kMaxN = 55, kMaxM = 1e4 + 5;

struct Edge {
  int v, w, pre;
} e[kMaxM];

int tot = 1, n, s, t, tail[kMaxN], cur[kMaxN], dep[kMaxN];
bool tag[kMaxN];

void init(int _n, int _s, int _t) {
  tot = 1, n = _n, s = _s, t = _t;
  for (int i = 1; i <= n; ++i) tail[i] = 0;
}
void adde(int u, int v, int w) { e[++tot] = {v, w, tail[u]}, tail[u] = tot; }
void add(int u, int v, int w) { adde(u, v, w), adde(v, u, 0); }

bool bfs() {
  for (int i = 1; i <= n; ++i) cur[i] = tail[i], dep[i] = 1e9;
  std::queue<int> q;
  dep[s] = 0, q.emplace(s);
  for (; !q.empty();) {
    int u = q.front(); q.pop();
    if (u == t) return 1;
    for (int i = tail[u]; i; i = e[i].pre) {
      int v = e[i].v, w = e[i].w;
      if (w && dep[v] == 1e9) {
        dep[v] = dep[u] + 1, q.emplace(v);
      }
    }
  }
  return 0;
}

int dfs(int u, int lim) {
  if (u == t || !lim) return lim;
  int flow = 0;
  for (int &i = cur[u]; i; i = e[i].pre) {
    int v = e[i].v, w = e[i].w;
    if (w && dep[v] == dep[u] + 1) {
      int fl = dfs(v, std::min(lim, w));
      if (!fl) dep[v] = 1e9;
      e[i].w -= fl, e[i ^ 1].w += fl;
      lim -= fl, flow += fl;
      if (!lim) break;
    }
  }
  return flow;
}

int maxflow() {
  int ans = 0;
  for (; bfs(); ans += dfs(s, 1e9)) {}
  return ans;
}

int calc(int s, int t) {
  init(::n, s, t);
  for (int i = 1; i <= m; ++i) add(u[i], v[i], w[i]), add(v[i], u[i], w[i]);
  return maxflow();
}

void dfs(int u = s) {
  if (u == s) std::fill_n(tag + 1, n, 0);
  tag[u] = 1;
  for (int i = tail[u]; i; i = e[i].pre) {
    int v = e[i].v;
    if (e[i].w && !tag[v]) dfs(v);
  }
}
} // namespace Dinic

void build(std::vector<int> id) {
  if (id.size() <= 1) return;
  int s = id[0], t = id[1], w = Dinic::calc(s, t);
  G[s].emplace_back(t, w), G[t].emplace_back(s, w);
  Dinic::dfs();
  std::vector<int> idl, idr;
  for (auto i : id) (Dinic::tag[i] ? idl : idr).emplace_back(i);
  build(idl), build(idr);
}

void dfs(int u, int fa, int *res) {
  if (!fa) res[u] = 1e9;
  for (auto [v, w] : G[u]) {
    if (v == fa) continue;
    res[v] = std::min(res[u], w);
    dfs(v, u, res);
  }
}

void prework() {
  for (int i = 1; i <= n; ++i) G[i].clear();
  std::vector<int> id;
  for (int i = 1; i <= n; ++i) id.emplace_back(i);
  build(id);
  for (int i = 1; i <= n; ++i) dfs(i, 0, res[i]);
}

bool solve1() {
  int d = 0;
  for (int i = 1; i <= n; ++i)
    for (int j = i + 1; j <= n; ++j)
      d = std::__gcd(d, res[i][j]);
  if (d == 1) return 0;
  std::cout << "1\n" << n << '\n';
  for (int i = 1; i <= n; ++i) std::cout << i << " \n"[i == n];
  return 1;
}

void solve2() {
  static int cnt[kMaxN][kMaxN], deg[kMaxN], col[kMaxN];
  static bool del[kMaxN];
  for (int i = 1; i <= n; ++i) {
    deg[i] = 0;
    for (int j = 1; j <= n; ++j) cnt[i][j] = 0;
  }
  std::function<void(int, int)> add = [&] (int u, int v) {
    cnt[u][v] ^= 1, cnt[v][u] ^= 1;
    deg[u] ^= 1, deg[v] ^= 1;
  };
  for (int i = 1; i <= m; ++i) {
    if (w[i] & 1) add(u[i], v[i]);
  }
  for (int i = 1; i <= n; ++i) col[i] = -1, del[i] = 0;
  std::function<void()> dfs = [&]() {
    int x = 0;
    for (int i = 1; i <= n; ++i) {
      if (!del[i] && deg[i]) x = i;
    }
    if (!x) {
      for (int i = 1; i <= n; ++i)
        if (!del[i])
          col[i] = 0;
      return;
    }
    std::vector<int> id;
    for (int i = 1; i <= n; ++i)
      if (cnt[x][i])
        id.emplace_back(i);
    del[x] = 1;
    for (auto i : id) add(x, i);
    for (int i = 0; i < id.size(); ++i)
      for (int j = i + 1; j < id.size(); ++j)
        add(id[i], id[j]);
    dfs();
    del[x] = 0;
    for (int i = 0; i < id.size(); ++i)
      for (int j = i + 1; j < id.size(); ++j)
        add(id[i], id[j]);
    for (auto i : id) {
      int deg = 0;
      for (int j = 1; j <= n; ++j)
        if (col[j] != -1 && col[i] == col[j])
          deg ^= cnt[i][j];
      if (deg) add(x, i), col[x] = col[i];
      col[x] = col[i] ^ deg ^ 1;
    }
  };
  dfs();
  std::vector<int> vec[2];
  for (int i = 1; i <= n; ++i) assert(col[i] != -1), vec[col[i]].emplace_back(i);
  std::cout << "2\n";
  std::cout << vec[0].size() << '\n';
  for (auto x : vec[0]) std::cout << x << ' ';
  std::cout << '\n';
  std::cout << vec[1].size() << '\n';
  for (auto x : vec[1]) std::cout << x << ' ';
  std::cout << '\n';
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) std::cin >> u[i] >> v[i] >> w[i];
  prework();
  if (!solve1()) solve2();
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