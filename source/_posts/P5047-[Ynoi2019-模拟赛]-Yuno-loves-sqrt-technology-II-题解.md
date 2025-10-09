---
title: P5047 [Ynoi2019 模拟赛] Yuno loves sqrt technology II 题解
date: 2023-09-29 21:46:00
---

## Description

给你一个长为 $n$ 的**排列**，$m$ 次询问，每次查询一个区间的逆序对数，强制在线。

[link](https://www.luogu.com.cn/problem/P5046)

$1\leq n,m\leq 10^5$。

## Solution

考虑分块。

首先如果 $l,r$ 在同一个块内，可以对于每个块暴力二维前缀和预处理。

如果 $l,r$ 在不同的块内。

设 $bel[l]=x,bel[r]=y$。

首先考虑 $x+1\sim y-1$ 块内的贡献，这个显然可以预处理。

然后是 $l\sim R_x$ 和 $L_y\sim r$ 的块内贡献，这个可以预处理 $A_i$ 表示 $i$ 到 $i$  所在块的末尾这些数的逆序对个数，$B_i$ 表示 $i$ 到这个块开头的逆序对数。

这两个还是可以预处理。

然后就是 $x+1\sim y-1$ 块之间的贡献，维护 $f_{i,j}$ 表示前 $i$ 个块到和前 $j$ 个块的逆序对数。

这个显然可以先枚举 $i$ 块，维护一个值域数组，然后暴力枚举其他的块统计答案，最后做个二维前缀和即可。

注意到这个玩意是没有顺序的，所以统计答案时要除以 $2$。

---

随后是 $[l,R_x],[L_y,r]$ 到 $[x+1,y-1]$ 块的贡献。

这个可以预处理 $g_{i,j}$ 表示前 $i$ 个块到和前 $j$ 个**数**的逆序对数，同样可以二维前缀和搞。

容易发现这个东西是不要除以 $2$ 的。

---

最后是 $[l,R_x]$ 和 $[L_y,r]$ 之间的贡献。

这个东西考虑把 $[l,R_x]$ 和 $[L_y,r]$ 都 sort 一遍然后跑双指针。

但这样就带 $\log$ 了。

解决方案是初始时对于每个块维护一个 sort 后的 pair 数组，第一维是权值，第二维是下标。

然后从前到后枚举 $x$ 和 $y$ 块的 pair 数组，如果下标在 $[l,r]$ 里就把权值加到新数组里即可。

时间复杂度：$O((n+q)\sqrt n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;

const int kMaxN = 1e5 + 5, kMaxB = 320;

int n, m, bl, tot;
int a[kMaxN], bel[kMaxN], L[kMaxB], R[kMaxB], sz[kMaxB], suf[kMaxN], cnt5[kMaxB][kMaxB][kMaxB];
std::pair<int, int> b[kMaxN];
i64 cnt1[kMaxB], cnt2[kMaxB][kMaxB], cnt3[kMaxN], cnt4[kMaxN], cnt6[kMaxB][kMaxN];

/*
  cnt1[i] : 前 i 个块内部的逆序对数量和
  cnt2[i][j] : 前 i 个块跟前 j 个块的逆序对数量和
  cnt3[i] : i 到 i 所在块结尾这些数的逆序对数量
  cnt4[i] : i 到 i 所在块开头这些数的逆序对数量
  cnt5[i][j][k] : 第 i 个块前 j 个数到前 k 个数的逆序对数量
  cnt6[i][j] : 前 i 个块跟前 j 个数的逆序对数量和
*/

struct BIT {
  int c[kMaxN];

  void upd(int x, int v) {
    for (; x <= n; x += x & -x)
      c[x] += v;
  }

  int qry(int x) {
    int ret = 0;
    for (; x; x -= x & -x)
      ret += c[x];
    return ret;
  }
  int qry(int l, int r) { return qry(r) - qry(l - 1); }
} bit;

i64 brute_force(int *a, int l1, int r1, int *b, int l2, int r2) {
  i64 ret = 0;
  int p = l2 - 1;
  for (int i = l1; i <= r1; ++i) {
    for (; p < r2 && b[p + 1] < a[i]; ++p) {}
    ret += p - l2 + 1;
  }
  return ret;
}

void prework() {
  bl = sqrt(n), tot = (n - 1) / bl + 1;
  for (int i = 1; i <= n; ++i)
    b[i] = {a[i], i};
  for (int i = 1; i <= tot; ++i) {
    L[i] = R[i - 1] + 1, R[i] = std::min(i * bl, n);
    std::sort(b + L[i], b + R[i] + 1);
    for (int j = L[i]; j <= R[i]; ++j)
      bel[j] = i;
  }
  for (int i = 1; i <= tot; ++i) {
    cnt1[i] = cnt1[i - 1];
    for (int j = L[i]; j <= R[i]; ++j)
      for (int k = j + 1; k <= R[i]; ++k)
        if (a[j] > a[k])
          ++cnt1[i], ++cnt5[i][j - L[i] + 1][k - L[i] + 1];
    for (int j = 1; j <= bl; ++j)
      for (int k = 1; k <= bl; ++k)
        cnt5[i][j][k] += cnt5[i][j - 1][k] + cnt5[i][j][k - 1] - cnt5[i][j - 1][k - 1];

    for (int j = R[i]; j >= L[i]; --j) {
      if (j < R[i]) cnt3[j] = cnt3[j + 1] + bit.qry(a[j] - 1);
      bit.upd(a[j], 1);
    }
    for (int j = L[i]; j <= R[i]; ++j)
      bit.upd(a[j], -1);
    for (int j = L[i]; j <= R[i]; ++j) {
      if (j > L[i]) cnt4[j] = cnt4[j - 1] + bit.qry(a[j] + 1, n);
      bit.upd(a[j], 1);
    }
    for (int j = L[i]; j <= R[i]; ++j)
      bit.upd(a[j], -1);
  
    for (int j = L[i]; j <= R[i]; ++j)
      ++suf[a[j]];
    for (int j = n; j; --j)
      suf[j] += suf[j + 1];
    for (int j = 1; j <= n; ++j) {
      if (bel[j] > i) cnt2[i][bel[j]] += suf[a[j] + 1], cnt6[i][j] += suf[a[j] + 1];
      else if (bel[j] < i) cnt2[i][bel[j]] += suf[1] - suf[a[j]], cnt6[i][j] += suf[1] - suf[a[j]];
    }
    std::fill_n(suf + 1, n, 0);
  }
  for (int i = 1; i <= tot; ++i)
    for (int j = 1; j <= tot; ++j)
      cnt2[i][j] += cnt2[i - 1][j] + cnt2[i][j - 1] - cnt2[i - 1][j - 1];
  for (int i = 1; i <= tot; ++i)
    for (int j = 1; j <= n; ++j)
      cnt6[i][j] += cnt6[i - 1][j] + cnt6[i][j - 1] - cnt6[i - 1][j - 1];
}

i64 query(int l, int r, int cs) {
  static int tmpa[kMaxN], tmpb[kMaxN];
  int x = bel[l], y = bel[r];
  if (x == y) {
    int pl = l - L[x] + 1, pr = r - L[x] + 1;
    return cnt5[x][pr][pr] - cnt5[x][pl - 1][pr] - cnt5[x][pr][pl - 1] + cnt5[x][pl - 1][pl - 1];
  } else {
    i64 ret = 0;
    ret += cnt3[l] + cnt4[r] + cnt1[y - 1] - cnt1[x];
    ret += ((cnt2[y - 1][y - 1] - cnt2[x][y - 1]) - (cnt2[y - 1][x] - cnt2[x][x])) / 2;
    ret += (cnt6[y - 1][r] - cnt6[x][r]) - (cnt6[y - 1][L[y] - 1] - cnt6[x][L[y] - 1]);
    ret += (cnt6[y - 1][R[x]] - cnt6[x][R[x]]) - (cnt6[y - 1][l - 1] - cnt6[x][l - 1]);
    int ca = 0, cb = 0;
    for (int i = L[x]; i <= R[x]; ++i)
      if (b[i].second >= l && b[i].second <= R[x])
        tmpa[++ca] = b[i].first;
    for (int i = L[y]; i <= R[y]; ++i)
      if (b[i].second >= L[y] && b[i].second <= r)
        tmpb[++cb] = b[i].first;
    ret += brute_force(tmpa, 1, ca, tmpb, 1, cb);
    return ret;
  }
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i <= n; ++i)
    std::cin >> a[i];
  prework();
  i64 lastans = 0;
  for (int i = 1; i <= m; ++i) {
    i64 l, r;
    std::cin >> l >> r;
    l ^= lastans, r ^= lastans;
    std::cout << (lastans = query(l, r, i)) << '\n';
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