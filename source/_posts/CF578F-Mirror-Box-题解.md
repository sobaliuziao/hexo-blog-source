---
title: 'CF578F Mirror Box 题解'
date: 2024-08-22 21:12:00
---

## Description

在一个 $n \times m$ 的网格中，每个格子里都有一个呈 `\` 或 `/` 状的镜子。

一个合法的网格需要满足**从任意一个边界段垂直射进网格中，光线会从相邻的边界段射出**，同时**网格中的每一段都被至少一条光线穿透**。

现在网格中有 $k$ 个位置的镜子形状不确定，求有多少种合法的网格。

$n,m \le 100$，$k \le 200$，答案对质数 $p$ 取模。

## Solution

考虑一个合法的方案是什么样的。

容易发现一个 `\` 或者 `/` 可以看作连接网络上格点的边，并且对这些格点黑白染色后每条边一定连接的是同色点。

有个结论是只要图中的黑点或者白点构成一颗生成树就合法。证明就考虑如果存在环的话，环内的网格边一定不可能被穿透到，也就是不满足第二条要求。而黑点和白点如果都不为连通块，感性理解一下会发现一定存在一段会射到别的地方去。并且构成生成树时一对相邻的段一定能够沿着树上的路径构成的边反射到对面。

由于确定了一个颜色的生成树时就能唯一确定另一个颜色的方案，所以只需要分别求出两种颜色的生成树数再加起来即可。

时间复杂度：$O\left(nm\log\left(nm\right)+k^3\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 205;

int n, m, k, mod;
int fa[kMaxN * kMaxN];
std::string s[kMaxN];

int getid(int x, int y) { return (x - 1) * (m + 1) + y; }
int getpos(std::vector<int> &v, int x) {
  return std::lower_bound(v.begin(), v.end(), x) - v.begin() + 1;
}

int find(int x) { return x == fa[x] ? x : fa[x] = find(fa[x]); }
bool unionn(int x, int y) {
  int fx = find(x), fy = find(y);
  if (fx != fy) return fa[fx] = fy, 1;
  else return 0;
}

constexpr int qpow(int bs, int64_t idx = mod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % mod)
    if (idx & 1)
      ret = (int64_t)ret * bs % mod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= mod ? x + y - mod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + mod); }
inline void inc(int &x, int y) { (x += y) >= mod ? x -= mod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += mod : x; }

struct Matrix {
  int n, a[kMaxN][kMaxN];

  void set(int _n) { n = _n; }
  void add(int u, int v) { inc(a[u][u], 1), inc(a[v][v], 1), dec(a[u][v], 1), dec(a[v][u], 1); }

  int getdet() {
    if (n > k + 1) return 0;
    int ret = 1;
    for (int i = 1; i < n; ++i) {
      if (!a[i][i]) {
        for (int j = i + 1; j <= n; ++j) {
          if (a[j][i]) {
            std::swap(a[i], a[j]), ret = sub(0, ret);
            break;
          }
        }
      }
      ret = 1ll * ret * a[i][i] % mod;
      for (int j = i + 1; j <= n; ++j) {
        int d = 1ll * a[j][i] * qpow(a[i][i]) % mod;
        for (int k = i; k <= n; ++k)
          dec(a[j][k], 1ll * a[i][k] * d % mod);
      }
    }
    return ret;
  }
} a[2];

void dickdreamer() {
  std::cin >> n >> m >> mod;
  for (int i = 1; i <= (n + 1) * (m + 1); ++i)
    fa[i] = i;
  for (int i = 1; i <= n; ++i) {
    std::cin >> s[i];
    s[i] = " " + s[i];
    for (int j = 1; j <= m; ++j) {
      if (s[i][j] == '/') {
        if (!unionn(getid(i, j + 1), getid(i + 1, j)))
          return void(std::cout << "0\n");
      } else if (s[i][j] == '\\') {
        if (!unionn(getid(i, j), getid(i + 1, j + 1)))
          return void(std::cout << "0\n");
      } else {
        ++k;
      }
    }
  }
  std::vector<int> v[2];
  for (int i = 1; i <= (n + 1) * (m + 1); ++i) {
    if (find(i) == i) {
      v[((i - 1) / (m + 1) + (i - 1) % (m + 1)) & 1].emplace_back(i);
    }
  }
  a[0].set(v[0].size()), a[1].set(v[1].size());
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      if (s[i][j] == '*') {
        int o = (i + j) & 1;
        if ((int)v[o].size() <= k + 1) a[o].add(getpos(v[o], find(getid(i, j))), getpos(v[o], find(getid(i + 1, j + 1))));
        if ((int)v[o ^ 1].size() <= k + 1) a[o ^ 1].add(getpos(v[o ^ 1], find(getid(i + 1, j))), getpos(v[o ^ 1], find(getid(i, j + 1))));
      }
    }
  }
  std::cout << add(a[0].getdet(), a[1].getdet()) << '\n';
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