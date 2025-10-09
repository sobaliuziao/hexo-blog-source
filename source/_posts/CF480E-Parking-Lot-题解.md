---
title: 'CF480E Parking Lot 题解'
date: 2025-09-05 20:25:00
---

## Description

有一个 $n\times m$ 的矩阵，有一些点不能选。$k$ 次操作，每次都让一个点变成不可选，每次都问当前可选的最大正方形。

$n,m,k≤2000$。

## Solution

首先这类求一个矩阵内最大的连续正方形的题有个想法是设 $len_{i,j}$ 表示以 $(i,j)$ 为右端点的线段的最长长度，使得这个线段里没有任何点不能选。那么判断一个是否存在一个以 $(x,y)$ 为右上角的正方形边长为 $k$ 的条件即为 $\forall i\in[x,x+k-1],len_{i,y}\geq k$。

回到这题，注意到只有至多 $2000$ 次修改，同时一次修改只会改变同行内点的 $len$，所以可以暴力维护 $len$。

对于求答案则注意到每次修改后答案不会变大，所以可以维护一个 $v$ 表示目前的答案，每次修改后判断 $v$ 是否仍然合法，不合法就每次减一。同时记录 $p_{i,j}=[len_{i,j}\geq v]$，那么对于每列等价于求最长的 $1$ 连续段，直接线段树维护即可。

时间复杂度：$O(n^2\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e3 + 5;

int n, m, k, ans;
int x[kMaxN], y[kMaxN], res[kMaxN], len[kMaxN][kMaxN];
std::string str[kMaxN];
std::vector<std::pair<int16_t, int16_t>> pos[kMaxN];

struct Node {
  int16_t len, lx, rx, mx;
  Node(int16_t _len = 0, int16_t _lx = 0, int16_t _rx = 0, int16_t _mx = 0) :
    len(_len), lx(_lx), rx(_rx), mx(_mx) {}
  friend Node operator +(const Node &a, const Node &b) {
    static Node ret;
    ret.len = a.len + b.len;
    ret.mx = std::max<int16_t>({a.mx, b.mx, a.rx + b.lx});
    if (a.lx == a.len) ret.lx = a.len + b.lx;
    else ret.lx = a.lx;
    if (b.rx == b.len) ret.rx = b.len + a.rx;
    else ret.rx = b.rx;
    return ret;
  }
};

struct SGT {
  Node t[kMaxN * 4];
  void pushup(int x) { t[x] = t[x << 1] + t[x << 1 | 1]; }
  void build(int x, int l, int r) {
    if (l == r) return void(t[x] = {1, 0, 0, 0});
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }
  void update(int x, int l, int r, int ql, int v) {
    if (l == r) return void(t[x] = {1, v, v, v});
    int mid = (l + r) >> 1;
    if (ql <= mid) update(x << 1, l, mid, ql, v);
    else update(x << 1 | 1, mid + 1, r, ql, v);
    pushup(x);
  }
} sgt[kMaxN];

void prework() {
  ans = std::max(n, m) + 1;
  for (int i = 1; i <= m; ++i) sgt[i].build(1, 1, n);
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      if (str[i][j] == 'X') len[i][j] = 0;
      else len[i][j] = len[i][j - 1] + 1;
      pos[len[i][j]].emplace_back(i, j);
    }
  }
}

void upd(int x, int y, int v) {
  pos[len[x][y] = v].emplace_back(x, y);
  sgt[y].update(1, 1, n, x, v >= ans);
}

bool check() {
  for (int i = 1; i <= m; ++i)
    if (sgt[i].t[1].mx >= ans)
      return 1;
  return 0;
}

void fix() {
  for (; !check(); --ans) {
    assert(ans);
    // std::cerr << ans << '\n';
    // for (int i = 1; i <= m; ++i) std::cerr << sgt[i].t[1].mx << ' ';
    // std::cerr << '\n';
    for (auto [x, y] : pos[ans - 1])
      if (len[x][y] == ans - 1)
        sgt[y].update(1, 1, n, x, 1);
  }
}

void update(int x, int y) {
  for (int i = y; i <= m; ++i) {
    if (str[x][i] == 'X') break;
    upd(x, i, i - y);
  }
  str[x][y] = 'X', fix();
}

void dickdreamer() {
  std::cin >> n >> m >> k;
  for (int i = 1; i <= n; ++i) {
    std::cin >> str[i];
    str[i] = " " + str[i];
  }
  prework();
  for (int i = 1; i <= k; ++i) {
    std::cin >> x[i] >> y[i];
    if (str[x[i]][y[i]] != 'X') update(x[i], y[i]);
    std::cout << ans << '\n';
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