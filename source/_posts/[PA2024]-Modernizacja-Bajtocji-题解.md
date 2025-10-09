---
title: [PA2024] Modernizacja Bajtocji 题解
date: 2024-11-04 10:15:00
---

## Description

Byteland 正在走向现代化。最新的政府项目旨在为那些没有电脑的村镇居民提供电脑。Byteasar 正在监督该计划中的一个村庄——Bytetown——的现代化进程，目前那里没有一个居民拥有电脑。

Bytetown 有 $n$ 个居民，为了简单起见，Byteasar 将他们用 $1$ 到 $n$ 的整数编号。最初没有一个居民拥有电脑。Byteasar 的任务是处理三种形式的事件：

- $\texttt{+}\ a_i\ b_i$：将一台电脑送给 Bytetown 的居民。然而，Byteasar 并不知道电脑是送给了编号为 $a_i$ 还是 $b_i$ 的居民。可能会出现 $a_i = b_i$ 的情况——在这种情况下，电脑肯定送给了编号为 $a_i$ 的居民。可以确定的是，电脑被送到了目前还没有电脑的居民手中。
- $\texttt{-}\ c_i$：编号为 $c_i$ 的居民的电脑坏了。可以肯定的是，该居民曾经拥有一台电脑（但现在不再拥有，因此将来可能会收到一台新电脑）。
- $\texttt{?}\ d_i$：Byteasar 需要（利用**迄今为止**获得的所有信息）确定编号为 $d_i$ 的居民：肯定有电脑，肯定没有电脑，还是不确定他是否有电脑。

请编写一个程序，帮助 Byteasar 回答所提出的问题！

注：在居民的电脑坏掉的前一刻，Byteasar 不一定可以确定这个居民是否有电脑。换句话说，在某居民电脑坏掉之前，不一定可以从之前的事件中确定他是否有电脑。

## Solution

首先没有 $-$ 操作是好做的，如果把 $+$ 操作的两个居民连一条边，则一定会连成树/基环树。对于一个连通块，如果大小为 $1$，则一定没电脑，否则如果为树，则全部无法确定，基环树则每个人都有。

加上 $-$ 操作后就把操作的点从其所在连通块删掉，原连通块如果为基环树则还是，否则如果删掉后只有一个点就看成单点，否则还是个树。

但是暴力删是做不了的，考虑把删点看成加点，即删掉点 $a$ 时，只将原连通块的状态更新但不删点，然后新建一个点 $a'$ 并把 $a$ 放到 $a'$ 上。

时间复杂度：$O((n+q)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1.3e6 + 5;
const char kC[] = "0?1";

int n, q, cnt;
int id[kMaxN], fa[kMaxN], sz[kMaxN], op[kMaxN];

// 0 : 单点，1 : 树，2 : 基环树

int find(int x) {
  return x == fa[x] ? x : fa[x] = find(fa[x]);
}

void unionn(int x, int y) {
  int fx = find(x), fy = find(y);
  if (fx == fy) op[fx] = 2;
  else fa[fx] = fy, op[fy] = ((op[fx] == 2 || op[fy] == 2) ? 2 : 1), sz[fy] += sz[fx];
}

void dickdreamer() {
  std::cin >> n >> q;
  cnt = n;
  for (int i = 1; i <= n; ++i) id[i] = fa[i] = i, sz[i] = 1;
  for (int i = 1; i <= q; ++i) {
    std::string s;
    int a, b;
    std::cin >> s;
    if (s[0] == '+') {
      std::cin >> a >> b;
      unionn(id[a], id[b]);
    } else if (s[0] == '-') {
      std::cin >> a;
      int f = find(id[a]);
      if (op[f] == 1 && --sz[f] == 1) op[f] = 0;
      id[a] = ++cnt;
      fa[cnt] = cnt, sz[cnt] = 1;
    } else {
      std::cin >> a;
      std::cout << kC[op[find(id[a])]];
    }
  }
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