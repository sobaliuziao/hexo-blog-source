---
title: 'CF2115F1 Gellyfish and Lycoris Radiata (Easy Version) 题解'
date: 2025-07-23 21:30:00
---

## Description

Gellyfish 有一个包含 $n$ 个集合的数组。最初，所有集合都是空的。

现在，Gellyfish 将进行 $q$ 次操作。每次操作包含一次修改操作和一次查询操作，对于第 $i$ 次（$1 \leq i \leq q$）操作：

首先，会有一次修改操作，可能是以下三种之一：

1. 插入操作：给定一个整数 $r$。将元素 $i$ 插入到第 $1$ 到第 $r$ 个集合中。注意，这里插入的元素是 $i$，即操作的编号，而不是集合的编号。
2. 反转操作：给定一个整数 $r$。将第 $1$ 到第 $r$ 个集合的顺序反转。
3. 删除操作：给定一个整数 $x$。从所有包含 $x$ 的集合中删除元素 $x$。

然后进行一次查询操作：

- 查询操作：给定一个整数 $p$。输出第 $p$ 个集合中的最小元素（如果该集合为空，则答案为 $0$）。

现在，Flower 需要为每次查询操作提供答案。请你帮助她！

本题有一个额外的约束：Gellyfish 只有在 Flower 回答了上一次查询操作后，才会给出下一次操作。也就是说，你需要在线处理本题。具体请参考输入格式。

$n,q\leq 10^5$。

## Solution

首先如果没有删除操作是好做的，可以直接维护。然后会发现这个删除操作非常麻烦，因为我们根本不知道需要修改哪些集合里的元素。

但是注意到做 $k$ 次操作会把整个序列分成 $O(k)$ 个连续段，每个连续段满足在操作之前是个区间，且现在的顺序是原先的顺序或者倒序的形式。这启发我们询问分块。

具体地，对每 $B$ 次修改进行分块，块内先假定每个集合都没有元素，然后修改时维护连续段，由于只有 $O(B)$ 个连续段，加入元素时暴力即可。

对于删除操作，块内的直接打标记，不在块内的，就找到其对应的块，把其从所在的所有集合删掉。

对于询问，块内的贡献可以直接求，块外的贡献还需要知道当前位置在之前任意块的最终位置，重构时可以预处理，得到这个之后也是直接求。

需要精细实现，实测能过 Hard Version。

时间复杂度：$O((n+q)\sqrt q)$，空间复杂度：$O((n+q)\sqrt q)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 3e5 + 5, kMaxB = 550;

struct Node {
  int l, r;
  Node(int _l = 0, int _r = 0) : l(_l), r(_r) {}
};

struct Block {
  int sz;
  Node seg[kMaxB];
  std::vector<short> vv[kMaxB];
  int cnt[kMaxB];
  void split(int x) {
    bool fl = 1;
    int ps = 0;
    for (int i = 1, now = 0; i <= sz; ++i) {
      auto [l, r] = seg[i];
      now += abs(r - l) + 1;
      if (now == x) { fl = 0; break; }
      if (now > x && !ps) { ps = i; break; }
    }
    if (!fl) return;
    for (int i = sz; i > ps; --i) {
      std::swap(seg[i], seg[i + 1]);
      vv[i].swap(vv[i + 1]);
    }
    vv[ps + 1] = vv[ps];
    int now = 0;
    for (int i = 1; i < ps; ++i) {
      auto [l, r] = seg[i];
      now += abs(r - l) + 1;
    }
    assert(now < x);
    auto [l, r] = seg[ps];
    if (l <= r) {
      seg[ps] = {l, l + x - now - 1};
      seg[ps + 1] = {l + x - now, r};
    } else {
      seg[ps] = {l, l - (x - now) + 1};
      seg[ps + 1] = {l - (x - now), r};
    }
    ++sz;
  }
  int getbel(int x) {
    for (int i = 1, now = 0; i <= sz; ++i) {
      auto [l, r] = seg[i];
      now += abs(r - l) + 1;
      if (now >= x) return i;
    }
    assert(0);
  }
  int getpre(int x) {
    // std::cerr << "heige\n";
    for (int i = 1, now = 0; i <= sz; ++i) {
      auto [l, r] = seg[i];
      int lst = now;
      now += abs(r - l) + 1;
      // std::cerr << "??? " << l << ' ' << r << '\n';
      if (now >= x) {
        if (l <= r) return l + x - lst - 1;
        else return l - (x - lst) + 1;
      }
    }
    assert(0);
    return 0;
  }
} t[kMaxB];

int n, q, B;
int op[kMaxN], a[kMaxN], p[kMaxN], res[kMaxN];
short pos[kMaxB][kMaxN];
int fir[kMaxN]; // pos[i][j] : 第 i 段末尾时，初始 j 所在的块；fir[i][j] : 第 i 末尾时，在第 j 个的数的初始位置
bool del[kMaxN];
std::vector<short> pp[kMaxN];

void update1(int id, int x) { // 给 [1, x] 插入 id
  int bid = (id - 1) / B + 1;
  t[bid].split(x);
  int now = 0;
  // std::cerr << x << " : \n";
  // for (int i = 1; i <= t[bid].sz; ++i) std::cerr << t[bid].seg[i].l << ' ' << t[bid].seg[i].r << '\n';
  for (int i = 1; i <= t[bid].sz; ++i) {
    auto [l, r] = t[bid].seg[i];
    now += abs(r - l) + 1;
    // std::cerr << now << '\n';
    if (now >= x) assert(now == x);
    if (now <= x) t[bid].vv[i].emplace_back(id - (bid - 1) * B);
    if (now >= x) break;
  }
  // std::cerr << "--------------\n";
}

void update2(int id, int x) { // [1, x] 翻转
  int bid = (id - 1) / B + 1;
  t[bid].split(x);
  int ps = 0;
  for (int i = 1, now = 0; i <= t[bid].sz; ++i) {
    auto [l, r] = t[bid].seg[i];
    now += abs(r - l) + 1;
    if (now == x) ps = i;
  }
  assert(ps);
  for (int i = 1, j = ps; i < j; ++i, --j) {
    std::swap(t[bid].seg[i], t[bid].seg[j]);
    t[bid].vv[i].swap(t[bid].vv[j]);
  }
  for (int i = 1; i <= ps; ++i) std::swap(t[bid].seg[i].l, t[bid].seg[i].r);
}

void update3(int id, int x) { // 把 x 删掉
  if (x > id || del[x]) return;
  assert(!del[x]);
  del[x] = 1;
  if ((x - 1) / B + 1 < (id - 1) / B + 1) {
    int bid = (x - 1) / B + 1;
    for (auto i : pp[x]) {
      if (!--t[bid].cnt[i]) std::vector<short>().swap(t[bid].vv[i]);
    }
    std::vector<short>().swap(pp[x]);
  }
}

void rebuild(int bid) {
  static int lst[kMaxN];
  for (int i = 1; i <= n; ++i) lst[i] = fir[i];
  int cnt = 0;
  // std::cerr << "????????????\n";
  for (int i = 1; i <= t[bid].sz; ++i) {
    auto [l, r] = t[bid].seg[i];
    // std::cerr << l << ' ' << r << '\n';
    if (l <= r) {
      for (int j = l; j <= r; ++j) pos[bid][lst[j]] = i, fir[++cnt] = lst[j];
    } else {
      for (int j = l; j >= r; --j) pos[bid][lst[j]] = i, fir[++cnt] = lst[j];
    }
    assert(!t[bid].cnt[i]);
    t[bid].cnt[i] = 0;
    for (auto _v : t[bid].vv[i]) {
      int v = _v + (bid - 1) * B;
      if (!del[v]) {
        ++t[bid].cnt[i], pp[v].emplace_back(i);
      }
    }
  }
  assert(cnt == n);
  // if (bid == 1) {
  //   for (auto x : t[bid].vv[2]) std::cerr << x << ' ';
  //   std::cerr << '\n';
  // }
  // std::cerr << "????????????\n";
}

int query(int id, int x) {
  int bid = (id - 1) / B + 1;
  int ps = t[bid].getbel(x);
  int ret = 1e9;
  for (auto _v : t[bid].vv[ps]) {
    int v = _v + (bid - 1) * B;
    if (!del[v])
      ret = std::min(ret, v);
  }
  if (bid > 1) {
    int ff = fir[t[bid].getpre(x)];
    for (int i = 1; i <= bid - 1; ++i) {
      int bb = pos[i][ff];
      if (t[i].cnt[bb]) {
        for (auto _v : t[i].vv[bb]) {
          int v = _v + (i - 1) * B;
          if (!del[v]) ret = std::min(ret, v);
        }
        return ret;
      }
      // int cc = 0;
      // // std::cerr << id << ' ' << i << '\n';
      // for (auto v : t[i].vv[bb])
      //   if (!del[v]) cc += !del[v], ret = std::min(ret, v);
      // assert(cc == t[i].cnt[bb]);
      // if (t[i].cnt[bb]) {
      //   for (auto v : t[i].vv[bb])
      //     if (!del[v]) ret = std::min(ret, v);
      //   assert(ret != 1e9);
      //   return ret;
      // }
    }
  }
  if (ret == 1e9) ret = 0;
  return ret;
}

void dickdreamer() {
  std::cin >> n >> q;
  B = sqrtl(q);
  if (!B) B = 1;
  for (int i = 1; i <= n; ++i) fir[i] = i;
  for (int i = 1; i <= q; ++i) {
  // for (int i = 1; i <= 8; ++i) {
    if ((i - 1) % B == 0) {
      int bid = (i - 1) / B + 1;
      t[bid].sz = 1, t[bid].seg[1] = {1, n};
    }
    std::cin >> op[i] >> a[i] >> p[i];
    a[i] = (a[i] + res[i - 1] - 1) % (op[i] <= 2 ? n : q) + 1;
    p[i] = (p[i] + res[i - 1] - 1) % n + 1;
    // std::cerr << op[i] << ' ' << a[i] << ' ' << p[i] << '\n';
    // if (i == 4) std::cerr << "fuckkk " << pos[1][2] << '\n';
    if (op[i] == 1) update1(i, a[i]);
    else if (op[i] == 2) update2(i, a[i]);
    else update3(i, a[i]);
    res[i] = query(i, p[i]);
    std::cout << res[i] << '\n';
    if (i % B == 0) rebuild(i / B);
    // std::cerr << "??? " << i << ' ' << res[i] << '\n';
  }
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