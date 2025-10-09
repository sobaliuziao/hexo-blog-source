---
title: 'CF521D Shop 题解'
date: 2024-07-23 16:24:00
---

## Description

- 有 $k$ 个正整数 $a_{1\dots k}$。
- 有 $n$ 个操作，每个操作给定正整数 $t, i, b$，有三种可能：
  - 如果 $t = 1$，这个操作是将 $a_i$ 赋值为 $b$；
  - 如果 $t = 2$，这个操作是将 $a_i$ 加上 $b$；
  - 如果 $t = 3$，这个操作是将 $a_i$ 乘以 $b$。
- 你可以从 $n$ 个操作中选择最多 $m$ 个操作，并按照一定顺序执行。
- 你的目标是最大化 $\prod_{i=1}^k a_i$ 的值。
- $k,n \le 10^5$。

## Solution

容易发现每个数一定是先赋值再加再乘，所以赋值可以转化为加，这样就剩下了加和乘。

由于要最大化乘积，所以考虑把加转化为乘。

不妨先让每个数把所有操作都做了，现在需要去掉一些操作使得剩下的乘积最大且选择不超过 $m$ 个操作。

显然每个数一定是去掉加或乘的最小的哪个。去掉一个乘法 $b$ 会让乘积乘以 $1/b$。$a_i$ 去掉加法 $b$，会让乘积乘以 $(a_i-b)/a_i$，注意到每次去掉加法最小的那个后，再去掉一个加法对乘积的贡献一定会变大，所以每次贪心地去掉对乘积贡献最小的那个就行了。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e5 + 5;

int n, m, k;
int a[kMaxN], op[kMaxN], pos[kMaxN], val[kMaxN], p0[kMaxN], p1[kMaxN];
std::pair<int, int> mx[kMaxN];
bool vis[kMaxN];
std::vector<int> sum[kMaxN];
std::vector<std::pair<int, int>> vec[kMaxN][2];

struct frac {
  int x, y;

  frac(int _x = 0, int _y = 1) : x(_x), y(_y) {}
  friend bool operator <(frac a, frac b) {
    return (__int128_t)a.x * b.y < (__int128_t)a.y * b.x;
  }
};

int getsum(int x, int k) {
  if (!~k) return a[x];
  else return a[x] + sum[x][k];
}

void dickdreamer() {
  std::cin >> n >> m >> k;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= m; ++i) {
    std::cin >> op[i] >> pos[i] >> val[i];
    if (op[i] == 1) mx[pos[i]] = std::max(mx[pos[i]], {val[i], i});
    else if (op[i] == 2) vec[pos[i]][0].emplace_back(val[i], i);
    else vec[pos[i]][1].emplace_back(val[i], i);
  }
  std::priority_queue<std::tuple<frac, int, int, int>> qq;
  int cnt = 0;
  for (int i = 1; i <= n; ++i) {
    if (mx[i].first > a[i]) vec[i][0].emplace_back(mx[i].first - a[i], mx[i].second);
    std::sort(vec[i][0].begin(), vec[i][0].end(), std::greater<std::pair<int, int>>());
    std::sort(vec[i][1].begin(), vec[i][1].end(), std::greater<std::pair<int, int>>());
    sum[i].resize(vec[i][0].size());
    for (int j = 0; j < (int)vec[i][0].size(); ++j) {
      sum[i][j] = (!j ? 0 : sum[i][j - 1]) + vec[i][0][j].first;
    }
    for (auto [x, id] : vec[i][0]) vis[id] = 1;
    for (auto [x, id] : vec[i][1]) vis[id] = 1;
    p0[i] = (int)vec[i][0].size() - 1;
    p1[i] = (int)vec[i][1].size() - 1;
    if (~p0[i]) qq.emplace(frac(getsum(i, p0[i] - 1), getsum(i, p0[i])), i, 0, vec[i][0][p0[i]].second);
    if (~p1[i]) qq.emplace(frac(1, vec[i][1][p1[i]].first), i, 1, vec[i][1][p1[i]].second);
    cnt += vec[i][0].size() + vec[i][1].size();
  }
  for (; cnt > k; --cnt) {
    auto [f, i, o, id] = qq.top(); qq.pop();
    vis[id] = 0;
    if (!o) {
      --p0[i];
      if (~p0[i]) qq.emplace(frac(getsum(i, p0[i] - 1), getsum(i, p0[i])), i, 0, vec[i][0][p0[i]].second);
    } else {
      --p1[i];
      if (~p1[i]) qq.emplace(frac(1, vec[i][1][p1[i]].first), i, 1, vec[i][1][p1[i]].second);
    }
  }
  std::vector<int> vec[3];
  for (int i = 1; i <= m; ++i) {
    if (vis[i])
      vec[op[i] - 1].emplace_back(i);
  }
  std::cout << cnt << '\n';
  for (auto x : vec[0]) std::cout << x << ' ';
  for (auto x : vec[1]) std::cout << x << ' ';
  for (auto x : vec[2]) std::cout << x << ' ';
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