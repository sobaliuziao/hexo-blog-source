---
title: 'CF1239E Turtle 题解'
date: 2024-09-22 21:44:00
---

## Description

一只乌龟从 $2 \times n$ 的棋盘的左上角走到右下角，只能往下或往右，需要给出一种方案来分配 $2n$ 个数字使得乌龟走过的路径上的数之和的最大值最小。

$2\leq n\leq 25,0\leq a_{1,i},a_{2,i}\leq 5\times 10^4$。

## Solution

设 $pre_{i}=\sum_{j=1}^{i}{a_{1,i}},suf_i=\sum_{j=i}^{n}{a_{2,i}}$。一组方案的权值即为 $\max\left\{pre_i+suf_i\right\}$。

先考虑固定两行数分别选的数后每行最终是怎么排的。

容易发现对于第一行，如果 $a_{1,i}>a_{1,i+1}$，将 $a_{1,i}$ 和 $a_{1,i+1}$ 交换后，在第 $i$ 列的权值变小其余不变，所以第一行一定是从小到大排列。第二行同理，为从大到小排列。

同时由于 $(pre_{i+1}+suf_{i+1})-(pre_i+suf_i)=a_{1,i+1}-a_{2,i}$ 且 $a_{1,i}$ 递增，$a_{2,i}$ 递减。所以对于一组方案，每列的权值构成一个下凸函数，最大权值即为 $pre_1+suf_1$ 或 $pre_n+suf_n$。

于是一组方案的权值为 $\max\left\{a_{1,1}+\sum{a_{2,i},a_{2,n}+\sum{a_{1,i}}}\right\}=a_{1,1}+a_{2,n}+\max\left\{\sum_{i=2}^{n}{a_{1,i}},\sum_{i=1}^{n-1}{a_{2,i}}\right\}$。

但是这样仍然做不了，因为 $a_{1,1}$ 和 $a_{2,n}$ 的权值不确定。

但是注意到 $a_{1,1}$ 和 $a_{2,n}$ 一定存在一个是全局最小值，而另一个经过调整一定可以变成次小值。所以题目转化为了要将剩余的 $2n-2$ 个数平均分成两组，使得这两组数的和的差的绝对值最小，bitset 优化背包即可。

时间复杂度：$O\left(\frac{n^2\sum a_{i,j}}{\omega}\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 30, kMaxS = 1.25e6 + 5;

int n;
int a[kMaxN * 2];
std::bitset<kMaxS> f[kMaxN * 2][kMaxN];
std::vector<int> v[2];

void print(int i, int j, int k) {
  if (i == 2) return;
  if (f[i - 1][j][k]) v[0].emplace_back(a[i]), print(i - 1, j, k);
  else v[1].emplace_back(a[i]), print(i - 1, j - 1, k - a[i]);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= 2 * n; ++i) std::cin >> a[i];
  std::sort(a + 1, a + 1 + 2 * n);
  int sum = std::accumulate(a + 3, a + 1 + 2 * n, 0);
  f[2][0][0] = 1;
  for (int i = 3; i <= 2 * n; ++i) {
    for (int j = 0; j <= std::min(i - 3, n - 1); ++j) {
      f[i][j] |= f[i - 1][j];
      f[i][j + 1] |= (f[i - 1][j] << a[i]);
    }
  }
  int ans = 1e9, s = 0;
  for (int i = 0; i <= sum; ++i) {
    if (f[2 * n][n - 1][i] && std::max(i, sum - i) < ans) {
      ans = std::max(i, sum - i);
      s = i;
    }
  }
  v[0] = {a[1]}, v[1] = {a[2]};
  print(2 * n, n - 1, s);
  std::sort(v[0].begin(), v[0].end());
  std::sort(v[1].begin(), v[1].end(), std::greater<>());
  for (auto x : v[0]) std::cout << x << ' ';
  std::cout << '\n';
  for (auto x : v[1]) std::cout << x << ' ';
  std::cout << '\n';
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