---
title: CF1718D Permutation for Burenka 题解
date: 2025-03-19 14:36:00
---

## Description

如果一个数组里面任意两个数字都是不同的，我们把这种数组称作为一个“纯数组”。举个例子。$[1,7,9]$ 是纯数组，$[1,3,3,7]$ 不是，因为 $3$ 出现了两次。

如果两个纯数组 $b,c$ 的长度相等且“类似”，并且对于所有数组中的 $l$ 和 $r (l \leq l \leq r \leq n)$，都满足

$\text{argmax}([b_l,b_{l+1}, \ldots, b_r])= \text{argmax}([c_l,c_{l+1}, \ldots, c_r]).$

$\text{argmax(x)}$ 返回值是 $x$ 中最大值的下标。举个例子，$\text{argmax}([1337,179,57])=1.$

最近，Tonya 发现 Burenka 非常喜欢长度为 $n$ 的排列 $p$。 Tonya 为了让她开心，于是给她一个类似于 $p$ 的数组。他已经修复了 $a$ 的一些元素，但恰好缺少 $k$ 个元素（在这些位置 $a_i$ 暂时等于 $0$）。保证$k≥2$。此外，他有一个由 $k-1$ 个数字组成的集合 $S$。

Tonya 意识到他缺少一个数字来填补 $a$ 的空白，所以他决定买下它。他有 $q$ 个购买的选项。 Tonya 认为数字 $d$ 适合他，如果可以用来自 $S$ 的数字和数字 $d$ 替换 $a$ 中的所有零，那么 $a$ 就变成了一个类似于 $p$ 的纯数组。对于 $d$ 的每个选项，输出这个数字是否适合他。

$1\leq n,q\leq 3\times 10^5$。

## Solution

首先两个序列类似当且仅当它们的笛卡尔树相同。

现在考虑对于给定的填空数，怎么 check 其是否合法。

先把笛卡尔树建出来，那么对于这棵树上的每个空缺的位置都有个限制区间 $[l_i,r_i]$，表示这个位置能填的数所在的区间。

显然 $l_i$ 为 $i$ 子树内已填点的数的最大值加一，$r_i$ 为 $i$ 的祖先已填的最小值减一。

有个结论是能把 $s_1,s_2,\ldots,s_k$ 填到这 $k$ 个限制区间内即合法，不用考虑这些要填的数之间的大小关系。

<details>
<summary>证明</summary>

因为如果存在 $i$ 是 $j$ 的祖先，且 $i$ 填的数 $a_i$ 小于 $j$ 填的数 $a_j$，由于 $l_i<a_i<r_i$，$l_j<a_j<r_j$，并且 $l_i\geq l_j,r_i\leq r_j$，所以将它们交换一定合法。

一直交换下去一定能满足条件。

</details>

那么现在问题转化为了有 $k$ 个位置，每个位置可以填 $[l_i,r_i]$ 内的数，问能否填完。

对于单组询问是个经典的贪心：先按照 $r$ 对区间排序，每次选择 $[l_i,r_i]$ 内最小的数填，如果找不到就无解。

时间复杂度：$O(nq\log n)$。

---

考虑优化。

现在把 $d$ 去掉，再用同样的方式做上面的贪心，如果在加入 $[l_i,r_i]$ 时找不到了，就说明 $d$ 必须小于等于 $r_i$，因为如果 $d$ 不满足这个条件，前 $i$ 个区间一定无解。然后继续对于后面的区间贪心，如果还有不满足条件的则对于任何 $d$ 都无解。

<details>
<summary>证明</summary>

这里可以把 $d$ 看成 $r_i$，因为对于 $i$ 后面的区间来说 $d$ 越大一定越优，如果这么做仍然不满足条件则一定无解。

</details>

同样地倒着做可以得到 $d$ 的下界，可以证明在得到的上下界之间就一定合法。

---

证明就考虑这是个完美匹配问题，可以用 Hall 定理转化为下面的形式：如果存在一个区间 $[l,r]$，完全包含于 $[l,r]$ 的区间数大于 $r-l+1$ 则无解，否则有解。

那么设 $F(l,r)$ 表示完全包含于 $[l,r]$ 的区间数，$G(l,r)=F(l,r)-(r-l+1)$。

如果存在 $G(l,r)\geq 2$ 则无解，因为需要加入两个数才能使其满足条件，同时上面已经给出构造性证明了。

那么 $d$ 的取值范围即为所有满足 $G(l,r)=1$ 的区间的交，而上面的贪心从小到大枚举 $r$，如果到 $R$ 就选不出来了就说明最小的右端点为 $R$，所以上面的做法得到的区间就是所有 $G(l,r)=1$ 的区间的交。

时间复杂度：$O(n\log n+q)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 3e5 + 5;

int n, q, k, rt, L, R;
int p[kMaxN], ls[kMaxN], rs[kMaxN];
int a[kMaxN], pos[kMaxN], s[kMaxN], ll[kMaxN], rr[kMaxN], l[kMaxN], r[kMaxN];

void build() {
  static int stk[kMaxN];
  int top = 0;
  rt = 0;
  for (int i = 1; i <= n; ++i) {
    ls[i] = rs[i] = 0;
    for (; top && p[stk[top]] < p[i]; ls[i] = stk[top--]) {}
    if (top) rs[stk[top]] = i;
    stk[++top] = i;
  }
  rt = stk[1];
}

void dfs(int u) {
  if (a[u]) ll[u] = std::max(ll[u], a[u]), rr[u] = std::min(rr[u], a[u]);
  if (ls[u]) {
    rr[ls[u]] = rr[u];
    if (a[u]) rr[ls[u]] = std::min(rr[ls[u]], a[u] - 1);
    dfs(ls[u]);
    ll[u] = std::max({ll[u], ll[ls[u]], a[ls[u]] + 1});
  }
  if (rs[u]) {
    rr[rs[u]] = rr[u];
    if (a[u]) rr[rs[u]] = std::min(rr[rs[u]], a[u] - 1);
    dfs(rs[u]);
    ll[u] = std::max({ll[u], ll[rs[u]], a[rs[u]] + 1});
  }
  if (!a[u]) l[pos[u]] = ll[u], r[pos[u]] = rr[u];
}

void getseg() {
  L = 1, R = 1e6;
  std::vector<std::pair<int, int>> vec;
  for (int i = 1; i <= k; ++i) {
    // std::cerr << l[i] << ' ' << r[i] << '\n';
    if (l[i] > r[i]) return void(R = 0);
    vec.emplace_back(l[i], r[i]);
  }
  std::sort(vec.begin(), vec.end(), [&] (auto p1, auto p2) { return p1.second < p2.second; });
  std::set<int> st;
  for (int i = 1; i <= k - 1; ++i) st.emplace(s[i]);
  bool fl = 0;
  for (auto [l, r] : vec) {
    auto it = st.lower_bound(l);
    if (it != st.end() && *it <= r) {
      st.erase(it);
    } else {
      if (fl) return void(R = 0);
      fl = 1, R = r;
    }
  }
  
  std::sort(vec.begin(), vec.end(), [&] (auto p1, auto p2) { return p1.first > p2.first; });
  fl = 0, st.clear();
  for (int i = 1; i <= k - 1; ++i) st.emplace(s[i]);
  for (auto [l, r] : vec) {
    auto it = st.upper_bound(r);
    if (it != st.begin() && *--it >= l) {
      st.erase(it);
    } else {
      if (fl) return void(R = 0);
      fl = 1, L = l;
    }
  }
}

void dickdreamer() {
  std::cin >> n >> q; k = 0;
  for (int i = 1; i <= n; ++i) std::cin >> p[i];
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
    if (!a[i]) pos[i] = ++k;
  }
  for (int i = 1; i <= k - 1; ++i) std::cin >> s[i];
  build();
  for (int i = 1; i <= n; ++i)
    ll[i] = 1, rr[i] = 1e6;
  dfs(rt), getseg();
  for (int i = 1; i <= n; ++i)
    if (ll[i] > rr[i])
      R = 0;
  for (int i = 1; i <= q; ++i) {
    int d;
    std::cin >> d;
    std::cout << (d >= L && d <= R ? "YES\n" : "NO\n");
  }
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