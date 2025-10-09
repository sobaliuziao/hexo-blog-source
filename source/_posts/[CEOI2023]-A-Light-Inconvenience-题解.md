---
title: [CEOI2023] A Light Inconvenience 题解
date: 2024-11-12 21:15:00
---

## Description

今年 CEOI 的开幕式上有一场精彩的火炬表演。表演者们站成一排，从 $1$ 开始从左往右编号。每个表演者举着一根火炬，初始只有一个举着点燃的火炬的表演者。

表演分为 $Q$ 幕。在第 $a$ 幕开始之前，要么 $p_a > 0$ 个表演者从右侧加入表演，他们的火炬是熄灭的；要么最右侧 $p_a > 0$ 个表演者决定离开，并熄灭他们的火炬（如果他们的火炬是点燃的）。表演者的加入和离开不受委员会的控制。最左侧的表演者永远留在台上。

一旦第 $a$ 幕准备好了，委员会需要宣布一个非负整数 $t_a \geq 0$。对于每个举着点燃的火炬的表演者，用他的火炬点燃他右侧 $t_a$ 个人的火炬。也就是说，第 $i$ 个人的火炬在传火后是点燃的，当且仅当表演者 $\max(1, i - t_a), \cdots, i$ 中至少一个人的火炬在传火前是点燃的。$t_a$ 不应超过 $p_a$。

在第 $a$ 幕结束时，委员会需要告知每个举着点燃的火炬的表演者是否熄灭火炬。出于美学原因，最右侧的表演者应保持他的火炬点燃。此外，为了节省汽油，点燃的火炬数量不应超过 $150$。

编写程序帮助委员会在上述限制下主持表演。

对于所有数据，$1\leq N\leq 10 ^ {17}$，$1\leq Q\leq 5\times 10 ^ 4$。

## Solution

考虑将整个 01 序列反转，转化为从开头加/删数。

设序列中第 $i$ 个 $1$ 的位置为 $f_i$，当 $p=f_i$ 时就需要满足 $f_i+1\leq f_{i+1}\leq 2f_i+1$，同时 $f_1=1,f_t=n$。所以如果没有删除操作，就让 $f_i=\min\{2f_{i-1}+1,n\}$ 即可。

加入删除操作就不好做了，因为删掉开头的 $p$ 个数后 $f$ 数组的形态会变得很不固定，难以维护。

不妨设 $g$ 数组为删除操作后的新的 $1$ 的位置序列，考虑用原来的 $f$ 序列构造 $g$ 序列。

显然 $g_{i-1}+1\leq g_i\leq 2g_{i-1}+1$，由于 $f_j$ 控制的区间为 $[f_j-2p,f_j-p]$，所以所有 $g_i$ 一定要出自这些区间。

假设已经构造好了 $g_1,g_2,\ldots,g_{i-1}$，设 $j$ 为满足 $f_j-2p\leq 2g_{i-1}+1$ 的最大的 $j$，那么 $2f_j+1-2p\geq f_{j+1}-2p>2g_{i-1}+1$，即 $f_j-p\geq g_{i-1}+1$，所以 $[f_j-2p,f_j-p]$ 与 $[g_{i-1}+1,2g_{i-1}+1]$ 一定有交，贪心地令 $g_i$ 为 $\min\{f_j-p,2g_{i-1}+1\}$ 即可。

下面算一下这个做法维护的序列长度。

如果 $g_i=2g_{i-1}+1$，则 $g$ 翻倍了。如果 $g_i=f_j-p$，则 $2g_i+1=2f_j-2p+1\geq f_{j+1}-2p$，所以 $g_{i+1}\geq\min\{f_{j+1}-p,2g_i+1\}$。如果 $g_{i+1}=2g_i+1$，则 $g$ 翻倍了，否则 $g_{i+1}=f_{j+1}-p\geq 2g_{i-1}+1$。

所以 $g$ 数组每两个就会翻一次倍，所以长度为 $2\log n+O(1)$。

## Code

```cpp
#include <bits/stdc++.h>
#include "light.h"

#ifdef ORZXKR
#include "sample_grader.cpp"
#endif

const int kMaxt = 155;

int64_t n = 1, t = 0;
int64_t f[kMaxt], g[kMaxt];

void prepare() {
  n = 1;
  f[t = 1] = 1;
}

std::pair<long long, std::vector<long long>> join(long long p) {
  if (f[t] == n) --t;
  if (!t) f[t = 1] = 1;
  n += p;
  for (;;) {
    if (f[t] == n) break;
    f[t + 1] = std::min<int64_t>(2ll * f[t] + 1, n);
    ++t;
  }
  std::vector<long long> vec;
  for (int i = t; i; --i) vec.emplace_back(n + 1 - f[i]);
  return {p, vec};
}

std::pair<long long, std::vector<long long>> leave(long long p) {
  n -= p;
  int _t = 0;
  g[_t = 1] = 1;
  for (int i = 1;;) {
    if (g[_t] == n) break;
    for (; i < t && f[i + 1] - 2ll * p <= 2ll * g[_t] + 1; ++i) {}
    g[_t + 1] = std::min<int64_t>({n, f[i] - p, 2ll * g[_t] + 1});
    ++_t;
  }
  t = _t;
  for (int i = 1; i <= t; ++i) f[i] = g[i];
  std::vector<long long> vec;
  for (int i = t; i; --i) vec.emplace_back(n + 1 - f[i]);
  return {p, vec};
}
```