---
title: CF704E Iron Man 题解
date: 2024-08-17 11:38:00
---

## Description

“铁人”yyb 在玩游戏。在一个 $n$ 个点的树上，yyb 放置了 $m$ 个鸡贼。每个鸡贼有四个整数参数 $t_i,c_i,v_i,u_i$，表示这个鸡贼会在 $t_i$ 时刻**出现**在点 $v_i$，并以每时刻 $c_i$ 条边的速度向 $u_i$ 点**匀速**移动，到达 $u_i$ 点时**立刻消失**。

如果一个时刻有两个鸡贼在同一位置，它们会立刻爆炸。

（注意，如果一个鸡贼的 $u_i=v_i$ 那么它会在 $t_i$ 时刻出现，此时如果这个点有其它鸡贼一样会发生爆炸）

yyb 想知道最早有鸡贼爆炸的时刻。如果自始至终都没发生爆炸输出 `-1`。

如果你的答案和标准答案的绝对或相对误差不超过 $10^{-6}$ 那么被视为正确。

## Solution

注意到树上问题很不好做，考虑通过树剖将每组移动拆分成 $O(\log n)$ 条链，然后转化为对于所有的 $O(n)$ 条链判断。

那么可以对于每个链用 $x$ 表示时间，$y$ 表示位置，所以每组移动就可以转化为一个线段，然后需要求出这些线段的交点中 $x$ 坐标的最小值。

考虑扫描线，把每个线段左右端点的 $x$ 坐标作为关键点，容易发现对于一对不相交的线段一定满足他们在所有的关键点时刻的 $y$ 坐标大小关系不变。

于是可以用 set 维护当前时刻每个线段的 $y$ 坐标，观察之后会发现每对相交的线段一定满足在某个相交之前的时刻他们在 set 上是相邻的，所以只要每次加入一个线段时求出这个线段和它前驱、后继的答案，如果答案已经小于当前时刻就说明找到了最终答案。

注意这里 set 需要重载运算符，由于找到答案后会直接退出所以不会出现奇怪的问题。

时间复杂度：$O(n+m\log^2n)$。

## Code

<details>
<summary>手写分数类实现</summary>

```cpp
#include <bits/stdc++.h>

#define int int64_t

using f64 = long double;

const int kMaxN = 1e5 + 5;
const f64 kEps = 1e-7;

struct Frac {
  int x, y; // x / y

  void fix() {
    if (y < 0) x = -x, y = -y;
  }

  Frac(__int128_t _x = 0, __int128_t _y = 1) {
    __int128_t d = std::__gcd(_x, _y);
    x = _x / d, y = _y / d;
    if (y < 0) x = -x, y = -y;
  }

  friend Frac operator +(Frac a, Frac b) { return Frac(a.x * b.y + a.y * b.x, a.y * b.y); }
  friend Frac operator -(Frac a, Frac b) { return Frac(a.x * b.y - a.y * b.x, a.y * b.y); }
  friend Frac operator *(Frac a, Frac b) { return Frac(a.x * b.x, a.y * b.y); }
  friend Frac operator /(Frac a, Frac b) { return Frac(a.x * b.y, a.y * b.x); }
  friend bool operator <(Frac a, Frac b) { a.fix(), b.fix(); return (__int128_t)a.x * b.y < (__int128_t)a.y * b.x; }
  friend bool operator <=(Frac a, Frac b) { a.fix(), b.fix(); return (__int128_t)a.x * b.y <= (__int128_t)a.y * b.x; }
  friend bool operator >(Frac a, Frac b) { a.fix(), b.fix(); return (__int128_t)a.x * b.y > (__int128_t)a.y * b.x; }
  friend bool operator >=(Frac a, Frac b) { a.fix(), b.fix(); return (__int128_t)a.x * b.y >= (__int128_t)a.y * b.x; }
  friend bool operator ==(Frac a, Frac b) { a.fix(), b.fix(); return (__int128_t)a.x * b.y == (__int128_t)a.y * b.x; }
  friend bool operator ==(Frac a, int b) { return a.x == (__int128_t)a.y * b; }
  friend bool operator !=(Frac a, int b) { return a.x != (__int128_t)a.y * b; }
  f64 real() { return (f64)x / y; }
};

int n, m;
int p[kMaxN], sz[kMaxN], wson[kMaxN], top[kMaxN], dep[kMaxN], dfn[kMaxN];
f64 ans = 1e18;
Frac a[kMaxN][4];
std::vector<int> G[kMaxN];
std::vector<std::pair<int, int>> upd[kMaxN * 2];
std::vector<std::tuple<Frac, Frac, Frac, Frac>> vec[kMaxN * 2];
// [初始位置，出现时间，结束时间，速度]

void dfs1(int u, int fa) {
  p[u] = fa, dep[u] = dep[fa] + 1, sz[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

void dfs2(int u, int fa, int t) {
  static int cnt = 0;
  top[u] = t;
  if (wson[u]) dfs2(wson[u], u, t);
  for (auto v : G[u]) {
    if (v == fa || v == wson[u]) continue;
    dfs2(v, u, v);
  }
}

void prework() {
  dfs1(1, 0), dfs2(1, 0, 1);
}

void work(int t, int c, int u, int v) {
  std::vector<std::tuple<int, int, int>> vecu, vecv;
  for (; top[u] != top[v];) {
    if (dep[top[u]] >= dep[top[v]]) {
      vecu.emplace_back(top[u], dep[u] - dep[top[u]], 0);
      vecu.emplace_back(top[u] + n, 1, 0);
      u = p[top[u]];
    } else {
      vecv.emplace_back(top[v], 0, dep[v] - dep[top[v]]);
      vecv.emplace_back(top[v] + n, 0, 1);
      v = p[top[v]];
    }
  }
  if (dep[u] <= dep[v])
    vecv.emplace_back(top[u], dep[u] - dep[top[u]], dep[v] - dep[top[u]]);
  else
    vecu.emplace_back(top[u], dep[u] - dep[top[u]], dep[v] - dep[top[u]]);

  std::reverse(vecv.begin(), vecv.end());
  for (auto p : vecv) vecu.emplace_back(p);
  Frac now = Frac(t, 1);
  for (auto [id, l, r] : vecu) {
    vec[id].emplace_back(Frac(l, 1), now, now + Frac(abs(l - r), c), Frac(l <= r ? c : -c, 1));
    now = now + Frac(abs(l - r), c);
  }
}

int getid(std::vector<Frac> &vec, Frac x) {
  int L = -1, R = vec.size(), res = -1;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (x <= vec[mid]) R = res = mid;
    else L = mid;
  }
  return res;
}

Frac calc(int x, int y) {
  Frac s = a[x][3] * a[x][1] - a[y][3] * a[y][1] + a[y][0] - a[x][0];
  Frac v = a[x][3] - a[y][3];
  if (v == 0 && !(s == 0)) {
    return Frac(1e14, 1);
  } else if (v == 0) {
    if (std::max(a[x][1], a[y][1]) <= std::min(a[x][2], a[y][2])) return std::max(a[x][1], a[y][1]);
    else return Frac(1e14, 1);
  } else {
    Frac t = s / v;
    if (t >= a[x][1] && t >= a[y][1] && t <= a[x][2] && t <= a[y][2]) return t;
    else return Frac(1e14, 1);
  }
}

void solve(int x) {
  std::vector<Frac> tmp, unq;
  int tot = 0;
  Frac nowt = Frac(0, 1);
  auto cmp = [&] (int i, int j) -> bool {
    return a[i][0] + a[i][3] * (nowt - a[i][1]) < a[j][0] + a[j][3] * (nowt - a[j][1]);
  };
  for (auto [p, l, r, c] : vec[x]) {
    ++tot;
    a[tot][0] = p, a[tot][1] = l, a[tot][2] = r, a[tot][3] = c;
    tmp.emplace_back(l), tmp.emplace_back(r);
  }
  std::sort(tmp.begin(), tmp.end());
  for (int i = 0; i < (int)tmp.size(); ++i) {
    if (!i) unq.emplace_back(tmp[i]);
    else if (!(tmp[i] == tmp[i - 1])) unq.emplace_back(tmp[i]);
  }
  for (int i = 0; i < (int)unq.size(); ++i) upd[i].clear();
  for (int i = 1; i <= tot; ++i) {
    upd[getid(unq, a[i][1])].emplace_back(i, 1);
    upd[getid(unq, a[i][2])].emplace_back(i, -1);
  }
  std::set<int, decltype(cmp)> st(cmp);
  Frac res = Frac(1e12, 1);
  for (int i = 0; i < (int)unq.size(); ++i) {
    nowt = unq[i];
    if (res < nowt) break;
    for (auto [x, v] : upd[i]) {
      if (v == 1) {
        auto it = st.lower_bound(x);
        if (it != st.end()) {
          Frac val = calc(*it, x);
          res = std::min(res, val);
          if (res < nowt) return void(ans = std::min(ans, res.real()));
        }
        if (it != st.begin()) {
          --it;
          Frac val = calc(*it, x);
          res = std::min(res, val);
          if (res < nowt) return void(ans = std::min(ans, res.real()));
        }
        st.emplace(x);
      }
    }
    for (auto [x, v] : upd[i]) {
      if (v == -1) st.erase(x);
    }
  }
  ans = std::min(ans, res.real());
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  prework();
  for (int i = 1; i <= m; ++i) {
    int t, c, u, v;
    std::cin >> t >> c >> u >> v;
    work(t, c, u, v);
  }
  for (int i = 1; i <= 2 * n; ++i) solve(i);
  if (ans >= 1e10) std::cout << "-1\n";
  else std::cout << std::fixed << std::setprecision(10) << ans << '\n';
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

</details>

<details>
<summary>float128 实现</summary>

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using f64 = long double;
using f128 = __float128;

const int kMaxN = 1e5 + 5;
const f128 kEps = 1e-7;

int n, m;
int p[kMaxN], sz[kMaxN], wson[kMaxN], top[kMaxN], dep[kMaxN], dfn[kMaxN];
f128 ans = 1e18, a[kMaxN][4];
std::vector<int> G[kMaxN];
std::vector<std::pair<int, int>> upd[kMaxN * 2];
std::vector<std::tuple<f128, f128, f128, f128>> vec[kMaxN * 2];
// [初始位置，出现时间，结束时间，速度]

void dfs1(int u, int fa) {
  p[u] = fa, dep[u] = dep[fa] + 1, sz[u] = 1;
  for (auto v : G[u]) {
    if (v == fa) continue;
    dfs1(v, u);
    sz[u] += sz[v];
    if (sz[v] > sz[wson[u]]) wson[u] = v;
  }
}

void dfs2(int u, int fa, int t) {
  static int cnt = 0;
  top[u] = t, dfn[u] = ++cnt;
  if (wson[u]) dfs2(wson[u], u, t);
  for (auto v : G[u]) {
    if (v == fa || v == wson[u]) continue;
    dfs2(v, u, v);
  }
}

void prework() {
  dfs1(1, 0), dfs2(1, 0, 1);
}

void work(int t, int c, int u, int v) {
  std::vector<std::tuple<int, int, int>> vecu, vecv;
  for (; top[u] != top[v];) {
    if (dep[top[u]] >= dep[top[v]]) {
      vecu.emplace_back(top[u], dep[u] - dep[top[u]], 0);
      vecu.emplace_back(top[u] + n, 1, 0);
      u = p[top[u]];
    } else {
      vecv.emplace_back(top[v], 0, dep[v] - dep[top[v]]);
      vecv.emplace_back(top[v] + n, 0, 1);
      v = p[top[v]];
    }
  }
  if (dep[u] <= dep[v])
    vecv.emplace_back(top[u], dep[u] - dep[top[u]], dep[v] - dep[top[u]]);
  else
    vecu.emplace_back(top[u], dep[u] - dep[top[u]], dep[v] - dep[top[u]]);

  std::reverse(vecv.begin(), vecv.end());
  for (auto p : vecv) vecu.emplace_back(p);
  f128 now = t;
  for (auto [id, l, r] : vecu) {
    vec[id].emplace_back(l, now, now + fabs(l - r) / c, l <= r ? c : -c);
    now += fabs(l - r) / c;
  }
}

int getid(std::vector<f128> &vec, f128 x) {
  int L = -1, R = vec.size(), res = -1;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (x <= vec[mid] + kEps) R = res = mid;
    else L = mid;
  }
  return res;
}

f128 calc(int x, int y) {
  f128 s = a[x][3] * a[x][1] - a[y][3] * a[y][1] + a[y][0] - a[x][0];
  f128 v = a[x][3] - a[y][3];
  if (fabs(v) <= kEps && fabs(s) > kEps) return 1e18;
  else if (fabs(v) <= kEps) {
    if (std::max(a[x][1], a[y][1]) <= std::min(a[x][2], a[y][2]) + kEps) return std::max(a[x][1], a[y][1]);
    else return 1e18;
  } else {
    f128 t = s / v;
    if (t >= a[x][1] - kEps && t >= a[y][1] - kEps && t <= a[x][2] + kEps && t <= a[y][2] + kEps) return t;
    else return 1e18;
  }
}

void solve(int x) {
  static std::vector<f128> tmp, unq;
  tmp.clear(), tmp.shrink_to_fit();
  unq.clear(), unq.shrink_to_fit();
  int tot = 0;
  f128 nowt = 0;
  auto cmp = [&] (int i, int j) -> bool {
    return a[i][0] + a[i][3] * (nowt - a[i][1]) < a[j][0] + a[j][3] * (nowt - a[j][1]);
  };
  for (auto [p, l, r, c] : vec[x]) {
    ++tot;
    a[tot][0] = p, a[tot][1] = l, a[tot][2] = r, a[tot][3] = c;
    tmp.emplace_back(l), tmp.emplace_back(r);
  }
  std::sort(tmp.begin(), tmp.end());
  for (int i = 0; i < (int)tmp.size(); ++i) {
    if (!i) unq.emplace_back(tmp[i]);
    else if (fabs(tmp[i] - tmp[i - 1]) > kEps) unq.emplace_back(tmp[i]);
  }
  for (int i = 0; i < (int)unq.size(); ++i) upd[i].clear();
  for (int i = 1; i <= tot; ++i) {
    upd[getid(unq, a[i][1])].emplace_back(i, 1);
    upd[getid(unq, a[i][2])].emplace_back(i, -1);
  }
  std::set<int, decltype(cmp)> st(cmp);
  f128 res = 1e18;
  for (int i = 0; i < (int)unq.size(); ++i) {
    nowt = unq[i];
    if (res < nowt - kEps) break;
    for (auto [x, v] : upd[i]) {
      if (v == 1) {
        auto it = st.lower_bound(x);
        if (it != st.end()) {
          f128 val = calc(*it, x);
          res = std::min(res, val);
          if (res < nowt - kEps) return void(ans = std::min(ans, res));
        }
        if (it != st.begin()) {
          --it;
          f128 val = calc(*it, x);
          res = std::min(res, val);
          if (res < nowt - kEps) return void(ans = std::min(ans, res));
        }
        st.emplace(x);
      }
    }
    for (auto [x, v] : upd[i]) {
      if (v == -1) st.erase(x);
    }
  }
  ans = std::min(ans, res);
}

void dickdreamer() {
  std::cin >> n >> m;
  for (int i = 1; i < n; ++i) {
    int u, v;
    std::cin >> u >> v;
    G[u].emplace_back(v), G[v].emplace_back(u);
  }
  prework();
  for (int i = 1; i <= m; ++i) {
    int t, c, u, v;
    std::cin >> t >> c >> u >> v;
    work(t, c, u, v);
  }
  for (int i = 1; i <= 2 * n; ++i) solve(i);
  if (ans >= 1e10) std::cout << "-1\n";
  else std::cout << std::fixed << std::setprecision(10) << (f64)ans << '\n';
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
</details>
