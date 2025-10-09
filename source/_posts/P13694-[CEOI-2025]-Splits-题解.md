---
title: 'P13694 [CEOI 2025] Splits 题解'
date: 2025-09-16 21:20:00
---

## Description

对于一个长度为 $n$ 的排列 $p = p[0], p[1], p[2], \ldots, p[n - 1]$（包含数字 $1, 2, 3, \ldots, n$ 的一个全排列），我们定义**分割排列**（split）为一个排列 $q$，它可以通过以下过程得到：

1. 选择两个数集  
   $A = i_1, i_2, \ldots, i_k$  
   $B = j_1, j_2, \ldots, j_l$  
   满足：
   - $A \cap B = \emptyset$
   - $A \cup B = \{0, 1, 2, \ldots, n - 1\}$
   - $i_1 < i_2 < \ldots < i_k$
   - $j_1 < j_2 < \ldots < j_l$
2. 将 $q$ 定义为：
   $$
   q = p[i_1]\, p[i_2] \ldots p[i_k]\, p[j_1]\, p[j_2] \ldots p[j_l]
   $$

进一步，我们定义 $S(p)$ 为排列 $p$ 的所有分割排列的集合。

现在，给定一个整数 $n$ 和一个集合 $T$，其中包含 $m$ 个长度为 $n$ 的排列。要求统计有多少个长度为 $n$ 的排列 $p$ 满足 $T \subseteq S(p)$。由于答案可能很大，请将结果对 $998\,244\,353$ 取模。

$1\leq n,m\leq 300$。

## Solution

首先这个条件等价于对于每个 $i$，都只存在至多一个 $j$，使得 $pos_{a_{i,j}}>pos_{a_{i,j+1}}$，令 $cut_i=j$。

那么如果得到了每个 $cut_i$，则可以直接设 $f_{i,j}$ 表示已经确定了第一行 $[1,i]$ 和 $[cut_1+1,j]$ 的数的位置的方案数。转移可以做到 $O(m)$，总复杂度为 $O(n^2m)$。

考虑如果没得到 $cut_i$ 怎么做。

这里有一个结论是暴搜前缀，直到得到每个 $cut_i$ 的这样的前缀数量是 $O(n^2+nm)$ 级别的。证明就考虑如果存在一个 $i$ 没得到 $cut_i$，则当前搜出来的前缀一定是 $a_i$ 的前缀，只有总共 $O(nm)$ 种。

考虑下一步就得到所有 $cut_i$ 的情况。

如果当前得到至少一个 $cut_i$，则下一步只有两种选择，贡献也就是 $O(nm)$。如果当前一个 $cut_i$ 都没得到，则当前的前缀是所有 $a_i$ 的公共前缀，最多 $O(n)$ 种，暴力枚举 $n$ 次总共是 $O(n^2)$。加起来就是 $O(n^2+nm)$。

搜出来 $cut_i$ 再暴力 dp 即可，因为常数很小，所以能过。

时间复杂度：$O(n^4m+n^3m^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include "grader.cpp"
#endif

const int kMaxN = 305, kMod = 998244353;

int n, m, t, ans;
int a[kMaxN][kMaxN], ps[kMaxN][kMaxN], cnt[kMaxN], p[kMaxN], pos[kMaxN];
int gg[kMaxN][kMaxN][kMaxN][2];

int qpow(int bs, int64_t idx = kMod - 2) {
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

int check() {
  int ret = 2;
  for (int i = 1; i <= m; ++i) {
    // int cnt = 0;
    // for (int j = 1; j < n; ++j) cnt += (pos[a[i][j]] > pos[a[i][j + 1]]);
    if (cnt[i] > 1) return 0;
    if (cnt[i] == 0) ret = 1;
  }
  return ret;
}

void getcnt() {
  static int f[kMaxN][kMaxN], cut[kMaxN];
  if (t == n) return inc(ans, 1);
  for (int i = 1; i <= m; ++i) {
    cut[i] = 0;
    for (int j = 1; j < n; ++j) {
      int v1 = pos[a[i][j]], v2 = pos[a[i][j + 1]];
      if (v1 && v2 && v1 > v2 || !v1 && v2) assert(!cut[i]), cut[i] = j;
    }
    assert(cut[i]);
  }
  memset(f, 0, sizeof(f));
  int ss = 0, tt = cut[1];
  for (int i = 1; i <= n; ++i) {
    int v1 = pos[a[1][i]], v2 = pos[a[1][i + 1]];
    if (v1 && !v2) {
      if (i <= cut[1]) ss = i;
      else tt = i;
    }
  }
  if (!ss && pos[a[1][cut[1]]]) ss = cut[1];
  // std::cerr << t << " : ";
  // for (int i = 1; i <= t; ++i) std::cerr << p[i] << " \n"[i == t];
  f[ss][tt] = 1;
  // std::cerr << "shabi " << ss << ' ' << tt << ' ' << cut[1] << '\n';
  for (int i = ss; i <= cut[1]; ++i) {
    for (int j = tt; j <= n; ++j) {
      if (!f[i][j]) continue;
      int x = 0, y = 0;
      bool fl1 = 0, fl2 = 0;
      if (i < cut[1]) x = a[1][i + 1], fl1 = 1;
      if (j < n) y = a[1][j + 1], fl2 = 1;
      if (x) assert(!pos[x]);
      if (y) assert(!pos[y]);
      // std::cerr << "shabi " << i << ' ' << j << ' ' << x << ' ' << y << '\n';
      for (int k = 2; k <= m; ++k) {
        if (fl1) {
          int p = ps[k][x], v = a[k][p - 1];
          if (v && (ps[1][v] > i && ps[1][v] <= cut[1] || ps[1][v] > j)) fl1 = 0;
        }
        if (fl2) {
          int p = ps[k][y], v = a[k][p - 1];
          if (v && (ps[1][v] > i && ps[1][v] <= cut[1] || ps[1][v] > j)) fl2 = 0;
        }
      }
      if (fl1) inc(f[i + 1][j], f[i][j]);
      if (fl2) inc(f[i][j + 1], f[i][j]);
      // if (fl2) std::cerr << "sbbb " << i << ' ' << j << ' ' << y << ' ' << ps[1][a[2][ps[2][y] - 1]] << '\n';
    }
  }
  // std::cerr << "fuck " << f[cut[1]][n] << ' ' << cut[1] << ' ' << cut[2] << ' ' << cut[3] << '\n';
  // std::cerr << "fuck " << cut[2] << ' ' << f[cut[1]][n] << ' ' << pos[1] << ' ' << pos[2] << ' ' << pos[3] << '\n';
  inc(ans, f[cut[1]][n]);
}

void dfs() {
  int fl = check();
  if (!fl) return;
  else if (t == n || fl == 2) return getcnt();
  for (int i = 1; i <= n; ++i) {
    if (pos[i]) continue;
    p[++t] = i, pos[i] = t;
    for (int j = 1; j <= m; ++j) cnt[j] += (ps[j][i] > 1 && !pos[a[j][ps[j][i] - 1]]);
    dfs();
    --t, pos[i] = 0;
    for (int j = 1; j <= m; ++j) cnt[j] -= (ps[j][i] > 1 && !pos[a[j][ps[j][i] - 1]]);
  }
}

int solve(int n, int m, std::vector<std::vector<int>>& splits) {
  ::n = n, ::m = m;
  for (int i = 1; i <= m; ++i)
    for (int j = 1; j <= n; ++j)
      ps[i][a[i][j] = splits[i - 1][j - 1]] = j;
  dfs();
  // p[++t] = 2, pos[2] = 1;
  // getcnt();
  // p[++t] = 2, p[++t] = 3;
  // pos[2] = 1, pos[3] = 2;
  // getcnt();
  return ans;
}
```