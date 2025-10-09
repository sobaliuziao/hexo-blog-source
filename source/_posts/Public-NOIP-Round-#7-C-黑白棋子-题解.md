---
title: Public NOIP Round #7 C 黑白棋子 题解
date: 2024-10-22 16:51:00
---

## Description

有一棵 $n$ 个点的树，顶点的编号为 $1$ 到 $n$。

对于树中的每个顶点，可能存在一个白色的棋子、一个黑色的棋子，或者没有棋子。树上正好有 $w$ 个白色棋子和 $b$ 个黑色棋子。另外，对于每一对具有相同颜色棋子的顶点，存在一条路径，路径上的每个顶点都包含相同颜色的棋子（即每种颜色的棋子形成一个连通块）。

你可以进行任意次以下操作：
- 选择一个带有棋子的顶点 $u$。
- 选择一条路径 $p_1, p_2, \dots, p_k$，使得 $p_1 = u$，且所有顶点 $p_1, p_2, \dots, p_{k-1}$ 都包含**相同颜色**的棋子，且 $p_k$ 上**没有棋子**。
- 将 $p_1$ 上的棋子移动到 $p_k$。此时 $p_1$ 上没有棋子，$p_k$ 上有一个棋子。

在每一步操作后，每种颜色的棋子仍然形成一个连通块。
对于两个初始的棋子状态 $S$ 和 $T$，如果你可以通过上述操作若干次（可以为零次）将 $S$ 变为 $T$，那么我们认为 $S$ 和 $T$ 是**等价**的。

定义 $f(w, b)$ 为在树上有  $w$ 个白色棋子和 $b$ 个黑色棋子时，等价类的数量。你需要求出：

$$\left(\sum_{w=1}^{n-1}\sum_{b=1}^{n-w} f(w,b)\cdot w\cdot b\right)\bmod 10^9+7$$

$n \ge 2,1\le \sum n\le 2\times 10^5,1\le fa_i<i$。

[link](https://pjudge.ac/contest/1811/problem/21859)

## Solution

考虑怎么对于给定的 $w,b$ 求出 $f(w,b)$。

不妨设 $w\geq b$，$mx_i$ 表示把 $i$ 号点删掉后剩余子树的最大大小。

那么如果 $w>mx_i$，则所有大小为 $w$ 的连通块都包含 $i$。

容易发现所有的必经点构成一个连通块，把这些必经点去掉后剩余的每个连通块之间都互不连通，所以黑色的连通块一定只与和其属于同一个连通块的黑色连通块等价，于是 $f(w,b)$ 就等于把必经点删掉后大小不小于 $b$ 的连通块数。

但是可能不存在必经点，即 $w\leq\min\left\{mx_i\right\}$。经过手玩会发现此时的 $f(w,b)$ 只可能等于 $1$ 或 $2$。

并且 $f(w,b)=1$ 的条件为存在一个点 $u$，其存在两个子树的大小 $\geq w$ 和另一个子树大小 $\geq b$，这是因为如果存在这样的点 $u$，移动黑色和白色连通块时可以先将后移动的连通块先寄存在一个不可能被经过的子树，等先移动的连通块动完再动，显然这样一定能构造出一组移动方案。

如果不满足那个条件，感性理解一下，黑色和白色连通块一定存在一个“先后顺序”，并且在移动的过程中这个顺序一定不会变，所以有 $2$ 种等价类。

对于存在必经点的情况，将重心当作根，直接枚举 $w$ 并维护删掉必经点后的每个子树的大小。如果不存在必经点，维护出满足 $f(w,b)=1$ 的最大的 $b$ 即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5, kMod = 1e9 + 7;

int n;
int p[kMaxN], sz[kMaxN], mx[kMaxN], suf[kMaxN], pos[kMaxN];
std::vector<int> G[kMaxN];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

int getsum(int n) {
  return 1ll * n * (n + 1) % kMod * ((kMod + 1) / 2) % kMod;
}
int getsum(int l, int r) {
  if (l > r) return 0;
  else return sub(getsum(r), getsum(l - 1));
}

void dfs(int u, int fa) {
  std::vector<int> vsz;
  sz[u] = 1, mx[u] = 0;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs(v, u);
    sz[u] += sz[v], mx[u] = std::max(mx[u], sz[v]);
    vsz.emplace_back(sz[v]);
  }
  mx[u] = std::max(mx[u], n - sz[u]);
  vsz.emplace_back(n - sz[u]);
  std::sort(vsz.begin(), vsz.end(), std::greater<>());
  if (vsz.size() >= 3) {
    suf[vsz[1]] = std::max(suf[vsz[1]], vsz[2]);
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) G[i].clear();
  std::fill_n(suf, n + 2, 0);
  for (int i = 2; i <= n; ++i) {
    std::cin >> p[i];
    G[p[i]].emplace_back(i), G[i].emplace_back(p[i]);
  }
  dfs(1, 0);
  std::vector<int> vec;
  for (int i = 1; i <= n; ++i) vec.emplace_back(i);
  std::sort(vec.begin(), vec.end(), [&] (int i, int j) { return mx[i] < mx[j]; });
  for (int i = 0; i < n; ++i) pos[vec[i]] = i;
  dfs(vec[0], 0);
  int ans = 0;
  for (int i = n; i; --i) {
    suf[i] = std::max(suf[i], suf[i + 1]);
    if (i > mx[vec[0]]) continue;
    int val = std::min(suf[i], i);
    if (val < i) {
      inc(ans, 2ll * i % kMod * getsum(1, val) % kMod);
      inc(ans, 4ll * i % kMod * getsum(val + 1, i - 1) % kMod);
      inc(ans, 2ll * i % kMod * i % kMod);
    } else {
      inc(ans, 2ll * i * getsum(1, i - 1) % kMod);
      inc(ans, 1ll * i * i % kMod);
    }
  }
  int now = getsum(n);
  for (int i = mx[vec[0]] + 1, j = 0; i <= n; ++i) {
    for (; j < n && mx[vec[j]] < i; ++j) {
      dec(now, getsum(sz[vec[j]]));
      for (auto v : G[vec[j]])
        if (pos[v] > j)
          inc(now, getsum(sz[v]));
    }
    inc(ans, 2ll * i * now % kMod);
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