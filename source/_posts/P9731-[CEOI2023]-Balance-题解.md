---
title: P9731 [CEOI2023] Balance 题解
date: 2024-04-03 16:07:00
---

## Description

由于黑客对评测机的攻击，组委会决定重测所有提交记录。

有 $N$ 台评测机，$T$ 个题目（编号为 $1, 2, \cdots, T$）。组委会已经确定，每台评测机要评测哪些提交（数目相同，都是 $S$ 个提交，保证 $S$ 是 $2$ 的整数次幂）。在接下来的 $S$ 分钟内，每分钟每台评测机会评测一个提交。

每个提交都会提交至某个题目。由于存数据的机器太脆弱了，所以要求，对于所有题目和任意两个时刻，在这两个时刻，这个题的被评测的提交的数量之差不超过 $1$。

请构造一组方案，使得满足上面的条件。

保证存在正整数 $k$ 使得 $S = 2 ^ k$，$1 \le N, S, T \le 10 ^ 5$，$NS \le 5 \times 10 ^ 5$。

## Solution

考虑 $S=2$ 的时候怎么做。

这里相当于要选择某些评测机并交换他们的两个题目，使得每个题目在第一列和第二列出现次数相差不超过 $1$。

那么如果把每个评测机的两个题目连一条无向边，题目等价于给每个无向边定向，使得每个点入度和出度相差不超过 $1$，这就是个欧拉回路的经典题了，只要建一个超级源点并与所有奇度点连边，然后对于每个连通块跑欧拉回路，每条边在欧拉回路里的方向就是最终的方向。

---

然后是 $S>2$ 的做法。

考虑把 $S$ 平分为两段，先让每个点在这两段里出现的次数相差不超过 $1$，然后分治处理，则最后的答案一定满足条件。

建图就考虑对于每行，$a_{i,j}$ 与 $a_{j+\frac{S}{2}}$ 连边，跑上面那个算法，虽然方案不一定是刚好 swap $a_{i,j}$ 与 $a_{j+\frac{S}{2}}$，但是这样一定能构造出来。

时间复杂度：$O\left((NS+T)\log^2 S\right)$，可以用 unordered_map 优化掉一个 $\log$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5, kMaxS = 5e5 + 5;

struct my_hash {
  static uint64_t splitmix64(uint64_t x) {
    x += 0x9e3779b97f4a7c15;
    x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9;
    x = (x ^ (x >> 27)) * 0x94d049bb133111eb;
    return x ^ (x >> 31);
  }

  size_t operator()(uint64_t x) const {
    static const uint64_t FIXED_RANDOM =
        std::chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x + FIXED_RANDOM);
  }

  size_t operator()(std::pair<uint64_t, uint64_t> x) const {
    static const uint64_t FIXED_RANDOM =
        std::chrono::steady_clock::now().time_since_epoch().count();
    return splitmix64(x.first + FIXED_RANDOM) ^
           (splitmix64(x.second + FIXED_RANDOM) >> 1);
  }
};

int n, m, t;
int cur[kMaxN];
bool vis[kMaxS], vs[kMaxN];
std::vector<int> a[kMaxN], vec;
std::vector<std::pair<int, int>> G[kMaxN];

void dfs(int u) {
  vs[u] = 1;
  for (int i = cur[u]; i < (int)G[u].size(); i = cur[u]) {
    cur[u] = i + 1;
    int v = G[u][i].first, id = G[u][i].second;
    if (vis[id]) continue;
    vis[id] = 1, dfs(v);
  }
  vec.emplace_back(u);
}

void solve(int l, int r) {
  if (l == r) return;
  for (int i = 0; i <= t; ++i)
    G[i].clear(), cur[i] = vs[i] = 0;
  int mid = (l + r) >> 1, len = r - l + 1, id = 0;
  for (int i = 1; i <= n; ++i) {
    for (int j = l; j <= mid; ++j) {
      vis[++id] = 0;
      G[a[i][j]].emplace_back(a[i][j + len / 2], id);
      G[a[i][j + len / 2]].emplace_back(a[i][j], id);
    }
  }
  int rt = 1;
  for (int i = 1; i <= t; ++i) {
    if (G[i].size() & 1) {
      rt = 0, vis[++id] = 0;
      G[rt].emplace_back(i, id), G[i].emplace_back(rt, id);
    }
  }
  cur[rt] = 0;
  std::unordered_map<std::pair<int, int>, int, my_hash> mp;
  for (int i = rt; i <= t; ++i) {
    if (!vs[i]) {
      vec.clear();
      dfs(i);
      for (int j = 0; j + 1 < (int)vec.size(); ++j)
        ++mp[{vec[j], vec[j + 1]}];
    }
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = l; j <= mid; ++j) {
      if (!mp[{a[i][j], a[i][j + len / 2]}]) {
        std::swap(a[i][j], a[i][j + len / 2]);
      }
      --mp[{a[i][j], a[i][j + len / 2]}];
    }
  }
  solve(l, mid), solve(mid + 1, r);
}

void dickdreamer() {
  std::cin >> n >> m >> t;
  for (int i = 1; i <= n; ++i) {
    a[i].resize(m);
    for (auto &x : a[i]) std::cin >> x;
  }
  solve(0, m - 1);
  for (int i = 1; i <= n; ++i) {
    for (auto x : a[i]) std::cout << x << ' ';
    std::cout << '\n';
  }
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