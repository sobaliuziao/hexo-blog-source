---
title: CF2124I Lexicographic Partition 题解
date: 2025-07-21 19:53:00
---

## Description

给定一个数组 $a$，定义函数 $f(a)$ 如下：

设 $k$ 是一个满足 $1 \leq k \leq n$ 的整数。
将数组 $a$ 分成 $k$ 个子数组 $s_1, s_2, \ldots, s_k$，使得 $s_1 + s_2 + \cdots + s_k = a$，这里的 $+$ 表示数组连接操作。

构造一个新的数组 $b$，初始为空。对于每个 $i = 1$ 到 $k$，将子数组 $s_i$ 的**最小值**添加到 $b$ 的末尾。

在所有可能的 $k$ 和划分方式中，定义 $f(a)$ 为使得生成的 $b$ 字典序最大的那个 $k$。

现在给定一个长度为 $n$ 的整数序列 $x_1, x_2, \ldots, x_n$，请判断是否**存在一个排列** $a$，使得对于每个 $1 \leq i \leq n$，都有 $f([a_1, a_2, \ldots, a_i]) = x_i$。

如果存在这样的排列 $a$，请输出其中一种可能的结果（如果有多种，任选一种输出即可）。

$n\leq 2\times 10^5$。

## Solution

首先考虑给定 $a$ 数组，怎么求这个数组的函数值。

考虑从前往后确定每个区间的左右端点，假设当前左端点在 $i$，那么右端点 $j$ 一定需要满足 $a_i,a_{i+1},\ldots,a_j$ 都大于等于 $a_i$，否则从这一位就不优。

同时需要让下一位尽可能优，就一定要最大化 $a_{j+1}$，设 $k$ 为最大的 $k$ 使得 $a_i\sim a_k$ 都大于等于 $a_i$，则下一个区间的左端点为 $a_i\sim a_k$ 的最大值。如果 $k=i$，则这个左端点是 $i+1$。

回到原问题。

容易发现这个跳的过程类似于给每个点找到唯一的父亲，显然 $i$ 的父亲是 $i$ 左边第一个 $x_j=x_i-1$ 的 $j$，因为跳前 $x_i-1$ 步时每次肯定是能往后跳就尽量往后跳，所以第 $x_i-1$ 步是一定跳到了 $j$，最后一步为 $i$。如果找不到这样的 $j$ 就无解。

然后有个引理，是一个合法序列 $x$ 建出来的树，一定满足每个子树构成一段区间。证明就考虑对于一个节点 $x$，如果已经证明了 $x$ 的子树是一个区间，然后去归纳证明 $x$ 的每个儿子的子树也是区间。

具体地，如果 $x$ 只有 $1$ 个儿子，则这个儿子一定是 $x+1$，显然还是区间。如果有大于等于 $2$ 个儿子，那么这些儿子的权值一定按升序排列，如果存在一条 $u\to v$ 且 $u$ 和 $v$ 对应的祖先不相同，则根据能往后跳就往后跳的原则，前面从 $x$ 开始时一定是先跳 $x$ 的儿子，再进入子树区间，不再出来。这里就矛盾了。

同时还有个无解条件是如果存在一个点有至少两个儿子，且存在一个儿子又有至少两个儿子。这个形式可以看成存在一个 $[1,2,2,3,3]$ 的子序列，显然 $a_1<a_2<a_3$ 且 $a_3<a_4<a_5$，这两个不等式可以联立起来，导致 $4,5$ 可以被 $1$ 跳到。

可以证明如果满足上述所有的条件，就一定有解。

---

构造就考虑对于子树递归构造，让每个子树的值域也构成一段区间。

设当前节点为 $x$，值域区间为 $[l,r]$。

这里钦定如果 $x$ 只有一个儿子，就让 $a_x$ 是子树最大值，否则让 $x$ 是子树最小值。

首先如果 $x$ 只有一个儿子，那么这个儿子一定是 $x+1$，递归儿子的子树，同时把值域区间设为 $[l,r-1]$ 即可。

如果 $x$ 有大于等于两个儿子，就按照儿子的编号大小，给儿子 $y$ 分配一个大小为 $sz_y$ 的区间。根据引理，$y$ 只有至多一个儿子，所以 $a_y$ 一定是子树最大值，这样就巧妙地保证了 $y$ 子树里除去 $y$ 的节点一定不能被 $x$ 一步跳到。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int x[kMaxN], sz[kMaxN], mx[kMaxN], res[kMaxN];
std::vector<int> G[kMaxN];

bool solve(int l, int r, int a, int b) {
  if (l == r) return res[l] = a, 1;
  if (G[l].size() == 1) {
    res[l] = b;
    return solve(l + 1, r, a, b - 1);
  } else {
    for (auto i : G[l])
      if (G[i].size() > 1)
        return 0;
    res[l] = a++;
    for (auto i : G[l]) {
      if (!solve(i, i + sz[i] - 1, a, a + sz[i] - 1)) return 0;
      a += sz[i];
    }
    return 1;
  }
}

void dickdreamer() {
  static int lst[kMaxN];
  std::cin >> n;
  for (int i = 0; i <= n; ++i) G[i].clear(), res[i] = lst[i] = 0;
  for (int i = 1; i <= n; ++i) std::cin >> x[i];
  lst[x[1]] = 1;
  for (int i = 2; i <= n; ++i) {
    if (!lst[x[i] - 1]) return void(std::cout << "NO\n");
    G[lst[x[i] - 1]].emplace_back(i);
    lst[x[i]] = i;
  }
  for (int i = n; i; --i) {
    sz[i] = 1, mx[i] = i;
    for (auto j : G[i]) sz[i] += sz[j], mx[i] = std::max(mx[i], mx[j]);
    if (mx[i] - i + 1 != sz[i]) return void(std::cout << "NO\n");
  }
  if (!solve(1, n, 1, n)) return void(std::cout << "NO\n");
  std::cout << "YES\n";
  for (int i = 1; i <= n; ++i) std::cout << res[i] << " \n"[i == n];
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