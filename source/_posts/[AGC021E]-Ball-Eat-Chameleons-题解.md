---
title: '[AGC021E] Ball Eat Chameleons 题解'
date: 2024-02-07 20:25:00
---

## Description

有 $n$ 只变色龙，一开始都是蓝色。现在你喂了 $k$ 次球，每次指定一只变色龙吃下你指定颜色的球。

一只变色龙从蓝色变成红色当且仅当它吃的红球比蓝球多；
一只变色龙从红色变成蓝色当且仅当它吃的蓝球比红球多。

求最后能使所有变色龙都变成红色的方案数。

两个方案不同当且仅当至少一次喂的球颜色不同（**而不是喂的变色龙不同**）。

**注意：存在一次喂的变色龙不同的两个方案可能是相同的方案。**

$1\leq n,k\leq 5\times 10^5$。

## Solution

考虑对于一只变色龙，怎样给他喂球才能变成红色。

设喂了 $a$ 个红球，$b$ 个蓝球。

1. $a>b$：为红色。
2. $a<b$：为蓝色。
3. $a=b$：为不同于最后喂的颜色的另一个颜色，即最后的颜色异或 $1$。

首先如果 $a-b\geq 2$，那么把多出来的 $a-b-1$ 个球给别人一定不劣，所以这里只需要满足 $a=b+1$ 或 $a=b$ 且最后一次选了蓝球。

不妨设一个方案总共放了 $R$ 个红球，$B$ 个蓝球，则要满足条件一定要满足 $R\geq B$。

容易发现 $a=b+1$ 的变色龙总共 $R-B$ 个，$a=b$ 的变色龙共 $n-(R-B)$ 个，不妨设 $cnt=n-(R-B)$。

所以判断一个方案是否合法等价于能否在其中找到 $cnt$ 个形如 `RB` 的匹配。

但是这个判定还不够简单。

注意到这些匹配一定是前 $cnt$ 个 `R` 和后 $cnt$ 个 `B` 按顺序进行匹配，那么对于倒数第 $i$ 个 `B`，它前面一定有至少 $cnt-i+1$ 个 `R`。

所以对于每个前缀，他的 `R` 的个数 $\geq$ `B` 的个数 $-(B-cnt)$。

那么把 `R` 看作 $+1$，`B` 看作 $-1$ 做一遍前缀和，只要满足每个前缀和 $\geq R-n$ 即可。

这就转化为了一个类似卡特兰数的东西，答案就是：

$$
\binom{R+B}{R}-\binom{R+B}{n+B-R-1}
$$

这里对于 $R=B$ 要特判，因为最后一步必须是 $B$，所以只要把 $B-1$ 再做上面那个式子即可。

时间复杂度：$O(k)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 5e5 + 5, kMod = 998244353;

int n, k;
int inv[kMaxN], fac[kMaxN], ifac[kMaxN];

int add(int x, int y) { return (x + y) >= kMod ? (x + y - kMod) : (x + y); }
int sub(int x, int y) { return (x < y) ? (x - y + kMod) : (x - y); }

int C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = inv[1] = 1;
  for (int i = 2; i <= k; ++i) {
    inv[i] = 1ll * (kMod - kMod / i) * inv[kMod % i] % kMod;
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = 1ll * inv[i] * ifac[i - 1] % kMod;
  }
}

void dickdreamer() {
  std::cin >> n >> k;
  if (k < n) return void(std::cout << "0\n");
  prework();
  int ans = 0;
  for (int i = (k + 1) / 2; i <= k; ++i) {
    int j = k - i;
    if (i == j) -- j;
    ans = add(ans, sub(C(i + j, i), C(i + j, n + j - i - 1)));
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
  // std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```