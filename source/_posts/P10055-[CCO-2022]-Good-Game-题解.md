---
title: P10055 [CCO 2022] Good Game 题解
date: 2025-08-28 09:00:00
---

## Description

Finn 正在玩一个叫做 Twos and Threes 的游戏。Twos and Threes 是一个单人游戏，它在一维棋盘上进行。在初始位置，有 $N$ 个方块排成一行，每个方块标有 $\tt{A}$ 或 $\tt{B}$。方块从左到右编号为 $1$ 到 $N$。Finn 可以进行以下操作：

- 选择 $2$ 或 $3$ 个连续的方块，它们有相同的标签，将它们从棋盘上移除并将剩余的方块连接起来，从左到右重新编号方块。

如果棋盘上的所有方块都被移除，Finn 就赢得了游戏。你的任务是帮助 Finn 确定一个赢得游戏的操作序列，或者确定游戏无法获胜。

$1 \leq N \leq 10^6$。

## Solution

容易发现每次选择 $2$ 或 $3$ 个删掉，等价于可以删掉任意长度 $\geq 2$ 的相同连续段，所以可以先把所有极长连续段缩起来，设长度为 $a_1,a_2,\ldots,a_m$。

显然一次操作一定是把一整个连续段删掉，否则不优。假设我们把第 $i$ 个连续段删掉，整个序列会变成 $a_1,a_2,\ldots,a_{i-2},a_{i-1}+a_{i+1},a_{i+2},\ldots,a_m$。由于我们只关心操作连续段的长度是否大于等于 $2$，所以把 $a_i$ 变为 $[a_i\geq 2]$ 后，一次操作就变为：$[...?1?...]\to [...1...]$，因为两个段合并后长度一定大于等于 $2$。

先考虑 $m=2k+1$ 的情况。

经过打表可以发现有解的充要条件是满足 $a_{k+1}=1$ 或者不存在一个长度为 $k$ 的 $0$ 连续段。

证明就考虑如果 $a_{k+1}=1$ 时，每次删掉正中间的段即可。否则如果存在一个长度为 $k$ 的 $0$ 连续段的话，设 $pre$ 为 $k+1$ 左边第一个 $1$，$nxt$ 为 $k+1$ 右边第一个 $1$。尽管 $[1,pre]$ 和 $[nxt,m]$ 全是 $1$，总共能消掉的 $0$ 的数量也为 $pre-1+m-nxt=m-1-(nxt-pre)\leq k-1$，所以一定不可能。（注：减一是因为操作开头或者末尾的 $1$ 没有意义）

如果不存在长度为 $k$ 的 $0$ 连续段，则我们一定可以通过一直删掉 $nxt$ 位置的连续段来把 $pre$ 移到正中间，然后一直操作 $pre$ 即可。

如果 $m=2k$，则最后一次操作一定是对 $11$ 进行操作，由于在之前一定没有边界上的操作，所以两个 $1$ 一定对应两个长度为奇数的区间，枚举一下是否存在这样的划分即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e6 + 5;

int n, m;
int a[kMaxN], pos[kMaxN], pre[kMaxN], nxt[kMaxN];
std::string str;
std::vector<std::pair<int, int>> vec;

void work(int x, int v) { assert(v == 2 || v == 3); vec.emplace_back(x, v); }

bool check(int l, int r) {
  if ((r - l) & 1) return 0;
  int mid = (l + r) >> 1;
  return a[mid] >= 2 || nxt[mid] - pre[mid] - 1 < (r - l) / 2;
}

void upd(int pos, int len) {
  assert(len >= 2);
  if (len & 1) work(pos, 3), len -= 3;
  for (; len;) work(pos, 2), len -= 2;
}

void solve(int l, int r) {
  static bool del[kMaxN] = {0};
  int mid = (l + r) >> 1, pre = ::pre[mid], nxt = ::nxt[mid];
  assert(pre >= l && nxt <= r && nxt - pre - 1 < (r - l) / 2);
  // std::cerr << l << ' ' << r << '\n';
  // for (int i = l; i <= r; ++i) std::cerr << a[i] << " \n"[i == r];
  for (int i = nxt, j = nxt, c = 1; c <= mid - pre; --i, ++j, ++c) {
    // std::cerr << "??? " << i << ' ' << j << ' ' << pos[i] << '\n';
    upd(pos[i], a[i] + (i != j) * a[j]), del[i] = del[j] = 1;
    if (c == mid - pre) a[i - 1] += a[j + 1], del[j + 1] = 1;
  }
  for (int i = pre, j = pre, c = 1; c <= pre - l + 1; --i, ++c) {
    for (; del[j]; ++j) {}
    assert(!del[i] && !del[j]);
    // std::cerr << "heige " << i << ' ' << j << '\n';
    upd(pos[i], a[i] + (i != j) * a[j]), del[j] = 1;
  }
}

void print() {
  std::cout << vec.size() << '\n';
  for (auto [x, v] : vec) std::cout << x << ' ' << v << '\n';
}

void dickdreamer() {
  std::cin >> n >> str; str = " " + str;
  for (int i = 1, lst = 0; i <= n; ++i) {
    if (i == n || str[i] != str[i + 1]) {
      a[++m] = i - lst, lst = i;
      pos[m] = pos[m - 1] + a[m - 1] + (m == 1);
      // std::cerr << pos[m] << '\n';
    }
  }
  for (int i = 1; i <= m; ++i) {
    if (a[i] >= 2) pre[i] = i;
    else pre[i] = pre[i - 1];
  }
  nxt[m + 1] = m + 1;
  for (int i = m; i; --i) {
    if (a[i] >= 2) nxt[i] = i;
    else nxt[i] = nxt[i + 1];
  }
  if (m & 1) {
    if (!check(1, m)) return void(std::cout << "-1\n");
    solve(1, m), print();
  } else {
    for (int i = 1; i < m; i += 2) {
      if (check(1, i) && check(i + 1, m)) {
        solve(i + 1, m), solve(1, i), print();
        return;
      }
    }
    std::cout << "-1\n";
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