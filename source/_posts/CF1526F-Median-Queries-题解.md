---
title: CF1526F Median Queries 题解
date: 2024-09-20 10:59:00
---

## Description

**本题是一道交互题。**

给定 $n$，你需要猜测一个长度为 $n$ 的排列 $p$（即 $p$ 包含所有 $1$ 到 $n$ 的整数各一次）。已知 $p$ 满足 $p_1<p_2$。

当然，你可以进行询问，每次询问你需要给定三个互不相同的整数 $a,b,c$，交互器会返回 $|p_a-p_b|,|p_b-p_c|,|p_c-p_a|$ 这三个数中第二小的数。

请在 $2\times n+420$ 次询问内求出整个排列 $p$。$T$ 组数据。

交互格式如下：

- 首先你需要读入整数 $T$ 表示数据组数。接下来对于每组数据：
- 首先读入一个整数 $n$ 表示排列长度。如果你希望询问，按照 `? a b c` 的格式输出，你将收到 $|p_a-p_b|,|p_b-p_c|,|p_c-p_a|$ 中第二小的数。你需要保证 $1\leq a,b,c\leq n$，且 $a,b,c$ 互不相同。请注意，如果你的询问不合法，或者你的询问次数过多，交互器会给出 `-1` 的结果，此时你需要立即停止程序，否则可能会得到任意的评测结果。如果你希望回答，按照 `! p_1 p_2 ... p_n` 的格式输出。如果你的回答正确，交互器会给出 `1` 的结果，此时你需要直接进行下一组数据（如果有的话），否则交互器会给出 `-1` 的结果，同样的你需要立刻结束程序。

注意刷新缓冲区。

$1\leq T\leq10^3,20\leq n,\sum n\leq10^5$。

## Solution

考虑怎么一一确定每个数。

注意到如果已经直到 $1$ 和 $2$ 或 $n-1$ 和 $n$ 的位置之后，再通过 $n-2$ 次操作就能确定每个数了。

同时我们如果只知道边上的两个数，但不知道是 $1,2$ 还是 $n-1,n$，也是可以做的。因为可以先把边上的数当作 $1,2$ 确定出整个排列，如果 $p_1>p_2$ 则让 $p_i\leftarrow n-p_i+1$，否则不变。

现在问题转化为怎么找到边上的两个数。

有个不显然的观察是对于一对距离不长的 $(a,b)$，与它们距离最大的两个点一定在边界上。结论是 $b-a+1\leq\frac{n-4}{3}$ 时就是对的。

找到长度不超过 $\frac{n-4}{3}$ 的点对是简单的，可以一直随，直到随到权值 $\leq\frac{n-4}{6}$ 的 $(a,b,c)$ 即可。单次随到的概率是 $\frac{1}{9}$，$420$ 次一定能随到。

细节见代码。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n;
int p[kMaxN], val[kMaxN];
std::mt19937 rnd(std::random_device{}());

int ask(int x, int y, int z) {
  std::cout << "? " << x << ' ' << y << ' ' << z << std::endl;
  int d;
  std::cin >> d;
  return d;
}

std::tuple<int, int, int> gettuple() {
  int a = rnd() % n + 1, b = rnd() % n + 1, c = rnd() % n + 1;
  while (a == b || a == c || b == c) a = rnd() % n + 1, b = rnd() % n + 1, c = rnd() % n + 1;
  return {a, b, c};
}

std::pair<int, int> getpair() {
  int a, b, c;
  for (int c = 1; c <= 420; ++c) {
    std::tie(a, b, c) = gettuple();
    if (ask(a, b, c) <= (n - 4) / 6) return {a, b};
  }
}

void dickdreamer() {
  std::cin >> n;
  auto [a, b] = getpair();
  for (int i = 1; i <= n; ++i) {
    val[i] = 0;
    if (i != a && i != b) val[i] = ask(a, b, i);
  }
  int p1 = 0, p2 = 0;
  p1 = std::max_element(val + 1, val + 1 + n) - val;
  std::vector<int> vec;
  for (int i = 1; i <= n; ++i) {
    if (val[i] == val[p1] - 1)
      vec.emplace_back(i);
  }
  if ((int)vec.size() == 1) {
    p2 = vec[0];
  } else {
    assert(vec.size() == 2);
    if (ask(a, p1, vec[0]) < ask(a, p1, vec[1])) p2 = vec[0];
    else p2 = vec[1];
  }
  p[p1] = 1, p[p2] = 2;
  for (int i = 1; i <= n; ++i)
    if (i != p1 && i != p2)
      p[i] = ask(i, p1, p2) + 2;
  if (p[1] > p[2]) {
    for (int i = 1; i <= n; ++i)
      p[i] = n - p[i] + 1;
  }
  std::cout << "! ";
  for (int i = 1; i <= n; ++i) std::cout << p[i] << ' ';
  std::cout << std::endl;
  std::cin >> n;
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  // std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```