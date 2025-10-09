---
title: 'CF1637H Minimize Inversions Number 题解'
date: 2025-03-25 16:00:00
---

## Description

给定一个 $1\sim n$ 的排列 $p$。 你可以进行下列操作正好一次：

- 选定 $p$ 的一个长度为 $k$ 的子序列，并将其按照相同的顺序移动到 $p$ 的最前面。

对于 $k=0,1,\ldots,n$，分别求出 $p$ 在操作后的最小逆序对数。

$1\leq n\leq 5\times 10^5$。

## Solution

考虑已经选定了 $q_1,q_2,\ldots,q_k$ 表示操作的数，怎么表示逆序对的**减少量**。

首先如果 $k=1$，则减少量为 $\displaystyle\sum_{j=1}^{i-1}{[p_j>p_i]}-\sum_{j=1}^{i-1}{[p_j<p_i]}$，设其为 $d_i$。

则对于 $k>1$ 的情况可以得到如下式子：

$$
\begin{aligned}
减少量=&\sum_{i=1}^{k}\left(\sum_{j=1}^{q_i-1}{[p_j>p_{q_i}]}-\sum_{j=1}^{q_i-1}{[p_j<p_{q_i}]}-\sum_{j=1}^{i-1}{[p_{q_j}>p_{q_i}]}+\sum_{j=1}^{i-1}{[p_{q_j}<p_{q_i}]}\right)\\
=&\binom{k}{2}+\sum_{i=1}^{k}d_{q_i}-2\sum_{i=1}^{k}\sum_{j=i+1}^{k}{[p_{q_i}>p_{q_j}]}
\end{aligned}
$$

所以现在只需要最大化 $\displaystyle\sum_{i=1}^{k}d_{q_i}-2\sum_{i=1}^{k}\sum_{j=i+1}^{k}{[p_{q_i}>p_{q_j}]}$ 了。

经过手玩会有一种感觉是如果存在 $i<j$ 且 $p_i>p_j$ 的话 $j$ 对 $[1,i-1]$ 和 $[j+1,n]$ 的贡献都比 $i$ 要优，而 $[i+1,j-1]$ 这部分二者是差不多的，所以可以猜测如果存在 $j$ 满足 $i<j,p_i>p_j$ 且 $i$ 选了 $j$ 没选就一定不优。

证明就考虑每次找到这样的 $(i,j)$ 中 $j-i$ 最小的一对，可以发现 $[i+1,j-1]$ 中不能有取值在 $[p_j+1,p_i-1]$ 内的，否则不管选不选都能和 $i$ 或者 $j$ 构成更小的对。同样的，取值在 $[p_i+1,n]$ 都不能选，$[1,p_j-1]$ 都选了。

设 $[i+1,j-1]$ 取值在 $[1,p_j-1]$ 的有 $cnt$ 个，那么式子里第二部分的增量至少为 $-2\cdot(-cnt)=2\cdot cnt$，同时 $d_j$ 比 $d_i$ 少算了至多 $[i+1,j-1]$ 之间的 $cnt$ 个数，所以将 $i$ 换成 $j$ 的变化量至少为 $2\cdot cnt-cnt=cnt\geq 0$，这说明我们每次选择这样的 $(i,j)$ 调整一定不劣。

最后一定能调整成猜测的情况。

那么此时选的数 $i$ 的贡献即为 $\displaystyle c_i=d_i-2\sum_{j=i+1}^{n}{[p_i>p_j]}$。

预处理出这个数组然后每次选择最大的 $k$ 个选即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;

const int kMaxN = 5e5 + 5;

int n;
int a[kMaxN], b[kMaxN];

struct BIT {
  int c[kMaxN];
  void clear() { std::fill_n(c + 1, n, 0); }
  void upd(int x, int v) {
    for (; x <= n; x += x & -x) c[x] += v;
  }
  int qry(int x) {
    int ret = 0;
    for (; x; x -= x & -x) ret += c[x];
    return ret;
  }
} bit;

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  i64 ans = 0;
  bit.clear();
  for (int i = 1; i <= n; ++i) {
    int cnt = i - 1 - bit.qry(a[i]);
    ans += cnt, b[i] = cnt - (i - 1 - cnt);
    bit.upd(a[i], 1);
  }
  bit.clear();
  for (int i = n; i; --i) {
    b[i] -= 2 * bit.qry(a[i]);
    bit.upd(a[i], 1);
  }
  std::sort(b + 1, b + 1 + n, std::greater<>());
  std::cout << ans << ' ';
  for (int i = 1; i <= n; ++i) {
    ans -= b[i];
    std::cout << ans - 1ll * i * (i - 1) / 2 << ' ';
  }
  std::cout << '\n';
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