---
title: 'CF1693F I Might Be Wrong 题解'
date: 2025-03-22 16:29:00
---

## Description

给定一个长度为 $n$ 的 `01` 字符串 $S$。  
你可以进行下列操作任意次：

- 选择 $S$ 的一个连续子串 $S[l,r]$。  
设 $cnt_0,cnt_1$ 分别表示该子段中字符 `0` 和字符 `1` 的数量。  
则你将花费 $|cnt_0-cnt_1|+1$ 枚金币并对 $S[l,r]$ 进行升序排序。

你需要求出使 $S$ 本身升序排序所需的最少金币数。

$n\leq 2\times 10^5$。

## Solution

首先如果 $cnt_0<cnt_1$，则可以让所有数反转并翻转整个序列，容易发现答案是不变的。现在 $cnt_0\geq cnt_1$。

经过手玩可以发现每次都是选择 $cnt_0=cnt_1$ 的区间进行操作。

<details>
<summary>证明</summary>

设 $d=cnt_0-cnt_1$，现在需要证明可以通过不超过 $d+1$ 次 $cnt_0=cnt_1$ 操作将整个序列排序。

如果 $a_1=0$，则把第一个数删掉后可归纳为 $d-1$ 的问题。

如果 $a_1=1$，由于 $cnt_0>cnt_1$，所以必然存在一个前缀使得其 $0$ 和 $1$ 的个数相等，操作这个前缀并把第一个 $0$ 删掉也可归纳为 $d-1$ 的问题。

</details>

得到这个结论后就可以贪心地选择以当前第一个 `1` 为左端点的最长区间进行操作。

实现时维护一个数组 $lst_i$ 表示最后一个前缀 $cnt_0-cnt_1=i$ 的位置即可。

时间复杂度：$O(n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e5 + 5;

int n;
int a[kMaxN], lst[kMaxN];
std::string s;

void dickdreamer() {
  std::cin >> n >> s;
  int cnt[2] = {0};
  for (int i = 1; i <= n; ++i) {
    a[i] = s[i - 1] - '0';
    ++cnt[a[i]];
  }
  if (cnt[0] < cnt[1]) {
    std::swap(cnt[0], cnt[1]);
    std::reverse(a + 1, a + 1 + n);
    for (int i = 1; i <= n; ++i) a[i] ^= 1;
  }
  for (int i = 0; i <= n; ++i) lst[i] = 0;
  for (int i = 1, sum = 0; i <= n; ++i) {
    sum += (!a[i] ? 1 : -1);
    if (sum >= 0) lst[sum] = i;
  }
  int ans = 0, pos = 0;
  for (; pos < n && a[pos + 1] == 0; ++pos) {}
  if (pos == cnt[0]) return void(std::cout << "0\n");
  for (; pos < cnt[0] - cnt[1];) {
    if (!lst[pos]) break;
    pos += (lst[pos] - pos) / 2, ++ans;
  }
  std::cout << ans + 1 << '\n';
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