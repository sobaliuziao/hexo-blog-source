---
title: [CEOI2023] Tricks of the Trade 题解
date: 2024-11-15 16:50:00
---

## Description

有 $n$ 个机器人排成一排，第 $i$ 个机器人的购买价是 $a_i$ 欧元，卖出价是 $b_i$ 欧元。

给定 $1\le k\le n$，你需要购买一段长度至少为 $k$ 的区间中所有的机器人，然后选择其中的恰好 $k$ 个机器人来卖出。

你需要求出：

1. 你能够得到的最大收益；
2. 在收益最大化的前提下，哪些机器人可以在某种最优方案中被卖出。

$1\leq k\leq n\leq 2.5\times 10^5$。

## Solution

先考虑第一问怎么求。

不妨设 $f(l,r)$ 表示 $[l,r]$ 这个区间的收益，即为 $b$ 数组在 $[l,r]$ 的前 $k$ 大的和减去 $a$ 数组在 $[l,r]$ 的区间和。

打表一下会发现 $f(l,r)$ 满足四边形不等式 $f(a,c)+f(b,d)\geq f(a,d)+f(b,c)$。

<details>
<summary>证明</summary>

容易发现 $a$ 数组的区间和没什么意义，先扔掉，设 $g(l,r)$ 表示 $b$ 数组在 $[l,r]$ 前 $k$ 大的和，那么转化为要证明 $g(l,r)+g(l+1,r+1)\geq g(l,r+1)+g(l+1,r)$。

先把 $g(l+1,r)$ 拿出来，$g(l,r+1)$ 相当于是在 $[l+1,r]$ 同时加入 $b_l,b_{r+1}$ 两个数去更新第 $k$ 大和第 $k-1$ 大，而 $g(l,r)+g(l+1,r+1)$ 则是分别加入 $b_l$ 和 $b_{r+1}$ 去更新 $[l+1,r]$ 第 $k$ 大，这个显然比两个去更新第 $k$ 大和第 $k-1$ 大优。
</details>

所以第一问直接决策单调性分治即可。

对于第二问，先把所有收益等于最大值的区间 $[l,r]$ 拿出来，那么 $[l,r]$ 内 $b_i$ 不小于区间第 $k$ 大的位置都会被标记。

但是这样的最优区间可能是 $O(n^2)$ 级别的，暴力找是做不了的。

考虑如果存在两个最优区间 $[l_1,r_1],[l_2,r_2]$，满足 $l_1\leq l_2\leq r_2\leq r_1$，由于 $f(l_1,r_2)+f(l_2,r_1)\geq f(l_1,r_2)+f(l_2,r_1)=2\times ans$，所以 $[l_1,r_2]$ 和 $[l_2,r_1]$ 也是最优区间，这两个区间加上 $[l_2,r_2]$ 可以覆盖任何 $[l_1,r_1]$ 可以覆盖的位置，所以只需要保留 $[l_1,r_2],[l_2,r_2],[l_2,r_1]$ 即可。

于是剩下的区间是个类似双指针的东西，只有 $O(n)$ 个，所以在决策单调性分治的时候求出使得每个右端点 $r$ 收益最大的最大左端点 $l$，后面找区间的时候双指针扫即可。

时间复杂度：$O(n\log^2 n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2.5e5 + 5, kMaxT = kMaxN * 35;

int n, k;
int a[kMaxN], b[kMaxN];
int sgt_tot, rt[kMaxN], ls[kMaxT], rs[kMaxT], cnt[kMaxT];
int64_t ans, suma[kMaxT], sumb[kMaxT], f[kMaxT], p[kMaxT];
bool op[kMaxN];
std::vector<std::pair<int, int>> seg;

int update(int x, int l, int r, int ql, int v) {
  int nz = ++sgt_tot;
  ls[nz] = ls[x], rs[nz] = rs[x], cnt[nz] = cnt[x] + v, sumb[nz] = sumb[x] + v * ql;
  if (l == r) return nz;
  int mid = (l + r) >> 1;
  if (ql <= mid) ls[nz] = update(ls[x], l, mid, ql, v);
  else rs[nz] = update(rs[x], mid + 1, r, ql, v);
  return nz;
}

int64_t query(int x, int y, int l, int r, int k) {
  if (k <= 0 || cnt[y] - cnt[x] == 0) return 0;
  if (l == r) return l * k;
  int mid = (l + r) >> 1, crs = cnt[rs[y]] - cnt[rs[x]];
  if (k <= crs) return query(rs[x], rs[y], mid + 1, r, k);
  else return sumb[rs[y]] - sumb[rs[x]] + query(ls[x], ls[y], l, mid, k - crs);
}

int getkth(int x, int y, int l, int r, int k) {
  if (l == r) return l;
  int mid = (l + r) >> 1, crs = cnt[rs[y]] - cnt[rs[x]];
  if (k <= crs) return getkth(rs[x], rs[y], mid + 1, r, k);
  else return getkth(ls[x], ls[y], l, mid, k - crs);
}

int64_t calc(int l, int r) {
  if (r - l + 1 < k) return -1e18;
  return query(rt[l - 1], rt[r], 1, 1e9, k) - (suma[r] - suma[l - 1]);
}

void prework() {
  for (int i = 1; i <= n; ++i) {
    rt[i] = update(rt[i - 1], 1, 1e9, b[i], 1);
    suma[i] = suma[i - 1] + a[i];
  }
}

void solve(int l, int r, int L, int R) {
  if (l > r) return;
  int mid = (l + r) >> 1;
  f[mid] = calc(L, mid), p[mid] = L;
  for (int i = L + 1; i <= R; ++i) {
    int64_t val = calc(i, mid);
    if (val >= f[mid]) {
      f[mid] = val, p[mid] = i;
    }
  }
  solve(l, mid - 1, L, p[mid]), solve(mid + 1, r, p[mid], R);
}

void getseg() {
  for (int i = k, j = 1; i <= n; ++i) {
    if (f[i] != ans) continue;
    for (;; ++j) {
      if (calc(j, i) == ans) seg.emplace_back(j, i);
      if (j == p[i]) break;
    }
  }
}

void work() {
  static std::vector<std::pair<int, int>> vec[kMaxN];
  for (auto [l, r] : seg) {
    int kth = getkth(rt[l - 1], rt[r], 1, 1e9, k);
    vec[l].emplace_back(kth, 1), vec[r + 1].emplace_back(kth, -1);
  }
  std::multiset<int> st;
  for (int i = 1; i <= n; ++i) {
    for (auto [x, v] : vec[i]) {
      if (v == 1) st.emplace(x);
      else st.erase(st.lower_bound(x));
    }
    if (st.size() && b[i] >= *st.begin()) op[i] = 1;
  }
}

void dickdreamer() {
  std::cin >> n >> k;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= n; ++i) std::cin >> b[i];
  prework();
  memset(f, 0xcf, sizeof(f));
  solve(k, n, 1, n);
  ans = *std::max_element(f + 1, f + 1 + n);
  getseg(), work();
  std::cout << ans << '\n';
  for (int i = 1; i <= n; ++i) std::cout << op[i];
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