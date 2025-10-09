---
title: 'CF666E Forensic Examination 题解'
date: 2025-02-20 17:27:00
---

## Description

给你一个串 $S$ 以及一个字符串数组 $T_{1\ldots m}$，$q$ 次询问，每次问 $S$ 的子串 $S[p_l\ldots p_r]$ 在 $T_{l\ldots r}$ 中的哪个串里的出现次数最多，并输出出现次数。

如有多解输出最靠前的那一个。

$|S|,q\leq 5\times 10^5$，$m,\sum|T_i|\leq 5\times 10^4$。

## Solution

首先将 $S$ 和 $T_1,T_2,\ldots,T_m$ 中间用不同的特殊字符拼起来，然后跑一遍 SA，就转化为求 $T_{l\ldots r}$ 里对应位置和 $rk_{p_l}$ 的区间 height 最小值不小于 $p_r-p_l+1$ 的最大个数。

考虑将 $height$ 数组看成一个长度为 $len$ 的链的边权，用 kruskal 重构树就将上面的问题转化为求某个点子树的区间众数。

线段树合并即可。

时间复杂度：$O(|S'|\log |S'|+q(\log |S'|+\log m))$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using pii = std::pair<int, int>;

const int kMaxN = 5e5 + 5, kMaxL = 6e5 + 5;

struct Node {
  int ls, rs;
  pii p;
} tt[kMaxL * 50];

int n, m, q, len, cnt;
int a[kMaxL], sa[kMaxL], rk[kMaxL], height[kMaxL], bel[kMaxL];
int fa[kMaxL], idd[kMaxL], val[kMaxL * 2], p[kMaxL * 2][22];
int rt[kMaxL * 2];
pii ans[kMaxN];
std::string s, t[kMaxN];
std::vector<int> T[kMaxL * 2];
std::vector<std::tuple<int, int, int>> qq[kMaxL * 2];

pii merge(pii a, pii b) {
  if (!a.first) a.second = -1e9;
  if (!b.first) b.second = -1e9;
  if (a.second > b.second) return a;
  else if (a.second < b.second) return b;
  else return std::min(a, b);
}

void getsa(int n, int *a, int *sa, int *rk) {
  static int cnt[kMaxL], id[kMaxL], ork[kMaxL * 2] = {0};
  for (int i = 1; i <= n; ++i) ++a[i];
  int v = *std::max_element(a + 1, a + 1 + n), m = 0;
  for (int i = 1; i <= n; ++i) ++cnt[a[i]];
  for (int i = 1; i <= v; ++i) cnt[i] += cnt[i - 1];
  for (int i = n; i; --i) sa[cnt[a[i]]--] = i;
  for (int i = 1; i <= n; ++i) {
    if (a[sa[i]] == a[sa[i - 1]]) rk[sa[i]] = rk[sa[i - 1]];
    else rk[sa[i]] = ++m;
  }
  for (int w = 1; m < n; w <<= 1) {
    for (int i = 1; i <= n; ++i) ork[i] = rk[i];
    int p = 0;
    for (int i = n - w + 1; i <= n; ++i) id[++p] = i;
    for (int i = 1; i <= n; ++i)
      if (sa[i] > w)
        id[++p] = sa[i] - w;
    std::fill_n(cnt + 1, m, 0);
    for (int i = 1; i <= n; ++i) ++cnt[rk[i]];
    for (int i = 1; i <= m; ++i) cnt[i] += cnt[i - 1];
    for (int i = n; i; --i) sa[cnt[rk[id[i]]]--] = id[i];
    m = 0;
    for (int i = 1; i <= n; ++i) {
      if (ork[sa[i]] == ork[sa[i - 1]] && ork[sa[i] + w] == ork[sa[i - 1] + w]) rk[sa[i]] = rk[sa[i - 1]];
      else rk[sa[i]] = ++m;
    }
  }
}

void getheight(int n, int *a, int *sa, int *rk, int *height) {
  for (int i = 1, p = 0; i <= n; ++i) {
    if (p) --p;
    int j = sa[rk[i] - 1];
    if (i && j && p) assert(a[i + p - 1] == a[j + p - 1]);
    for (; p < n - std::max(i, j) && a[i + p] == a[j + p]; ++p) {}
    height[rk[i]] = p;
  }
}

int find(int x) { return x == fa[x] ? x : fa[x] = find(fa[x]); }
void unionn(int x, int y, int v) {
  int fx = find(x), fy = find(y);
  if (fx != fy) {
    fa[fx] = fy, val[++cnt] = v;
    T[cnt].emplace_back(idd[fx]), T[cnt].emplace_back(idd[fy]);
    p[idd[fx]][0] = p[idd[fy]][0] = cnt, idd[fy] = cnt;
  }
}

void build() {
  for (int i = 1; i <= len; ++i) fa[i] = idd[i] = i;
  cnt = len;
  std::vector<std::pair<int, int>> vec;
  for (int i = 2; i <= len; ++i) vec.emplace_back(height[i], i);
  std::sort(vec.begin(), vec.end(), std::greater<>());
  for (auto [v, x] : vec) unionn(x - 1, x, v);
}

void prework() {
  int now = 26;
  for (int i = 1; i <= n; ++i) a[++len] = s[i] - 'a';
  a[++len] = ++now;
  for (int i = 1; i <= m; ++i) {
    for (int j = 1; j < t[i].size(); ++j)
      a[++len] = t[i][j] - 'a', bel[len] = i;
    a[++len] = ++now;
  }
  getsa(len, a, sa, rk), getheight(len, a, sa, rk, height), build();
  for (int i = cnt; i; --i)
    for (int j = 1; j <= std::__lg(cnt); ++j)
      p[i][j] = p[p[i][j - 1]][j - 1];
}

std::pair<int, int> solve(int l, int r, int pl, int pr) {
  static int cnt[kMaxN];
  std::fill_n(cnt + 1, m, 0);
  int mi = 1e9;
  for (int i = rk[pl] + 1; i <= len; ++i) {
    mi = std::min(mi, height[i]);
    if (mi >= pr - pl + 1) ++cnt[bel[sa[i]]];
    else break;
  }
  mi = 1e9;
  for (int i = rk[pl]; i > 1; --i) {
    mi = std::min(mi, height[i]);
    if (mi >= pr - pl + 1) ++cnt[bel[sa[i - 1]]];
    else break;
  }
  std::pair<int, int> ret = {-1, -1};
  for (int i = l; i <= r; ++i) {
    if (cnt[i] > ret.second || cnt[i] == ret.second && i < ret.first)
      ret = {i, cnt[i]};
  }
  return ret;
}

int gettop(int x, int v) {
  for (int i = std::__lg(len); ~i; --i)
    if (val[p[x][i]] >= v)
      x = p[x][i];
  return x;
}

void pushup(int x) {
  tt[x].p = merge(tt[tt[x].ls].p, tt[tt[x].rs].p);
}

void update(int &x, int l, int r, int ql, int v) {
  static int sgt_cnt = 0;
  if (!x) x = ++sgt_cnt;
  if (l == r) {
    tt[x].p.first = l, tt[x].p.second += v;
    return;
  }
  int mid = (l + r) >> 1;
  if (ql <= mid) update(tt[x].ls, l, mid, ql, v);
  else update(tt[x].rs, mid + 1, r, ql, v);
  pushup(x);
}

int merge(int x, int y, int l, int r) {
  if (!x || !y) return x + y;
  if (l == r) {
    tt[x].p.first = l, tt[x].p.second += tt[y].p.second;
    return x;
  }
  int mid = (l + r) >> 1;
  tt[x].ls = merge(tt[x].ls, tt[y].ls, l, mid), tt[x].rs = merge(tt[x].rs, tt[y].rs, mid + 1, r);
  pushup(x);
  return x;
}

pii query(int x, int l, int r, int ql, int qr) {
  if (l > qr || r < ql) return {0, 0};
  else if (!x) return {std::max(l, ql), 0};
  else if (l >= ql && r <= qr) return tt[x].p;
  int mid = (l + r) >> 1;
  return merge(query(tt[x].ls, l, mid, ql, qr), query(tt[x].rs, mid + 1, r, ql, qr));
}

void dfs(int u) {
  // static int cnt[500][500] = {0};
  if (u <= len && bel[sa[u]]) update(rt[u], 1, m, bel[sa[u]], 1);
  for (auto v : T[u]) {
    dfs(v);
    rt[u] = merge(rt[u], rt[v], 1, m);
  }
  for (auto [l, r, id] : qq[u]) {
    // ans[id] = {-1, -1};
    // for (int i = l; i <= r; ++i) ans[id] = merge(ans[id], {i, cnt[u][i]});
    ans[id] = query(rt[u], 1, m, l, r);
  }
}

void dickdreamer() {
  std::cin >> s >> m;
  n = s.size(), s = " " + s;
  for (int i = 1; i <= m; ++i) {
    std::cin >> t[i];
    t[i] = " " + t[i];
  }
  prework();
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int l, r, pl, pr;
    std::cin >> l >> r >> pl >> pr;
    // auto p = solve(l, r, pl, pr);
    // std::cout << p.first << ' ' << p.second << '\n';
    qq[gettop(rk[pl], pr - pl + 1)].emplace_back(l, r, i);
  }
  dfs(cnt);
  for (int i = 1; i <= q; ++i) std::cout << ans[i].first << ' ' << ans[i].second << '\n';
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