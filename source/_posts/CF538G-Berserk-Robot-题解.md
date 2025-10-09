---
title: CF538G Berserk Robot 题解
date: 2024-07-29 19:29:00
---

## Description

有一个机器人，第 $0$ 秒时在 $(0,0)$ 位置。

机器人会循环执行一个长度为 $l$ 的指令序列，每秒执行一个指令。

指令有 `ULDR` 四种，分别代表向上/左/下/右移动一格。

你不知道这个指令序列具体是什么，但是你知道 $n$ 条信息，第 $i$ 条信息为「第 $t_i$ 秒时机器人在 $(x_i,y_i)$」，保证 $t$ 递增。

你需要构造一个满足这些信息的指令序列，或判断不存在。

$n \le 2 \times 10^5$，$l \le 2 \times 10^6$，$t_i,|x_i|,|y_i| \le 10^{18}$。

## Solution

注意到这里每次移动 $x,y$ 会互相影响，而不是独立的，考虑把原图转 $45^{\circ}$ 即点 $(x,y)$ 变为 $(x+y,x-y)$，这样操作就变为 $(1,1),(1,-1),(-1,1),(-1,-1)$。

这样已经可以做了，但 $1,-1$ 这类操作不够优美，考虑让 $(x,y)$ 变为 $\left(\frac{y+x+t}{2},\frac{y-x+t}{2}\right)$，操作就只有 $(1,1),(1,0),(0,1),(0,0)$，这样题目就简化很多了。

先考虑 $x$ 的情况，对于 $y$ 同理。

不妨设 $s_i$ 表示前 $i$ 个指令对 $x$ 的贡献值，对于一组信息 $(t_i,x_i)$，$r_i=t_i\bmod l,k_i=\left\lfloor\frac{t_i}{l}\right\rfloor$，一定满足 $x_i=s_{r_i}+k_is_l$，所以$s_{r_i}=x_i-k_is_l$。

考虑按照 $r_i$ 排序，容易发现按照 $r$ 把 $[1,l]$ 分成若干块，对于块内的操作可以随便排序，所以 $0\leq (x_{i+1}-k_{i+1}s_l)-(x_{i}-k_is_l)\leq r_{i+1}-r_{i}$，这里为了让 $[1,r_1]$ 和 $[r_n+1,l]$ 这两个块也考虑到，可以加入 $k=0,r=0,x=0$ 和 $k=-1,r=l,x=0$ 这两组信息。

通过解不等式就可以得到 $s_l$ 的范围，然后随便取一个 $s_l$ 的可能取值对于每个块分别考虑就可以构造出答案了。

时间复杂度：$O(n\log n+l)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5, kMaxL = 2e6 + 5;

int n, l;
bool ans[kMaxL][2];
std::tuple<int, int, int, int> a[kMaxN];

char getch(bool o1, bool o2) {
  if (!o1 && !o2) return 'D';
  else if (!o1 && o2) return 'L';
  else if (o1 && !o2) return 'R';
  else return 'U';
}

int cei(int x, int k) {
  if (k < 0) x = -x, k = -k;
  if (x >= 0) return (x + k - 1) / k;
  else return -((-x) / k);
  // return ceil((long double)x / k);
}

int flr(int x, int k) {
  if (k < 0) x = -x, k = -k;
  if (x >= 0) return x / k;
  else return -((-x + k - 1) / k);
  // return floor((long double)x / k);
}

void dickdreamer() {
  std::cin >> n >> l;
  for (int i = 1; i <= n; ++i) {
    int t, x, y;
    std::cin >> t >> x >> y;
    if ((x + y - t) & 1) return void(std::cout << "NO\n");
    a[i] = {t % l, t / l, (y + x + t) / 2, (y - x + t) / 2};
  }
  a[++n] = {0, 0, 0, 0}, a[++n] = {l, -1, 0, 0};
  std::sort(a + 1, a + 1 + n);
  int L = 0, R = l;
  for (int i = 1; i < n; ++i) {
    int k = std::get<1>(a[i]) - std::get<1>(a[i + 1]);
    int nl = std::get<2>(a[i]) - std::get<2>(a[i + 1]);
    int nr = nl + std::get<0>(a[i + 1]) - std::get<0>(a[i]);
    assert(nl <= nr);
    if (!k && (nl > 0 || nr < 0)) return void(std::cout << "NO\n");
    if (k > 0)
      L = std::max(L, cei(nl, k)), R = std::min(R, flr(nr, k));
    else if (k < 0)
      L = std::max(L, cei(nr, k)), R = std::min(R, flr(nl, k));
  }
  if (L > R) return void(std::cout << "NO\n");
  for (int i = 1; i < n; ++i) {
    int det = (std::get<2>(a[i + 1]) - L * std::get<1>(a[i + 1])) -
              (std::get<2>(a[i]) - L * std::get<1>(a[i]));
    assert(det >= 0);
    int nl = std::get<0>(a[i]) + 1, nr = std::get<0>(a[i]) + det;
    for (int j = nl; j <= nr; ++j) ans[j][0] = 1;
  }
  L = 0, R = l;
  for (int i = 1; i < n; ++i) {
    int k = std::get<1>(a[i]) - std::get<1>(a[i + 1]);
    int nl = std::get<3>(a[i]) - std::get<3>(a[i + 1]);
    int nr = nl + std::get<0>(a[i + 1]) - std::get<0>(a[i]);
    assert(nl <= nr);
    if (!k && (nl > 0 || nr < 0)) return void(std::cout << "NO\n");
    if (k > 0)
      L = std::max(L, cei(nl, k)), R = std::min(R, flr(nr, k));
    else if (k < 0)
      L = std::max(L, cei(nr, k)), R = std::min(R, flr(nl, k));
  }
  if (L > R) return void(std::cout << "NO\n");
  for (int i = 1; i < n; ++i) {
    int det = (std::get<3>(a[i + 1]) - L * std::get<1>(a[i + 1])) -
              (std::get<3>(a[i]) - L * std::get<1>(a[i]));
    assert(det >= 0);
    int nl = std::get<0>(a[i]) + 1, nr = std::get<0>(a[i]) + det;
    for (int j = nl; j <= nr; ++j) ans[j][1] = 1;
  }

  for (int i = 1; i <= l; ++i) std::cout << getch(ans[i][0], ans[i][1]);
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