---
title: 'P6922 [ICPC2016 WF] Longest Rivers 题解'
date: 2023-12-25 15:48:00
---

## Description

有 $n$ 条河和 $m+1$ 个交汇处构成一棵以 $0$ 号点（即大海） 为根的树。

每条河有各自的名称。对于一个交汇处，从它流出的干流的名称是流入这个交汇处的各个支流的名称之一。一条河流的长度是以它为名称的河流的长度之和。对于一个可能的命名方案，一条河流的排名等于长度大于它的河流数 $+1$ 。

对于每条河，求出它在所有命名方案中，最小的排名。

$n,m\leq 5\times 10^5$。

## Solution

先考虑对于每条河怎么 $O(n)$ 求答案。

容易发现当前河一定要一冲到底，设长度为 $L$，那么就要要求其余长度 $>L$ 的河流数量最少。

然后从下往上考虑每个点，有下面 2 种情况：

1. 如果有儿子流过来是长的，那么当前点就流这个最长的。
2. 如果儿子流过来全是短的，那么流里面最短的。

这样递归处理即可做到 $O(n)$。

---

考虑怎样一次求出所有的答案。

这里有个转化就是只要求出所有河流中 $>L$ 的河流的最小数量，而不用考虑当前河是否要连到根。

因为如果一个最小数量的方案当前河没有连到根，那么把当前河到根的路径上全都连到当前河一定不会更劣。

然后从小到大枚举 $L$，这时候有 3 种情况：

1. 有儿子流过来是长的。
2. 儿子流过来全是短的，但最短的流完当前点到父亲的边后变长。
3. 儿子流过来全是短的，但最短的流完当前点到父亲的边后还是短的。

容易发现答案就是 2 号点的数量$+1$，并且随着 $L$ 的增大，部分 2 号点会变为 3 号点，1 号点可能会变成 2 或 3 号点。

设 $f_i$ 表示将 $i$ 从 2 变到 3 的最小长度。

那么只要用一个 pair 的优先队列维护所有 2 号点，其中 $\{l,x\}$ 分别表示 $x$ 需要从 2 变到 3 的最小长度和当前点的编号。

每次从队列中取出 $l$ 最小的 $x$，然后不停跳父亲，如果这个祖先 $y$ 的所有儿子都变 3 并且 $f_y\leq L$ 说明 $y$ 也是 3 号点，就继续跳，否则退出。

最后如果跳出来一个 $y$，使得他的所有儿子全是 3 并且 $f_y>L$ 就说明他变成了个 2 号点，加到队列里即可。

如果要输出一个任意 $L$ 的答案，就只要找到求出的所有答案中小于等于 $L$ 的最大长度的答案即可。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e6 + 5;
const int64_t kInf = 1e18;

int n, m;
int fa[kMaxN], w[kMaxN], cnt[kMaxN];
int64_t sum[kMaxN], f[kMaxN];
std::string name[kMaxN];
std::vector<int> G[kMaxN];
std::map<int64_t, int> mp;
std::priority_queue<std::pair<int64_t, int>, std::vector<std::pair<int64_t, int>>, std::greater<std::pair<int64_t, int>>> q;

void dfs(int u) {
  int64_t minn = kInf;
  for (auto v : G[u]) {
    sum[v] = sum[u] + w[v];
    dfs(v);
    minn = std::min(minn, f[v]);
    ++cnt[u];
  }
  if (minn == kInf) f[u] = w[u];
  else f[u] = minn + w[u];
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = m + 1; i <= m + n; ++i) {
    std::cin >> name[i] >> fa[i] >> w[i];
    G[fa[i]].emplace_back(i);
  }
  for (int i = 1; i <= m; ++i) {
    std::cin >> fa[i] >> w[i];
    G[fa[i]].emplace_back(i);
  }
  dfs(0);
  for (int i = m + 1; i <= m + n; ++i)
    q.emplace(f[i], i);
  for (; !q.empty();) {
    auto [L, u] = q.top();
    q.pop();
    --cnt[fa[u]];
    for (u = fa[u]; u && !cnt[u]; u = fa[u]) {
      if (L >= f[u]) {
        --cnt[fa[u]];
      } else {
        q.emplace(f[u], u);
        break;
      }
    }
    mp[L] = q.size() + 1;
  }
  mp[kInf] = 0;
  for (int i = m + 1; i <= m + n; ++i)
    std::cout << name[i] << ' ' << prev(mp.upper_bound(sum[i]))->second << '\n';
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