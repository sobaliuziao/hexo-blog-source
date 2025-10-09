---
title: [AGC062D] Walk Around Neighborhood 题解
date: 2024-10-10 10:12:00
---

## Description

给定正整数 $N$ 和 $N$ 个正偶数 $D_i$。

在平面直角坐标系中，小麦初始在 $(0,0)$，每次他可以选取一个未被擦去的 $D_i$，将其擦去，并从 $(x,y)$ 移动到 $(x',y')$ 使得 $|x-x'|+|y-y'|=D_i$。注意，所有坐标都是实数而非整数。例如，$D_i=2$，你可以从 $(0,0)$ 到 $(0.85486,1.14514)$。

请问经过 $N$ 次移动后，是否可以回到 $(0,0)$。

如果可以的话，对于所有到达的点 $(x,y)$ 请求出 $\max(|x|+|y|)$ 可能取到的最小值是多少。

$1\leq N\leq 2\times 10^5,2\leq D_i\leq 2\times 10^5,2|D_i$。

## Solution

先对 $D_i$ 进行排序。显然无解的条件是 $D_n>\sum_{i=1}^{n-1}{D_i}$。

不妨设最小答案为 $r$，那么每次跳都不能跳出半径为 $r$ 的圆。有个结论是 $\frac{D_n}{2}\leq r\leq D_n$，这是因为当 $r=D_n$ 时，由于 $\sum_{i=1}^{n-1}{D_i}\leq D_n$，所以只需要从小到大往一个方向走，如果走出这个圆了则最后一步一定能调整方向并走到圆上，于是走到第 $n-1$ 步时一定在圆的边界上，最后一步走 $D_n$ 的距离刚好回到原点。

对于 $r<\frac{D_n}{2}$ 的情况，则无论在圆内的哪个点走 $D_n$ 的距离一定会走出圆，就矛盾了。

---

然后判断 $r$ 是否是最小值。

由于 $r$ 是最小值，所以一定会存在某个时刻走到圆的边界上，并且因为要回来，所以问题等价于将 $D$ 划分成两个子序列，两个子序列分别可以走到边界。

考虑一个 $D$ 数组能走到边界 $r$ 的条件，如果 $D_i$ 中小于等于 $r$ 的数的和 $\geq r$，则这些数一定能走到 $r$，大于 $r$ 的进行调整即可。如果和小于 $r$，不妨设小于等于 $r$ 的数走到了 $p$，下一步走 $x$，如果 $x>p+r$ 就说明这时走 $x$ 会走出圆，否则一定能刚好走到圆边界，于是最优条件一定是选大于 $r$ 的最小的 $x$ 走，如果这么走都会出去则走不到，否则走得到。

求答案时先从小到大枚举 $r$，并将所有 $\leq r$ 的数加到背包里，分类讨论一下两个子序列是哪种合法的情况即可。具体见代码。

时间复杂度：$O\left(\frac{nV}{\omega}\right)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN];
std::bitset<kMaxN> f;

bool check(int l, int r) {
  int p = f._Find_next(l - 1);
  return p <= r;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  std::sort(a + 1, a + 1 + n);
  int ss = 0;
  for (int i = 1; i < n; ++i) ss += a[i];
  if (ss < a[n]) return void(std::cout << "-1\n");
  f[0] = 1;
  int sum = 0;
  a[n + 1] = 1e9;
  for (int r = a[n] / 2, p = 1; r <= a[n]; ++r) {
    for (; a[p] <= r; f |= (f << a[p++])) sum += a[p];
    if (check(r, sum - r)) return void(std::cout << r << '\n');
    if (p <= n && check(r, sum + r - a[p])) return void(std::cout << r << '\n');
    if (p <= n - 1 && check(a[p] - r, sum + r - a[p + 1])) return void(std::cout << r << '\n');
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