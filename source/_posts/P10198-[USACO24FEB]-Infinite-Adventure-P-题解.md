---
title: 'P10198 [USACO24FEB] Infinite Adventure P 题解'
date: 2025-08-22 16:09:00
---

## Description

Bessie 正在计划一次在 $N$（$1\le N\le 10^5$）个城市的大陆上的无尽冒险。每个城市 $i$ 都有一个传送门以及循环周期 $T_i$。所有 $T_i$ 均为 $2$ 的幂，且 $T_1+\cdots+T_N\le 10^5$。如果你在日期 $t$ 进入城市 $i$ 的传送门，那么你会立即从城市 $c_{i,t\bmod T_i}$ 的传送门出来。

Bessie 的旅行有 $Q$（$1\le Q\le 5\cdot 10^4$）个计划，每个计划由一个元组 $(v,t,\Delta)$ 组成。在每个计划中，她将于日期 $t$ 从城市 $v$ 出发。然后，她将执行以下操作 $\Delta$ 次：她将进入当前城市的传送门，然后等待一天。对于她的每一个计划，她想要知道她最终会在哪个城市。

## Solution

首先 $\Delta$ 可能很大，所以显然是倍增求答案。

有一个普遍的想法是设 $f_{i,j,k}$ 表示目前的时间 $t$ 模 $a_i$ 为 $j$，再往后走 $2^k$ 步的位置。

但是这么做是无法转移的，因为如果后面走到一个点 $u$，满足 $a_u>a_i$ 则状态就不够用了。不过注意到整个路径上的不同前缀最大值数量只有 $O(\log A)$ 级别，所以容易想到找下个权值大于 $a_i$ 的位置。

具体地，将状态改成 $f_{i,j,k}$ 表示目前的时间 $t$ 模 $a_i$ 为 $j$，再往后走 $2^k$ 步的位置，如果这 $2^k$ 步存在权值比 $a_i$ 大的点则停在第一个这样的点，$g_{i,j,k}$ 表示这么走的步数。

预处理这个东西就考虑先走 $2^{k-1}$ 步，如果走到大于 $a_i$ 的点，就可以停止了。

如果走不到，设走到了 $x$，则需要在原来的基础上再走 $2^{k-1}$ 步，这种情况可以每次找到 $x$ 走到的下一个大于 $a_x$ 的位置，如果步数超过了剩余时间，则直接从 $f_{x,t,k-1}$ 转移过来，否则跳到这个大于 $a_x$ 的位置后再做同样的事情。

由于每次会让 $a_x$ 增加，所以只会跳 $O(\log A)$ 步。由于跳的过程中无法保证剩余时间一定是 $2$ 的幂次，所以每次还要倍增走，复杂度为 $O(n\log A\log^2 V)$。过不了。

---

上面做法的缺点是转移的时候先走 $2^{k-1}$ 步后当前的状态和走完之后的状态不能直接拼接在一起，导致预处理的时候会很慢。

考虑改变状态，设 $f_{i,j,k}$ 表示从 $(i,j)$ 往后走到的第 $2^k$ 个和 $a_i$ 权值相等的位置或者第一个大于 $a_i$ 的位置，这样预处理的时候就能 $O(1)$ 合并了。

查询就类似之前转移的做法每次跳到下一个大于当前位置权值的位置即可。

时间复杂度：$O(n\log V+q\log V\log A)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;
using i128 = __int128_t;
using pii = std::pair<int, i128>;

const int kMaxN = 1e5 + 5, kMaxQ = 5e4 + 5;

int n, q, mi;
int t[kMaxN];
std::vector<int> G[kMaxN], id[20];
std::vector<std::array<pii, 64>> f[kMaxN];

void prework() {
  for (int c = 0; c <= 16; ++c) {
    if (!id[c].size()) continue;
    // std::cerr << c << '\n';
    for (auto i : id[c]) {
      for (int j = 0; j < t[i]; ++j) {
        int x = G[i][j]; i128 len = 1;
        if (t[x] >= t[i]) { f[i][j][0] = {x, len}; continue; }
        // std::cerr << "---------------\n";
        for (;;) {
          auto [pos, _len] = f[x][(len + j) % t[x]][60];
          // std::cerr << pos << ' ' << t[pos] << '\n';
          if (t[pos] >= t[i]) {
            f[i][j][0] = {pos, len + _len};
            break;
          } else if (t[pos] > t[x]) {
            x = pos, len += _len;
          } else {
            f[i][j][0] = {0, 0};
            break;
          }
        }
        // f[i][j][0] = {G[i][j], 1};
      }
    }
    // std::cerr << c << '\n';
    for (int i = 1; i <= 60; ++i) {
      for (auto j : id[c]) {
        for (int k = 0; k < t[j]; ++k) {
          auto [pos, len] = f[j][k][i - 1];
          // if (pos) std::cerr << "shabi " << j << ' ' << pos << ' ' << len << '\n';
          if (!pos) {
            f[j][k][i] = {0, 0};
            continue;
          }
          if (t[pos] > t[j]) {
            f[j][k][i] = {pos, len};
          } else {
            auto [_pos, _len] = f[pos][(k + len) % t[pos]][i - 1];
            f[j][k][i] = {_pos, len + _len};
          }
        }
      }
    }
  }
}

int solve(int x, i64 T, i64 det) {
  for (; det;) {
    bool fl = 0;
    for (int i = 60; ~i; --i) {
      auto [pos, len] = f[x][T % t[x]][i];
      if (pos && len <= det) {
        fl = 1;
        T += len, det -= len;
        if (t[pos] > t[x]) { x = pos; break; }
        else x = pos;
      }
    }
    if (!det) break;
    if (!fl) x = G[x][T % t[x]], ++T, --det;
  }
  return x;
}

void dickdreamer() {
  std::cin >> n >> q;
  mi = 1e9;
  for (int i = 1; i <= n; ++i) {
    std::cin >> t[i];
    mi = std::min(mi, t[i]), id[__builtin_ctz(t[i])].emplace_back(i);
  }
  for (int i = 1; i <= n; ++i) {
    G[i].resize(t[i]), f[i].resize(t[i]);
    for (auto &x : G[i]) std::cin >> x;
  }
  prework();
  for (int i = 1; i <= q; ++i) {
    int x; i64 T, det;
    std::cin >> x >> T >> det;
    // std::cerr << x << ' ' << T << ' ' << det << '\n';
    std::cout << solve(x, T, det) << '\n';
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