---
title: '[AGC040C] Neither AB nor BA 题解'
date: 2024-02-17 11:46:00
---

## Description

给出一个大于0的偶数 $N$ 。

请找出长度为 $N$ ，由 `A`，`B`，`C` 这三个字母组成且可以由下列规则把其变为空串的字符串 $s$ 的数量。

- 不断选择 $s$ 中任意除 `AB` 和 `BA` 外的长度为 $2$ 的子串并删除。

比如 `ABBC` 是 $N=4$ 条件下的一个合法字符串，因为我们可以通过这样的方式将其变为空串：`ABBC` →（删除 `BB`）→`AC`→（删除`AC`）→`(空串)`

答案可能很大，所以请将结果对 $998244353$ 取模。

$N\leq 10^7$。

## Solution

注意到如果把奇数位染成黑色，偶数位染成白色，那么每次操作一定是删除一个黑格一个白格。

所以同色位置之间是没有影响的，那么把黑色位置的 `AB` 反转，题目就等价于每次删除任意除 `AA` 和 `BB` 外的长度为 $2$ 的子串。

先考虑没有 `C` 怎么做。

容易发现只要 `A` 的个数和 `B` 的个数相等，那么每次操作前必定会有相邻的 `AB`，随便选一个删掉，显然是合法的。而个数不相等则一定不合法。

然后考虑有 `C` 怎么做。

由于 `C` 可以和任意一个字符一起删掉，所以可以把每个 `C` 替换成 `A` 或 `B`，如果有一种方案合法就一定合法。

不妨设 `A` 有 $x$ 个，`B` 有 $y$ 个，`C` 有 $n-x-y$ 个。

则字符串合法等价于 $n-x-y\geq |x-y|$，算一下可以得出：$x,y\leq\frac{n}{2}$。

然后用总方案 - 不合法方案数即可。答案是：

$$3^n-2\times\sum_{i=\frac{n}{2}+1}^{n}{\binom{n}{i}\cdot 2^{n-i}}$$

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e7 + 5, kMod = 998244353;

int n;
int fac[kMaxN], ifac[kMaxN], inv[kMaxN], pw2[kMaxN] = {1, 2};

int C(int m, int n) {
  if (m < n) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = inv[1] = 1;
  for (int i = 2; i <= n; ++i) {
    pw2[i] = 2ll * pw2[i - 1] % kMod;
    inv[i] = 1ll * (kMod - kMod / i) * inv[kMod % i] % kMod;
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = 1ll * inv[i] * ifac[i - 1] % kMod;
  }
}

void dickdreamer() {
  std::cin >> n;
  prework();
  int ans = 1;
  for (int i = 1; i <= n; ++i) ans = 3ll * ans % kMod;
  for (int i = n / 2 + 1; i <= n; ++i) {
    ans = (ans - 1ll * pw2[n - i + 1] * C(n, i) % kMod + kMod) % kMod;
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