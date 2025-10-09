---
title: CF1326F2 Wise Men (Hard Version) 题解
date: 2025-09-05 20:48:00
---

## Description

有 $n$ 位智者居住在一座美丽的城市中。他们中的一些人彼此认识。

对于智者的每一种 $n!$ 种排列 $p_1, p_2, \ldots, p_n$，我们可以生成一个长度为 $n-1$ 的二进制字符串：对于每个 $1 \leq i < n$，如果 $p_i$ 和 $p_{i+1}$ 彼此认识，则设 $s_i=1$，否则 $s_i=0$。

对于所有可能的 $2^{n-1}$ 个二进制字符串，求有多少种排列会生成该二进制字符串。

$n\leq 18$。

## Solution

由于排列不好做，考虑容斥在数列中出现过的数的集合 $S$，结束之后做一遍 FWT 即可。

这时会发现枚举 $S$ 的复杂度已经有 $O(2^n)$ 了，再用 dp 算答案的复杂度至少是 $O(4^nn)$，过不了。

考虑对相邻认识的人继续容斥。具体地，我们可以钦定若干个位置 $i$，使得 $s_i$ 必须是 $1$，那么整个排列就会被划分成若干个连续段，连续段内部必须满足相邻的人互相认识，连续段之间互不影响。

维护 $g_i$ 表示在 $S$ 的情况下长度为 $i$ 的不同连续段数量，直接搜索可以做到 $O(4^n)$ 仍然过不了。

但是注意到我们只关心连续段中每个长度出现的次数，而不关心这些长度之间的顺序，所以不同的状态数实际上只有 $n$ 拆分数 $P(n)$ 个。

$n=18$ 时 $P(n)=385$，直接搜出这些状态后再做即可。

时间复杂度：$O(2^nnP(n))$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using u64 = uint64_t;

const int kMaxN = 19, kMaxS = (1 << 18) + 5, kMaxT = 390;

int n, t;
u64 f[kMaxS], ff[kMaxT];
bool gr[kMaxN][kMaxN];
std::vector<int> vec[kMaxT];
std::map<std::vector<int>, int> mp;

void dfs(int x, int len, std::vector<int> &v) {
  if (len == n) {
    vec[++t] = v, mp[v] = t;
    return;
  }
  if (x + len > n) return;
  dfs(x + 1, len, v);
  for (int i = 1; len + x * i <= n; ++i) {
    v.emplace_back(x);
    dfs(x + 1, len + x * i, v);
  }
  for (; v.size() && v.back() == x; v.pop_back()) {}
}

void getf() {
  std::vector<int> vv;
  dfs(1, 0, vv);
  for (int S = 1; S < (1 << n); ++S) {
    static int id[kMaxN];
    static u64 g[kMaxN][kMaxN], h[kMaxN];
    int t = 0; u64 coef = ((n - __builtin_popcount(S)) & 1) ? -1 : 1;
    memset(g, 0, sizeof(g));
    for (int i = 1; i <= n; ++i)
      if (S >> (i - 1) & 1)
        g[1][id[++t] = i] = 1;
    for (int i = 2; i <= n; ++i) {
      for (int lst = 1; lst <= n; ++lst) {
        for (int j = 1; j <= t; ++j)
          if (gr[lst][id[j]])
            g[i][id[j]] += g[i - 1][lst];
      }
    }
    for (int i = 1; i <= n; ++i) {
      h[i] = 0;
      for (int j = 1; j <= t; ++j)
        h[i] += g[i][id[j]];
      // std::cerr << h[i] << ' ';
    }
    // std::cerr << '\n';
    for (int i = 1; i <= ::t; ++i) {
      u64 cnt = coef;
      for (auto x : vec[i]) cnt *= h[x];
      ff[i] += cnt;
      // if (i == 3) std::cerr << "fuck " << S << ' ' << cnt << '\n';
    }
    // std::cerr << __builtin_popcount(S) << ' ' << h[n] << '\n';
    // int cnt = coef, len = 0, s = (1 << (n - 1)) - 1;
    // std::function<void()> dfs = [&] () {
    //   if (len == n) return void(f[s] += cnt);
    //   for (int i = 1; i <= n - len; ++i) {
    //     if (!h[i]) continue;
    //     cnt *= h[i], len += i;
    //     if (len < n) s ^= (1 << (len - 1));
    //     dfs();
    //     if (len < n) s ^= (1 << (len - 1));
    //     // assert(cnt % h[i] == 0);
    //     cnt /= h[i], len -= i;
    //   }
    // };
    // dfs();
  }
  // std::cerr << ff[3] << '\n';
  // std::cerr << t << '\n';
  // for (int i = 1; i <= t; ++i) {
  //   for (auto x : vec[i]) std::cerr << x << ' ';
  //   std::cerr << '\n';
  // }
  // std::cerr << "-------------\n";
  for (int s = 0; s < (1 << (n - 1)); ++s) {
    int lst = 0;
    std::vector<int> v;
    for (int i = 1; i <= n; ++i) {
      if ((~s >> (i - 1) & 1) || i == n) v.emplace_back(i - lst), lst = i;
    }
    std::sort(v.begin(), v.end());
    // std::cerr << mp[v] << '\n';
    // for (auto x : v) std::cerr << x << ' ';
    // std::cerr << '\n';
    f[s] = ff[mp[v]];
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::string str;
    std::cin >> str;
    for (int j = 1; j <= n; ++j) gr[i][j] = str[j - 1] - '0';
  }
  getf();
  // for (int s = 0; s < (1 << (n - 1)); ++s) std::cerr << f[s] << ' ';
  // std::cerr << '\n';
  for (int i = 0; i < n - 1; ++i)
    for (int s = 0; s < (1 << (n - 1)); ++s)
      if (~s >> i & 1)
        f[s] -= f[s | (1 << i)];
  for (int s = 0; s < (1 << (n - 1)); ++s) std::cout << f[s] << ' ';
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