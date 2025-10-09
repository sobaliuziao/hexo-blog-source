---
title: 'HDU3085 Nightmare Ⅱ 题解'
date: 2022-09-21 21:06:00
---

## Description

[link](https://acm.hdu.edu.cn/showproblem.php?pid=3085)

## Solution

这是个双向广搜板子题。

首先鬼的分裂实际上就是每一次走两步，由于没有障碍所以直接曼哈顿距离即可。
男孩每一次可以走 3 步，所以直接 bfs 连走 3 步即可。而女孩就只用走一步。

双向广搜需要用 2 个队列分别存储男孩和女孩的状态，不妨设这 2 个队列为 $q_0$ 和 $q_1$

处理答案时，就定义 $step[0/1][x][y]$ 表示 $(x,y)$ 这个格点由 男孩/女孩 走到的最少次数，初始设为无穷大。
如果走了 $s$ 步且当前拓展的点以前有**异性**走过，那么就输出 $s$ 并停止 bfs。
如果 $q_0$ 和 $q_1$ 均为空切没有停止 bfs 时，则男孩和女孩无法相遇，输出 $-1$ 即可。

这样做是 $O(Tnm)$ 的，有个很大的常数，并且这题 $T$ 非常大，需要注意一下常数。

## Code

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include <debug.h>
#else
#define debug(...) 114514
#endif

using namespace std;

const int kMaxN = 805, kInf = 0x3f3f3f3f;
const pair<int, int> dir[] = {{0, 1}, {0, -1}, {-1, 0}, {1, 0}};

struct Node {
  int x, y, step;
  
  Node() {}
  Node(int _x, int _y, int _step) : x(_x), y(_y), step(_step) {}
  ~Node() {}
};

int T, n, m, ct;
int xx, xy, yx, yy;
int a[kMaxN][kMaxN], step[2][kMaxN][kMaxN];
string s;
char c[kMaxN][kMaxN];
pair<int, int> z[2];
queue<Node> q1, q2;

void init() {
  while (!q1.empty()) q1.pop();
  while (!q2.empty()) q2.pop();
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= m; ++j) {
      step[0][i][j] = step[1][i][j] = kInf;
    }
  }
}

int get(int x, int y, int p) {
  return abs(x - z[p].first) + abs(y - z[p].second);
}

bool check(int x, int y, int p) {
  if (x < 1 || x > n || y < 1 || y > m || a[x][y] == 2) return 0;
  if (get(x, y, 0) <= p * 2 || get(x, y, 1) <= p * 2) return 0;
  return 1;
}

int bfs() {
  init();
  q1.emplace(Node(xx, xy, 0)), q2.emplace(Node(yx, yy, 0));
  step[0][xx][xy] = step[1][yx][yy] = 0;
  int st = 0;
  while (!q1.empty() || !q2.empty()) {
    int x, y; ++st;
    if (!q1.empty()) {
      for (int k = 0; k < 3; ++k) {
        int m3, n3;
        int kk = q1.size();
        for (int hbq = 1; hbq <= kk; ++hbq) {
          auto p1 = q1.front(); q1.pop();
          x = p1.x, y = p1.y;
          if (!check(x, y, st)) continue ;
          for (auto d3 : dir) {
            m3 = x + d3.first, n3 = y + d3.second;
            if (!check(m3, n3, st) || step[0][m3][n3] != kInf) continue ;
            q1.emplace(Node(m3, n3, st)), step[0][m3][n3] = st;
            if (step[1][m3][n3] == kInf) continue ;
            return st;
          }
        }

      }

    }
// =====================
    if (!q2.empty()) {
      int kk = q2.size();
      for (int hbq = 1; hbq <= kk; ++hbq) {
        auto p2 = q2.front(); q2.pop();
        x = p2.x, y = p2.y;
        if (!check(x, y, st)) continue ;
        for (auto d : dir) {
          int tx = x + d.first, ty = y + d.second;
          if (!check(tx, ty, st) || step[1][tx][ty] != kInf) continue ;
          q2.emplace(Node(tx, ty, st)), step[1][tx][ty] = st;
          if (step[0][tx][ty] == kInf) continue ;
          return st;
        }        
      }

    }
  }
  debug(step[0][5][3]);
  return -1;
}

int main() {
  scanf("%d", &T);
  while (T--) {
    ct = 0;
    scanf("%d%d", &n, &m);
    for (int i = 1; i <= n; ++i) {
      scanf("%s", c[i] + 1);
    }
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= m; ++j) {
        if (c[i][j] == '.') {
          a[i][j] = 1;
        } else if (c[i][j] == 'X') {
          a[i][j] = 2;
        } else if (c[i][j] == 'M') {
          a[i][j] = 1, xx = i, xy = j;
        } else if (c[i][j] == 'G') {
          a[i][j] = 1, yx = i, yy = j;
        } else if (c[i][j] == 'Z') {
          a[i][j] = 2, z[ct++] = {i, j};
        } else {
          assert(0);
        }
      }
    }
    printf("%d\n", bfs());
  }
  return 0;
}
/*
1
10 10
..........
..X.......
..M.X...X.
X.........
.X..X.X.X.
.........X
..XX....X.
X....G...X
...ZX.X...
...Z..X..X
*/
```