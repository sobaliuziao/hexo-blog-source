---
title: 'P2016 战略游戏 题解'
date: 2021-04-02 14:25:00
---

这题一眼看上去是一道树形DP的题目，然后后面一想好像可以用二分图来做（虽然是教练提醒的），故产生了此份题解。

## 题目大意

给定一个无根树，每个节点可以“管制”一堆给定点，求选择最少的点数来覆盖这棵树。

## Solution

这题的“覆盖”看起来有那么亿点点像最小点覆盖，所以可以想想如何用二分图来解。

### 如何建立二分图？

注意到这是一棵树，则每层之间肯定不会有连接，而且没有跨越两层的边，所以我们可以把原图划分为奇数层和偶数层。

然后跑匈牙利貌似就可以了。

Tips：最小点覆盖数就是最大匹配数。

## Code

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1505;

vector <int> G[N];

int n, ind, k, r;
int ans, tot, dep[N], points[N];//tot表示奇数层点个数，dep[]表示每个点的层数，points[]表示所有奇数层点

bool vis[N];

void Pre (int k) {//处理出层数
  for (int i = 0; i < (int)G[k].size(); ++i) {
    int to = G[k][i];
    if (vis[to]) continue ;
    vis[to] = true, dep[to] = dep[k] + 1;
    Pre(to);
  }
}

int match[N];

bool DFS (int k) {//匈牙利板子
  for (int i = 0; i < (int)G[k].size(); ++i) {
    int to = G[k][i];
    if (!vis[to]) {
      vis[to] = true;
      if (!match[to] || DFS(match[to])) {
        match[to] = k; return true;
      }
    }
  }
  return false;
}

int main() {
  scanf("%d", &n);
  for (int Case = 0; Case ^ n; ++Case) {
    scanf("%d%d", &ind, &k); ++ind;
    for (int i = 0; i ^ k; ++i) {
      scanf("%d", &r); ++r;
      G[ind].push_back(r), G[r].push_back(ind);
    }
  }
  vis[1] = true, dep[1] = 1, Pre(1);
  for (int i = 1; i <= n; ++i)//取出奇数层点
    if (dep[i] % 2 == 1) points[++tot] = i;
  for (int i = 1; i <= tot; ++i) {//最大匹配
    memset(vis, false, sizeof(vis));
    if (DFS(points[i])) ++ans;
  }
  printf("%d\n", ans);
  return 0;
}
```