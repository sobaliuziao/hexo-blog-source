---
title: 'P2065 [TJOI2011]卡片 题解'
date: 2021-04-17 22:14:00
---

刚学网络流，记一篇题解。

## 题意

给你两堆卡片，分蓝的和红的，分别有 $n$ 个和 $m$ 个，然后每个卡片上都有一个数。一个人要拿很多张卡片，每次只能从两堆中各取一个，而且这两个卡片上的 $\gcd>1$，问：最多能拿多少个。

## 思路1

> 这不就是个二分图板子吗，暴力建图然后跑EK不就可以过了吗？

然后：

![](https://cdn.luogu.com.cn/upload/image_hosting/etrcic7o.png?x-oss-process=image/resize,m_lfit,h_170,w_225)

稍微想一下发现建图就 $O(nm)$ 了，再带一堆常数就 T 飞了。

## 思路2

知道是建图慢了，就要去优化建图。

很明显这里不能两边同时建，所以要两边分开建图。

问题来了：怎么建？

这里发现是用 $\gcd$ 连接两边的，那么只要找到中间的一堆“中间商”即可。然后就很容易想到用**质因数**。

先预处理一遍 $1\sim 10^7$ 的质因数，然后对于每个卡片，再向卡片上数字的所有质因数连一条边，然后跑一遍网络流，问题就迎刃而解了。

## 代码(EK)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 2e4 + 5;
const int M = 1e5 + 5;
const int PRIME = 1e7 + 5;
const int CNT = 6e5 + 5;

int T;
int n, m, s, t, ans;
int b[N], r[N];
int tot, pre[M << 1], to[M << 1], val[M << 1], tail[N];

void addEdge (int u, int v, int w) {
  to[++tot] = v, val[tot] = w, pre[tot] = tail[u], tail[u] = tot;
  to[++tot] = u, val[tot] = 0, pre[tot] = tail[v], tail[v] = tot;
}

int gcd (int m, int n) {
  if (m < n) swap(m, n);
  if (n == 0) return m;
  return gcd(n, m % n);
}

int cnt;
int primes[CNT];
void Prework () { //预处理质数（埃氏筛）
  bool vis[PRIME] = {0};
  for (int i = 2; i * i <= 1e7; ++i)
    if (!vis[i])
      for (int j = i * i; j <= 1e7; j += i)
        vis[j] = true;
  for (int i = 2; i <= 1e7; ++i)
    if (!vis[i]) primes[++cnt] = i;
}

namespace MaxFlow { //网络流
#define INF 0x3f3f3f3f
  int p[N] = {0}, inc[N];
  bool vis[N];
  int q[N];
  void Init () { memset(p, 0, sizeof(p)), memset(inc, 0, sizeof(inc)); }
  bool BFS () {
    memset(vis, false, sizeof(vis));
    int head = 0, back = 1;
    vis[s] = true, inc[s] = INF; q[1] = s;
    while (head < back) {
      int nowfront = q[++head];
      for (int ind = tail[nowfront]; ind; ind = pre[ind]) {
        if (!val[ind]) continue ;
        if (vis[to[ind]]) continue ;
        inc[to[ind]] = min(inc[nowfront], val[ind]);
        vis[to[ind]] = true, q[++back] = to[ind], p[to[ind]] = ind;
        if (to[ind] == t) return true;
      }
    }
    return false;
  }
  void Work () {
    int cur = t;
    while (cur ^ s) {
      int las = p[cur];
      val[las] -= inc[t], val[las ^ 1] += inc[t];
      cur = to[las ^ 1];
    }
    ans += inc[t];
    return ;
  }
}

int main() {
  scanf("%d", &T);
  Prework();
  while (T--) {
    scanf("%d%d", &n, &m); s = n + m + 1, t = n + m + 2;
    memset(pre, 0, sizeof(pre)), memset(tail, 0, sizeof(tail));
    tot = 1; ans = 0;
    for (int i = 1; i <= n; ++i) scanf("%d", &b[i]), addEdge(s, i, 1); //左边的超级源点向i连边
    for (int i = 1; i <= m; ++i) scanf("%d", &r[i]), addEdge(i + n, t, 1); //右边的超级源点向i+n连边（至于为什么是i+n就不用解释了吧）
    for (int i = 1; i <= n; ++i) {
      for (int j = 1; j <= cnt; ++j) {
        if (primes[j] > b[i]) break ;
        if (b[i] % primes[j] == 0) addEdge(i, j + n + m + 2, 1); //找到质因数然后建边
      }
    }
    for (int i = 1; i <= m; ++i) {
      for (int j = 1; j <= cnt; ++j) {
        if (primes[j] > r[i]) break ;
        if (r[i] % primes[j] == 0) addEdge(j + n + m + 2, i + n, 1);
      }
    }
    while (MaxFlow::BFS()) MaxFlow::Work();
    printf("%d\n", ans);
  }
  return 0;
} 

```

至于时间复杂度：不会算。