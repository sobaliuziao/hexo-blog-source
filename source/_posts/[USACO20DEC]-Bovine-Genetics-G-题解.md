---
title: [USACO20DEC] Bovine Genetics G 题解
date: 2022-10-09 16:26:00
---

## Description

[link](https://www.luogu.com.cn/problem/P7152)

## Solution

容易发现一种结果串的合法分割方案就对应着一种原字符串所以可以考虑 dp。

令 $f[i][a][b][c]$ 表示将 $s[1\sim i]$，且最后一个字串尾字母为 $a$，首字母为 $b$，倒数第 $2$ 段首字母为 $c$。

那么对于 $s[i]$ 则有两种可能：

1. 与 $s[i-1]$ 在同一个字串，则用 $f[i-1][lst][b][c]$ 转移，其中 $lst\neq a$ 且 $b$ 和 $c$ 随便选。
因为如果 $lst=a$，那么就在同一个字串里有两个连续且相同的字符，与题意矛盾。

2. 重新开一个字串，那么 $a$ 必须等于 $b$。用 $f[i-1][lst][b][d]$ 转移，其中 $lst=c$ 且 $d$ 随便选。

然后取和即可，这样做是 $O(64\times n^2)$ 的。

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

namespace FASTIO {
char ibuf[1 << 21], *p1 = ibuf, *p2 = ibuf;
char getc() {
  return p1 == p2 && (p2 = (p1 = ibuf) + fread(ibuf, 1, 1 << 21, stdin), p1 == p2) ? EOF : *p1++;
}
template<class T> bool read(T &x) {
  x = 0; int f = 0; char ch = getc();
  while (ch < '0' || ch > '9') f |= ch == '-', ch = getc();
  while (ch >= '0' && ch <= '9') x = (x * 10) + (ch ^ 48), ch = getc();
  x *= f; return 1;
}
template<typename A,typename ...B> bool read(A &x, B &...y) { return read(x) || read(y...); }

char obuf[1 << 21], *o1 = obuf, *o2 = obuf + (1 << 21) - 1;
void flush() { fwrite(obuf, 1, o1 - obuf, stdout), o1 = obuf; }
void putc(char x) { *o1++ = x; if (o1 == o2) flush(); }
template<class T> void write(T x) {
  if (!x) putc('0');
  if (x < 0) x = -x, putc('-');
  char c[40]; int tot = 0;
  while (x) c[++tot] = x % 10, x /= 10;
  for (int i = tot; i; --i) putc(c[i] + '0');
}
void write(char x) { putc(x); }
template<typename A,typename ...B> void write(A x, B ...y) { write(x), write(y...); }
struct Flusher {
  ~Flusher() { flush(); }
} flusher;
} // namespace FASTIO
using FASTIO::read; using FASTIO::putc; using FASTIO::write;

const int kMaxN = 1e5 + 5, kMod = 1e9 + 7;

int n;
int ss[kMaxN], f[kMaxN][4][4][4];
char s[kMaxN];

int add(int x, int y) {
  return (x + y >= kMod) ? (x + y - kMod) : (x + y);
}

int main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  scanf("%s", s + 1);
  n = strlen(s + 1);
  for (int i = 1; i <= n; ++i) {
    if (s[i] == 'A') ss[i] = 0;
    else if (s[i] == 'G') ss[i] = 1;
    else if (s[i] == 'C') ss[i] = 2;
    else if (s[i] == 'T') ss[i] = 3;
    else ss[i] = -1;
  }
  for (int i = 0; i < 4; ++i) {
    if (ss[1] != -1 && ss[1] != i) continue ;
    for (int j = 0; j < 4; ++j) {
      f[1][i][i][j] = 1;
    }
  }
  for (int i = 2; i <= n; ++i) {
    for (int a = 0; a < 4; ++a) {
      if (ss[i] != -1 && ss[i] != a) continue ;
      for (int b = 0; b < 4; ++b) { // 不重新开一段
        for (int c = 0; c < 4; ++c) {
          for (int lst = 0; lst < 4; ++lst) {
            if (lst != a) f[i][a][b][c] = add(f[i][a][b][c], f[i - 1][lst][b][c]);
          }
        }
      }
      for (int b = 0; b < 4; ++b) { // 重新开一段
        for (int c = 0; c < 4; ++c) {
          for (int lst = 0; lst < 4; ++lst) {
            if (lst == c) f[i][a][a][b] = add(f[i][a][a][b], f[i - 1][lst][b][c]);
          }
        }
      }
    }
  }
  int ans = 0;
  for (int i = 0; i < 4; ++i) {
    for (int j = 0; j < 4; ++j) {
      ans = add(ans, f[n][i][j][i]);
    }
  }
  write(ans);
  return 0;
}
```

</details>