---
title: '[NOIP2011 提高组] Mayan 游戏 题解'
date: 2022-10-01 20:29:00
---

## Description

[link](https://www.luogu.com.cn/problem/P1312)

## Solution

令当当前棋盘为 $a$。

注意到  $n\leq 5$ 且棋盘是 $5\times7$ 的，所以直接爆搜可以做到 $O(35^5)=O(52521875)$，然而这里还有很大的常数，所以需要剪枝。

剪枝 1：对于第 $i$ 列，第 $j$ 行的方块，如果 $a_{i,j}=0$ 就剪掉，这是显然的。

剪枝 2：对于第 $i$ 列，第 $j$ 行的方块，如果 $j\geq 1$ 并且 $a_{i,j-1}=a_{i,j}$ 就剪掉。因为两个相同颜色的块互换没有任何意义。

剪枝 3：对于第 $i$ 列，第 $j$ 行的方块，如果 $j\leq 5$ 并且 $a_{i,j+1}\neq 0$ 就剪掉。因为在 `剪枝2` 中遍历到 $i,j+1$ 时并不会被剪掉，所以这种情况会算重。
并且当 $a_{i,j+1}=0$ 时，遍历到 $i,j+1$ 时会被 `剪枝1` 剪掉，所以这个要算上。

## Code

<details>
<summary>代码</summary>

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include <debug.h>
#else
#define debug(...) 114514
#endif

using namespace std;

typedef vector<int> ln;
typedef unsigned long long ull;

const int dx[] = {1, -1}, dy[] = {0, 0};

int n, cnt;
int a[6][3];
int l[5][7], nw[5][7];

void print() {
  for (int i = 0; i < 5; ++i, fprintf(stderr, "\n")) {
    fprintf(stderr, "%d : ", i);
    for (int j = 0; j < 7 && nw[i][j]; ++j, fprintf(stderr, " ")) {
      fprintf(stderr, "%d", nw[i][j]);
    }
  }
}

bool clr() {
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      if (nw[i][j]) return 0;
    }
  }
  return 1;
}

void check() {
  for (int i = 1; i <= n; ++i) {
    cout << a[i][0] << ' ' << a[i][1] << ' ' << a[i][2] << endl;
  }
}

bool chk() {
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      if (!nw[i][j]) continue ;
      if (i - 2 >= 0) {
        if (nw[i][j] == nw[i - 1][j] && nw[i][j] == nw[i - 2][j]) {
          return 0;
        }
      }
      if (i + 2 <= 4) {
        if (nw[i][j] == nw[i + 1][j] && nw[i][j] == nw[i + 2][j]) {
          return 0;
        }
      }
      if (j - 2 >= 0) {
        if (nw[i][j] == nw[i][j - 1] && nw[i][j] == nw[i][j - 2]) {
          return 0;
        }
      }
      if (j + 2 <= 6) {
        if (nw[i][j] == nw[i][j + 1] && nw[i][j] == nw[i][j + 2]) {
          return 0;
        }
      }
    }
  }
  return 1;
}

void drop() {
  int tmp[7];
  for (int i = 0; i < 5; ++i) {
    int c = 0;
    for (int j = 0; j < 7; ++j) {
      if (nw[i][j]) tmp[c++] = nw[i][j];
    }
    for (int j = 0; j < 7; ++j) {
      if (j < c) nw[i][j] = tmp[j];
      else nw[i][j] = 0;
    }
  }
}

void del() {
  int tmp[5][7];
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      tmp[i][j] = nw[i][j];
    }
  }
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      if (i - 2 >= 0) {
        if (nw[i][j] == nw[i - 1][j] && nw[i][j] == nw[i - 2][j]) {
          tmp[i][j] = tmp[i - 1][j] = tmp[i - 2][j] = 0;
        }
      }
      if (i + 2 <= 4) {
        if (nw[i][j] == nw[i + 1][j] && nw[i][j] == nw[i + 2][j]) {
          tmp[i][j] = tmp[i + 1][j] = tmp[i + 2][j] = 0;
        }
      }
      if (j - 2 >= 0) {
        if (nw[i][j] == nw[i][j - 1] && nw[i][j] == nw[i][j - 2]) {
          tmp[i][j] = tmp[i][j - 1] = tmp[i][j - 2] = 0;
        }
      }
      if (j + 2 <= 6) {
        if (nw[i][j] == nw[i][j + 1] && nw[i][j] == nw[i][j + 2]) {
          tmp[i][j] = tmp[i][j + 1] = tmp[i][j + 2] = 0;
        }
      }
    }
  }
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      nw[i][j] = tmp[i][j];
    }
  }
  drop();
  if (chk()) return ;
  del();
}

void dfs(int step) {
  if (step == n + 1) {
    if (!clr()) return ;
    return check(), exit(0);
  }
  if (clr()) return ;
  int tmp[5][7];
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      if (!nw[i][j]) break ;
      for (int k = 0; k < 2; ++k) {
        int ti = i + dx[k], tj = j + dy[k];
        if (ti < 0 || ti >= 5 || tj < 0 || tj >= 7) continue ;
        if (dx[k] == 1 && nw[ti][tj] == nw[i][j] || dx[k] == -1 && nw[ti][tj]) continue ;
        for (int i = 0; i < 5; ++i) {
          for (int j = 0; j < 7; ++j) {
            tmp[i][j] = nw[i][j];
          }
        }
        a[step][0] = i, a[step][1] = j, a[step][2] = dx[k];   
        swap(nw[i][j], nw[ti][tj]);
        drop(), del();
        dfs(step + 1);
        for (int i = 0; i < 5; ++i) {
          for (int j = 0; j < 7; ++j) {
            nw[i][j] = tmp[i][j];
          }
        }
      }
    }
  }
}

int main() {
  cin >> n;
  for (int i = 0; i < 5; ++i) {
    int x = 1, c = 0;
    while (cin >> x) {
      if (!x || c == 7) break ;
      l[i][c++] = x;
    }
  }
  for (int i = 0; i < 5; ++i) {
    for (int j = 0; j < 7; ++j) {
      nw[i][j] = l[i][j];
    }
  }
  dfs(1);
  puts("-1");
  return 0;
}
```

</details>