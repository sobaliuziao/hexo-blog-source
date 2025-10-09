---
title: CF559E Gerald and Path 题解
date: 2024-07-25 14:24:00
---

## Description

- 有 $n$ 条线段。
- 每条线段给定其中一端的位置及长度。
- 求所有线段覆盖的最大长度。
- $n \le 100$。

## Solution

考虑 dp。

先按照一端的位置进行排序，设 $f_{i,j,0/1}$ 表示前 $i$ 个线段，右端点最靠右的线段是 $j$ 向左/右覆盖，所有线段的最大长度。

直接枚举 $i+1$ 转移可能会出现 $i+1$ 完全覆盖了 $j$ 而无法算贡献，但是思考一下会发现如果 $i+1$ 完全覆盖 $j$ 则把 $j$ 删掉也毫无影响，所以只用钦定 $j$ 没有被完全覆盖，然后枚举下一个对答案有影响的线段。

设 $d_0$ 为 $k$ 倒的方向，转移即为：$f_{k,k,d_0}\leftarrow f_{i,j,d}+\min\{pos_k+d_0 len_k-(pos_j+d\cdot len_j), len_k\}$。

但是可能会出现这种情况：

![](https://cdn.luogu.com.cn/upload/image_hosting/6op82xst.png)

红的是枚举的下一个线段 $k$，但是可能 $k$ 向左并且存在一个 $x$ 使得 $i<x<k$ 且 $pos_x+len_x>pos_k$，此时 $x$ 也会有贡献，贡献显然为 $pos_x+len_x-pos_k$。

容易发现 $x$ 对答案的贡献只与其右端点有关，并且这些线段一定是向右倒，所以枚举下一个没有完全覆盖的线段 $k$ 时还需要维护位于 $(i,k)$ 这个区间里往右倒的线段的右端点最大值。

转移即为 $f_{k,x,1}\leftarrow f_{i,j,d}+\min\{pos_k+d_0 len_k-(pos_j+d\cdot len_j), len_k\}+(pos_x+len_x-(pos_k+d_0 len_k))$。

具体见代码。

时间复杂度：$O(n^2)$。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

const int kMaxN = 105;

int n;
int f[kMaxN][kMaxN][2];
std::pair<int, int> a[kMaxN];

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i].first >> a[i].second;
  std::sort(a + 1, a + 1 + n);
  a[0].first = -1e9;
  for (int i = 0; i <= n; ++i) {
    f[i][i][0] = std::max(f[i][i][0], a[i].second);
    f[i][i][1] = std::max(f[i][i][1], a[i].second);
    if (i == n) continue;
    for (int j = 0; j <= i; ++j) {
      for (int d = 0; d < 2; ++d) {
        int r = a[j].first + d * a[j].second;
        f[i + 1][j][d] = std::max(f[i + 1][j][d], f[i][j][d]);
        std::tuple<int, int, int> t = {-1e9, 0, 0};
        for (int tj = i + 1; tj <= n; ++tj) {
          for (int td = 0; td < 2; ++td) {
            int tr = a[tj].first + td * a[tj].second;
            t = std::max(t, {tr, tj, td});
            auto [_r, _j, _d] = t;
            f[tj][_j][_d] = std::max(f[tj][_j][_d], f[i][j][d] + std::min(tr - r, a[tj].second) + _r - tr);
          }
        }
      }
    }
  }
  int ans = 0;
  for (int i = 1; i <= n; ++i)
    for (int j = 1; j <= i; ++j)
      ans = std::max({ans, f[i][j][0], f[i][j][1]});
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