---
title: [ARC058F] Iroha Loves Strings 题解
date: 2024-09-29 21:50:00
---

## Description

给你 $n$ 个字符串，请你从中选出若干个，按给出顺序连接起来。选出字符串的总长必须等于 $k$，求字典序最小的。保证有解。

$1 \leq n \leq 2000$，$1\leq k \leq 10^4$，字符串总长不超过 $10^6$。

## Solution

显然是个 dp。

有个暴力的想法是设 $f_{i,j}$ 表示前 $i$ 个字符串组合成的长度为 $j$ 的最小字符串，总状态数是 $nk$，但是字符串总长为 $O(nk^2)$，过不了。

考虑优化。

先用 01 背包求出后缀能够拼出的所有长度，对于 $f_{i,j}$，如果 $[i+1,n]$ 这些字符串无法拼出 $k-j$ 就把 $f_{i,j}$ 扔掉。

对于剩下的字符串，如果 $f_{i,j}$ 和 $f_{i,k}$ 都不为互相的前缀且 $f_{i,j}<f_{i,k}$，则 $f_{i,k}$ 无论怎么拼都无法优于 $f_{i,j}$，可以把 $f_{i,k}$ 扔掉。

设剩下的最长的字符串为母串，则所有剩下的 $f_{i,j}$ 一定是母串的前缀，所以维护这个母串和每个 $f_{i,j}$ 的长度即可让状态能被承受。

---

然后考虑怎么转移。

先从小到大枚举 $j$，则 $f_{i,j}=\min\left\{f_{i-1,j},f_{i-1,j-|s_i|}+s_i\right\}$，可以用二分+哈希得到。同时维护一个从栈顶到栈底长度从大到小的单调栈，表示当前求出的有用的状态。

如果 $f_{i,top}$ 是 $f_{i,j}$ 的前缀，就直接将 $f_{i,j}$ 放到栈顶。如果 $f_{i,j}>f_{i,top}$，$f_{i,j}$ 就没用了。否则就一直弹栈直到栈顶是 $f_{i,j}$ 的前缀后再把 $f_{i,j}$ 加到栈里。

时间复杂度：$O\left(nk\log k+\sum\left|s_i\right|\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using u64 = uint64_t;

const int kMaxN = 2e3 + 5, kMaxK = 1e4 + 5, kMod = 998244353;

int n, k, m, sz;
int len[kMaxN], pos[kMaxK], hs1[kMaxK], pw[kMaxK];
bool vis[kMaxK];
std::pair<int, int> stk[kMaxK];
std::bitset<kMaxK> f[kMaxN];
std::string s[kMaxN], str;
std::vector<int> hs2[kMaxN];

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

void prework() {
  for (int i = 1; i <= n; ++i) {
    hs2[i].resize(len[i] + 1);
    for (int j = 1; j <= len[i]; ++j)
      hs2[i][j] = add(13331ll * hs2[i][j - 1] % kMod, s[i][j]);
  }
  pw[0] = 1;
  for (int i = 1; i <= k; ++i) pw[i] = 13331ll * pw[i - 1] % kMod;
}

u64 gethash(int p, int r, int pos, int o = 0) {
  if (!o || r <= pos) return hs1[r];
  else return add(1ll * hs1[pos] * pw[r - pos] % kMod, hs2[p][r - pos]);
}

bool cmp(int p, std::pair<int, int> p1, std::pair<int, int> p2) { // p1 <= p2
  int len1 = p1.first + p1.second * len[p], len2 = p2.first + p2.second * len[p];
  int L = 0, R = std::min(len1, len2) + 1, res = 0;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (gethash(p, mid, p1.first, p1.second) == gethash(p, mid, p2.first, p2.second)) L = res = mid;
    else R = mid;
  }
  if (res == std::min(len1, len2)) return len1 <= len2;
  else {
    ++res;
    char c1, c2;
    if (res <= p1.first) c1 = str[res];
    else c1 = s[p][res - p1.first];
    if (res <= p2.first) c2 = str[res];
    else c2 = s[p][res - p2.first];
    return c1 <= c2;
  }
}

bool checkpre(int p, std::pair<int, int> p1, std::pair<int, int> p2) {
  int len1 = p1.first + p1.second * len[p];
  int len2 = p2.first + p2.second * len[p];
  if (len1 > len2) return 0;
  return gethash(p, len1, p1.first, p1.second) == gethash(p, len1, p2.first, p2.second);
}

std::pair<int, int> getmin(int p, std::pair<int, int> p1, std::pair<int, int> p2) {
  return cmp(p, p1, p2) ? p1 : p2;
}

void dickdreamer() {
  std::cin >> n >> k;
  for (int i = 1; i <= n; ++i) {
    std::cin >> s[i];
    len[i] = (int)s[i].size();
    s[i] = " " + s[i];
  }
  prework();
  f[n + 1][0] = 1;
  for (int i = n; i; --i) {
    f[i] = f[i + 1] | (f[i + 1] << len[i]);
  }
  str = " " + str, pos[++m] = 0, vis[0] = 1;
  for (int i = 1; i <= n; ++i) {
    int top = 0;
    for (int j = 0; j <= k; ++j) {
      if (!f[i + 1][k - j]) continue;
      std::pair<int, int> now = {0, 0};
      if (vis[j]) now = {j, 0};
      if (j >= len[i] && vis[j - len[i]]) {
        if (!now.first && !now.second) now = {j - len[i], 1};
        else now = getmin(i, now, {j - len[i], 1});
      }
      if (j && !now.first && !now.second) continue;
      if (!top) {
        stk[++top] = now;
      } else {
        if (checkpre(i, stk[top], now) || cmp(i, now, stk[top])) {
          for (; top && !checkpre(i, stk[top], now); --top) {}
          stk[++top] = now;
        }
      }
    }
    std::fill_n(vis, k + 1, 0);
    m = top;
    for (int j = 1; j <= top; ++j) pos[j] = stk[j].first + stk[j].second * len[i];
    str.resize(stk[m].first + 1);
    if (stk[m].second) {
      for (int j = 1; j <= len[i]; ++j) str.push_back(s[i][j]);
    }
    sz = (int)str.size() - 1;
    for (int j = 1; j <= sz; ++j)
      hs1[j] = add(13331ll * hs1[j - 1] % kMod, str[j]);
    for (int j = 1; j <= m; ++j) vis[pos[j]] = 1;
  }
  for (int i = 1; i < (int)str.size(); ++i) std::cout << str[i];
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