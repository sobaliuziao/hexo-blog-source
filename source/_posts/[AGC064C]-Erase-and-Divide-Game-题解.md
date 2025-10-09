---
title: [AGC064C] Erase and Divide Game 题解
date: 2024-10-08 20:38:00
---

## Description

Takahashi 和 Aoki 玩游戏。先在黑板上写若干个数，由 $N$ 个**互不相交**的区间 $[l_i,r_i]$ 组成。

两人轮流操作，每次操作先删去所有的奇数/偶数，再把剩下的数除以 $2$（向下取整），无法操作的人输。

Takahashi 先手，假设两人都采用最优策略，问谁能获胜。

$1\leq N\leq 10^4,0\leq l_i\leq r_i\leq 10^{18}$。

## Solution

首先如果总的数的个数不大，可以把每个数加到 trie 树，每次操作相当于是选择一个儿子往下走，如果没有儿子可走则输。显然可以 dp。

如果数的个数很多，可以把每个区间拆成 $\log V$ 个形如 $\left[x,x+2^k-1\right]$ 的区间，这些区间的在 trie 树上相当于在深度为 $k$ 的满二叉树每个叶子下面加上同样的一条链。

然后对于每个深度 $k$ 维护一个单独的 trie，表示接在深度为 $k$ 的满二叉树下面的链构成的 trie。

在 trie 树上走可以看成初始有 $\log V$ 个根，每次对于每个根同时往 $0/1$ 方向走，如果当前每个根的子树都没有点则当前操作的人输。

此时 dp 状态改为 $\log V$ 个树分别走到的点的位置，记忆化搜索即可。

时间复杂度：$O(n\log^3V)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e4 + 5, kMaxT = kMaxN * 60 * 60;

int n, tot = 1;
int trie[kMaxT][2];
bool vis[kMaxT];
std::array<int, 60> rt;
std::map<std::array<int, 60>, bool> f;

void init() {
  f.clear();
  for (int i = 1; i <= tot; ++i)
    trie[i][0] = trie[i][1] = vis[i] = 0;
  tot = 0;
  for (int i = 0; i < 60; ++i) {
    rt[i] = ++tot;
    int lst = tot;
    for (int j = 0; j < i; ++j) {
      trie[lst][0] = trie[lst][1] = ++tot;
      lst = tot;
    }
  }
}

void ins(int cur, int x) {
  assert(cur);
  vis[cur] = 1;
  for (int i = 0; i < 60; ++i) {
    int k = (x >> i & 1);
    if (!trie[cur][k]) trie[cur][k] = ++tot;
    vis[cur = trie[cur][k]] = 1;
  }
}

void update(int l, int r, int ql, int qr) {
  if (l > qr || r < ql) return;
  else if (l >= ql && r <= qr) return ins(rt[__builtin_ctzll(r - l + 1)], l);
  int mid = (l + r) >> 1;
  update(l, mid, ql, qr), update(mid + 1, r, ql, qr);
}

bool solve(std::array<int, 60> a) {
  if (f.count(a)) return f[a];
  bool fl = 0;
  for (int i = 0; i < 60; ++i) fl |= vis[a[i]];
  if (!fl) return 0;
  bool res = 1;
  for (int o = 0; o < 2; ++o) {
    auto b = a;
    for (auto &x : b) x = trie[x][o];
    res &= solve(b);
    if (!res) break;
  }
  return f[a] = (res ^ 1);
}

void dickdreamer() {
  std::cin >> n;
  init();
  for (int i = 1; i <= n; ++i) {
    int l, r;
    std::cin >> l >> r;
    update(0, (1ll << 60) - 1, l, r);
  }
  std::cout << (solve(rt) ? "Takahashi\n" : "Aoki\n");
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