---
title: CF516E Drazil and His Happy Friends 题解
date: 2024-07-23 11:29:00
---

## Description

有 $n$ 个男生 $m$ 个女生，编号分别为 $0 \sim n - 1$ 和 $0 \sim m - 1$。

有 $b$ 个男生和 $g$ 个女生是快乐的，其他人是不快乐的。

在第 $i$ 天，编号为 $i \bmod n$ 的男生和编号为 $i \bmod m$ 的女生会一起玩。

如果他们俩中有一个人是快乐的，则另一个人也会变快乐。

求至少要多少天所有人都会变快乐，或者判断不可能所有人都变快乐。

$n,m \leq 10^9$，$b,g \leq 10^5$。

## Solution

不妨设 $d=\gcd(n,m)$，那么$\bmod d$ 不相等的数一定不会相互感染，所以如果对于 $0\leq r<d$ 不存在初始时就快乐的人 $x$，使得 $x\bmod d=r$，就必然无解，否则一定有解。

所以如果 $d>b+g$ 则必然无解，因为至少存在一个余数没有任何数。这样 $d$ 就不大了，考虑对于每个余数求解。

假设余数为 $r$，那么把每个数 $x$ 变为 $(x-r)/d$，$n$ 变为 $n/d$，$m$ 变为 $m/d$，此时求出的答案 $\times d+r$ 就是这个余数的答案，并且此时 $n,m$ 互质，细节变少。

先考虑女生什么时候会全部快乐。

由于女生变快乐必须有男生的参与，所以考虑怎么把男生的参与去掉。

注意到一个女生 $i$ 在第 $k$ 轮变成快乐或者把对应的男生变快乐，那么 $k+n$ 轮女生 $(i+n)\bmod m$ 一定会快乐。所以可以说是女生 $i$ 用了 $n$ 的时间把女生 $(i+n)\bmod m$ 变快乐，这样就把男生的影响消除了，就只用考虑女生内部的影响。

不妨设 $f_i$ 表示女生 $i$ 第一次变快乐的时间，容易预处理出通过最开始就快乐的男生转移过来或者自己最开始就快乐的女生所用的时间。

那么转移就是 $f_{(i+n)\bmod m}\leftarrow f_i+n$，这是个最短路的形式。

所以可以源点向最开始就快乐的女生 $i$ 连长度为 $i$ 的边。对于最开始就快乐的男生 $j$，就让源点向女生 $j\bmod m$ 连长度为 $j$ 的边。然后 $i$ 向 $(i+n)\bmod m$ 连长度为 $n$ 的边。

跑最短路后不用考虑最开始就快乐的女生，否则答案会大。

但是这里点数很多，不好跑最短路。注意到 $n,m$ 互质，那么 $i\to (i+n)\bmod m$ 这类边把女生连成了一个大环，所以只需要把关键点找出来就可以快速求答案。

时间复杂度：$O\left(\left(b+g\right)\log\left(b+g\right)\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5, kInf = 1e18;

int n, m, x, y, B, G;
std::vector<int> b[kMaxN], g[kMaxN];

int exgcd(int a, int b, int &x, int &y) {
  if (!b) { x = 1, y = 0; return a; }
  int d = exgcd(b, a % b, y, x);
  y -= a / b * x;
  return d;
}

int solve(int n, int m, int x, std::vector<int> &b, std::vector<int> &g) {
  if (g.size() == m) return -1;
  std::vector<std::tuple<int, int, int>> vec;
  for (auto i : b) vec.emplace_back(i * x % m, 0, i);
  for (auto i : g) vec.emplace_back(i * x % m, 1, i);
  std::sort(vec.begin(), vec.end());
  vec.emplace_back(std::get<0>(vec.front()) + m, std::get<1>(vec.front()), std::get<2>(vec.front()));
  int ret = 0, dis = kInf;
  for (int i = 1; i < (int)vec.size(); ++i)
    dis = std::min(dis + n * (std::get<0>(vec[i]) - std::get<0>(vec[i - 1])), std::get<2>(vec[i]));
  for (int i = 0; i + 1 < (int)vec.size(); ++i) {
    if (i) dis = std::min(dis + n * (std::get<0>(vec[i]) - std::get<0>(vec[i - 1])), std::get<2>(vec[i]));
    if (std::get<0>(vec[i]) == std::get<0>(vec[i + 1])) continue;
    if (std::get<0>(vec[i + 1]) - std::get<0>(vec[i]) > 1) ret = std::max(ret, dis + n * (std::get<0>(vec[i + 1]) - std::get<0>(vec[i]) - 1));
    else if (!std::get<1>(vec[i])) ret = std::max(ret, dis);
  }
  return ret;
}

void dickdreamer() {
  std::cin >> n >> m >> B;
  int d = exgcd(n, m, x, y);
  if (d > 2e5) return void(std::cout << "-1\n");
  for (int i = 1; i <= B; ++i) {
    int x;
    std::cin >> x;
    b[x % d].emplace_back(x / d);
  }
  std::cin >> G;
  for (int i = 1; i <= G; ++i) {
    int x;
    std::cin >> x;
    g[x % d].emplace_back(x / d);
  }
  x = (x % m + m) % m, y = (y % n + n) % n;
  int ans = 0;
  for (int i = 0; i < d; ++i) {
    if (b[i].empty() && g[i].empty()) return void(std::cout << "-1\n");
    ans = std::max(ans, solve(n / d, m / d, x, b[i], g[i]) * d + i);
    ans = std::max(ans, solve(m / d, n / d, y, g[i], b[i]) * d + i);
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
  // std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```