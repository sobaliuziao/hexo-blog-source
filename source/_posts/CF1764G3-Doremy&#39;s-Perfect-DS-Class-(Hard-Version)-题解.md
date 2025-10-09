---
title: CF1764G3 Doremy&#39;s Perfect DS Class (Hard Version) 题解
date: 2025-08-20 15:23:00
---

## Description

给定一个长度为 $ m $ 的数组 $ a $，Doremy 树支持查询 $ Q(l,r,k) $，其中 $ 1 \leq l \leq r \leq m $ 且 $ 1 \leq k \leq m $，该查询返回数组 $ \left[\left\lfloor\frac{a_l}{k} \right\rfloor, \left\lfloor\frac{a_{l+1}}{k} \right\rfloor, \ldots, \left\lfloor\frac{a_r}{k} \right\rfloor\right] $ 中不同整数的个数。

Doremy 有一个秘密排列 $ p $，它是 $ 1 $ 到 $ n $ 的一个排列。你可以进行查询，每次查询你给出 $ 3 $ 个整数 $l,r,k$（$1 \leq l \leq r \leq n$，$1 \leq k \leq n$），你会收到 $Q(l,r,k)$ 在数组 $ p $ 上的值。你能否在最多 $ \mathbf{20} $ 次查询内，找到下标 $y$（$ 1 \leq y \leq n $）使得 $ p_y=1 $？

注意，排列 $ p $ 在你进行任何查询之前就已经确定。

$n\leq 1024$。

## Solution

首先询问肯定是考虑 $k$ 比较特殊的情况，比如 $k=2$ 或者 $k=n$ 这种很大或者很小的询问。

这里先询问 $k=2$。

对于 $\lfloor x/2\rfloor$ 相同的两个位置，所有包含它们中至少一个的区间会得到贡献 $1$，同时包含 $1$ 的区间也会得到贡献 $1$。容易发现只有 $1$ 和 $n$ 是偶数时的 $n$ 会比较特殊，因为它们的颜色只有一个位置。

对于一个前缀 $[1,i]$ 和后缀 $[i+1,n]$。设 $c_1=Q(1,i,2),c_2=Q(i+1,n,2)$，则我们可以计算出横跨前后缀的颜色数量，然后就可以得出两边分别只有恰好一个位置的颜色数量 $v_1$ 和 $v_2$。

考虑二分答案，如果 $v_1\neq v_2$，则往更大的那边走即可。如果 $v_1=v_2$，则此时一定满足一边有 $1$，另一边有 $n$，再通过询问 $Q(1,mid,n)$ 即可得到 $n$ 在哪一边，$1$ 则在另一边，往 $1$ 那边继续递归即可。

经过计算会发现上面的做法次数是 $2\left\lceil\log_2n\right\rceil+1=21$，会多一次。

这一次在二分区间长度为 $2$ 的时候分讨一下即可。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

int n;

int query(int l, int r, int k) {
  static std::map<std::tuple<int, int, int>, int> mp;
  if (l > r) return 0;
  if (l == r) return 1;
  if (l == 1 && r == n) return n / k + 1;
  if (mp.count({l, r, k})) return mp[{l, r, k}];
  std::cout << "? " << l << ' ' << r << ' ' << k << '\n';
  fflush(stdout);
  int v;
  std::cin >> v;
  return mp[{l, r, k}] = v;
}

void dickdreamer() {
  std::cin >> n;
  int L = 1, R = n, posn = -1;
  while (L < R) {
    int mid = (L + R) >> 1;
    // int c1 = query(1, mid, 2), c2 = query(mid + 1, n, 2);
    int c1, c2;
    if (L + 1 == R && n % 2 == 0) {
      if (!~posn) {
        c1 = query(1, L - 1, 2) + 1, c2 = query(R + 1, n, 2) + 1;
      } else {
        if (query(1, R, 2) == query(1, L - 1, 2) + 1) {
          c1 = query(1, L, 2), c2 = query(R + 1, n, 2) + 1;
        } else {
          c1 = query(1, L - 1, 2) + 1, c2 = query(R, n, 2);
        }
      }
    } else {
      c1 = query(1, mid, 2), c2 = query(mid + 1, n, 2);
    }
    int cc = c1 + c2 - (n / 2 + 1);
    // cc : 两边共有的数量
    int v1 = 2 * c1 - mid - cc, v2 = 2 * c2 - (n - mid) - cc;
    if (posn != -1) {
      if (posn <= mid) --v1;
      else --v2;
    }
    if (v1 > v2){
      R = mid;
    } else if (v1 < v2) {
      L = mid + 1;
    } else {
      if (mid >= 2) {
        if (query(1, mid, n) == 2) posn = mid, L = mid + 1;
        else posn = mid + 1, R = mid;
      } else {
        if (query(mid + 1, n, n) == 2) posn = mid + 1, R = mid;
        else posn = mid, L = mid + 1;
      }
    }
  }
  std::cout << "! " << L << '\n';
  fflush(stdout);
}

int32_t main() {
// #ifdef ORZXKR
//   freopen("in.txt", "r", stdin);
//   freopen("out.txt", "w", stdout);
// #endif
//   std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  // std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```