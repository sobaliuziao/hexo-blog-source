---
title: [ABC311Ex] Many Illumination Plans 题解
date: 2025-08-25 20:12:00
---

## Description

给定一棵根节点为 $1$ 的有根树 $T$，树中共有 $N$ 个节点，编号从 $1$ 到 $N$。对于每个顶点 $i$（$2 \leq i \leq N$），其父节点是 $P_i$。每个节点都有两个非负整数属性，分别称为**美丽值**和**重量**。节点 $i$ 的美丽值为 $B_i$，重量为 $W_i$。此外，节点被涂上红色或蓝色，其颜色用整数 $C_i$ 表示：当 $C_i=0$ 时，节点 $i$ 为红色；当 $C_i=1$ 时，为蓝色。

对于每一个节点 $v$，定义函数 $F(v)$ 表示以下问题的解：

> 从树 $T$ 中提取出以 $v$ 为根的子树，称之为 $U$。对 $U$ 可以进行若干次以下操作（操作不会改变未删除节点的属性）：
>
> - 选择一个非根节点 $c$，设 $c$ 的父节点为 $p$。
> - 对于所有与 $c$ 相连的边：
>   - 假设边的另一端是 $u$，删除这条边，然后用一条以 $p$ 为父节点的新边连接 $p$ 和 $u$。
> - 删除节点 $c$ 和边 $p,c$。
>
> 最终的 $U$ 满足以下条件即为**好的有根树**：
>
> - $U$ 中相连节点的颜色不同。
> - 所有节点的重量总和不超过 $X$。
>
> 找出在所有可能的好的有根树中，节点美丽值总和的最大值。

请输出每个节点 $v$ 对应的 $F(v)$，即 $F(1), F(2), \dots, F(N)$。

$2\leq N\leq 200,0\leq X\leq 50000$。

## Solution

首先这题有个很简单的想法是设 $f_{u,s,0/1}$ 表示 $u$ 的子树，选的总重量为 $s$，最上面的那些点的颜色为 $0/1$ 的最大美丽度之和，暴力转移就是 $O(nX^2)$。

注意到如果按照上面的做法从下往上转移，则无法规避掉单次 $O(X^2)$ 的 $\min$ 加卷积，所以考虑从上往下 dp，将 dp 数组合并改为往 dp 中插入元素。

先考虑固定子树的根怎么做。

对于当前的点 $u$，由于儿子之间是平等的，所以有个很巧妙的想法是往 dfs 的状态里加入一个数组 $f$，表示这个子树里面的选择需要在 $f$ 的基础上更新，然后 dfs 的返回结果改成两个大小为 $x+1$ 的数组，分别表示 $u$ 的子树内选的最浅的点颜色为 $0/1$，且在 $f$ 的基础上更新的结果数组。

由于 $u$ 的儿子中有一个儿子可以只遍历一次，其余都需要两次，容易想到先遍历重儿子，得到只有重儿子子树的 $f_0$ 和 $f_1$。然后对于其它儿子 $v$，分别调用 $f_0\leftarrow \text{dfs}(v,f_0)[0],f_1\leftarrow\text{dfs}(v,f_1)[1]$。

这个东西的复杂度是 $\displaystyle T(sz_u)=T(sz_{son_u})+2\sum_{v\neq son_u}{T(sz_v)}+O(X)\leq 3\cdot T(sz_u/2)+O(X)=O(n^{\log_23}X)=O(n^{1.59}X)$。

暴力对于每个子树做这件事情就是 $O(n^{2.59}X)$，过不了。

---

考虑优化。

可以感受到上面的做法还是有些浪费，因为如果要求以 $u$ 为根的答案，这个需要用到 $son_u$ 从零开始的 dp 结果，暴力枚举根的化这个 $son_u$ 的 dp 结果就会算两次，很不优。

所以可以往 dfs 的状态中加一维 $op$ 表示是否需要从零开始计算 $u$ 子树里的答案，即 $\text{dfs}(u,f,0/1)$。

如果 $op=0$，则按照上面的做法转移即可。如果 $op=1$，则对于轻儿子全都从零开始计算，$u$ 不继承这些结果。然后 $u$ 先继承重儿子的结果，对于轻儿子和 $op=0$ 的做法一样。

可以证明时间复杂度仍然是 $O(n^{1.59}X)$。

时间复杂度：$O(n^{1.59}X)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 205;

int n, x;
int p[kMaxN], b[kMaxN], w[kMaxN], c[kMaxN], res[kMaxN];
int sz[kMaxN], wson[kMaxN];
std::vector<int> G[kMaxN];

inline void chkmax(int &x, int y) { x = (x > y ? x : y); }
inline void chkmin(int &x, int y) { x = (x < y ? x : y); }

void dfs1(int u) {
  sz[u] = 1;
  for (auto v : G[u]) {
    dfs1(v);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

std::array<std::vector<int>, 2> dfs2(int u, std::vector<int> now, bool op) {
  if (op) {
    for (auto v : G[u]) {
      if (v != wson[u]) dfs2(v, now, op);
    }
  }
  std::array<std::vector<int>, 2> f = {now, now};
  if (wson[u]) f = dfs2(wson[u], now, op);
  for (auto v : G[u]) {
    if (v == wson[u]) continue;
    f[0] = dfs2(v, f[0], 0)[0];
    f[1] = dfs2(v, f[1], 0)[1];
  }
  if (op) {
    for (int i = x; i >= w[u]; --i) {
      if (i >= w[u]) chkmax(res[u], f[c[u] ^ 1][i - w[u]] + b[u]);
    }
  }
  for (int i = x; i >= w[u]; --i) chkmax(f[c[u]][i], f[c[u] ^ 1][i - w[u]] + b[u]);
  return f;
}

void dickdreamer() {
  std::cin >> n >> x;
  for (int i = 2; i <= n; ++i) std::cin >> p[i], G[p[i]].emplace_back(i);
  for (int i = 1; i <= n; ++i) std::cin >> b[i] >> w[i] >> c[i];
  dfs1(1);
  std::vector<int> now(x + 1, -1e18);
  now[0] = 0;
  dfs2(1, now, 1);
  for (int i = 1; i <= n; ++i) std::cout << res[i] << '\n';
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