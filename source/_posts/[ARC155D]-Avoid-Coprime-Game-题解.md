---
title: [ARC155D] Avoid Coprime Game 题解
date: 2024-02-25 09:51:00
---

## Description

非负整数 $x,y$ 的最大公约数记为 $\gcd(x,y)$，规定 $\gcd(x,0)=\gcd(0,x)=x$。

黑板上写了 $N$ 个整数 $A_1,A_2,...,A_N$，这 $N$ 个数的最大公约数是 $1$。Takahashi 和 Aoki 在玩游戏，有一个变量 $G$ 初值为 $0$，他们轮流进行以下操作：

> 从黑板上选择一个数 $a$，必须满足 $\gcd(a,G)\ne 1$，从黑板上擦掉这个数，并将 $G$ 的值改为 $\gcd(a,G)$。

Takahashi 先手，谁无法操作就输了，两人都采取最优策略。

请你对于 $i=1,2,..,N$ 分别判断，假如第一步 Takahashi 选择的数是 $A_i$，最后谁会获胜。

- $ 2\ \leq\ N\ \leq\ 2\ \times\ 10^5 $
- $ 2\ \leq\ A_i\ \leq\ 2\ \times\ 10^5 $

## Code

考虑对于必胜必败态进行 dp，不妨设当前 gcd 为 $G$，注意到删数很难用状态表示，但是发现删掉的数一定是当前 $G$ 的倍数，而其他 $G$ 的倍数与 $G$ 的 gcd 还是 $G$，并且不是 $G$ 的倍数的数一定没被删。

所以只要记录 $G$ 和当前轮数即可刻画这个状态，显然过不了。

---

先考虑每次 $G$ 一定会变小的情况，设 $f_i$ 表示 $G=i$ 是否必胜/必败，$cnt_i$ 表示 $i$ 的倍数的个数。

那么枚举一个 $j$ 使得 $\exists x,gcd(i,x)=j$，如果 $f_j$ 为必败，则 $f_i$ 必胜。如果所有 $j$ 全必胜，则 $f_i$ 必败。

但是这题 $G$ 不一定会变小，考虑什么情况下 $G$ 不会变小。

注意到如果存在一个 $f_j(j<i)$ 满足其是必败态，则当前操作一定最优。所以 $G$ 不变小当且仅当所有转移到的 $f_j$ 都必胜，则两人一定不停操作直到必须变小，即操作到 $cnt_i$ 轮的人会必胜。

所以只要记录一维状态表示当前操作了奇数/偶数轮，$f_{i,0/1}$ 表示当前 $G=i$，在这之前操作了偶数/奇数轮。

然后同样进行 dp，如果后继状态全必胜，则 $f_{i,1-(cnt_i\bmod 2)}$ 必胜。

时间复杂度：$O(V\log^2 V+N)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN], cnt[kMaxN], tmp[kMaxN];
bool f[kMaxN][2];
std::vector<int> d[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    ++cnt[a[i]];
  }
  for (int i = 2; i <= 2e5; ++i) {
    d[i].emplace_back(i);
    for (int j = 2 * i; j <= 2e5; j += i)
      cnt[i] += cnt[j], d[j].emplace_back(i);
  }
  for (int i = 2; i <= 2e5; ++i) {
    bool fl = 0;
    for (auto j : d[i]) tmp[j] = cnt[j];
    for (int j = (int)d[i].size() - 1; ~j; --j) {
      int x = d[i][j];
      if (x != i && tmp[x]) {
        if (!f[x][0]) f[i][1] = 1, fl = 1;
        if (!f[x][1]) f[i][0] = 1, fl = 1;
      }
      for (auto k : d[x]) tmp[k] -= tmp[x];
    }
    if (!fl) f[i][~cnt[i] & 1] = 1;
  }
  for (int i = 1; i <= n; ++i) {
    std::cout << (f[a[i]][1] ? "Aoki\n" : "Takahashi\n");
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