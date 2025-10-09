---
title: '[CERC2016]机棚障碍 Hangar Hurdles 题解'
date: 2022-10-13 17:32:00
---

## Description

给定一个 $n\times n$ 的网格图，其中部分格点有障碍物使得箱子不能置于其上。规定箱子是一个奇数边长的正方形，其坐标为其中心格点的坐标。箱子只能上下左右移动，每次询问从一个格点能移动到另一个格点的最大箱子。

## Solution

首先对于每个点 $(x,y)$ 用二分求出以这个点为中心格点的最大边长 $d[x][y]$，是 $O(n^2\log n)$ 的。

然后发现这是多组询问，所以不能暴力。

---

先把这个看成一个普通的无向图，把相邻的格点连无向边，边权为两个点的 $d$ 值取较小值，那么相当于就是询问图上两点的最大瓶颈路径。

这个东西可以用 Kruskal 先跑出最大生成树，然后最大瓶颈路径就是这两点的树上最短路径。

---

证明：

先看到 Kruskal 过程：将边权从大到小排序，然后枚举，如果加上当前边不会出现环，就加边。相当于就是能连边就连边。

假设 $u$ 和 $v$ 所在集合在枚举到从大到小第 $k$ 条边时**第一次**被合并，如果 $u$ 和 $v$ 的最大瓶颈路径小于当前边权，那么这相当于在这条边之前 $u$ 和 $v$ 的集合已经被合并了，那么这与假设矛盾。所以 Kruskal 跑出来的最大生成树就是最大瓶颈生成树。

---

注意：这可能是个森林，所以要对于每棵树都跑一遍最大生成树。

建完最大生成树后，询问就转化为求树上两点路径的最小边权，直接倍增 LCA 即可，每次是 $O(\log n)$ 的。

于是整个程序复杂度就为 $O(n^2\log n)$，由于时限开的很大，所以可以轻松通过。

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
  x = (f ? -x : x); return 1;
}
bool read(char &x) {
  while ((x = getc()) == ' ' || x == '\n' || x == '\r');
  return x != EOF;
}
bool read(char *x) {
  while ((*x = getc()) == '\n' || *x == ' ' || *x == '\r');
  if (*x == EOF) return 0;
  while (!(*x == '\n' || *x == ' ' || *x == '\r' || *x == EOF)) *(++x) = getc();
  *x = 0;
  return 1;
}
template<typename A, typename ...B> bool read(A &x, B &...y) { return read(x) && read(y...); }

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
template<typename A, typename ...B> void write(A x, B ...y) { write(x), write(y...); }
struct Flusher {
  ~Flusher() { flush(); }
} flusher;
} // namespace FASTIO
using FASTIO::read; using FASTIO::putc; using FASTIO::write;

const int kMaxN = 1e3 + 5, kMaxS = 1e6 + 5, dx[] = {0, 1, 0, -1}, dy[] = {1, 0, -1, 0};

class DSU {
  public:
    void init(int n) {
      for (int i = 1; i <= n; ++i) {
        fa[i] = i;
      }
    }
    int find(int x) {
      return x == fa[x] ? x : fa[x] = find(fa[x]);
    }
    void unionn(int x, int y) {
      int fx = find(x), fy = find(y);
      if (fx != fy) fa[fx] = fy;
    }
  private:
    int fa[kMaxS];
} d;

int n, q, yxy;
int dis[kMaxS];
char s[kMaxN][kMaxN];
vector<pair<int, int>> G[kMaxS];

int getid(int x, int y) {
  return (x - 1) * n + y;
}

void addE(int u, int v, int w) {
  G[u].emplace_back(v, w);
}

namespace GETDIS {

int sum[kMaxN][kMaxN], d[kMaxN][kMaxN];
queue<pair<int, int>> q;

int get(int m1, int n1, int m2, int n2) {
  return sum[m2][n2] - sum[m1 - 1][n2] - sum[m2][n1 - 1] + sum[m1 - 1][n1 - 1];
}

void solve() {
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      sum[i][j] = sum[i - 1][j] + sum[i][j - 1] - sum[i - 1][j - 1] + (s[i][j] == '#');
    }
  }
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      if (s[i][j] == '#') continue ;
      int L = 0, R = min({i - 1, n - i, j - 1, n - j}) + 1, res = 0;
      while (L + 1 < R) {
        int mid = (L + R) >> 1;
        if (!get(i - mid, j - mid, i + mid, j + mid)) L = res = mid;
        else R = mid;
      }
      d[i][j] = dis[getid(i, j)] = 2 * res + 1;
    }
  }
}

} // namespace GETDIS

namespace KRUSKAL {

struct Edge {
  int u, v, w;
} ed[kMaxS << 2];

DSU dd;

int tot, cnt[kMaxS], tt[kMaxS], fa[kMaxS];

void build() {
  for (int i = 1; i <= n; ++i) {
    for (int j = 1; j <= n; ++j) {
      if (s[i][j] == '#') continue ;
      for (int k = 0; k < 2; ++k) {
        int tx = i + dx[k], ty = j + dy[k];
        if (tx < 1 || tx > n || ty < 1 || ty > n || s[tx][ty] == '#') continue ;
        int u = getid(i, j), v = getid(tx, ty), w = min(dis[u], dis[v]);
        ed[++tot] = {u, v, w}, d.unionn(u, v);
      }
    }
  }
}

void solve() {
  d.init(n * n), dd.init(n * n), build();
  for (int i = 1; i <= n * n; ++i) {
    if (dis[i]) ++tt[fa[i] = d.find(i)];
  }
  sort(ed + 1, ed + 1 + tot, [&] (Edge e1, Edge e2) { return e1.w > e2.w; });
  for (int i = 1; i <= tot; ++i) {
    int fu = dd.find(ed[i].u), fv = dd.find(ed[i].v);
    if (fu != fv) {
      if (cnt[fa[ed[i].u]] == tt[fa[ed[i].u]] - 1) continue ;
      dd.unionn(ed[i].u, ed[i].v);
      addE(ed[i].u, ed[i].v, ed[i].w), addE(ed[i].v, ed[i].u, ed[i].w);
      ++cnt[fa[ed[i].u]];
    }
  }
}

} // namespace KRUSKAL

namespace LCA {

int lg[kMaxS], dep[kMaxS], mi[kMaxS][22], fa[kMaxS][22];

void getlg() {
  memset(mi, 0x3f, sizeof(mi));
  lg[0] = -1;
  for (int i = 1; i <= n * n; ++i) {
    lg[i] = lg[i >> 1] + 1;
  }
}

void dfs(int u, int fat, int lw) {
  dep[u] = dep[fat] + 1, fa[u][0] = fat, mi[u][0] = lw;
  for (int i = 1; i <= lg[n * n]; ++i) {
    fa[u][i] = fa[fa[u][i - 1]][i - 1];
    mi[u][i] = min(mi[u][i - 1], mi[fa[u][i - 1]][i - 1]);
  }
  for (auto [v, w] : G[u]) {
    if (v == fat) continue ;
    dfs(v, u, w);
  }
}

int LCA(int x, int y) {
  if (dep[x] < dep[y]) swap(x, y);
  for (int i = lg[n * n]; ~i; --i) {
    if (dep[fa[x][i]] >= dep[y]) {
      x = fa[x][i];
    }
  }
  if (x == y) return x;
  for (int i = lg[n * n]; ~i; --i) {
    if (fa[x][i] != fa[y][i]) {
      x = fa[x][i], y = fa[y][i];
    }
  }
  return fa[x][0];
}

int getmx(int x, int y) {
  int lca = LCA(x, y), ret = 1e9;
  for (int i = lg[n * n]; ~i; --i) {
    if (dep[fa[x][i]] > dep[lca]) ret = min(ret, mi[x][i]), x = fa[x][i];
    if (dep[fa[y][i]] > dep[lca]) ret = min(ret, mi[y][i]), y = fa[y][i];
  }
  if (x != lca) ret = min(ret, mi[x][0]);
  if (y != lca) ret = min(ret, mi[y][0]);
  return ret;
}

} // namespace LCA

int main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  read(n);
  for (int i = 1; i <= n; ++i) {
    read(s[i] + 1);
  }
  GETDIS::solve(), KRUSKAL::solve(), LCA::getlg();
  for (int i = 1; i <= n * n; ++i) {
    if (dis[i] && d.find(i) == i) {
      LCA::dfs(i, 0, 1e9);
    }
  }
  read(q);
  while (q--) {
    int s1, t1, s2, t2;
    read(s1, t1, s2, t2);
    int u = getid(s1, t1), v = getid(s2, t2);
    if (d.find(u) == d.find(v)) write(LCA::getmx(getid(s1, t1), getid(s2, t2)), '\n');
    else write(0, '\n');
  }
  return 0;
}
```

</details>