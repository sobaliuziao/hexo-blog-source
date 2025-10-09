---
title: [JOI2018] Dango Maker 题解
date: 2022-10-07 21:40:00
---

## Description

[link](https://www.luogu.com.cn/problem/P7668)

## Solution

如果两个团子重合肯定是下面三种情况：

```
  R          RGW          R
  G          G           RGW
RGW          W            W
```

我们会发现两个重合团子的 `G` 一定是在从右上到左下的对角线上的，且距离小于等于 $1$。根据这个性质就可以发现任意两个对角线上的团子肯定互不影响，那么对于每一个对角线进行 dp 即可。

其中 $f[i][0/1/2]$ 表示当前对角线上前 $i$ 行，第 $i$ 行的团子 不放/横放/竖放 的最大团子数，依次递推即可。

时间复杂度：$O(nm)$，吊打二分图。
## Code

<details>
<summary>代码</summary>

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include <debug.h>
#else
#define debug(...) 1
#endif

#define file(s) freopen(s".in", "r", stdin), freopen(s".out", "w", stdout)

using namespace std;

int read() {
  int x = 0, f = 0; char ch = getchar();
  while (ch < '0' || ch > '9') f |= ch == '-', ch = getchar();
  while (ch >= '0' && ch <= '9') x = (x * 10) + (ch ^ 48), ch = getchar();
  return f ? -x : x;
}

const int kMaxN = 3005;

int n, m, ans;
int f[kMaxN][3]; // 0/1/2 : 不放/横放/竖放
char s[kMaxN][kMaxN];

int main() {
  scanf("%d%d", &n, &m);
  for (int i = 1; i <= n; ++i) {
    scanf("%s", s[i] + 1);
  }
  for (int sm = 2; sm <= n + m; ++sm) {
    memset(f, 0, sizeof(f));
    int tmp = 0;
    for (int i = max(1, sm - m), j = sm - i; i <= n && j; ++i, --j) {
      f[i][0] = max({f[i - 1][0], f[i - 1][1], f[i - 1][2]});
      if (s[i][j] == 'G') {
        if (s[i - 1][j] == 'R' && s[i + 1][j] == 'W') 
          f[i][1] = max(f[i][1], max(f[i - 1][0], f[i - 1][1]) + 1);
        if (s[i][j - 1] == 'R' && s[i][j + 1] == 'W')
          f[i][2] = max(f[i][2], max(f[i - 1][0], f[i - 1][2]) + 1);
      }
      tmp = max(tmp, max({f[i][0], f[i][1], f[i][2]}));
    }
    ans += tmp;
  }
  printf("%d\n", ans);
  return 0;
}
```

</details>