---
title: [AGC018F] Two Trees 题解
date: 2024-02-29 10:51:00
---

## Description

给定两棵都是 $n$ 个节点的有根树 $A,B$，节点均从 $1..n$ 标号。

我们需要给每个标号定一个权值，使在两棵树上均满足任意节点子树权值和为 $1$ 或 $-1$。

输出任意一种解，需要判断无解。

$1\leq n\leq 10^5$。

## Solution

注意到每个点权值的奇偶性是确定的，所以如果两棵树对应点的奇偶性不同则一定无解，否则可以证明有解。

考虑如何构造方案。

先新建一个根，连接原来两棵树的根，然后对于 $i$，如果 $i$ 在两棵树里的度数均为奇数，则连一条 $i$ 左树点到右树点的边，这时每个点的度数就都为偶数了，所以可以跑一遍欧拉回路。

如果 $i$ 原来度数为偶数，权值为 $0$。否则如果 $(L_i,R_i)$ 这条边是从 $L_i\to R_i$，权值为 $1$，$R_i\to L_i$ 则为 $-1$。

下面证明这个构造是正确的。

考虑对于欧拉回路上的每个环计算贡献，对于点 $i$，一个环有三种情况：

1. 先走儿子，然后再从儿子或横叉边回来。
2. 先走儿子，再从父亲回来。
3. 先走父亲，再从儿子或横叉边回来。

对于 1 情况，$i$ 的子树会贡献一个 $1$ 一个 $-1$ 就抵消了。

对于 $2$ 和 $3$ 情况，$i$ 的子树都会有 $1$ 或 $-1$ 的贡献，但是注意到 $i$ 到父亲的边只有一条，所以 $2$ 和 $3$ 总共有且仅会出现一次，所以 $i$ 的子树最后权值和还是 $1$ 或 $-1$。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, rt1, rt2, cnt;
int fa1[kMaxN], fa2[kMaxN], deg1[kMaxN], deg2[kMaxN], cur[kMaxN], res[kMaxN];
bool vis[kMaxN * 2];
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u) {
  for (int i = cur[u]; i < G[u].size(); i = cur[u]) {
    cur[u] = i + 1;
    auto [v, id] = G[u][i];
    if (vis[id]) continue;
    vis[id] = 1;
    dfs(v);
    if (v && u == v + n) res[v] = 1;
    else if (u && v == u + n) res[u] = -1;
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> fa1[i];
    if (~fa1[i]) {
      deg1[fa1[i]] ^= 1, deg1[i] ^= 1;
      G[fa1[i]].emplace_back(i, ++cnt), G[i].emplace_back(fa1[i], cnt);
    } else {
      rt1 = i;
    }
  }
  for (int i = 1; i <= n; ++i) {
    std::cin >> fa2[i];
    if (~fa2[i]) {
      deg2[fa2[i]] ^= 1, deg2[i] ^= 1;
      G[fa2[i] + n].emplace_back(i + n, ++cnt), G[i + n].emplace_back(fa2[i] + n, cnt);
    } else {
      rt2 = i;
    }
  }
  deg1[rt1] ^= 1, deg2[rt2] ^= 1;
  for (int i = 1; i <= n; ++i) {
    if (deg1[i] != deg2[i])
      return void(std::cout << "IMPOSSIBLE\n");
  }
  G[0].emplace_back(rt1, ++cnt), G[rt1].emplace_back(0, cnt);
  G[0].emplace_back(rt2 + n, ++cnt), G[rt2 + n].emplace_back(0, cnt);
  for (int i = 1; i <= n; ++i) {
    if (deg1[i]) {
      G[i].emplace_back(i + n, ++cnt), G[i + n].emplace_back(i, cnt);
    }
  }
  dfs(0);
  std::cout << "POSSIBLE\n";
  for (int i = 1; i <= n; ++i) std::cout << res[i] << ' ';
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