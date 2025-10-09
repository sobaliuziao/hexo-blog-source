---
title: CF578E Walking! 题解
date: 2024-07-26 19:15:00
---

## Description

- 给定一个长度为 $n$ 的只包含 `L,R` 的字符串 $s$。
- 构造一个 $n$ 排列 $p$ 满足 $s[p_i] \ne s[p_{i+1}](1 \le i < n)$。
- 最小化 $p$ 中 $p_i > p_{i+1}(1 \le i < n)$ 的数量。
- $n \le 10^5$，数据保证有解。

## Solution

考虑把 $p$ 中的每个极长连续上升子序列拿出来，显然这些子序列为 $1,2,\ldots,n$ 的一个划分，使得每个子序列一定是 LR 交错出现。

所以第一问的答案为把 $1,2,\ldots,n$ 划分成最少的子序列数$-1$，使得每个子序列是 LR 交错出现。

有一个显然的贪心策略是从前往后扫，不妨设 $s_i$ 为 L，如果 $s_i$ 能找到末尾与其不同的子序列就把它加到那个子序列末尾，如果找不到就创建一个新的子序列。

证明就考虑如果能找到但是不加，就说明当前答案会 $+1$，如果加了顶多是后面的一个 R 找不到 L 与其配对，也只会 $+1$，并且在这之前答案一直更优。

然后需要构造方案，用 $cnt_{ij}$ 表示开头为 $i$，末尾为 $j$ 的子序列数量。

容易发现当 $cnt_{LR},cnt_{RL}\neq 0,cnt_{LL}=cnt_{RR}=0$ 时是无法直接构造方案的，这时可以任意取一对 LR 和 RL 的序列，把末尾更靠后的那个序列的末尾放到另一个序列的末尾，这样就有了 LL 和 RR。

注意到 $|cnt_{LL}-cnt_{RR}|\leq 1$，不妨设 $cnt_{LL}\geq cnt_{RR}$，可以构造：LR、LR、...、LR、LL、RL、RL、...、RL、RR、LL、RR、LL、...

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e5 + 5;

int n, tot;
std::string str;
std::vector<int> vec[2], vv[kMaxN], id[2][2];

void fix() {
  int x = id[0][1].back(), y = id[1][0].back();
  id[0][1].pop_back(), id[1][0].pop_back();
  if (vv[x].back() < vv[y].back()) std::swap(x, y);
  vv[y].emplace_back(vv[x].back()), vv[x].pop_back();
  id[str[vv[x].front()] == 'R'][str[vv[x].back()] == 'R'].emplace_back(x);
  id[str[vv[y].front()] == 'R'][str[vv[y].back()] == 'R'].emplace_back(y);
}

void print(int x) {
  for (auto i : vv[x]) std::cout << i << ' ';
}

void dickdreamer() {
  std::cin >> str;
  n = str.size(); str = " " + str;
  for (int i = 1; i <= n; ++i) {
    int c = (str[i] == 'R');
    if (!vec[c ^ 1].size()) {
      vec[c].emplace_back(++tot);
      vv[tot] = {i};
    } else {
      int t = vec[c ^ 1].back(); vec[c ^ 1].pop_back();
      vv[t].emplace_back(i), vec[c].emplace_back(t);
    }
  }
  std::cout << tot - 1 << '\n';
  for (int i = 1; i <= tot; ++i)
    id[str[vv[i].front()] == 'R'][str[vv[i].back()] == 'R'].emplace_back(i);
  if (id[0][1].size() && id[1][0].size() && !id[0][0].size() && !id[1][1].size()) fix();
  int o = 0;
  if (id[0][0].size() < id[1][1].size()) o = 1;
  for (auto x : id[o][o ^ 1]) print(x);
  if (id[o][o].size()) print(id[o][o].front());
  for (auto x : id[o ^ 1][o]) print(x);
  for (int i = 0; i < (int)id[o ^ 1][o ^ 1].size(); ++i) {
    print(id[o ^ 1][o ^ 1][i]);
    if (i + 1 < (int)id[o][o].size()) print(id[o][o][i + 1]);
  }
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