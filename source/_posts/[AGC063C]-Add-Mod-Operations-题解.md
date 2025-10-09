---
title: '[AGC063C] Add Mod Operations 题解'
date: 2024-10-08 16:54:00
---

## Description

给定两个长度为 $N$ 的非负整数序列 $A,B$。你需要通过 $0$ 至 $N$ 次以下的操作，使 $A$ 变成 $B$（如果不行，报告无解；否则给出相应构造方案，注意你并不需要最小化操作次数）：

- 选择两个整数 $x,y\ (0\le x<y\le 10^{18})$，对于所有 $1\le i\le N$，使 $A_i\leftarrow(A_i+x)\bmod y$。

## Solution

容易发现无解的条件是存在 $i,j$，满足 $a_i=a_j,b_i\neq b_j$。

先按照 $A$ 的大小对数组进行排序，考虑此时 $B$ 递增时怎么做。

我们想要通过取模让最终的数组可以自由控制。注意到先操作小的再操作大的会对后面的产生影响，这是我们不想看到的，所以倒着做。

具体的，从大到小枚举 $i$，每次做 $(x_i,a_i+x_i)$ 操作，可以让当前最大的清零。做完一轮后 $a_i=\sum_{j=1}^{i-1}{x_j}$，通过最终的数组解出 $x$ 再做一遍 $(b_1,+\infty)$ 操作即可做到 $n+1$ 次。

考虑优化。注意到最后一次操作是没有意义的，因为只做前 $n-1$ 次操作，数组是：

$$
x_2+x_3+\ldots+x_n,0,x_2,x_2+x_3,\ldots,x_2+x_3+\ldots+x_{n-1}
$$

显然同样可以通过 $b$ 数组解出 $x$。

对于 $b$ 不递增的情况可以让 $b_i\leftarrow b_i+\infty\times (i-1)$。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 1e3 + 5, kInf = 1e12;

int n;
int a[kMaxN], _a[kMaxN], b[kMaxN], x[kMaxN];
std::vector<std::pair<int, int>> res;

void work(int x, int y) {
  if (!y) return;
  x = (x % y + y) % y;
  res.emplace_back(x, y);
  // std::cerr << "fuck " << x << ' ' << y << '\n';
  for(int i = 1; i <= n; ++i) _a[i] = (_a[i] + x) % y;
}

void dickdreamer() {
  std::cin >> n;
  std::vector<std::pair<int, int>> vec(n);
  for (auto &[x, y] : vec) std::cin >> x;
  for (auto &[x, y] : vec) std::cin >> y;
  std::sort(vec.begin(), vec.end());
  for (int i = 1; i <= n; ++i)
    a[i] = _a[i] = vec[i - 1].first, b[i] = vec[i - 1].second;

  for (int i = 1; i <= n; ++i)
    for (int j = i + 1; j <= n; ++j)
      if (a[i] == a[j] && b[i] != b[j])
        return void(std::cout << "No\n");
  if (n == 1) {
    std::cout << "Yes\n1\n" << (b[1] - a[1] + kInf) % kInf << ' ' << kInf << '\n';
    return;
  }
  b[1] += (n - 1) * kInf;
  for (int i = 2; i <= n; ++i) b[i] += (i - 2) * kInf;
  // for (int i = 1; i <= n; ++i) std::cerr << a[i] << ' ';
  // std::cerr << '\n';
  // for (int i = 1; i <= n; ++i) std::cerr << b[i] << ' ';
  // std::cerr << '\n';
  x[n] = b[1] - a[1] - b[n];
  for (int i = n; i > 2; --i) x[i - 1] = b[i] - b[i - 1];
  // for (int i = 2; i <= n; ++i) std::cerr << x[i] << ' ';
  // std::cerr << '\n';
  int sum = 0;
  for (int i = n; i >= 2; --i) {
    work(x[i], a[i] + sum + x[i]);
    sum += x[i];
  }
  work(b[2], kInf);
  // for (int i = 1; i <= n; ++i) std::cerr << _a[i] << ' ';
  // std::cerr << '\n';
  std::cout << "Yes\n";
  std::cout << (int)res.size() << '\n';
  for (auto [x, y] : res) std::cout << x << ' ' << y << '\n';
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