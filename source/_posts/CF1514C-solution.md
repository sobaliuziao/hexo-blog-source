---
title: 'CF1514C Product 1 Modulo N 题解'
date: 2021-05-08 16:24:00
---

~~赛时想了一下就过了~~

一个显然的结论：给定一个正整数 $n$，很多个与 $n$ 互质的正整数的积与 $n$ 互质。

由于这题要求的数的乘积被 $n$ 除余 $1$，所以这些数都是与 $n$ 互质的。

所以长度 $\leq$ $n$ 的既约剩余系长度（指的就是 $1\sim n$ 与 $n$ 互质的数的个数）。

由于这些数的乘积 $\bmod n$ 不一定为 $1$，所以要考虑去掉一些最少的数使得剩下的数的积满足条件。然后很明显去掉这个乘积 $\bmod n$ 即为最多的情况。

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 5;

int n, tot, a[N];

int gcd (int m, int n) {
  if (m < n) swap(m, n);
  if (n == 0) return m;
  return gcd(n, m % n);
}

int main() {
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    if (gcd(i, n) == 1) a[++tot] = i;
  }
  int times = 1;
  for (int i = 1; i <= tot; ++i) {
    times = 1ll * times * a[i] % n;
  }
  if (times == 1) {
    cout << tot << endl;
    for (int i = 1; i <= tot; ++i) cout << a[i] << " ";
    cout << endl;
  }
  if (times > 1) {
    cout << tot - 1 << endl;
    for (int i = 1; i <= tot; ++i)
      if (a[i] != times) cout << a[i] << " ";
    cout << endl;
  }
  return 0;
}
```