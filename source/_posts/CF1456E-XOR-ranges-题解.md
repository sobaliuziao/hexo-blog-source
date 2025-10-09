---
title: 'CF1456E XOR-ranges 题解'
date: 2025-08-12 09:01:00
---

## Description

有 $n$ 个位数不超过 $K$ 的二进制变量 $x_1, x_2, \dots, x_n$，其中 $x_i$ 的取值范围是 $[l_i, r_i]$。

给出数列 $c_0, c_1, \dots, c_{K-1}$，并由此定义一个代价函数 $f(x)$：

$$
f(x) = \sum_{i=0}^{K-1} \left( \left\lfloor \frac{x}{2^i} \right\rfloor \bmod 2 \right) \cdot c_i
$$

换句话说，$f(x)$ 表示：如果 $x$ 的二进制第 $i$ 位是 $1$，则代价加上 $c_i$。

现在你需要确定每个变量的取值，使得：$\sum_{i=2}^{n} f(x_i \oplus x_{i-1})$ 最小；输出该最小值。

$2 \leq n \leq 50$，$1 \leq K \leq 50$，$0 \leq l_i \leq r_i < 2^K$，$0 \leq c_i \leq 10^{12}$。

## Solution

首先显然是按照数位从高到低进行区间 dp，但是直接不太好刻画，因为如果区间有很多位置卡了上下界就会不好转移。

设当前位是 $b$，注意到如果到 $b$ 位之后一个区间的数都没卡上下界了，那么把这个区间删掉就没有影响了。

考虑对上面这个东西进行 dp，即设 $f_{b,l,r,x,y}$ 表示从最高位到第 $b$ 位，$[l+1,r-1]$ 都被删掉了，$l$ 卡了下界/上界，$r$ 卡了下界/上界时 $[l,r]$ 这个区间贡献的最小值。

转移时就枚举有哪些 $[l+1,r-1]$ 的数在第 $b$ 位被删掉，直接区间 dp 计算贡献就是 $O(n^3k)$ 的，但是还有更好的写法。

就是考虑只枚举第一个在第 $b$ 位被删掉，假设是 $i$，那么 $[l,i]$ 的贡献就是 $f_{b+1,l,i,x,op}$，但是 $[i,r]$ 的贡献不是 $w_{b,i,r,x,y}+f_{b,i,r,op,y}$，因为这里 $i$ 第 $b$ 位需要取与 $op$ 对应的界异或 $1$ 的结果，转移就会存在问题。

容易发现可以加一维状态 $z$ 表示 $l$ 这一位需不需要异或 $1$。这样就能直接转移了，即：$f_{b,l,r,x,y,z}\leftarrow f_{b+1,l,i,x,op,0}+w_{b,l,i,x,op,z\oplus 1}+f_{b,i,r,op,y,1}$，注意这里如果 $op$ 对应 $l_i$，则需要满足 $l_i$ 第 $b$ 位是 $0$，同理转移 $r_i$ 就要这一位是 $1$。

不要忘记还有当前位没有新删掉点的转移：$f_{b,l,r,x,y,z}\leftarrow f_{b+1,l,r,x,y,0}+w_{b,l,r,x,y,z}$。

时间复杂度：$O(n^3k)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 55;

int n, k;
int l[kMaxN], r[kMaxN], c[kMaxN];
int f[kMaxN][kMaxN][kMaxN][2][2][2];
bool vis[kMaxN][kMaxN][kMaxN][2][2][2];

inline void chkmax(int &x, int y) { x = (x > y ? x : y); }
inline void chkmin(int &x, int y) { x = (x < y ? x : y); }

int cost(int b, int i, int j, int x, int y, int z) {
  if (!i || j == n + 1) return 0;
  int v1 = (!x ? l[i] : r[i]) >> b & 1;
  int v2 = (!y ? l[j] : r[j]) >> b & 1;
  return (v1 ^ v2 ^ z) * c[b];
}

int dp(int b, int l, int r, int x, int y, int z) {
  if (vis[b][l][r][x][y][z]) return f[b][l][r][x][y][z];
  else if (b == k) return r - l <= 1 ? 0 : 1e18;
  vis[b][l][r][x][y][z] = 1;
  int &ret = f[b][l][r][x][y][z];
  ret = 1e18;
  chkmin(ret, dp(b + 1, l, r, x, y, 0) + cost(b, l, r, x, y, z));
  for (int i = l + 1; i <= r - 1; ++i) {
    if ((::l[i] >> (b + 1)) == (::r[i] >> (b + 1))) continue;
    for (int op = 0; op < 2; ++op) {
      if (op == 0 && (::l[i] >> b & 1) || op == 1 && !(::r[i] >> b & 1)) continue;
      chkmin(ret, dp(b + 1, l, i, x, op, 0) + cost(b, l, i, x, op, z ^ 1) + dp(b, i, r, op, y, 1));
    }
  }
  return ret;
}

void dickdreamer() {
  std::cin >> n >> k; k += 2;
  for (int i = 1; i <= n; ++i) {
    std::cin >> l[i] >> r[i];
    l[i] = (l[i] << 2), r[i] = (r[i] << 2) | 3;
  }
  for (int i = 2; i < k; ++i) std::cin >> c[i];
  std::cout << dp(0, 0, n + 1, 0, 0, 0) << '\n';
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