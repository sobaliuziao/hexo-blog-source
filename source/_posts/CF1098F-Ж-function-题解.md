---
title: CF1098F Ж-function 题解
date: 2025-04-21 11:53:00
---

## Description

给出一个长度为 $n$ 的字符串 $s$，定义函数 $f(l,r)$ 为 $s[l,r]$ 的每个后缀与 $s[l,r]$ 的 $\text{lcp}$ 之和。现在询问 $q$ 次，每次给出 $l,r$，请输出 $f(l,r)$。

$n,q\leq 2\times 10^5$。

## Solution

先将整个串翻转，题目变为求 $s[l,r]$ 的每个前缀与 $s[l,r]$ 的 $\text{lcs}$ 之和。

对当前串建 SAM，即求：$\displaystyle\sum_{i=l}^{r}{\min\{\text{len}[\text{LCA}(id_i,id_r)],i-l+1\}}$，其中 $id_i$ 表示 $s$ 长度为 $i$ 的前缀在 SAM 上对应的点。

考虑离线，并对 parent 树做重链剖分，计算 LCA 在某个重链上对答案的贡献。

先枚举重链，设 $anc_i$ 表示 $i$ 在这个重链上最近的祖先的 $\text{len}$。

那么如果 $id_i$ 和 $id_r$ 都在当前重链下，且属于不同的子树，则 $\text{len}[\text{LCA}(id_i,id_r)]=\min\{anc_{id_i},anc_{id_r}\}$。

设 $x=anc_{id_r}$，考虑枚举 $anc_{id_i}$ 和 $anc_x$ 的大小关系。

如果 $anc_{id_i}<anc_x$，则贡献为 $\min\{anc_{id_i},i-l+1\}=\begin{cases}anc_{id_i}\quad &l\leq i-anc_{id_i}+1\\i-l+1\quad&l>i-anc_{id_i}+1\end{cases}$，同时由于需要满足 $l\leq i\leq r$ 的限制，所以按照 **dfs 序**加入修改和询问后这是个三维偏序，cdq 分治即可。

如果 $anc_{id_i}\geq anc_x$，贡献为 $\min\{anc_{x},i-l+1\}=\begin{cases}anc_{x}\quad &l\leq i-anc_{x}+1\\i-l+1\quad&l>i-anc_{x}+1\end{cases}$，此时和 $i-anc_{id_i}+1$ 没有关系了，所以这部分是二维偏序，直接做。

注意需要保证修改和询问的点不在同一个重链上轻儿子的子树里，这里只需要在第一部分对于一个子树，先一起加入询问再加入修改，重链上的点特殊处理。第二部分先加入修改再加入询问。

时间复杂度：$O(n\log^3n)$，常数很小，可以过。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using i64 = int64_t;

const int kMaxN = 2e5 + 5, kMaxT = kMaxN * 2;

struct Node {
  int x, y, id;
} a[kMaxN * 4];

int n, q, tot, ta;
int id[kMaxN], len[kMaxT], L[kMaxN], R[kMaxN];
int p[kMaxT], sz[kMaxT], dfn[kMaxT], idx[kMaxT], wson[kMaxT];
bool vis[kMaxN];
i64 ans[kMaxN];
std::vector<int> G[kMaxT], qq[kMaxT], vec[kMaxT];
std::string str;

struct BIT {
  int c[kMaxN * 2];
  void upd(int x, int v) {
    for (x += n + 1; x <= 2 * n + 1; x += x & -x) c[x] += v;
  }
  int qry(int x) {
    int ret = 0;
    for (x += n + 1; x; x -= x & -x) ret += c[x];
    return ret;
  }
  int qry(int l, int r) { return l <= r ? qry(r) - qry(l - 1) : 0; }
} bit1, bit2, bit3;

struct SAM {
  int tot = 1, lst = 1, fa[kMaxT], len[kMaxT];
  std::array<int, 26> nxt[kMaxT];
  void ins(int c) {
    int p = lst, cur = ++tot;
    lst = cur;
    len[cur] = len[p] + 1;
    for (; p && !nxt[p][c]; p = fa[p]) nxt[p][c] = cur;
    int q = nxt[p][c];
    if (!p) {
      fa[cur] = 1;
    } else if (len[q] == len[p] + 1) {
      fa[cur] = q;
    } else {
      int r = ++tot;
      len[r] = len[p] + 1, fa[r] = fa[q], nxt[r] = nxt[q];
      fa[q] = fa[cur] = r;
      for (; p && nxt[p][c] == q; p = fa[p]) nxt[p][c] = r;
    }
  }
  void build() {
    ::tot = tot;
    for (int i = 2; i <= tot; ++i) {
      ::len[i] = len[i];
      G[fa[i]].emplace_back(i);
    }
  }
} sam;

void buildsam() {
  for (int i = 1; i <= n; ++i) sam.ins(str[i] - 'a');
  sam.build();
  id[0] = 1;
  for (int i = 1; i <= n; ++i) {
    id[i] = sam.nxt[id[i - 1]][str[i] - 'a'];
    vec[id[i]].emplace_back(i);
  }
}

void dfs1(int u, int fa) {
  static int cnt = 0;
  p[u] = fa, idx[dfn[u] = ++cnt] = u, sz[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

void dfs2(int u, int fa, int anc, bool op = 0) {
  if (!op) {  // 添加修改
    for (auto i : vec[u]) a[++ta] = {anc, i, 0};
  } else {  // 添加询问
    for (auto i : qq[u]) a[++ta] = {anc, R[i], i};
  }
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs2(v, u, anc, op);
  }
}

void prework() { dfs1(1, 0); }

void solve1(int l = 1, int r = ta) {
  if (l == r) return;
  int mid = (l + r) >> 1;
  solve1(l, mid), solve1(mid + 1, r);
  std::sort(a + l, a + 1 + mid, [&](Node a, Node b) { return a.y < b.y; });
  std::sort(a + 1 + mid, a + 1 + r, [&](Node a, Node b) { return a.y < b.y; });
  int p = l;
  for (int i = mid + 1; i <= r; ++i) {
    if (!a[i].id) continue;
    for (; p <= mid && a[p].y <= a[i].y; ++p) {
      if (a[p].id) continue;
      bit1.upd(a[p].y - a[p].x + 1, a[p].x);  // anc[id[i]]
      bit2.upd(a[p].y - a[p].x + 1, a[p].y);  // i
      bit3.upd(a[p].y - a[p].x + 1, 1);       // 1
    }
    int id = a[i].id;
    ans[id] += bit1.qry(L[id], n) + bit2.qry(-n, L[id] - 1) -
               (L[id] - 1) * bit3.qry(-n, L[id] - 1);
  }
  for (int i = l; i < p; ++i) {
    if (a[i].id) continue;
    bit1.upd(a[i].y - a[i].x + 1, -a[i].x);  // anc[id[i]]
    bit2.upd(a[i].y - a[i].x + 1, -a[i].y);  // i
    bit3.upd(a[i].y - a[i].x + 1, -1);       // 1
  }
  // for (int i = 1; i <= ta; ++i) {
  //   if (a[i].id) continue;
  //   for (int j = i + 1; j <= ta; ++j) {
  //     if (!a[j].id) continue;
  //     int id = a[j].id;
  //     if (a[i].y <= a[j].y) {
  //       ans[id] += std::min({a[i].y - L[id] + 1, a[i].x, a[j].x});
  //       // std::cerr << "!!! " << a[i].y << ' ' << a[i].x << '\n';
  //     }
  //   }
  // }
}
// dbba
void solve2() {
  for (int i = ta; i; --i) {
    if (!a[i].id) {
      bit1.upd(a[i].y, a[i].y);
      bit2.upd(a[i].y, 1);
    } else {
      int id = a[i].id;
      ans[id] +=
          a[i].x * bit2.qry(L[id] + a[i].x - 1, a[i].y) +
          bit1.qry(1, std::min(L[id] + a[i].x - 2, a[i].y)) -
          (L[id] - 1) * bit2.qry(1, std::min(L[id] + a[i].x - 2, a[i].y));
    }
  }
  for (int i = 1; i <= ta; ++i) {
    if (!a[i].id) {
      bit1.upd(a[i].y, -a[i].y);
      bit2.upd(a[i].y, -1);
    }
  }
  // for (int i = 1; i <= ta; ++i) {
  //   if (!a[i].id) continue;
  //   for (int j = i + 1; j <= ta; ++j) {
  //     if (a[j].id) continue;
  //     int id = a[i].id;
  //     if (a[j].y <= a[i].y) {
  //       ans[id] += std::min(a[j].y - L[id] + 1, a[i].x);
  //       // std::cerr << "??? " << a[j].y << ' ' << a[i].x << '\n';
  //     }
  //   }
  // }
}

void solve(int t) {
  ta = 0;
  for (int u = t; u; u = wson[u]) {
    for (auto i : qq[u]) a[++ta] = {len[u], R[i], i};
    for (auto i : vec[u]) a[++ta] = {len[u], i, 0};
    for (auto v : G[u]) {
      if (v == p[u] || v == wson[u]) continue;
      dfs2(v, u, len[u], 1), dfs2(v, u, len[u], 0);
    }
  }
  solve1();
  ta = 0;
  for (int u = t; u; u = wson[u]) {
    for (auto i : qq[u]) a[++ta] = {len[u], R[i], i};
    for (auto i : vec[u]) a[++ta] = {len[u], i, 0};
    for (auto v : G[u]) {
      if (v == p[u] || v == wson[u]) continue;
      dfs2(v, u, len[u], 0), dfs2(v, u, len[u], 1);
    }
  }
  solve2();
}

void dickdreamer() {
  std::cin >> str;
  std::reverse(str.begin(), str.end());
  n = str.size(), str = " " + str;
  buildsam(), prework();
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    std::cin >> L[i] >> R[i];
    L[i] = n + 1 - L[i], R[i] = n + 1 - R[i];
    std::swap(L[i], R[i]);
    qq[id[R[i]]].emplace_back(i);
  }
  // std::cerr << len[id[1]] << ' ' << len[id[2]] << '\n';
  for (int i = 1; i <= tot; ++i)
    if (i != wson[p[i]]) solve(i);
  for (int i = 1; i <= q; ++i) {
    if (L[i] > 1) ans[i] += 1ll * (L[i] - 2) * (L[i] - 1) / 2;
    std::cout << ans[i] << '\n';
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