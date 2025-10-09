---
title: 'CF603E Pastoral Oddities 题解'
date: 2024-11-17 15:58:00
---

## Description

给定一张 $n$ 个点的无向图，初始没有边。

依次加入 $m$ 条带权的边，每次加入后询问是否存在一个边集，满足每个点的度数均为奇数。

若存在，则还需要最小化边集中的最大边权。

$n \le 10^5$，$m \le 3 \times 10^5$。

## Solution

考虑给定一个图，怎么判断这个图存在一个边集满足条件。

结论是这个图的每个连通块大小为偶数就合法，否则不合法。证明就考虑如果存在一个连通块大小为奇数，则这个连通块最终总度数一定为奇数，而显然加入一条边所有点的度数和奇偶性不变，仍为偶数，所以矛盾。

如果一个连通块大小为偶数，就随便拿出一个生成树，然后从叶子向根考虑。如果一个点儿子连过来的边有偶数个，这个点就连父亲，否则不连。剩下的根节点也一定满足条件。

所以如果固定边集的可选范围，只需要先对于边权从小到大排序，在加边的过程中维护奇连通块的个数即可。

但是如果需要动态加边，上面那个做法就没用了，因为你无法确定某一个时刻的连通块状态。

考虑线段树分治。

由于答案从后往前不降，所以第 $i$ 条边在最优边集中存在的时间一定是一个以 $i$ 为左端点区间。线段树分治时先分治右子树，再分治左子树，到叶子时如果存在奇连通块就加入新边，直到不存在奇连通块。由于在加边的过程中新加入的边的存在时间被确定，所以在线段树上更新即可。

时间复杂度：$O(m\log n\log m)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5, kMaxM = 3e5 + 5;

int n, m, p, cnt_odd;
int ans[kMaxM];
std::tuple<int, int, int, int> ed[kMaxM];
std::vector<std::pair<int, int>> vec[kMaxM * 4];

struct DSU {
  int fa[kMaxN], sz[kMaxN], rnk[kMaxN];
  std::vector<std::tuple<int, int, int>> vec;

  void init() {
    for (int i = 1; i <= n; ++i)
      fa[i] = i, sz[i] = 1, rnk[i] = 0;
    cnt_odd = n;
  }

  void back(int t) {
    for (; vec.size() > t; vec.pop_back()) {
      auto [fx, fy, det] = vec.back();
      cnt_odd -= (sz[fy] & 1);
      fa[fx] = fx, rnk[fy] -= det, sz[fy] -= sz[fx];
      cnt_odd += (sz[fx] & 1) + (sz[fy] & 1);
    }
  }

  int find(int x) { return x == fa[x] ? x : find(fa[x]); }
  void unionn(int x, int y) {
    int fx = find(x), fy = find(y);
    if (fx == fy) return;
    if (rnk[fx] > rnk[fy]) std::swap(fx, fy);
    int det = (rnk[fx] == rnk[fy]);
    cnt_odd -= (sz[fx] & 1) + (sz[fy] & 1);
    fa[fx] = fy, rnk[fy] += det, sz[fy] += sz[fx];
    vec.emplace_back(fx, fy, det);
    cnt_odd += (sz[fy] & 1);
  }
} dsu;

void update(int x, int l, int r, int ql, int qr, std::pair<int, int> ed) {
  if (l > qr || r < ql) return;
  else if (l >= ql && r <= qr) return void(vec[x].emplace_back(ed));
  int mid = (l + r) >> 1;
  update(x << 1, l, mid, ql, qr, ed), update(x << 1 | 1, mid + 1, r, ql, qr, ed);
}

void solve(int x, int l, int r) {
  int t = dsu.vec.size();
  for (auto [u, v] : vec[x]) dsu.unionn(u, v);
  if (l == r) {
    for (; p < m && cnt_odd;) {
      ++p;
      auto [w, u, v, id] = ed[p];
      if (id <= l) {
        dsu.unionn(u, v);
        update(1, 1, m, id, l - 1, {u, v});
      }
    }
    if (!cnt_odd) ans[l] = std::get<0>(ed[p]);
    else ans[l] = -1;
  } else {
    int mid = (l + r) >> 1;
    solve(x << 1 | 1, mid + 1, r);
    solve(x << 1, l, mid);
  }
  dsu.back(t);
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= m; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    ed[i] = {w, u, v, i};
  }
  std::sort(ed + 1, ed + 1 + m);
  dsu.init();
  solve(1, 1, m);
  for (int i = 1; i <= m; ++i) std::cout << ans[i] << '\n';
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