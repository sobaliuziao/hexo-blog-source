---
title: 'P12546 [UOI 2025] Convex Array 题解'
date: 2025-05-21 10:38:00
---

## Description

给定一个长度为 $n$ 的整数数组 $a$。

判断是否存在一种元素排列 $b$，使得对于每个 $2 \leq i \leq n-1$，都满足条件 $b_{i-1} + b_{i+1} \geq 2 \cdot b_i$。

本题中，每个测试点包含多组输入数据。你需要对每组数据独立求解。

$\sum n\leq 3\times 10^5$。

## Solution

先把 $a_i$ 排序，那么问题可以看成将 $a_2,a_3,\ldots,a_n$ 划分成两个集合，每个集合分别和 $a_1$ 构成的序列都是上凸的。

考虑 dp。

设 $f_{i,b,c,d}$ 表示扫了前 $i$ 个数，第一个集合末尾为 $a_i$ 和 $a_b$，第二个集合末尾为 $a_c$ 和 $a_d$。直接转移是 $O(n^4)$ 的。

注意到 $b,c$ 中至少有一个是 $i-1$，所以状态数变为 $O(n^3)$。

不妨设 $b=i-1$，那么固定 $c$ 之后，一定是让 $d$ 越大越好，所以可以改变状态，$f_{i,c}$ 表示满足条件的状态 $(i,i-1,c,d)$ 的最大的 $d$。

如果 $c=i-1$，则一定满足 $b=i-2$ 或者 $d=i-2$，这两种状态同样只需要记录最大的第四者，所以这里只有两种状态，容易分讨转移。

考虑 $b=i-1$ 怎么转移。

1. $i+1$ 放在第一个集合：即如果 $a_{i+1}+a_{i-1}\geq 2a_i$，则转移到 $(i+1,i,c,d)$。
2. $i+1$ 放在第二个集合：如果 $a_{i+1}+a_d\geq 2a_c$，转移到 $(i,i-1,i+1,c)$。

观察第二种转移，容易想到维护一个 $(2a_c-a_d,c)$ 的集合，可以用动态开点线段树做，不过也可以用 set 维护一个两维分别递增的集合，只有这个集合内的数是有用的，插入时简单维护即可。而第一种转移的意思就是要不要清空 set，同样容易维护。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 3e5 + 5;

int n;
int a[kMaxN];
std::set<std::pair<int, int>> st;

void ins(int c, int d) {
  if (c == -1 || d == -1) return;
  std::pair<int, int> p = {2 * a[c] - a[d], c};
  auto it = st.lower_bound({p.first, 0});
  for (; it != st.end() && it->second < c;) {
    st.erase(it);
    it = st.lower_bound({p.first, 0});
  }
  if (it != st.end() && it->first == p.first && it->second > c) return;
  if (it != st.begin()) {
    --it;
    if (it->second < c) st.emplace(p);
  } else {
    st.emplace(p);
  }
}

int get(int x) {
  auto it = st.lower_bound({a[x] + 1, 0});
  if (it != st.begin()) return prev(it)->second;
  else return -1;
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  st.clear();
  std::sort(a + 1, a + 1 + n);
  a[0] = 1e18, a[++n] = a[1];
  std::sort(a + 1, a + 1 + n);
  int d1 = 0, d2 = 0;
  for (int i = 2; i <= n - 1; ++i) {
    int _d1 = -1, _d2 = -1;
    _d2 = std::max(_d2, get(i + 1));
    if (a[i + 1] + a[i - 1] < 2 * a[i]) st.clear();
    if (~d1) {
      if (a[i + 1] + a[i - 2] >= 2 * a[i]) ins(i - 1, d1);
      if (a[i + 1] + a[d1] >= 2 * a[i - 1]) _d1 = std::max(_d1, i - 2);
    }
    if (~d2) {
      if (a[i + 1] + a[d2] >= 2 * a[i]) ins(i - 1, i - 2);
      if (a[i + 1] + a[i - 2] >= 2 * a[i - 1]) _d1 = std::max(_d1, d2);
    }
    d1 = _d1, d2 = _d2;
  }
  std::cout << ((~d1 || ~d2 || st.size()) ? "YES\n" : "NO\n");
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