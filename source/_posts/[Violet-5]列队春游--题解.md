---
title: [Violet 5]列队春游  题解
date: 2022-10-02 17:12:00
---

## Description

[link](https://hydro.ac/d/bzoj/p/2720)

## Solution

考虑对于每一个人算贡献。

令 $P(i)$ 表示这个人视野距离为 $i$ 的概率， $Q(i)$ 表示视野距离不小于 $i$ 的概率，令 $k$ 表示能够阻拦这个人视野的人的个数（当然不包括当前人）。

那么贡献即为：

$$
\sum_{i=1}^{n}{i\times P(i)}
$$

把这个式子转化下为：

$$
\sum_{i=1}^{n}{Q(i)}
$$

所以这时候只需要算出来 $Q(i)$ 即可，那么：

$$
Q(i)=\dfrac{(n-i+1)\cdot A_{n-k-1}^{i-1}\cdot (n-i)!}{n!}
$$

这个式子中 $(n-i+1)$ 表示当前人有 $n-i+1$ 个位置可以选。
$A_{n-k-1}^{i-1}$ 表示当前人前面的 $i-1$ 个位置只能由不能阻拦当前人视野的人来选，一共有 $n-k-1$ 个人。
$(n-i)!$ 就表示除了当前人和其前面的 $i-1$ 人外，其他人全排列的方案数。

---

然后化简即可：

$$
\begin{aligned}
ans&=\sum_{i=1}^{n}{\dfrac{(n-i+1)\cdot A_{n-k-1}^{i-1}\cdot (n-i)!}{n!}}\\
&=\sum_{i=1}^{n}{\dfrac{(n-i+1)\cdot\dfrac{(n-k-1)!}{(n-k-i)!}\cdot (n-i)!}{n!}}\\
&=\dfrac{(n-k-1)!}{n!}\cdot\sum_{i=1}^{n}{\dfrac{(n-i+1)!}{(n-k-1)!}}\\
&=\dfrac{(n-k-1)!}{n!}\cdot (k+1)!\cdot\sum_{i=1}^{n}{C_{n-i+1}^{k+1}}
\end{aligned}
$$

---

然后考虑这样一个式子：

$$
\sum_{i=1}^{n}{C_{i}^{k}}
$$

这个式子的组合意义就是在 $n+1$ 个不同元素中选取 $k+1$ 个元素的方案数。这里相当于就是枚举选的元素中编号最大的，假设为 $s$，那么方案数就为 $\sum\limits_{s=1}^{n+1}{C_{s-1}^{k}}=\sum\limits_{i=1}^{n}{C_{i}^{k}}=C_{n+1}^{k+1}$。

所以 $\sum\limits_{i=1}^{n}{C_{n-i+1}^{k+1}}=C_{n+1}^{k+2}$.

---

那么：

$$
\begin{aligned}
ans=&\dfrac{(n-k-1)!}{n!}\cdot (k+1)!\cdot C_{n+1}^{k+2}\\
=&\dfrac{(n-k-1)!}{(k+1)!}\cdot (k+1)!\cdot \dfrac{(n+1)!}{(k+2)!\cdot (n-k-1)!}\\
=&\dfrac{n+1}{k+2}
\end{aligned}
$$

---

所以就可以线性求解了。

## Code

<details>

<summary>代码</summary>

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include <debug.h>
#else
#define debug(...) 114514
#endif

using namespace std;

const int kMaxN = 305, kMaxA = 1005;

int n, x;
int sum[kMaxA];
double ans;

int main() {
  cin >> n;
  for (int i = 1, x; i <= n; ++i) {
    cin >> x;
    ++sum[x];
  }
  for (int i = 1; i <= 1000; ++i) {
    ans += sum[i] * (n + 1) * 1.0 / (n - sum[i - 1] + 1);
    sum[i] += sum[i - 1];
  } 
  cout << fixed << setprecision(2) << ans << endl;
  return 0;
}
```

</details>