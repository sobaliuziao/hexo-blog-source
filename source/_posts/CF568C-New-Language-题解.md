---
title: CF568C New Language 题解
date: 2024-07-25 16:50:00
---

## Description

- 将 $\texttt{a} \sim \texttt{a} + l - 1$ 这 $l$ 个字符分成 $\texttt{V,C}$ 两个集合。
- 你需要构造一个**长度为 $n$** 且**满足 $m$ 个限制**且**不小于另一个长度为 $n$ 的字符串 $s$** 的**最小**字符串。
- 每一个限制为**若字符串的第 $p_1$ 个位置上的字符 $\in t_1$，则第 $p_2$ 个位置上的字符 $\in t_2$**。
- $l \le 26$，$n \le 200$，$m \le 4n(n-1)$。

## Solution

要满足答案不小于 $s$ 就直接枚举第一个与 $s$ 不同的位填的字符，然后就是判断能否让一个后缀随便填，使得其满足限制，如果能满足就直接输出最小字符串。

注意到限制类似于 2-SAT，所以先建图。

然后从前往后枚举每一位，如果这一位已经确定就填确定的，否则要选尽量小的填，所以用 tarjan 求 2-SAT 方案显然做不了，但是用 dfs 求 2-SAT 就可以贪心地判断小的是否可行，如果可行就填小的，否则判断大的是否可行，如果还不可行就不存在方案。

具体实现见代码。

时间复杂度：$O(n^2m)$，但是显然跑不满。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 405;

int l, n, m;
int mi[26][2], op[26], vis[kMaxN];
std::vector<int> G[kMaxN];
std::string s, ans;

bool dfs(int u) {
  if (vis[(u <= n) ? (u + n) : (u - n)]) return 0;
  else if (vis[u]) return 1;
  vis[u] = 1;
  for (auto v : G[u])
    if (!vis[v] && !dfs(v))
      return vis[u] = 0;
  return 1;
}

bool check(int k) { // 前 k 位确定，后面的随便填是否可行
  std::fill_n(vis + 1, 2 * n, 0);
  ans = s;
  for (int i = 1; i <= k; ++i)
    if (!dfs(i + op[s[i] - 'a'] * n))
      return 0;
  for (int i = k + 1; i <= n; ++i) {
    int x = mi[0][0], y = mi[0][1];
    if (!~x) {
      if (!dfs(i + op[y] * n)) return 0;
      ans[i] = char('a' + y);
    } else if (!~y) {
      if (!dfs(i + op[x] * n)) return 0;
      ans[i] = char('a' + x);
    } else if (x < y) {
      if (!dfs(i + op[x] * n)) {
        if (!dfs(i + op[y] * n)) return 0;
        else ans[i] = char('a' + y);
      } else {
        ans[i] = char('a' + x);
      }
    } else {
      if (!dfs(i + op[y] * n)) {
        if (!dfs(i + op[x] * n)) return 0;
        else ans[i] = char('a' + x);
      } else {
        ans[i] = char('a' + y);
      }
    }
  }
  return 1;
}

void print(std::string s) {
  for (int i = 1; i <= n; ++i) std::cout << s[i];
  std::cout << '\n';
}

void dickdreamer() {
  std::string str;
  std::cin >> str >> n >> m;
  l = str.size();
  for (int i = 0; i < l; ++i) op[i] = (str[i] == 'C');
  memset(mi, -1, sizeof(mi));
  for (int i = 0; i < l; ++i) {
    for (int j = l - 1; j >= i; --j) mi[i][op[j]] = j;
  }
  for (int i = 1; i <= m; ++i) {
    int x, y;
    std::string sx, sy;
    std::cin >> x >> sx >> y >> sy;
    int ox = (sx[0] == 'C'), oy = (sy[0] == 'C');
    G[x + ox * n].emplace_back(y + oy * n);
    G[y + (oy ^ 1) * n].emplace_back(x + (ox ^ 1) * n);
  }
  std::cin >> s; s = " " + s;
  if (check(n)) return print(s);
  for (int i = n; i; --i) {
    int now = s[i] - 'a', x = mi[now + 1][0], y = mi[now + 1][1];
    if (!~x && !~y) {
      continue;
    } else if (!~x) {
      s[i] = char(y + 'a');
      if (!check(i)) continue;
      else return print(ans);
    } else if (!~y) {
      s[i] = char(x + 'a');
      if (!check(i)) continue;
      else return print(ans);
    } else {
      if (x < y) {
        s[i] = char(x + 'a');
        if (!check(i)) {
          s[i] = char(y + 'a');
          if (!check(i)) continue;
          else return print(ans);
        } else {
          return print(ans);
        }
      } else {
        s[i] = char(y + 'a');
        if (!check(i)) {
          s[i] = char(x + 'a');
          if (!check(i)) continue;
          else return print(ans);
        } else {
          return print(ans);
        }
      }
    }
    s[i] = char(now + 'a');
  }
  std::cout << "-1\n";
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