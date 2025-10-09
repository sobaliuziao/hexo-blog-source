---
title: CF2124H Longest Good Subsequence 题解
date: 2025-07-20 20:41:00
---

## Description

将一个长度为 $m$ 的数组 $b$ 称为 **好数组（good）**，如果它满足以下两个条件：

1. 对于每个 $1 \leq i \leq m$，都有 $1 \leq b_i \leq i$。

2. 存在一个长度为 $m$ 的排列 $p$，使得对于每个 $1 \leq i \leq m$，都有：
   $b_i$ 是使得区间 $[b_i, i]$ 中的最小值恰好等于 $p_i$ 的**最小下标**，也就是满足

   $$
   \min(p_{b_i}, p_{b_i+1}, \dots, p_i) = p_i
   $$

例如，数组 $[1,1,3,3,5]$ 是一个好数组（可以取排列 $p = [2,1,5,3,4]$ 来满足第二个条件）；
而数组 $[1,1,2]$ 不是好数组。

注意：**空数组被视为好数组。**

---

现在给定一个长度为 $n$ 的数组 $a$，你需要找出其中**最长的好子序列**的长度。

$n\leq 15000$。

## Solution

考虑什么样的数组 $b$ 是合法的。

显然需要满足 $b_{b_i-1}$ 是 $b_i$ 左边第一个比 $b_i$ 小的数，那么由于 $b_{b_i}\geq b_i>b_{b_i-1}$，所以 $b_{b_i}=b_i$。

考虑对 $b_x=x$ 的这些位置进行区间 dp。

具体地，设 $f_{i,j}$ 表示只考虑 $[i,j]$ 中大于等于 $a_i$ 的数，$i$ 必须选，且 $i$ 是第 $a_i$ 个选的数的最长长度。注意这里由于已经钦定 $i$ 的位置了，所以就不管前面是否能选以及 $a_i$ 这里是否满足条件，把这个区间内的数看成一个独立的个体。

有如下几种转移：

1. $a_j<a_i$，则 $f_{i,j}\leftarrow f_{i,j-1}$。
2. $a_j=a_i$，则 $f_{i,j}\leftarrow f_{i,j-1}+1$。
3. $a_j>a_i$，现在需要为 $a_j$ 找到其对应的开头 $k$，满足 $a_k=a_j$，且 $k$ 可以作为第 $a_k$ 个数出现。

	这个显然等价于 $f_{i,k-1}\geq a_k-1$，因为由于这个子序列支持从末尾删除，所以可以得到一个长度为 $a_k-1$ 的子序列，而 $b_i\leq i$，所以前面的数都小于等于 $a_k-1$，此时 $a_k$ 就可以作为开头了。

	转移为 $f_{i,j}\leftarrow\max\{f_{i,j-1},f_{k,j}\}$，由于只需要找到最小的满足条件的 $k$，扫右端点的时候维护一个数组即可。

答案即为所有满足 $a_i=1$ 的 $i$ 中 $f_{i,n}$ 的最大值。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1.5e4 + 5;

int n;
int a[kMaxN], f[kMaxN][kMaxN];

void chkmax(int &x, int y) { x = (x > y ? x : y); }
void chkmin(int &x, int y) { x = (x < y ? x : y); }

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  int ans = 0;
  for (int i = n; i; --i) {
    static int fir[kMaxN];
    std::fill_n(fir + 1, n, 0);
    f[i][i] = a[i];
    for (int j = i + 1; j <= n; ++j) {
      f[i][j] = f[i][j - 1];
      if (a[j] < a[i]) continue;
      if (a[j] == a[i]) chkmax(f[i][j], f[i][j - 1] + 1);
      if (!fir[a[j]] && f[i][j - 1] + 1 >= a[j]) fir[a[j]] = j;
      if (fir[a[j]]) chkmax(f[i][j], f[fir[a[j]]][j]);
    }
    if (a[i] == 1) chkmax(ans, f[i][n]);
  }
  std::cout << ans << '\n';
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