---
title: 'CF585F Digits of Number Pi 题解'
date: 2024-07-26 21:52:00
---

## Description

给定长度为 $n$ 的数字串 $s$ 和长度为 $d$ 的不含前导零的数字串 $x,y(x \le y)$。

求**存在长度至少为 $\left\lfloor\frac{d}{2}\right\rfloor$ 的子串是 $s$ 的子串**的数字串 $t \in [x,y]$ 的数量。

$n \le 10^3$，$d \le 50$，答案对 $10^9+7$ 取模。

## Solution

先把 $s$ 所有长度为 $\left\lfloor\frac{d}{2}\right\rfloor$ 的子串拿出来，那么相当于要求这些子串必须在 $t$ 里出现，考虑用总数减去没出现的数量。

考虑用 $[0,y]$ 的答案减去 $[0,x-1]$ 的答案，这样就只有上界了。

注意到这里是很多个字符串匹配一个串，考虑把 $s$ 的这些子串加到 AC 自动机里，那么这些子串没在 $t$ 里出现当且仅当从前往后扫 $t$ 的每一个字符，每次让 $cur\leftarrow trie_{cur,t_i}$，如果这里的 $cur$ 每次都不在 $s$ 子串对应的节点上就说明子串没在 $t$ 里出现。

这样就可以 dp 了。设 $f_{i,j,0/1}$ 表示 $1\sim i-1$ 走到 $j$，$i\sim n$ 每次不走子串对应节点，后面有没有卡上界的限制的方案数。

转移就每次枚举 $t_i$ 即可。

时间复杂度：$O\left(|\Sigma|^2nd^2\right)$，$|\Sigma|$ 为字符集大小。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1e3 + 5, kMaxD = 55, kMaxT = kMaxN * kMaxD * 5, kMod = 1e9 + 7;

int n, d, tot;
int a[kMaxN], trie[kMaxT][10], fail[kMaxT], f[kMaxD][kMaxT][2];
bool tag[kMaxT], vis[kMaxD][kMaxT][2];
std::string s, L, R;

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

std::string sub(std::string s) {
  for (int i = d; i; --i) {
    if (s[i] != '0') {
      --s[i];
      for (int j = i + 1; j <= d; ++j) s[j] = '9';
      break;
    }
  }
  return s;
}

void ins(std::string s) {
  int cur = 0;
  for (auto c : s) {
    int k = c - '0';
    if (!trie[cur][k]) trie[cur][k] = ++tot;
    cur = trie[cur][k];
  }
  tag[cur] = 1;
}

void build() {
  std::queue<int> q;
  for (int i = 0; i < 10; ++i) {
    if (trie[0][i]) {
      q.emplace(trie[0][i]);
    }
  }
  for (; !q.empty();) {
    int u = q.front(); q.pop();
    for (int i = 0; i < 10; ++i) {
      if (trie[u][i]) {
        fail[trie[u][i]] = trie[fail[u]][i];
        q.emplace(trie[u][i]);
      } else {
        trie[u][i] = trie[fail[u]][i];
      }
    }
  }
}

int dfs(int x, int k, bool op) {
  if (x > d || tag[k]) return !tag[k];
  else if (vis[x][k][op]) return f[x][k][op];
  int ret = 0;
  for (int i = 0; i <= (op ? a[x] : 9); ++i) {
    inc(ret, dfs(x + 1, trie[k][i], op && (i == a[x])));
  }
  vis[x][k][op] = 1;
  return f[x][k][op] = ret;
}

int solve(std::string t) {
  for (int i = 1; i <= d; ++i) a[i] = t[i] - '0';
  int ans = 0;
  for (int i = 1; i <= d; ++i) ans = (10ll * ans + a[i]) % kMod;
  memset(f, 0, sizeof(f)), memset(vis, 0, sizeof(vis));
  return sub(ans, dfs(1, 0, 1));
}

void dickdreamer() {
  std::cin >> s >> L >> R;
  n = s.size(), d = L.size();
  s = " " + s, L = " " + L, R = " " + R;
  for (int i = 1; i <= n - (d / 2) + 1; ++i)
    ins(s.substr(i, d / 2));
  build();
  std::cout << sub(solve(R), solve(sub(L))) << '\n';
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