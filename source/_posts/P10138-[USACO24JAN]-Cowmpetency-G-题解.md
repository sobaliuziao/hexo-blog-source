---
title: P10138 [USACO24JAN] Cowmpetency G 题解
date: 2024-02-23 20:20:00
---

## Description

Farmer John 正在为他的奶牛们雇用一位新的牛群领队。为此，他面试了 $N$（$2\le N\le 10^9$）头奶牛来担任该职位。在每次面试后，他会为候选牛分配一个 $1$ 到 $C$（$1\le C\le 10^4$）范围内的整数「牲任力」分数 $c_i$，与她们的领导能力相关。

由于 Farmer John 面试了如此多的奶牛，他已经忘记了所有奶牛的牲任力分数。然而，他确实记得 $Q$（$1\le Q\le \min(N−1,100)$）对数字 $(a_i,h_i)$，其中奶牛 $h_i$ 是第一头比奶牛 $1$ 到 $a_i$ 拥有**严格**更高牲任力分数的奶牛（所以 $1\le a_i<h_i\le N$）。

Farmer John 现在告诉你这 $Q$ 个数对 $(a_i,h_i)$。请帮助他数一下有多少个牲任力分数序列与此信息一致！输入保证存在至少一个这样的序列。由于这个数字可能非常大，输出该值模 $10^9+7$ 的余数。

## Solution

先考虑 $N\leq 2000$ 的情况。

容易发现那个限制等价于 $\max_{j=a_i+1}^{h_i-1}{c_j}\leq \max_{j=1}^{a_i}{c_j}<c_{h_i}$，那么此时每个位置就出现了三种状态：一定是前缀最大值、一定不是前缀最大值和无法确定。不妨设一定不是前缀最大值标号为 $0$，无法确定为 $1$，一定是则为 $2$。

对这个进行 dp 可做到 $O(NC)$。

考虑到连续的 $0/1$ 段是 $O(Q)$ 级别的，所以把连续的 $0/1$ 段缩掉然后 dp 即可。转移方程如下：

$$
f_{i,j}=\begin{cases}
op_i=0:f_{i-1,j}\cdot j^{len_i}\\
op_i=1:f_{i-1,j}\cdot j^{len_i}+\sum_{k=1}^{j-1}{f_{i-1,k}\cdot \left[j^{len_i}-(j-1)^{len_i}\right]}\\
op_i=2:\sum_{k=1}^{j-1}{f_{i-1}{k}}
\end{cases}
$$

时间复杂度：$O(QC\log N)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxQ = 305, kMaxC = 1e4 + 5, kMod = 1e9 + 7;

int n, q, c;
int f[2][kMaxC];
std::vector<std::pair<int, int>> vec, seg;

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

int qpow(int bs, int idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = 1ll * bs * bs % kMod)
    if (idx & 1)
      ret = 1ll * ret * bs % kMod;
  return ret;
}

void prework() {
  std::sort(vec.begin(), vec.end());
  std::vector<std::pair<int, int>> tmp;
  for (int i = 0; i < vec.size(); ++i) {
    if (!i || vec[i].first != vec[i - 1].first)
      tmp.emplace_back(vec[i].second, vec[i].first);
  }
  for (int i = 0; i < tmp.size(); ++i) {
    if (!i && tmp[i].first > 1)
      seg.emplace_back(tmp[i].first - 1, 1);
    else if (i && tmp[i].first > tmp[i - 1].second + 1)
      seg.emplace_back(tmp[i].first - tmp[i - 1].second - 1, 1);
    if (tmp[i].first != tmp[i].second)
      seg.emplace_back(tmp[i].second - tmp[i].first, 0);
    seg.emplace_back(1, 2);
    if (i + 1 == tmp.size() && tmp[i].second < n) seg.emplace_back(n - tmp[i].second, 1);
  }
}

void dickdreamer() {
  std::cin >> n >> q >> c;
  for (int i = 1; i <= q; ++i) {
    int a, h;
    std::cin >> a >> h;
    vec.emplace_back(h, a + 1);
  }
  prework();
  int o = 0;
  f[o][0] = 1;
  for (auto [len, op] : seg) {
    o ^= 1;
    std::fill_n(f[o], c + 1, 0);
    int sum = 0;
    if (op == 2) assert(len == 1);
    for (int i = 1; i <= c; ++i) {
      inc(sum, f[o ^ 1][i - 1]);
      if (op == 0) f[o][i] = 1ll * f[o ^ 1][i] * qpow(i, len) % kMod;
      else if (op == 1) f[o][i] = add(1ll * f[o ^ 1][i] * qpow(i, len) % kMod, 1ll * sum * sub(qpow(i, len), qpow(i - 1, len)) % kMod);
      else f[o][i] = sum;
    }
  }
  int ans = 0;
  for (int i = 1; i <= c; ++i) inc(ans, f[o][i]);
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