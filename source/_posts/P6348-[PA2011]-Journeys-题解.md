---
title: P6348 [PA2011] Journeys 题解
date: 2024-08-23 22:44:00
---

## Description

一个星球上有 $n$ 个国家和许多双向道路，国家用 $1\sim n$ 编号。

但是道路实在太多了，不能用通常的方法表示。于是我们以如下方式表示道路：$(a,b),(c,d)$ 表示，对于任意两个国家 $x,y$，如果 $a\le x\le b,c\le y\le d$，那么在 $x,y$ 之间有一条道路。

首都位于 $P$ 号国家。你想知道 $P$ 号国家到任意一个国家最少需要经过几条道路。保证 $P$ 号国家能到任意一个国家。

$1\le n\le 5\times 10^5$，$1\le m\le 10^5$，$1\le a\le b\le n$，$1\le c\le d\le n$。

## Solution

这里给出一个比较新颖的做法。

首先如果暴力建图显然会超时，而超时的原因是对于每个道路都两两建边过于浪费，因为对于一个 $[a,b]\to[c,d]$ 的道路，只需要让 $[a,b]$ 中 $dis$ 最小的那个位置去更新 $[c,d]$。

考虑类似 dijkstra 的过程，按 $dis$ 从小到大确定每个 $dis_x$，同时维护一个关于转移边的优先队列。假如当前确定了 $dis_x$，就暴力枚举所有还没有更新过的道路 $[a,b]\to[c,d]$，将 $[c,d,dis_x+1]$ 加入优先队列，表示可以让 $[c,d]$ 这个区间里的 $dis$ 更新为 $dis_x+1$。

由于这里是从小到大确定 $dis$ 的，所以每次取出队头的转移 $[l,r,v]$ 只需要暴力找到 $[l,r]$ 中还没有确定 $dis$ 的位置更新为 $v$，同时维护优先队列即可。

时间复杂度：$O\left(\left(n+m\right)\log^2n\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 5e5 + 5;

int n, m, s;
int l1[kMaxN], r1[kMaxN], l2[kMaxN], r2[kMaxN], dis[kMaxN];
std::set<int> st, t[kMaxN * 4];
std::queue<std::tuple<int, int, int>> q;

void update(int x, int l, int r, int id, int op) {
  int ql = l1[id], qr = r1[id];
  if (l > qr || r < ql) {
    return;
  } else if (l >= ql && r <= qr) {
    if (op == 1) t[x].emplace(id);
    else t[x].erase(id);
    return;
  }
  int mid = (l + r) >> 1;
  update(x << 1, l, mid, id, op), update(x << 1 | 1, mid + 1, r, id, op);
}

void getvec(int x, int l, int r, int ql, std::vector<int> &vec) {
  for (auto id : t[x]) vec.emplace_back(id);
  if (l == r) return;
  int mid = (l + r) >> 1;
  if (ql <= mid) getvec(x << 1, l, mid, ql, vec);
  else getvec(x << 1 | 1, mid + 1, r, ql, vec);
}

void upd(int x) {
  std::vector<int> vec;
  st.erase(x), getvec(1, 1, n, x, vec);
  for (auto id : vec) {
    update(1, 1, n, id, -1);
    q.emplace(l2[id], r2[id], dis[x] + 1);
  }
}

void dijkstra() {
  for (int i = 1; i <= n; ++i) st.emplace(i);
  for (int i = 1; i <= m; ++i) update(1, 1, n, i, 1);
  memset(dis, 0x3f, sizeof(dis));
  dis[s] = 0, upd(s);
  for (; !q.empty();) {
    auto [l, r, val] = q.front(); q.pop();
    for (auto it = st.lower_bound(l); it != st.end() && *it <= r; it = st.lower_bound(l)) {
      int u = *it;
      dis[u] = val, upd(u);
    }
  }
}

void dickdreamer() {
  std::cin >> n >> m >> s;
  for (int i = 1; i <= m; ++i) {
    std::cin >> l1[i] >> r1[i] >> l2[i] >> r2[i];
    l1[i + m] = l2[i], r1[i + m] = r2[i], l2[i + m] = l1[i], r2[i + m] = r1[i];
  }
  m *= 2;
  dijkstra();
  for (int i = 1; i <= n; ++i) std::cout << dis[i] << '\n';
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