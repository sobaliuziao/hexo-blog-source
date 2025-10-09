---
title: 'P9058 [Ynoi2004] rpmtdq 题解'
date: 2024-04-05 15:46:00
---

## Description

给定一棵有边权的无根树，需要回答一些询问。

定义 $\texttt{dist(i,j)}$ 代表树上点 $i$ 和点 $j$ 之间的距离。

对于每一组询问，会给出 $l,r$，你需要输出 $\min(\texttt{dist(i,j)})$ 其中 $l\leq i < j \leq r$。$n\leq2\times 10^5$，$q\leq 10^6$，$1\le z\le 10^9$。

## Solution

注意到一个点对 $[l,r]$ 能作为询问的答案，当且仅当 $\min(\texttt{dist(i,j)})=\texttt{dist(i,j)}(l\leq i<j\leq r)$，考虑求出所有这样的 $[l,r]$，然后二维数点即可。

先点分治，假设分治中心为 $x$，$i$ 到 $x$ 的距离为 $a_i$。

那么 $\texttt{dist(i,j)}=a_i+a_j$，则如果 $i<k<j$ 且 $\texttt{dist(i,k)}\geq \texttt{dist(i,j)},\texttt{dist(k,j)}\geq \texttt{dist(i,j)}$，$[i,j]$ 就可以加到重要区间内。

化简一下就是 $\max\left\{a_i,a_j\right\}\leq \min_{k=i+1}^{j-1}{a_k}$，容易发现如果按照 $a$ 从小到大加点，那么加入 $j$ 时，$i$ 一定是 $j$ 的前驱或后继，用 set 维护即可。

时间复杂度：$O(n\log^2n+q\log n)$。

但是这样做常数太大了，过不了，因此点分治部分可以先按照编号大小排序，然后正反扫两边，维护单调栈即可。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5, kMaxQ = 1e6 + 5;

int n, q, rt;
int mx[kMaxN], sz[kMaxN], stk[kMaxN];
int64_t dis[kMaxN], ans[kMaxQ];
bool del[kMaxN];
std::vector<int> vec;
std::vector<std::pair<int, int64_t>> qq[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN], qr[kMaxN];

struct BIT {
  int64_t c[kMaxN];

  BIT() { memset(c, 0x3f, sizeof(c)); }

  void upd(int x, int64_t v) {
    for (; x; x -= x & -x) c[x] = std::min(c[x], v);
  }

  int64_t qry(int x) {
    int64_t ret = 1e18;
    for (; x <= n; x += x & -x) ret = std::min(ret, c[x]);
    return ret;
  }
} bit;

void getsz(int u, int fa) {
  mx[u] = 0, sz[u] = 1;
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    getsz(v, u);
    sz[u] += sz[v], mx[u] = std::max(mx[u], sz[v]);
  }
}

void getrt(int u, int fa, int tot) {
  mx[u] = std::max(mx[u], tot - sz[u]);
  if (mx[u] < mx[rt]) rt = u;
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    getrt(v, u, tot);
  }
}

void dfs2(int u, int fa) {
  vec.emplace_back(u);
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    dis[v] = dis[u] + w;
    dfs2(v, u);
  }
}

void dfs1(int u) {
  dis[u] = 0, dfs2(u, 0);
  std::sort(vec.begin(), vec.end());
  int top = 0;
  for (auto x : vec) {
    for (; top && dis[stk[top]] > dis[x]; --top) {}
    if (top) qq[x].emplace_back(stk[top], dis[x] + dis[stk[top]]);
    stk[++top] = x;
  }
  top = 0;
  std::reverse(vec.begin(), vec.end());
  for (auto x : vec) {
    for (; top && dis[stk[top]] > dis[x]; --top) {}
    if (top) qq[stk[top]].emplace_back(x, dis[x] + dis[stk[top]]);
    stk[++top] = x;
  }
  vec.clear(), vec.shrink_to_fit();
  del[u] = 1;

  for (auto [v, w] : G[u]) {
    if (del[v]) continue;
    rt = 0, getsz(v, 0), getrt(v, 0, sz[v]), dfs1(rt);
  }
}

void solve() {
  for (int r = 1; r <= n; ++r) {
    for (auto [l, w] : qq[r]) bit.upd(l, w);
    for (auto [l, id] : qr[r]) ans[id] = bit.qry(l);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
  }
  mx[0] = 1e9, getsz(1, 0), getrt(1, 0, n), dfs1(rt);
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int l, r;
    std::cin >> l >> r;
    ans[i] = 1e18;
    if (l != r) qr[r].emplace_back(l, i);
    else ans[i] = -1;
  }
  solve();
  for (int i = 1; i <= q; ++i) std::cout << ans[i] << '\n';
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