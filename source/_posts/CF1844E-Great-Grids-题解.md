---
title: 'CF1844E Great Grids 题解'
date: 2023-10-07 20:35:00
---

## Description

定义一个矩形 $a$ 是好的，当且仅当其满足以下条件：

1. 矩形中每一个元素 $x$ 都为 $A,B,C$ 其中之一
2. 每一个 $2\times 2$ 的子矩形都必须包含三个不同的字符
3.  共用一条边的两个元素不相等

给定 $k$ 个限制条件，限制条件分为两类：

1. $(x,x+1,y,y+1)$，限制 $a[x,y]= a[x+1,y+1]$
2. $(x,x+1,y,y-1)$，限制 $a[x,y]= a[x+1,y-1]$ 

求满足所有条件的矩形是否存在。

[link](https://codeforces.com/problemset/problem/1844/E)

## Solution

先不考虑限制条件，思考一个 $2\times 2$ 的子矩形怎样才能包含三个不同的字符。

不妨设左上角为 $0$，那么这个子矩形一定长这样：

$$
\begin{bmatrix}
0\ \ 1\\
1\ \ 2
\end{bmatrix}

\begin{bmatrix}
0\ \ 2\\
2\ \ 1
\end{bmatrix}

\begin{bmatrix}
0\ \ 1\\
2\ \ 0
\end{bmatrix}

\begin{bmatrix}
0\ \ 2\\
1\ \ 0
\end{bmatrix}
$$

观察到左上角+右下角=右上角+左下角，所以 $a_{x,y}+a_{x+1,y+1}=a_{x,y+1}+a_{x+1,y}$，得到：$a_{x,y+1}-a_{x,y}=a_{x+1,y+1}-a_{x+1}{y}$ 且 $a_{x+1,y}-a_{x,y}=a_{x+1,y+1}-a_{x,y+1}$。

所以每行和每列的差都相等，设 $b_{x}=a_{x+1,y}-a_{x,y},c_{y}=a_{x,y+1}-a_{x,y}$。

由于相邻的不能相等，所以 $b_x$ 和 $c_y$ 只能为 $1,2$。

---

然后考虑那个限制条件。

对于限制 1，会发现 $a_{x,y}=a_{x+1,y},a_{x+1,y}\neq a_{x,y+1}\neq a_{x,y}$，所以 $b_x\neq c_y$。

对于限制 2，满足 $a_{x,y+1}=a_{x+1,y},a_{x,y}\neq a_{x+1,y+1}\neq a_{x,y+1}$，所以 $b_x= c_y$。

容易发现存在 $b,c$ 数组满足所有的条件，就是原题能构造出矩形的充要条件。

然后跑二分图染色即可。

时间复杂度：$O(n+m+k)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxK = 4e3 + 5;

int n, m, k;
bool fl;
int col[kMaxK], xx[kMaxK], yx[kMaxK], xy[kMaxK], yy[kMaxK];
std::vector<std::pair<int, int>> G[kMaxK];

void dfs(int u) {
  for (auto [v, w] : G[u]) {
    if (~col[v] && col[v] != (col[u] ^ w)) {
      fl = 0;
    } else if (!~col[v]) {
      col[v] = col[u] ^ w;
      dfs(v);
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m >> k;
  for (int i = 1; i <= n + m; ++i) {
    G[i].clear();
    col[i] = -1;
  }
  for (int i = 1; i <= k; ++i) {
    std::cin >> xx[i] >> yx[i] >> xy[i] >> yy[i];
    if (yy[i] == yx[i] - 1) {
      G[xx[i]].emplace_back(yy[i] + n, 0);
      G[yy[i] + n].emplace_back(xx[i], 0);
    } else {
      G[xx[i]].emplace_back(yx[i] + n, 1);
      G[yx[i] + n].emplace_back(xx[i], 1);
    }
  }
  fl = 1;
  for (int i = 1; i <= n + m; ++i)
    if (!~col[i]) col[i] = 0, dfs(i);
  std::cout << (fl ? "YES\n" : "NO\n");
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