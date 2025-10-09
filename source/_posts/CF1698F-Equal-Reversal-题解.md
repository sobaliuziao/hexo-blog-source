---
title: CF1698F Equal Reversal 题解
date: 2025-09-18 09:08:00
---

## Description

有一个长度为 $n$ 的数组 $a$。你可以对其进行如下操作：

- 选择两个下标 $l$ 和 $r$，满足 $1 \le l \le r \le n$ 且 $a_l = a_r$。然后，将第 $l$ 个到第 $r$ 个元素的子段翻转，即将 $[a_l, a_{l + 1}, \ldots, a_{r - 1}, a_r]$ 变为 $[a_r, a_{r-1}, \ldots, a_{l+1}, a_l]$。

你还给定了另一个长度为 $n$ 的数组 $b$，它是 $a$ 的一个排列。请找出一组不超过 $n^2$ 次操作的方案，将数组 $a$ 变为 $b$，或者报告不存在这样的操作序列。

$n\leq 500$。

## Solution

注意到一次翻转操作是不会改变 $\left\{\{a_i,a_{i+1}\}\right\}$ 的，同时 $a_1$ 和 $a_n$ 也不会改变。所以猜测无解的充要条件是 $\left\{\{a_i,a_{i+1}\}\right\}=\left\{\{b_i,b_{i+1}\}\right\},a_1=b_1,a_n=b_n$。

构造就考虑从前往后依次让 $a_i=b_i$，满足了 $a_i=b_i$ 后就把 $a_{i-1}$ 删掉，根据判定条件这个是不会改变正确性的。

假设现在第一个 $a_i\neq b_i$ 的下标是 $k$，我们设 $a_{k-1}=x,a_k=y,b_k=z$。那么 $a_{[i-1,n]}=x,y,\ldots$，$b_{[i-1,n]}=x,z,\ldots$。

根据第一个条件，$[i-1,n]$ 中一定存在一个下标 $j$ 满足 $\{a_j,a_{j+1}\}=\{x,z\}$，把这个 $j$ 拿出来。

如果 $a_j=z$ 且 $a_{j+1}=x$，则直接翻转 $[i-1,j+1]$ 即可。

如果 $a_j=x$ 且 $a_{j+1}=z$，则需要用一次操作让 $a_j$ 和 $a_{j+1}$ 交换顺序。我们断言当前状态一定存在一个 $(l,r)$，使得 $a_l=a_r$ 且 $l\leq j<j+1\leq r$。

证明就考虑如果不存在这样的数对，那么 $a_{[i-1,j]}$ 和 $a_{[j+1,n]}$ 的颜色种类一定不交。又根据第一个充要条件，$\{b_i,b_{i+1}\}$ 出现在 $a_{[i-1,n]}$ 中，由于 $b_i=z=a_{j+1}$ 且 $\{b_{i-1},b_i\}$ 已经把 $\{a_j,a_{j+1}\}$ 抵消掉了，所以 $b_{i+1}$ 一定在 $a_{[j+1,n]}$ 范围内。依次类推，$b_{i+2},b_{i+3},\ldots,b_n$ 都在 $[j+1,n]$ 中，这说明 $a_{[j,n]}$ 构成的数对 把 $b_{[i-1,n]$ 的给抵消了，显然不可能。

暴力找到这样的区间后翻转即可。

总次数是 $2n$。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 505;

int n;
int a[kMaxN], b[kMaxN], cnta[kMaxN][kMaxN], cntb[kMaxN][kMaxN];
std::vector<std::pair<int, int>> vec;

void work(int l, int r) {
  assert(a[l] == a[r]);
  vec.emplace_back(l, r);
  std::reverse(a + l, a + 1 + r);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= n; ++j)
      cnta[i][j] = cntb[i][j] = 0;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    if (i > 1) ++cnta[std::min(a[i - 1], a[i])][std::max(a[i - 1], a[i])];
  }
  for (int i = 1; i <= n; ++i) {
    std::cin >> b[i];
    if (i > 1) ++cntb[std::min(b[i - 1], b[i])][std::max(b[i - 1], b[i])];
  }
  for (int i = 1; i <= n; ++i)
    for (int j = i; j <= n; ++j)
      if (cnta[i][j] != cntb[i][j])
        return void(std::cout << "NO\n");
  if (a[1] != b[1] || a[n] != b[n]) return void(std::cout << "NO\n");
  vec.clear();
  for (int i = 1; i <= n;) {
    for (; i <= n && a[i] == b[i]; ++i) {}
    if (i >= n) break;
    int p1 = 0, p2 = 0;
    for (int j = i; j < n; ++j) {
      if (!p1 && a[j] == b[i - 1] && a[j + 1] == b[i]) p1 = j;
      if (!p2 && a[j] == b[i] && a[j + 1] == b[i - 1]) p2 = j;
    }
    assert(p1 || p2);
    // for (int j = 1; j <= n; ++j) std::cerr << a[j] << " \n"[j == n];
    // 3 3 3 3 3 4 1 3 3
    // 3 3 3 3 4 1 3 3 3
    if (p2) {
      work(i - 1, p2 + 1);
    } else {
      static int lst[kMaxN];
      std::fill_n(lst + 1, n, 0);
      int l = 0, r = 0;
      for (int j = n; j >= i - 1; --j) {
        if (j <= p1 && lst[a[j]] >= p1 + 1) {
          l = j, r = lst[a[j]];
          break;
        }
        lst[a[j]] = j;
      }
      assert(l && r);
      work(l, r);
    }
  }
  std::cout << "YES\n" << vec.size() << '\n';
  for (auto [l, r] : vec) std::cout << l << ' ' << r << '\n';
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