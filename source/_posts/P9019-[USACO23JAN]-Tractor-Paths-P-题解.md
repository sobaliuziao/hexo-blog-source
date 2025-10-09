---
title: 'P9019 [USACO23JAN] Tractor Paths P 题解'
date: 2023-10-04 22:22:00
---

## Description

有 $n$ 个区间，第 $i$ 个区间为 $[l_i,r_i]$。保证 $l_1<l_2<\cdots<l_n$ 且 $r_1<r_2<\cdots<r_n$。其中一部分区间是特殊的，输入会给定。

如果第 $i$ 个区间和第 $j$ 个区间相交，那么 $i,j$ 之间有一条边。保证 $1,n$ 联通。 

给定 $Q$ 组询问，每次给定 $a,b$ 满足 $1\le a < b\le n$，你需要回答 $a$ 到 $b$ 至少要经过多少条边，以及有多少个特殊区间对应的点，使得这个点可能在 $a$ 到 $b$ 的最短路径上。

$n,Q\le 2\times 10^5$。

## Solution

显然一个区间肯定是尽量跳能跳的最远的区间，那么设 $nxt_{i}$ 表示区间 $i$ 能跳的最远的区间，第一问就可以直接倍增求了。

第二问实际上是求：

$$
\sum_{i=a}^{b}{a_i\times [dis(a,i)+dis(i,b)=dis(a,b)]}
$$

设 $dis(a,b)=len$，钦定 $dis(a,i)=x,dis(i,b)=len-x$，还是不好做。

容易发现 $\forall i\in[a,b],dis(a,i)+dis(i,b)\geq dis(a,b)$，所以只要满足 $dis(a,i)\leq x,dis(i,b)\leq len-x$ 即可。

如果设 $L_{i,j}$ 表示 $i$ 往左跳 $2^j$ 步到达的点，$R_{i,j}$ 表示 $i$ 往右跳 $2^j$ 步到达的点，那么满足条件的 $i$ 要满足 $i\in[L_{b,len-x},R_{a,x}]$，答案就是：$\sum\limits_{i=1}^{len-1}{cnt(L_{b,len-x},R_{a,x})}$

考虑设 $sum_i$ 表示前 $i$ 个区间的特殊区间的个数，$sl_{i,j}=\sum\limits_{k=i-2^j}^{i-1}{sum_{k-1}},sr_{i,j}=\sum\limits_{k=i+1}^{i+2^j}{sum_k}$。

预处理后只要在询问里面倍增即可。

时间复杂度：$O((n+q)\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n, q;
int a[kMaxN], l[kMaxN], r[kMaxN], sum[kMaxN];
int nxt[kMaxN][20], pre[kMaxN][20], sumn[kMaxN][20], sump[kMaxN][20];

int getdis(int s, int t) {
  if (s == t) return 0;
  int ret = 1;
  for (int i = 19; ~i; --i)
    if (nxt[s][i] < t)
      s = nxt[s][i], ret += (1 << i);
  return ret;
}

void dickdreamer() {
  std::string str1, str2;
  std::cin >> n >> q >> str1 >> str2;
  int ccl = 0, ccr = 0;
  for (int i = 1; i <= 2 * n; ++i) {
    if (str1[i - 1] == 'L') {
      l[++ccl] = i;
    } else {
      r[++ccr] = i;
    }
  }
  for (int i = 1; i <= n; ++i) {
    a[i] = (str2[i - 1] == '1');
    sum[i] = sum[i - 1] + a[i];
  }
  for (int i = 1; i <= n; ++i) {
    int L = i, R = n + 1, res = i;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (l[mid] <= r[i]) L = res = mid;
      else R = mid;
    }
    nxt[i][0] = res;
    sumn[i][0] = sum[res];
    L = 0, R = i, res = i;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (r[mid] >= l[i]) R = res = mid;
      else L = mid;
    }
    pre[i][0] = res;
    sump[i][0] = sum[res - 1];
  }
  for (int i = 1; i <= 19; ++i) {
    for (int j = 1; j <= n; ++j) {
      nxt[j][i] = nxt[nxt[j][i - 1]][i - 1];
      pre[j][i] = pre[pre[j][i - 1]][i - 1];
      sumn[j][i] = sumn[j][i - 1] + sumn[nxt[j][i - 1]][i - 1];
      sump[j][i] = sump[j][i - 1] + sump[pre[j][i - 1]][i - 1];
    }
  }
  for (int cs = 1; cs <= q; ++cs) {
    int s, t;
    std::cin >> s >> t;
    int mi = getdis(s, t), cnt = a[s] + a[t];
    for (int i = 19; ~i; --i)
      if ((mi - 1) >> i & 1)
        cnt -= sump[t][i], t = pre[t][i];
    for (int i = 19; ~i; --i)
      if ((mi - 1) >> i & 1)
        cnt += sumn[s][i], s = nxt[s][i];
    std::cout << mi << ' ' << cnt << '\n';
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