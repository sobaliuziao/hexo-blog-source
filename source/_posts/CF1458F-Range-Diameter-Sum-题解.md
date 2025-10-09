---
title: 'CF1458F Range Diameter Sum 题解'
date: 2025-02-07 17:31:00
---

## Description

给定一棵包含 $n$ 个节点(编号 $1$ 到 $n$)， $n-1$ 条长度为 $1$ 的无向边的树。

设 $d(u,v)$ 为编号 $u$ 到编号 $v$ 两点之间唯一路径的长度。

设 $f(l,r)$ 为 $\max\{d(u,v)\}(l\leq u,v\leq r)$

求:

$$\sum_{l=1}^{n}\sum_{r=l}^{n}f(l,r)$$

第一行输入 $1$ 个整数 $n\ (1\leq n\leq 10^5)$。

接下来 $n-1$ 行，每行两个整数 $x,y$ 表示编号为 $x$ 和编号为 $y$ 的点之间有一条长度为 $1$ 的边$(1\leq x,y\leq n)$，保证给定的图是一棵树。

输出对于这棵树，上述表达式的值。

$1\leq n\leq 10^5$。

## Solution

首先需要说一下树上圆理论。

对于任意一个点集 $S$，则所有直径的中点一定重合，否则一定存在另一个更长的直径，设 $C(S)=(v,r)$ 表示 $v$ 是直径的中点，$r$ 是直径长度的一半（$v$ 可以在边上）。

---

引理 1：如果 $S\subseteq (v,r)$ 且 $a,b\in S$，则 $dist(mid(a,b),v)+\frac{dist(a,b)}{2}\leq r$。

<details>
<summary>证明</summary>
画图后易得。
</details>

---

引理 2：如果 $S\subseteq (v,r)$，则 $C(s)\subseteq (v,r)$。

<details>
<summary>证明</summary>

设 $C(S)=(v',r')$，则 $v'$ 一定是 $S$ 中某个直径的中点，由引理 1 可得：$dist(v,v')+r'\leq r$。

那么对于任意 $x\in C(S)$，则 $dist(v,x)\leq dist(v,v')+dist(v',x)\leq r-r'+r'\leq r$。结论得证。

</details>

---

然后考虑怎么合并两个树上圆。

如果 $C_1\supseteq C_2$，则合并为 $C_1$，条件为 $dist(v_1,v_2)\leq r_1-r_2$。

如果 $C_1\subseteq C_2$，则合并为 $C_2$，条件为 $dist(v_1,v_2)\leq r_2-r_1$。

否则可以用类似几何圆的合并，将其合并为 $(v,r)$，满足 $r=\frac{r_1+r_2+dist(v_1,v_2)}{2}$，$v$ 为 $v_1$ 向 $v_2$ 的方向移动 $r-r_1$ 步的最终位置。证明略。

回到这题，先分治，假设当前分治区间为 $[l,r]$，$mid$ 为中点。

设 $C_{1,i}$ 为将 $[i,mid]$ 合并后的圆，$C_{2,i}$ 为将 $[mid+1,i]$ 合并后的圆。

那么固定 $C_{1,i}$，则有三段：$[mid+1,t_{1,i}]$ 结果为 $r_i$，$(t_{1,i},t_{2,i}-1)$ 结果为 $r_i+r_j+dist(r(C_{1,i},r(C_{2,j})))$，后面的结果是 $r_j$。

第一和第三部分是好算的，第二部分树剖维护即可。

时间复杂度：$O(n\log^3n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;
using pii = std::pair<int, int>;

const int kMaxN = 2e5 + 5;

int n; i64 ans = 0;
int p[kMaxN], dep[kMaxN], sz[kMaxN], wson[kMaxN], st[kMaxN][20];
int dfn[kMaxN], idx[kMaxN], top[kMaxN];
std::vector<int> G[kMaxN];

/*
  sum1[i] (bit1) : i 或者 i 的轻子树的标记点到 i 的距离和
  cnt1[i] (bit2) : i 或者 i 的轻子树的标记点个数
  sum2[i] (bit3) : i 或者 i 的轻子树的标记点个数 * dep[i]
  cnt2[i] (bit4) : i 的子树内的标记点个数
  sum3[i] (bit5) : i 的子树内标记点的 dep 和
*/

struct BIT {
  i64 c[kMaxN];
  void upd(int x, int v) {
    for (; x <= 2 * n; x += x & -x) c[x] += v;
  }
  void upd(int l, int r, int v) {
    if (l <= r) upd(l, v), upd(r + 1, -v);
  }
  i64 qry(int x) {
    i64 ret = 0;
    for (; x; x -= x & -x) ret += c[x];
    return ret;
  }
  i64 qry(int l, int r) { return l <= r ? qry(r) - qry(l - 1) : 0; }
} bit1, bit2, bit3, bit4, bit5;

int get(int x, int y) { return dfn[x] < dfn[y] ? x : y; }

void dfs1(int u, int fa) {
  sz[u] = 1, dep[u] = dep[fa] + 1, p[u] = fa;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

void dfs2(int u, int fa, int t) {
  static int cnt = 0;
  st[dfn[u] = ++cnt][0] = fa, idx[cnt] = u, top[u] = t;
  if (wson[u]) dfs2(wson[u], u, t);
  for (auto v : G[u]) {
    if (v == fa || v == wson[u]) continue;
    dfs2(v, u, v);
  }
}

int LCA(int x, int y) {
  if (x == y) return x;
  if (dfn[x] > dfn[y]) std::swap(x, y);
  int k = std::__lg(dfn[y] - dfn[x]);
  return get(st[dfn[x] + 1][k], st[dfn[y] - (1 << k) + 1][k]);
}

int getdis(int x, int y) { return dep[x] + dep[y] - 2 * dep[LCA(x, y)]; }

int getfa(int x, int k) {
  assert(dep[x] - 1 >= k);
  for (; x; k -= dep[x] - dep[p[top[x]]], x = p[top[x]]) {
    if (k <= dep[x] - dep[top[x]])
      return idx[dfn[x] - k];
  }
  assert(0);
}

int move(int x, int y, int k) {
  int lca = LCA(x, y), len = dep[x] + dep[y] - 2 * dep[lca];
  assert(k <= len);
  if (k <= dep[x] - dep[lca]) return getfa(x, k);
  else return getfa(y, len - k);
}

pii merge(pii a, pii b) {
  if (a.second < b.second) std::swap(a, b);
  auto [u1, r1] = a;
  auto [u2, r2] = b;
  int dis = getdis(u1, u2);
  if (dis <= r1 - r2) return a;
  assert((r1 + r2 + dis) % 2 == 0);
  int r = (r1 + r2 + dis) / 2, u = move(u1, u2, r - r1);
  return {u, r};
}

void prework() {
  dfs1(1, 0), dfs2(1, 0, 1);
  for (int i = 1; i <= std::__lg(2 * n - 1); ++i)
    for (int j = 1; j <= 2 * n - 1 - (1 << i) + 1; ++j)
      st[j][i] = get(st[j][i - 1], st[j + (1 << (i - 1))][i - 1]);
}

void update(int x, int v) {
  bit4.upd(dfn[x], v), bit5.upd(dfn[x], v * dep[x]);
  for (int i = x; i; i = p[top[i]]) {
    bit1.upd(dfn[i], v * (dep[x] - dep[i])), bit2.upd(dfn[i], v);
    bit3.upd(dfn[i], v * dep[i]);
  }
}

i64 query(int x) {
  i64 ret = 0;
  int lst = 0;
  for (int i = x; i; i = p[top[i]]) {
    int cnt = bit2.qry(dfn[top[i]], dfn[i] - 1);
    ret += 1ll * cnt * dep[x] - bit3.qry(dfn[top[i]], dfn[i] - 1) + bit1.qry(dfn[top[i]], dfn[i] - 1);
    int cnt1 = bit4.qry(dfn[i], dfn[i] + sz[i] - 1);
    ret += 1ll * cnt1 * (dep[x] - dep[i]) + bit5.qry(dfn[i], dfn[i] + sz[i] - 1) - 1ll * cnt1 * dep[i];
    if (lst) {
      int cnt2 = bit4.qry(dfn[lst], dfn[lst] + sz[lst] - 1);
      ret -= 1ll * cnt2 * (dep[x] - dep[i]) + bit5.qry(dfn[lst], dfn[lst] + sz[lst] - 1) - 1ll * cnt2 * dep[i];
    }
    lst = top[i];
  }
  return ret;
}

void solve(int l, int r) {
  static pii c[kMaxN];
  static int t1[kMaxN], t2[kMaxN];
  static i64 sum[kMaxN];
  if (l == r) return;
  int mid = (l + r) >> 1;
  solve(l, mid), solve(mid + 1, r);
  c[mid] = {mid, 0}, c[mid + 1] = {mid + 1, 0};
  for (int i = mid - 1; i >= l; --i) c[i] = merge(c[i + 1], {i, 0});
  for (int i = mid + 2; i <= r; ++i) c[i] = merge(c[i - 1], {i, 0});
  for (int i = mid + 1; i <= r; ++i) sum[i] = sum[i - 1] + c[i].second;
  int nl = mid + 1, nr = mid;
  for (int i = l; i <= mid; ++i) {
    int L = mid, R = r + 1;
    t1[i] = mid, t2[i] = r + 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (merge(c[i], c[mid]) == c[i]) L = t1[i] = mid;
      else R = mid;
    }
    L = t1[i], R = r + 1;
    while (L + 1 < R) {
      int mid = (L + R) >> 1;
      if (merge(c[i], c[mid]) == c[mid]) R = t2[i] = mid;
      else L = mid;
    }
    ans += 2ll * c[i].second * (t1[i] - mid) + 2ll * (sum[r] - sum[t2[i] - 1]);
    ans += 1ll * c[i].second * (t2[i] - t1[i] - 1) + sum[t2[i] - 1] - sum[t1[i]];
    for (; nr < t2[i] - 1; update(c[++nr].first, 1)) {}
    for (; nl > t1[i] + 1; update(c[--nl].first, 1)) {}
    for (; nr > t2[i] - 1; update(c[nr--].first, -1)) {}
    for (; nl < t1[i] + 1; update(c[nl++].first, -1)) {}
    ans += query(c[i].first);
  }
  for (int i = nl; i <= nr; ++i) update(c[i].first, -1);
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(i + n), G[i + n].emplace_back(u);
    G[v].emplace_back(i + n), G[i + n].emplace_back(v);
  }
  prework(), solve(1, n);
  std::cout << ans / 2 << '\n';
}

int32_t main() {
  freopen("image.in", "r", stdin);
  freopen("image.out", "w", stdout);
  std::ios::sync_with_stdio(0), std::cin.tie(0), std::cout.tie(0);
  int T = 1;
  // std::cin >> T;
  while (T--) dickdreamer();
  // std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```