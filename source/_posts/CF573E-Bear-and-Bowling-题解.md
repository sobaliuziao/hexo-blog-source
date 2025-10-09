---
title: CF573E Bear and Bowling 题解
date: 2024-08-06 21:24:00
---

## Description

- 给定一个长度为 $n$ 的序列 $a_{1\dots n}$。
- 你要求一个 $a$ 的子序列 $b_{1\dots m}$（可以为空），使得 $\sum_{i=1}^m ib_i$ 的值最大。
- $n \le 10^5$，$|a_i| \le 10^7$。

## Solution

有一个显然的 dp 是设 $f_{i,j}$ 表示前 $i$ 个数，选 $j$ 个数的最大值，转移即为：$f_{i,j}=\max\left\{f_{i-1,j},f_{i-1,j-1}+j\cdot a_i\right\}$，由于这题时限很大并且 $n$ 很小，所以这个能过。。。

考虑优化。

有一个结论是对于每个 $i$，都存在一个分界点 $k_i$，使得对于 $\forall j<k_i$，$f_{i,j}=f_{i-1,j}$，对于 $j\geq k_i$，$f_{i,j}=f_{i-1,j-1}+j\cdot a_i$。

证明就考虑设 $g_{i,j}=f_{i,j}-f_{i,j-1}$，那么 $f_{i,j}=f_{i-1,j}$ 的充分必要条件为 $f_{i-1,j}\geq f_{i-1,j-1}+j\cdot a_i$，即 $\frac{g_{i-1,j}}{j}\geq a_i$。

通过观察可以发现 $\frac{g_{i,j}}{j}$ 对于 $j$ 单调不增，那么不妨假设 $\frac{g_{i-1,j}}{j}$ 单调不增，考虑归纳证明 $g_i$ 也满足条件。

设 $k$ 为满足 $\frac{g_{i-1,j}}{j}<a_i$ 的最小的 $j$，则对于 $j\in [0,k-1]$，$g_{i,j}=g_{i-1,j}$。同时 $g_{i,k}$ 变为 $k\cdot a_i$，所以 $\frac{g_{i,k}}{k}=a_i\leq \frac{g_{i,k-1}}{k-1}$。

对于 $j>k$，$g_{i,j}=g_{i-1,j-1}+a_i$，所以对于 $j>k$ 满足 $\frac{g_{i,j}}{j}\geq \frac{g_{i,j+1}}{j+1}$ 的条件为：

$$
\begin{aligned}
\frac{g_{i-1,j-1}+a_i}{j}&\geq\frac{g_{i-1,j}+a_i}{j+1}\\
g_{i-1,j-1}&\geq\frac{j}{j+1}\cdot g_{i-1,j}-\frac{1}{j+1}\cdot a_i\\
g_{i-1,j-1}-\left(\frac{j}{j+1}\cdot g_{i-1,j}-\frac{1}{j+1}\cdot a_i\right)&\geq 0\\
\end{aligned}
$$

又因为：

$$
\begin{aligned}
LHS\geq&\frac{j-1}{j}\cdot g_{i-1,j}-\frac{j}{j+1}\cdot g_{i-1,j}+\frac{1}{j+1}\cdot a_i\\
=&\frac{j\cdot a_i-g_{i-1,j}}{j(j+1)}\\
\geq& 0
\end{aligned}
$$

所以结论得证。

然后就可以从前往后枚举 $a_i$，维护 $g$ 数组，每次相当于是在某个位置插入和将某个后缀区间加某个数，并且需要快速找到分界点，可以用平衡树维护。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n;
int64_t a[kMaxN];

struct FHQTreap {
  int tot = 0, rt, ch[kMaxN][2], rd[kMaxN], sz[kMaxN];
  int64_t val[kMaxN], rnk[kMaxN], tag1[kMaxN], tag2[kMaxN];
  std::mt19937 rnd;

  int newnode(int64_t x, int64_t y) {
    val[++tot] = x, rnk[tot] = y;
    ch[tot][0] = ch[tot][1] = tag1[tot] = tag2[tot] = 0, rd[tot] = rnd();
    sz[tot] = 1;
    return tot;
  }

  FHQTreap() {
    tot = 0, rnd.seed(std::random_device{}());
    rt = newnode(-1e18, 1);
  }

  void pushup(int x) {
    sz[x] = sz[ch[x][0]] + sz[ch[x][1]] + 1;
  }

  void addtag(int x, int64_t v1, int64_t v2) {
    val[x] += v1, rnk[x] += v2, tag1[x] += v1, tag2[x] += v2;
  }

  void pushdown(int x) {
    if (ch[x][0]) addtag(ch[x][0], tag1[x], tag2[x]);
    if (ch[x][1]) addtag(ch[x][1], tag1[x], tag2[x]);
    tag1[x] = tag2[x] = 0;
  }

  int merge(int x, int y) {
    if (!x || !y) return x + y;
    pushdown(x), pushdown(y);
    if (rd[x] < rd[y]) {
      ch[x][1] = merge(ch[x][1], y), pushup(x);
      return x;
    } else {
      ch[y][0] = merge(x, ch[y][0]), pushup(y);
      return y;
    }
  }

  void split(int x, int v, int &a, int &b) { // a : >= v, b : < v
    if (!x) return void(a = b = 0);
    pushdown(x);
    if (val[x] >= rnk[x] * v) {
      a = x, split(ch[x][1], v, ch[a][1], b);
    } else {
      b = x, split(ch[x][0], v, a, ch[b][0]);
    }
    pushup(x);
  }

  void ins(int64_t x) {
    int a, b;
    split(rt, x, a, b);
    if (b) addtag(b, x, 1);
    rt = merge(merge(a, newnode(x * (sz[a] + 1), sz[a] + 1)), b);
  }

  int64_t getval(int x) {
    if (!x) return 0;
    pushdown(x);
    int64_t ret = std::max<int64_t>(val[x], 0);
    return ret + getval(ch[x][0]) + getval(ch[x][1]);
  }
} t;

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    t.ins(a[i]);
  }
  std::cout << t.getval(t.rt) << '\n';
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