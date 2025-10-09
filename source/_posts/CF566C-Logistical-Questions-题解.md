---
title: 'CF566C Logistical Questions 题解'
date: 2024-08-02 15:00:00
---

## Description

一棵 $n$ 个节点的树，点有点权，边有边权。

两点间的距离定义为两点间边权和的 $\frac 32$ 次方。

求这棵树的带权重心。

$n \le 2 \times 10^5$。

## Solution

不妨设 $d(i,j)=dist(i,j)^{1.5}$，考虑找到一个最小的在树上的端点或边上的一个位置，使得这个位置到所有节点的距离之和最小。

注意到 $\left(x^{1.5}\right)'=1.5\sqrt{x}$，所以 $y=x^{1.5}$ 是一个下凸函数。如果存在一个位置使得距离和最小，那么从这个位置往外走，距离和一定会变大。

考虑怎么求出这个位置。

注意到求权值和只能暴力，所以可以先随便找一个点 $u$，暴力求出答案，然后判断走哪个儿子会让答案变小。

暴力走儿子肯定会超时，考虑每次只向儿子 $v$ 走一个极小距离 $k$，显然答案的减少量是 $\Delta(v)=k\sum_{i\in subtree(v)}{\frac{3}{2}\sqrt{dist(i,u)}}$，增加量即为其余儿子的  $\Delta$ 之和，这部分暴力求，然后找到 $\Delta$ 值最大的 $v$ 走即可。

但是这样做可能会被链的情况卡成 $O(n^2)$。由于这里只需要锁定位置，所以每次可以选点分治的分治重心作根判断往哪边走，走后 $size$ 的大小一定不超过原来的 $\frac 12$，这样就只要做 $\log n$ 次了。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using f64 = long double;

const int kMaxN = 2e5 + 5;

int n, rt, ansid;
int val[kMaxN], sz[kMaxN], mx[kMaxN];
f64 ansdis;
bool del[kMaxN];
std::vector<std::pair<int, int>> G[kMaxN];

f64 pw(f64 x) { return x * sqrtl(x); }

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
  if (mx[u] < mx[rt]) rt = u;
  for (auto [v, w] : G[u]) {
    if (v == fa || del[v]) continue;
    getrt(v, u, tot);
  }
}

f64 dfs1(int u, int fa, int dis) {
  f64 ret = (f64)val[u] * pw(dis);
  for (auto [v, w] : G[u]) {
    if (v != fa) ret += dfs1(v, u, dis + w);
  }
  return ret;
}

f64 dfs2(int u, int fa, int dis) {
  f64 ret = (f64)val[u] * sqrtl((f64)dis);
  for (auto [v, w] : G[u]) {
    if (v != fa) ret += dfs2(v, u, dis + w);
  }
  return ret;
}

void solve(int u) {
  if (del[u]) return;
  mx[0] = 1e9, getsz(u, 0), getrt(u, 0, sz[u]);
  u = rt, del[u] = 1;
  f64 now = dfs1(u, 0, 0);
  if (!ansid || now < ansdis) ansid = u, ansdis = now;

  int idx = u;
  f64 mx = 0, sum = 0;
  for (auto [v, w] : G[u]) {
    f64 t = dfs2(v, u, w);
    sum += t;
    if (t > mx) mx = t, idx = v;
  }
  if (mx > sum - mx) solve(idx);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> val[i];
  for (int i = 1; i < n; ++i) {
    int u, v, w;
    std::cin >> u >> v >> w;
    G[u].emplace_back(v, w), G[v].emplace_back(u, w);
  }
  solve(1);
  std::cout << std::fixed << std::setprecision(10) << ansid << ' ' << ansdis << '\n';
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