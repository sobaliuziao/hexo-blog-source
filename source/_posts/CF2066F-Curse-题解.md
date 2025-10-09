---
title: 'CF2066F Curse 题解'
date: 2025-08-08 17:25:00
---

## Description

给定两个整数数组 $a_1, a_2, \ldots, a_n$ 和 $b_1, b_2, \ldots, b_m$。

你需要判断是否可以通过若干次（可能为零）如下操作将数组 $a$ 转换为数组 $b$。

- 在所有 $a$ 的非空子数组$^{\text{∗}}$中，选择一个具有最大和的子数组，并将该子数组替换为任意非空整数数组。

如果可能，你需要构造任意可行的操作序列。约束条件：你的答案中，所有操作使用的替换数组的长度之和不得超过 $n + m$。所有数字的绝对值不得超过 $10^9$。

$^{\text{∗}}$ 如果数组 $a$ 可以通过从数组 $b$ 的开头和结尾删除若干（可能为零或全部）元素得到，则称 $a$ 是 $b$ 的子数组。

$n,m\leq 500$。

## Solution

首先显然如果存在两个最大子段和区间互相包含，则小的那个没有用。那么如果我们把所有极长的最大子段拿出来，这些子段互不相交。

然后每次选出长度最长的最大子段和区间，把它删掉，并对这个区间的左右两侧分别进行递归，则可以把整个数组划分成 $[l_1,r_1],[l_2,r_2],\ldots,[l_k,r_k]$。

有个关键结论是后面每次操作的区间不能跨过现在划分出来的这 $k$ 个区间。

> 假设第一步操作的是 $[l_i,r_i]$，那么操作完的划分一定满足其余 $k-1$ 个区间划分不变，第 $i$ 个区间分裂为一些区间。
>
>这是因为如果分裂出来存在一个区间 $[L,R]$ 满足 $L<l_i\leq R<r_i$，由于  $[L,l_i-1]$ 的和一定小于零，否则 $[l_i,r_i]$ 拓展之后一定更优，所以 $[l_i,R]$ 一定比 $[L,R]$ 和更大，根据贪心划分的原则，$[L,R]$ 就不会被划分出来，也就不会被操作。

设最小的被操作过的初始划分区间和为 $x$，那么和小于 $x$ 的一定不会动，同时在操作和为 $x$ 的区间时所有原来和大于 $x$ 的区间一定满足当前状态下最大子段和不超过 $x$。

这启发我们贪心地先把和大于等于 $x$ 的区间先变成一个 $\{x\}$，然后再对这些 $\{x\}$ 一起操作，容易证明这个操作方式一定不劣。后面的操作就是这些 $\{x\}$ 至多只能有一个操作完最大子段和大于 $x$，否则一定会矛盾。满足了这个条件后操作方案就一定能构造出来了。

对于可行性，考虑对上面的东西进行 dp，设 $f_{i,j,0/1}$ 表示前 $i$ 个区间，目前匹配到 $b$ 的前 $j$ 个数，最大子段和大于 $x$ 的有 $0/1$ 个是否可行。然后进行分讨：

- $[l_i,r_i]$ 和小于 $x$：则转移是唯一的，即如果 $a[l_i,r_i]$ 和 $b[j+1,j+r_i-l_i+1]$ 相等，就能转移到 $f_{i,j+r_i-l_i+1,op}$。
- $[l_i,r_i]$ 和大于等于 $x$：

    1. 操作后的最大子段和小于等于 $x$，需要满足 $a[j+1,k]$ 的最大子段和小于等于 $x$，就能转移到 $f_{i,k,op}$。
    2. 操作后的最大子段和大于 $x$，则只需要满足 $op=0$，即可能转移到 $f_{i,k,1}$。

上面那个东西暴力转移是 $O(n^2m^2)$ 的，优化就考虑和大于等于 $x$ 的 $2$ 号转移只要找到最小的 $j$ 满足 $f_{i-1,j,0}=1$，然后暴力转移。$1$ 号转移由于 $j$ 能转移到的最大右端点随 $j$ 增加而增加，直接维护 $r_{op}$ 表示目前最大的 $k$ 满足 $f_{i,k,op}$ 转移过，这样的话每次转移就不会重复了。

时间复杂度：$O(n^2m+nm^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 505;

int n, m, t;
int a[kMaxN], b[kMaxN], l[kMaxN], r[kMaxN], sum[kMaxN][kMaxN], mxs[kMaxN][kMaxN], mxs1[kMaxN][kMaxN], lcp[kMaxN][kMaxN];
std::tuple<int, int, bool> pre[kMaxN][kMaxN][2];
bool f[kMaxN][kMaxN][2];

void getseg(int l, int r) {
  if (l > r) return;
  int ll = 0, rr = -1;
  for (int i = l; i <= r; ++i)
    for (int j = i; j <= r; ++j)
      if (sum[i][j] == mxs[l][r] && j - i > rr - ll)
        ll = i, rr = j;
  getseg(l, ll - 1);
  ::l[++t] = ll, ::r[t] = rr;
  getseg(rr + 1, r);
}

void dickdreamer() {
  std::cin >> n >> m; t = 0;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  for (int i = 1; i <= m; ++i) std::cin >> b[i];
  for (int i = 1; i <= n; ++i) {
    int now = a[i];
    sum[i][i] = mxs[i][i] = a[i];
    for (int j = i + 1; j <= n; ++j) {
      now = std::max(a[j], a[j] + now);
      sum[i][j] = sum[i][j - 1] + a[j];
      mxs[i][j] = std::max(now, mxs[i][j - 1]);
    }
  }
  for (int i = 1; i <= m; ++i) {
    int now = b[i];
    mxs1[i][i] = b[i];
    for (int j = i + 1; j <= m; ++j) {
      now = std::max(b[j], b[j] + now);
      mxs1[i][j] = std::max(now, mxs1[i][j - 1]);
    }
  }
  for (int i = 1; i <= n + 1; ++i)
    for (int j = 1; j <= m + 1; ++j)
      lcp[i][j] = 0;
  for (int i = n; i; --i) {
    for (int j = m; j; --j) {
      if (a[i] == b[j]) lcp[i][j] = lcp[i + 1][j + 1] + 1;
      else lcp[i][j] = 0;
    }
  }
  getseg(1, n);
  std::vector<int> vec;
  for (int i = 1; i <= t; ++i) vec.emplace_back(sum[l[i]][r[i]]);
  std::sort(vec.begin(), vec.end());
  vec.erase(std::unique(vec.begin(), vec.end()), vec.end());
  for (auto x : vec) {
    for (int i = 1; i <= t; ++i)
      for (int j = 1; j <= m; ++j)
        f[i][j][0] = f[i][j][1] = 0;
    f[0][0][0] = 1;
    for (int i = 1; i <= t; ++i) {
      if (sum[l[i]][r[i]] < x) {
        for (int j = 0; j < m; ++j) {
          for (int o = 0; o < 2; ++o) {
            if (!f[i - 1][j][o]) continue;
            if (lcp[l[i]][j + 1] >= r[i] - l[i] + 1) {
              f[i][j + r[i] - l[i] + 1][o] |= f[i - 1][j][o];
              pre[i][j + r[i] - l[i] + 1][o] = {i - 1, j, o};
            }
          }
        }
      } else {
        int mij = m + 1;
        for (int j = m; ~j; --j)
          if (f[i - 1][j][0])
            mij = j;
        for (int j = mij + 1; j <= m; ++j) {
          f[i][j][1] = 1;
          pre[i][j][1] = {i - 1, mij, 0};
        }
        int r[2] = {0};
        for (int j = 0; j < m; ++j) {
          for (int o = 0; o < 2; ++o) {
            if (!f[i - 1][j][o]) continue;
            for (int k = std::max(j + 1, r[o] + 1); k <= m; ++k) {
              if (mxs1[j + 1][k] <= x) {
                f[i][k][o] |= f[i - 1][j][o];
                pre[i][k][o] = {i - 1, j, o};
                r[o] = k;
              } else {
                break;
              }
            }
          }
        }
      }
    }
    if (!f[t][m][0] && !f[t][m][1]) continue;
    int posa = t, posb = m, op = f[t][m][1];
    std::vector<std::tuple<int, int, int>> vec1, vec2;
    std::vector<int> vec3;
    for (; posa && posb;) {
      auto [prea, preb, preop] = pre[posa][posb][op];
      // std::cerr << l[posa] << ' ' << r[posa] << ' ' << preb + 1 << ' ' << posb << '\n';
      if (sum[l[posa]][r[posa]] >= x) {
        vec3.emplace_back(posa);
        if (op ^ preop) {
          vec1.emplace_back(posa, preb + 1, posb);
        } else {
          vec2.emplace_back(posa, preb + 1, posb);
        }
      }
      posa = prea, posb = preb, op = preop;
    }
    static int len[kMaxN];
    for (int i = 1; i <= t; ++i) len[i] = r[i] - l[i] + 1;
    std::vector<std::tuple<int, int, std::vector<int>>> vv;
    std::sort(vec3.begin(), vec3.end(), [&] (auto a, auto b) { return sum[l[a]][r[a]] > sum[l[b]][r[b]]; });
    for (auto i : vec3) {
      int posl = 0, posr = 0;
      std::vector<int> vec = {x};
      for (int j = 1; j < i; ++j) posl += len[j];
      ++posl, posr = posl + len[i] - 1, len[i] = 1;
      vv.emplace_back(posl, posr, vec);
    }
    for (auto [i, l, r] : vec2) {
      int posl = 0, posr = 0;
      std::vector<int> vec;
      for (int j = 1; j < i; ++j) posl += len[j];
      ++posl, posr = posl + len[i] - 1, len[i] = r - l + 1;
      for (int j = l; j <= r; ++j) vec.emplace_back(b[j]);
      vv.emplace_back(posl, posr, vec);
    }
    for (auto [i, l, r] : vec1) {
      int posl = 0, posr = 0;
      std::vector<int> vec;
      for (int j = 1; j < i; ++j) posl += len[j];
      ++posl, posr = posl + len[i] - 1, len[i] = r - l + 1;
      for (int j = l; j <= r; ++j) vec.emplace_back(b[j]);
      vv.emplace_back(posl, posr, vec);
    }
    std::cout << vv.size() << '\n';
    for (auto &[l, r, vec] : vv) {
      std::cout << l << ' ' << r << ' ' << vec.size() << '\n';
      for (auto x : vec) std::cout << x << ' ';
      std::cout << '\n';
    }
    return;
  }
  std::cout << "-1\n";
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```