---
title: 'CF1361E James and the Chase 题解'
date: 2024-04-08 19:45:00
---

## Description

给定一个有 $n$ 个点 $m$ 条边的**有向强连通图**。称一个点是**好的**当且仅当它到其他点都有且只有一条**简单路径**。如果好的点至少有 $20\%$ 则输出所有好的点，否则输出 `-1`。

**单个测试点内有多组数据。**
$1\leq T\leq 2\times 10^3,1\leq n\leq 10^5,1\leq m\leq 2\times 10^5,\sum n\leq 10^5,\sum m\leq 2\times 10^5$。

## Solution

考虑如何判断一个点是否是好的。

先以一个点 $x$ 为根建出 dfs 树，如果建不出来显然不合法，并且如果一条非树边不是返祖边，就说明存在横叉边，显然不合法。

容易发现满足上面的两个条件就一定合法，但是这样做单次是 $O(n)$ 的，过不了。

先不妨假设 $x$ 是好点，那么对于一个点 $y$，如果他是好点，就说明其子树里有且仅有 $1$ 条返祖边其祖先为 $y$ 的祖先，设其为 $z\to w$。

然后有一个性质：如果 $y$ 是好点当且仅当 $w$ 是好点。

证明：

如果 $y$ 是好点，由于 $w\to y$ 只有一条路径，所以 $w\to y$ 的子树的路径都有且仅有一条，并且 $y$ 要出 $w$ 的子树就必须经过 $w$，由于 $y\to w$ 子树外的点的路径都是唯一的，所以 $w\to w$ 子树外的点的路径也是唯一的，所以 $w$ 是好点。

如果 $w$ 是好点，由于 $w$ 到所有点路径唯一且 $y$ 出 $w$ 子树必须经过 $w$，所以 $y$ 也是好点。

所以先找到一个为好点的 $x$，然后做树上差分对于每个 $y$ 求出 $w$ 用并查集合并即可。

然后对于每个好点就一定和 $x$ 在同一并查集，否则无论如何也到不了 $x$。

至于找 $x$，就每次随机一个点做 $100$ 次，失败的概率是 $\left(\frac{4}{5}\right)^{100}$，非常小。

时间复杂度：$O\left(100(n+m)\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, m, fl = 1;
int cnt[kMaxN], sum[kMaxN], fa[kMaxN];
bool ins[kMaxN], vis[kMaxN];
std::vector<int> G[kMaxN];

int find(int x) { return x == fa[x] ? x : fa[x] = find(fa[x]); }

void unionn(int x, int y) {
  int fx = find(x), fy = find(y);
  if (fx != fy) fa[fx] = fy;
}

void dfs1(int u) {
  vis[u] = ins[u] = 1;
  for (auto v : G[u]) {
    if (!vis[v]) {
      dfs1(v);
    } else {
      if (!ins[v]) fl = 0;
      else ++cnt[u], --cnt[v], sum[u] += v, sum[v] -= v;
    }
  }
  ins[u] = 0;
}

void dfs2(int u) {
  ins[u] = 1;
  for (auto v : G[u]) {
    if (!ins[v]) {
      dfs2(v);
      cnt[u] += cnt[v], sum[u] += sum[v];
    } else {
    }
  }
  ins[u] = 0;
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (int i = 1; i <= m; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v);
  }
  std::vector<int> vec;
  for (int i = 1; i <= n; ++i) vec.emplace_back(i);
  std::shuffle(vec.begin(), vec.end(), std::mt19937(std::chrono::steady_clock::now().time_since_epoch().count()));
  for (int i = 0; i < std::min(100, (int)vec.size()); ++i) {
    int x = vec[i];
    for (int i = 1; i <= n; ++i) {
      fa[i] = i;
      cnt[i] = sum[i] = ins[i] = vis[i] = 0;
    }
    fl = 1, dfs1(x);
    if (!fl) continue;
    std::fill_n(ins + 1, n, 0);
    dfs2(x);
    for (int i = 1; i <= n; ++i) {
      if (cnt[i] == 1) {
        unionn(i, sum[i]);
      }
    }
    std::vector<int> idx;
    for (int i = 1; i <= n; ++i)
      if (find(i) == find(x))
        idx.emplace_back(i);
    if (idx.size() >= (n + 4) / 5) {
      for (auto u : idx) std::cout << u << ' ';
      std::cout << '\n';
    } else {
      std::cout << "-1\n";
    }
    return;
  }
  std::cout << "-1\n";
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