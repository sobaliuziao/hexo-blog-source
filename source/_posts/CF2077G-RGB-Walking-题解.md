---
title: 'CF2077G RGB Walking 题解'
date: 2025-08-04 11:24:00
---

## Description

给定一个包含 $n$ 个顶点和 $m$ 条双向边的连通图，每条边的权重不超过 $x$。第 $i$ 条边连接顶点 $u_i$ 和 $v_i$，权重为 $w_i$，颜色为 $c_i$（$1 \leq i \leq m$，$1 \leq u_i, v_i \leq n$）。颜色 $c_i$ 为红色（red）、绿色（green）或蓝色（blue）。保证图中至少存在一条每种颜色的边。

对于一条允许重复顶点和边的路径，设 $s_r$、$s_g$、$s_b$ 分别表示路径中经过的红色、绿色和蓝色边的权重之和。若某条边被多次遍历，每次遍历均会被单独计数。

请找到从顶点 $1$ 到顶点 $n$ 的所有可能路径中，$\max(s_r, s_g, s_b) - \min(s_r, s_g, s_b)$ 的最小值。

$4 \leq n \leq 2 \cdot 10^5$，$n-1 \leq m \leq 2 \cdot 10^5$，$1 \leq x \leq 2 \cdot 10^5$。

## Solution

设 $t_i$ 表示第 $i$ 条边经过的次数。

首先显然可以对于每个 $t_i$ 变成一个很大的偶数，使得目前的 $\max(s_r, s_g, s_b) - \min(s_r, s_g, s_b)$ 为 $0$。后面就只需要满足度数奇偶性的限制之后即可满足答案。

然后对于每个颜色先单独考虑，注意到对于一条边 $i$，如果让 $t_i\leftarrow t_i+2$，整个图仍然是可以走出来的，也就是说这个颜色的权值和可以随意增加 $2\cdot w_i$。设 $g=\gcd(w_i)$，则如果 $r$ 能走出来，则 $r+2g$ 也能走出来。

所以我们只关心 $sum\bmod 2g$ 的值，又因为每个 $w_i$ 一定是 $g$ 的倍数，所以这样的余数只有两种，可以用 bfs 求出来。

三个颜色一起的话就用一个大小为 $8$ 的状态把这个压起来，再跑 bfs 即可求出三个颜色同时满足条件的余数。

现在问题变为有三个方程 $x_i\equiv r_i\pmod {M_i}$，问 $\max\{x_i\}-\min\{x_i\}$ 的最小值。

首先有个直观思路是枚举任意一个 $x_i$，另外的两个就只有 $O(1)$ 种可能取值，但是暴力做是 $O(V^2)$ 的。

注意到对于一个 $M_i$，如果它存在一个质因数 $p$ 使得另外两个都没有，则这个 $p$ 可以删掉，即让 $M_0\leftarrow\gcd(M_0,\text{lcm}(M_1,M_2))$。

这是因为这么操作完如果存在一个数 $x$ 满足条件，那么每次让 $x$ 加上 $\text{lcm}(M_1,M_2)$，总共加 $\frac{\text{lcm}(M_0,M_1,M_2)}{\text{lcm}(M_1,M_2)}$ 轮，一定存在恰好一次满足原先的限制。

操作完后可以设 $M_0=gab,M_1=gac,M_2=gbc$，其中 $a,b,c$ 两两互质。现在再去做最开始的暴力做法需要跑 $\frac{\text{lcm}(M_0,M_1,M_2)}{\max\{M_0,M_1,M_2\}}$ 次，也就是 $\min\{a,b,c\}$，由于 $ab,ac,bc\leq x$，所以 $\min\{a,b,c\}\leq\sqrt x$，所以复杂度变为 $O(\sqrt x)$。

时间复杂度：$O(n+m\log x+\sqrt x)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, m, x;
int u[kMaxN], v[kMaxN], w[kMaxN], col[kMaxN], st[kMaxN];
bool f[kMaxN][8];
std::vector<int> G[kMaxN];

int64_t lcm(int x, int y) { return 1ll * x / std::__gcd(x, y) * y; }

void bfs() {
  std::queue<std::pair<int, int>> q;
  for (int i = 1; i <= n; ++i)
    for (int s = 0; s < 8; ++s)
      f[i][s] = 0;
  f[1][0] = 1, q.emplace(1, 0);
  for (; !q.empty();) {
    auto [u, s] = q.front(); q.pop();
    for (auto i : G[u]) {
      int v = ::u[i] ^ ::v[i] ^ u, w = st[i], t = s ^ w;
      if (!f[v][t]) f[v][t] = 1, q.emplace(v, t);
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m >> x;
  for (int i = 1; i <= n; ++i) G[i].clear();
  int g[3] = {0};
  for (int i = 1; i <= m; ++i) {
    std::string str;
    std::cin >> u[i] >> v[i] >> w[i] >> str;
    if (str[0] == 'r') g[0] = std::__gcd(g[0], w[i]), col[i] = 0;
    else if (str[0] == 'g') g[1] = std::__gcd(g[1], w[i]), col[i] = 1;
    else g[2] = std::__gcd(g[2], w[i]), col[i] = 2;
    G[u[i]].emplace_back(i), G[v[i]].emplace_back(i);
  }
  g[0] *= 2, g[1] *= 2, g[2] *= 2;
  for (int i = 1; i <= m; ++i) {
    if (w[i] % g[col[i]] == 0) st[i] = 0;
    else st[i] = (1 << col[i]);
  }
  bfs();
  int ans = 1e9;
  int MM[3] = {std::__gcd<int64_t>(g[0], lcm(g[1], g[2])), std::__gcd<int64_t>(g[1], lcm(g[0], g[2])), std::__gcd<int64_t>(g[2], lcm(g[0], g[1]))};
  int LCM = lcm(MM[0], lcm(MM[1], MM[2]));
  for (int s = 0; s < 8; ++s) {
    if (!f[n][s]) continue;
    int M[3] = {MM[0], MM[1], MM[2]};
    int R[3] = {(s & 1) * g[0] / 2 % M[0], (s >> 1 & 1) * g[1] / 2 % M[1], (s >> 2 & 1) * g[2] / 2 % M[2]};
    if (M[1] > std::max(M[0], M[2])) std::swap(M[0], M[1]), std::swap(R[0], R[1]);
    else if (M[2] > std::max(M[0], M[1])) std::swap(M[0], M[2]), std::swap(R[0], R[2]);
    for (int i = R[0]; i <= LCM + R[0]; i += M[0]) {
      if (i < R[1] || i < R[2]) continue;
      int id[2][2] = {{(i - R[1]) / M[1] * M[1] + R[1], (i - R[1]) / M[1] * M[1] + M[1] + R[1]},
                      {(i - R[2]) / M[2] * M[2] + R[2], (i - R[2]) / M[2] * M[2] + M[2] + R[2]}};
      for (int o1 = 0; o1 < 2; ++o1)
        for (int o2 = 0; o2 < 2; ++o2)
          ans = std::min(ans, std::max({i, id[0][o1], id[1][o2]}) - std::min({i, id[0][o1], id[1][o2]}));
    }
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