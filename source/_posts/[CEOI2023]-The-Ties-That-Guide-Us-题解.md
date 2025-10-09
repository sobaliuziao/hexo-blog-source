---
title: [CEOI2023] The Ties That Guide Us 题解
date: 2024-11-15 19:11:00
---

## Description

你用销售机器人的利润雇佣了一名助手，现在你准备好去拿走装有 CEOI 奖章的保险箱了。

保险箱位于一所由 $n$ 个房间所组成的大学建筑内，这些房间由 $n-1$ 扇门连接。每个房间都可以从其他任何房间到达，且每个房间最多与 $3$ 扇门相连。

你和你的助手都有描述建筑物内房间相连情况的平面图，但是你们两个各自拥有的平面图虽然描述了相同的房间结构布局，但是房间和门的编号可能不同。

在比赛的第二天，委员会忙于处理赛时通知和选手提问。这将是接近装着奖牌的保险箱的完美机会。

你的助手会首先搜索整栋大楼。一旦他找到保险箱所在的房间，它就会给你留下前往那个房间的提示。由于手机不能带进赛场，他用了去年 BOI 留下的几乎无限供应的领带。由于这些领带完全相同无法区分，你能获得的信息就是他在任何给定房间里所留下的领带数量。由于一个房间内过多的领带非常可疑，因此任何单个房间内领带的最大数量应当尽可能少（参阅评分部分）。

之后，你计划在上厕所的时候溜出去，利用助手留下来的领带找到有保险箱的房间。保险箱藏在房间里，所以你进入带有保险箱的房间时，必须依靠领带识别这个房间；此外，由于“上厕所”时间过长会被发现，你必须尽快找到保险箱。你最多可以走过 $d+30$ 扇门，其中 $d$ 是你的初始位置到保险箱所在位置的最短路径上的门数量。若重复穿过同一扇门，则每次都计入。

因此，你需要编写一个程序，告诉助手需要在每个房间留下多少条领带，并引导你前往带有保险箱的房间。

## Solution

首先对于 Sub2 只有一个点度数为 $2$，所以可以直接取出这个唯一的点作为根，然后将目标点到根的路径颜色染黑。这样查询的时候只要暴力跳父亲，直到当前点颜色为黑，然后暴力枚举儿子，如果找到颜色为黑的儿子就往儿子跳，否则就是终点了。

不过这么做有个问题，就是找儿子的过程可能会浪费过多的询问次数，而注意到限制是 $dist(s,t)+30$，由于每次试错会浪费两次，所以只能走错 $15$ 步，为 $O(\log n)$ 级别。

这启发我们重链剖分，每次跳子树大小最大的儿子，由于终点到 $lca$ 路径上的轻儿子只有 $O(\log n)$ 个，所以这样就是对的。

如果树没有特殊性质，可以利用树哈希的思想选定重心作为根，但是可能有两个重心，这时需要选取离起点更近的重心作为根。

查询时如果跳到根节点颜色还为白，就说明根是另一个重心，直接跳到那个重心即可。

总次数：$d+2\log n$。

## Code

```cpp
#include <bits/stdc++.h>
#include "incursion.h"

#ifdef ORZXKR
#include "grader.cpp"
#endif

const int kMaxN = 4.5e4 + 5;

int n, safe;
int p[kMaxN], sz[kMaxN], mx[kMaxN];
bool vis[kMaxN];
std::vector<int> G[kMaxN], rt;

void dfs1(int u, int fa) {
  sz[u] = 1, mx[u] = 0;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v], mx[u] = std::max(mx[u], sz[v]);
  }
  mx[u] = std::max(mx[u], n - sz[u]);
  if (mx[u] <= n / 2) rt.emplace_back(u);
}

void dfs2(int u, int fa) {
  p[u] = fa;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs2(v, u);
  }
}

void dfs3(int u, int fa) {
  vis[u] = 1;
  for (auto v : G[u]) {
    if (v == fa || vis[v]) continue;
    if (visit(v)) return dfs3(v, u);
    else visit(u);
  }
}

std::vector<int> mark(std::vector<std::pair<int, int>> F, int safe) {
  n = (int)F.size() + 1;
  std::vector<int> vec(n, 0);
  for (int i = 1; i <= n; ++i) G[i].clear();
  for (auto [u, v] : F)
    G[u].emplace_back(v), G[v].emplace_back(u);
  rt.clear(), dfs1(1, 0), dfs2(rt[0], 0);
  for (int i = safe; i; i = p[i]) {
    vec[i - 1] = 1;
    if (rt.size() == 2 && (i == rt[0] || i == rt[1])) break;
  }
  return vec;
}

void locate(std::vector<std::pair<int, int>> F, int cur, int t) {
  n = (int)F.size() + 1;
  for (int i = 1; i <= n; ++i) G[i].clear(), vis[i] = 0;
  for (auto [u, v] : F)
    G[u].emplace_back(v), G[v].emplace_back(u);
  rt.clear(), dfs1(1, 0), dfs2(rt[0], 0);
  for (int i = 1; i <= n; ++i)
    std::sort(G[i].begin(), G[i].end(), [&] (int x, int y) { return sz[x] > sz[y]; });
  for (; p[cur] && !t; t = visit(cur = p[cur])) vis[cur] = 1;
  vis[cur] = 1;
  if (!t) assert(cur == rt[0]), visit(cur = rt[1]);
  vis[cur] = 1;
  dfs3(cur, p[cur]);
}
```