---
title: 'CF1477D Nezzar and Hidden Permutations 题解'
date: 2024-12-20 21:59:00
---

## Description

给定一张 $n$ 个点 $m$ 条边的简单无向图，构造两个排列 $p,q$，使得：

- 对任意 $(u,v)\in E$，$(p_u-p_v)(q_u-q_v)>0$.
- 在此基础上，最大化 $\left|\left\{i\ |\ p_i\neq q_i\right\}\right|$.

$1\leq n,m\leq 5\times 10^5$。

## Solution

首先显然如果存在一个点 $x$ 的度数等于 $n-1$，则将边定向后这个点的拓扑序一定唯一，所以这个位置一定会相同，可以把 $p_x,q_x$ 赋值为 $n$，然后将这个点删掉。

那么剩下的点一定满足度数 $\leq n-2$，可以猜测剩下的点一定没有位置相同。

考虑把现在的图的补图建出来，则一定构成若干个大小不小于 $2$ 的连通块。

如果补图是**恰好**一个菊花图，设菊花心为 $x$，其它点为 $a_1,a_2,\ldots,a_{n-1}$，让 $p_x=1,p_{a_i}=i+1,q_x=n,q_{a_i}=i$ 可以满足条件且没有位置相同。

这启发我们对于一般情况去把补图划分成若干个大小不小于 $2$ 的菊花图。

下面给出构造：

1. 从前往后扫 $i$，如果 $i$ 已经被划分进菊花图了，就不管。
2.  否则遍历 $i$ 的邻域，如果存在点 $j$ 使得 $j$ 没被划分进菊花图，就让 $i$ 和 $i$ 邻域所有没被划分的点放到一个菊花图里。
3. 如果找不到这样的 $j$，就随便取 $i$ 邻域的一个点 $k$，如果 $k$ 所在菊花大小等于 $2$，则将 $k$ 所在菊花的菊花心设为 $k$，并对 $k$ 做 $2$ 过程。
4. 如果菊花大小大于 $2$，就把 $k$ 从原来的菊花里踢出，然后和 $i$ 组成菊花。根据上面的构造方式，一定能保证 $k$ 不是原来所在菊花的心，所以构造方式仍然合法。

注意补图可能边数很多，这里只需要找到补图的一个生成树，找生成树时就维护一个 set 表示目前没被遍历的点，每次拓展时就暴力遍历 set，找到不与当前点在原图上有边的点，并在补图上连边即可。

时间复杂度：$O((n+m)\log n)$。

## Code

```C++
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e5 + 5;

int n, m, cnt;
int u[kMaxN], v[kMaxN], p[kMaxN], q[kMaxN], deg[kMaxN], bel[kMaxN];
bool del[kMaxN];
std::vector<int> G[kMaxN], T[kMaxN];
std::set<int> chry[kMaxN];

void init() {
  cnt = 0;
  for (int i = 1; i <= n; ++i)
    G[i].clear(), T[i].clear(), chry[i].clear(), p[i] = q[i] = deg[i] = bel[i] = del[i] = 0;
}

void solve1() { // 求出度数为 n - 1 的点
  std::set<std::pair<int, int>> st;
  for (int i = 1; i <= n; ++i) st.emplace(deg[i] = G[i].size(), i);
  int now = n;
  for (int i = 1; i <= n; ++i) {
    if (prev(st.end())->first != now - 1) break;
    int u = prev(st.end())->second;
    st.erase(prev(st.end()));
    p[u] = q[u] = ++cnt, --now, del[u] = 1;
    for (auto v : G[u]) {
      if (!del[v]) {
        st.erase({deg[v], v});
        --deg[v];
        st.emplace(deg[v], v);
      }
    }
  }
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (int i = 1; i <= m; ++i)
    if (!del[u[i]] && !del[v[i]])
      G[u[i]].emplace_back(v[i]), G[v[i]].emplace_back(u[i]);
}

void solve2() { // 求出补图生成森林
  std::set<int> st;
  for (int i = 1; i <= n; ++i) {
    if (!del[i]) st.emplace(i);
    std::sort(G[i].begin(), G[i].end());
  }
  std::function<void(int)> dfs = [&] (int u) {
    std::vector<int> vec;
    for (auto v : st)
      if (std::find(G[u].begin(), G[u].end(), v) == G[u].end())
        vec.emplace_back(v), T[u].emplace_back(v), T[v].emplace_back(u);
    for (auto v : vec) st.erase(v);
    for (auto v : vec) dfs(v);
  };
  for (int i = 1; i <= n; ++i) {
    if (!del[i] && st.count(i)) {
      st.erase(i);
      dfs(i);
    }
  }
}

void solve3() { // 求出菊花划分
  for (int i = 1; i <= n; ++i) {
    if (!del[i] && !bel[i]) {
      bool fl = 0;
      for (auto j : T[i]) fl |= !bel[j];
      if (fl) {
        chry[i].emplace(i), bel[i] = i;
        for (auto j : T[i]) {
          if (!bel[j]) chry[i].emplace(j), bel[j] = i;
        }
      } else {
        int j = T[i][0];
        if (chry[bel[j]].size() == 2) {
          chry[j].swap(chry[bel[j]]);
          bel[bel[j]] = j;
          for (auto x : T[j]) {
            if (!bel[x]) chry[j].emplace(x), bel[x] = j;
          }
        } else {
          chry[bel[j]].erase(j);
          bel[i] = bel[j] = i;
          chry[i].emplace(i), chry[i].emplace(j);
        }
      }
    }
  }
  int sum = cnt;
  for (int i = 1; i <= n; ++i) sum += chry[i].size();
  for (int i = 1; i <= n; ++i) {
    if (chry[i].size()) {
      p[i] = cnt + 1;
      int now = 1;
      for (auto x : chry[i]) {
        if (x != i) p[x] = cnt + (++now);
      }
      q[i] = cnt + now;
      now = 0;
      for (auto x : chry[i]) {
        if (x != i) q[x] = cnt + (++now);
      }
      cnt += chry[i].size();
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  init();
  for (int i = 1; i <= m; ++i) {
    std::cin >> u[i] >> v[i];
    G[u[i]].emplace_back(v[i]), G[v[i]].emplace_back(u[i]);
  }
  solve1(), solve2(), solve3();
  for (int i = 1; i <= n; ++i) std::cout << p[i] << " \n"[i == n];
  for (int i = 1; i <= n; ++i) std::cout << q[i] << " \n"[i == n];
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