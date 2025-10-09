---
title: 'P11696 [JRKSJ ExR] 七影蝶 题解'
date: 2025-09-10 23:03:00
---

## Description

给定一个长度为 $n$ 的非负整数序列 $a_{1\sim n}$。

接下来有 $q$ 次询问，每次询问给出非负整数 $L,R$，求

$$\max_{x=L}^R\left(\sum_{i=1}^n\mathrm{popcount}(a_i+x)\right)$$

其中 $\mathrm{popcount}(x)$ 表示 $x$ 在二进制形式下数位 $1$ 的出现次数。

$1\le n,q\le 5\times 10^5$，$0\le L\le R\le 10^{11}$，$0\le a_i\le 10^{11}$。

## Solution

首先这题显然是把每位的贡献分开算。第 $b$ 位有贡献当且仅当 $2^b\leq (x+v)\bmod 2^{b+1}<2^{b+1}$，即 $x\bmod 2^{b+1}$ 在 $[2^b-v,2^{b+1}-1-v]$ 内。

直接显然是无法维护的，所以考虑按照位数从低位到高位考虑。

这里用线段树的结构去维护这个东西。假设 $[0,b-1]$ 位的线段树已经确定好了，根是 $rt$。

设新的根是 $rt'$。由于 $rt'$ 的左右子树在前 $b-1$ 位的贡献是完全一样的，所以我们可以先把 $rt'$ 的左右儿子都设成 $rt$。修改一个区间 $[l,r]$ 的过程也是类似线段树，每次把访问到的位置新开一个点即可。

时空复杂度都是 $O(n\log^2V)$。

---

考虑优化。

注意到我们维护的东西不一定需要是线段树，只要是有层数且存在递归关系的图就行。

经过观察可以发现如果把第 $b$ 层 $n$ 个区间的断点拿出来，将值域划分成 $2n$ 个线段，如果 $x$ 和 $y$ 在第 $b$ 位在同一个线段则说明在 $>b$ 位也仍然在同一个线段。

证明就考虑一个修改区间 $[l,r)$ 在 $b$ 位贡献的断点是 $l$ 和 $r$，在 $b+1$ 位的贡献则为 $l,r,l+2^b,r+2^b$，显然构成包含关系。

所以我们对于一层把这些线段拿出来再建树，排序用基数排序。询问时由于递归的过程中每一次只会有至多 $2$ 个散区间，线性预处理 rmq+暴力递归即可。这个做法时间复杂度是 $O((n+q)\log V)$。

不过这么做需要做线性 rmq，且询问过程也很繁琐。我们初始时把询问的 $l$ 和 $r+1$ 的后 $b+1$ 位加到第 $b$ 位的修改中就只需要在最高位求一遍区间最大值即可。

可能要卡常。

时间复杂度：$O((n+q)\log V)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using i64 = int64_t;
using pis = std::pair<int, short>;
using pis1 = std::pair<i64, short>;

namespace FASTIO {
char ibuf[1 << 21], *p1 = ibuf, *p2 = ibuf;
inline char getc() {
  return p1 == p2 && (p2 = (p1 = ibuf) + fread(ibuf, 1, 1 << 21, stdin), p1 == p2) ? EOF : *p1++;
}
template<class T> bool read(T &x) {
  x = 0; int f = 0; char ch = getc();
  while (ch < '0' || ch > '9') f |= ch == '-', ch = getc();
  while (ch >= '0' && ch <= '9') x = (x * 10) + (ch ^ 48), ch = getc();
  x = (f ? -x : x); return 1;
}
template<typename A, typename ...B> bool read(A &x, B &...y) { return read(x) && read(y...); }
 
char obuf[1 << 21], *o1 = obuf, *o2 = obuf + (1 << 21) - 1;
void flush() { fwrite(obuf, 1, o1 - obuf, stdout), o1 = obuf; }
inline void putc(char x) { *o1++ = x; if (o1 == o2) flush(); }
template<class T> void write(T x) {
  if (!x) putc('0');
  if (x < 0) x = -x, putc('-');
  char c[40]; int tot = 0;
  while (x) c[++tot] = x % 10, x /= 10;
  for (int i = tot; i; --i) putc(c[i] + '0');
}
void write(char x) { putc(x); }
void write(char *x) { while (*x) putc(*x++); }
void write(const char *x) { while (*x) putc(*x++); }
template<typename A, typename ...B> void write(A x, B ...y) { write(x), write(y...); }
struct Flusher {
  ~Flusher() { flush(); }
} flusher;
} // namespace FASTIO
using FASTIO::read; using FASTIO::putc; using FASTIO::write;

const int kMaxN = 1e6 + 5, kMaxT = 4e7 + 5;

int n, q, lim, tree_cnt;
int mx[kMaxT], tg[40];
i64 a[kMaxN], l[kMaxN], r[kMaxN];
int sz[40];
pis upd[40][kMaxN * 2];
std::vector<int> pos[40];
std::vector<std::pair<int, int>> id[40];
// std::vector<pis> upd[40];

inline void chkmax(int &x, int y) { x = (x > y ? x : y); }
inline void chkmin(int &x, int y) { x = (x < y ? x : y); }



struct SGT {
  int mx[kMaxN * 16];
  void pushup(int x) { mx[x] = std::max(mx[x << 1], mx[x << 1 | 1]); }
  void build(int x, int l, int r) {
    if (l == r) return void(mx[x] = ::mx[id[lim][l].second]);
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }
  int query(int x, int l, int r, int ql, int qr) {
    if (l > qr || r < ql) return 0;
    else if (l >= ql && r <= qr) return mx[x];
    int mid = (l + r) >> 1;
    return std::max(query(x << 1, l, mid, ql, qr), query(x << 1 | 1, mid + 1, r, ql, qr));
  }
} sgt;

namespace Sub1 {
void solve() {
  lim = 31;
  for (int i = 1; i <= n; ++i) {
    for (int b = 0; b <= lim - 1; ++b) {
      i64 len = (1ll << (b + 1)), m = len / 2;
      i64 l = (m - (a[i] & (len - 1)) + len) % len, r = (len - (a[i] & (len - 1)) + len) % len;
      // upd[b + 1].emplace_back(l, 1), upd[b + 1].emplace_back(r, -1);
      upd[b + 1][sz[b + 1]++] = {l, 1}, upd[b + 1][sz[b + 1]++] = {r, -1};
      if (l > r) ++tg[b + 1];
    }
  }
  for (int i = 1; i <= q; ++i) {
    for (int b = 1; b <= lim; ++b) {
      // upd[b].emplace_back(l[i] & ((1ll << b) - 1), 0);
      // upd[b].emplace_back((r[i] + 1) & ((1ll << b) - 1), 0);
      upd[b][sz[b]++] = {l[i] & ((1ll << b) - 1), 0};
      upd[b][sz[b]++] = {(r[i] + 1) & ((1ll << b) - 1), 0};
    }
  }
  id[0] = {{0, 0}};
  int sum = 0;
  for (int b = 1; b <= 31; ++b) {
    static int tag[kMaxN * 2];
    // upd[b].emplace_back(0, 0);
    upd[b][sz[b]++] = {0, 0};
    // for (auto p : upd[b]) std::cerr << p.first << ' ';
    // std::cerr << '\n';
    std::function<void()> radixsort = [&] () {
      static pis pr[kMaxN * 2];
      static std::vector<pis> vec[65536];
      static int cnt[65536];
      int bl = (1 << ((b + 1) / 2)), bl2 = (1ll << b) / bl;
      // if (bl > 4) bl /= 4, bl2 *= 4;
      for (int i = 0; i < bl2; ++i) cnt[i] = 0;
      for (int i = 0; i < sz[b]; ++i) {
        auto [x, v] = upd[b][i];
        ++cnt[x / bl], vec[x % bl].emplace_back(x, v);
      }
      for (int i = 1; i < bl2; ++i) cnt[i] += cnt[i - 1];
      int t = cnt[bl2 - 1];
      for (int i = bl - 1; ~i; --i) {
        for (; vec[i].size(); vec[i].pop_back()) {
          auto [x, v] = vec[i].back();
          pr[cnt[x / bl]--] = {x, v};
        }
      }
      for (int i = 1; i <= t; ++i) {
        auto [x, v] = pr[i];
        if (!pos[b].size() || x != pos[b].back()) pos[b].emplace_back(x);
        tag[pos[b].size() - 1] += v;
      }
    };
    radixsort();
    // for (auto x : pos[b]) std::cout << x << ' ';
    // std::cout << '\n';
    tag[0] += tg[b];
    // for (int i = 0; i < pos[b].size(); ++i) std::cerr << tag[i] << ' ';
    // std::cerr << '\n';
    std::vector<std::pair<int, int>> tmp;
    for (auto [p, id] : id[b - 1]) tmp.emplace_back(p, id);
    for (auto [p, id] : id[b - 1]) tmp.emplace_back(p + (1 << (b - 1)), id);
    //
    for (int i = 0, j = 0; i < pos[b].size(); ++i) {
      assert(tmp[j].first == pos[b][i]);
      if (i) tag[i] += tag[i - 1];
      int nz = ++tree_cnt;
      i64 nxt = (i == pos[b].size() - 1 ? (1ll << b) : pos[b][i + 1]);
      for (; j < tmp.size() && tmp[j].first < nxt; ++j) chkmax(mx[nz], mx[tmp[j].second] + tag[i]);
      id[b].emplace_back(pos[b][i], nz);
    }
    std::fill_n(tag, pos[b].size(), 0);
  }
  sgt.build(1, 0, id[31].size() - 1);
  for (int i = 1; i <= q; ++i) {
    int itl = std::lower_bound(pos[31].begin(), pos[31].end(), l[i]) - pos[31].begin();
    int itr = std::lower_bound(pos[31].begin(), pos[31].end(), r[i] + 1) - pos[31].begin();
    // int ans = 0;
    // for (int j = itl; j < itr; ++j) chkmax(ans, mx[id[31][j].second]);
    // std::cout << ans << '\n';
    write(sgt.query(1, 0, id[31].size() - 1, itl, itr - 1), '\n');
  }
}
} // namespace Sub1

namespace Sub2 {
std::vector<i64> pos[40];
std::vector<std::pair<i64, int>> id[40];

struct SGT {
  int mx[kMaxN * 16];
  void pushup(int x) { mx[x] = std::max(mx[x << 1], mx[x << 1 | 1]); }
  void build(int x, int l, int r) {
    if (l == r) return void(mx[x] = ::mx[id[lim][l].second]);
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }
  int query(int x, int l, int r, int ql, int qr) {
    if (l > qr || r < ql) return 0;
    else if (l >= ql && r <= qr) return mx[x];
    int mid = (l + r) >> 1;
    return std::max(query(x << 1, l, mid, ql, qr), query(x << 1 | 1, mid + 1, r, ql, qr));
  }
} sgt;

void solve() {
  std::vector<i64> upd1, upd2;
  for (int i = 1; i <= n; ++i) {
    upd1.emplace_back(a[i]);
    for (int b = 0; b <= lim - 1; ++b) {
      i64 len = (1ll << (b + 1)), m = len / 2;
      i64 l = (m - (a[i] & (len - 1)) + len) % len, r = (len - (a[i] & (len - 1)) + len) % len;
      if (l > r) ++tg[b + 1];
    }
  }
  upd2.emplace_back(0);
  for (int i = 1; i <= q; ++i) {
    upd2.emplace_back(l[i]), upd2.emplace_back(r[i] + 1);
  }
  id[0] = {{0, 0}};
  int sum = 0;
  for (int b = 1; b <= lim; ++b) {
    static int tag[kMaxN * 2];
    std::vector<pis1> vec1, vec2;
    i64 len = (1ll << b), m = len / 2;
    for (auto x : upd1) {
      if ((x & (m - 1)) == 0) {
        i64 l = (m - (x & (len - 1)) + len) % len, r = (len - (x & (len - 1)) + len) % len;
        if (~l >> (b - 1) & 1) vec1.emplace_back(l, 1);
        else vec1.emplace_back(r, -1);
      }
    }
    for (int i = (int)upd1.size() - 1; ~i; --i) {
      i64 x = upd1[i];
      if ((x & (m - 1)) == 0) continue;
      i64 l = (m - (x & (len - 1)) + len) % len, r = (len - (x & (len - 1)) + len) % len;
      if (~l >> (b - 1) & 1) vec1.emplace_back(l, 1);
      else vec1.emplace_back(r, -1);
    }
    for (auto x : upd1) {
      if ((x & (m - 1)) == 0) {
        i64 l = (m - (x & (len - 1)) + len) % len, r = (len - (x & (len - 1)) + len) % len;
        if (l >> (b - 1) & 1) vec1.emplace_back(l, 1);
        else vec1.emplace_back(r, -1);
      }
    }
    for (int i = (int)upd1.size() - 1; ~i; --i) {
      i64 x = upd1[i];
      if ((x & (m - 1)) == 0) continue;
      i64 l = (m - (x & (len - 1)) + len) % len, r = (len - (x & (len - 1)) + len) % len;
      if (l >> (b - 1) & 1) vec1.emplace_back(l, 1);
      else vec1.emplace_back(r, -1);
    }

    std::vector<i64> now1, now2;

    for (auto x : upd1) {
      if (~x >> (b - 1) & 1) now1.emplace_back(x);
    }
    for (auto x : upd1) {
      if (x >> (b - 1) & 1) now1.emplace_back(x);
    }
    for (auto x : upd2) {
      if (~x >> (b - 1) & 1) now2.emplace_back(x), vec2.emplace_back(x % len, 0);
    }
    for (auto x : upd2) {
      if (x >> (b - 1) & 1) now2.emplace_back(x), vec2.emplace_back(x % len, 0);
    }
    upd1.swap(now1), upd2.swap(now2);
    for (int i = 0, j = 0; i < vec1.size() || j < vec2.size();) {
      i64 x; int v;
      if (j == vec2.size() || i < vec1.size() && vec1[i].first < vec2[j].first) std::tie(x, v) = vec1[i++];
      else std::tie(x, v) = vec2[j++];
      if (!pos[b].size() || x != pos[b].back()) pos[b].emplace_back(x);
      assert(x == pos[b].back());
      tag[pos[b].size() - 1] += v;
    }
    tag[0] += tg[b];
    std::vector<std::pair<i64, int>> tmp;
    for (auto [p, id] : id[b - 1]) tmp.emplace_back(p, id);
    for (auto [p, id] : id[b - 1]) tmp.emplace_back(p + (1ll << (b - 1)), id);
    //
    for (int i = 0, j = 0; i < pos[b].size(); ++i) {
      assert(tmp[j].first == pos[b][i]);
      if (i) tag[i] += tag[i - 1];
      int nz = ++tree_cnt;
      i64 nxt = (i == pos[b].size() - 1 ? (1ll << b) : pos[b][i + 1]);
      for (; j < tmp.size() && tmp[j].first < nxt; ++j) chkmax(mx[nz], mx[tmp[j].second] + tag[i]);
      id[b].emplace_back(pos[b][i], nz);
    }
    std::fill_n(tag, pos[b].size(), 0);
  }
  sgt.build(1, 0, id[lim].size() - 1);
  for (int i = 1; i <= q; ++i) {
    int itl = std::lower_bound(pos[lim].begin(), pos[lim].end(), l[i]) - pos[lim].begin();
    int itr = std::lower_bound(pos[lim].begin(), pos[lim].end(), r[i] + 1) - pos[lim].begin();
    int ans = 0;
    for (int j = itl; j < itr; ++j) chkmax(ans, mx[id[lim][j].second]);
    write(sgt.query(1, 0, id[lim].size() - 1, itl, itr - 1), '\n');
  }
}
} // namespace Sub2

void dickdreamer() {
  read(n, q); lim = 31;
  i64 mx = 0;
  for (int i = 1; i <= n; ++i) read(a[i]), mx = std::max(mx, a[i]);
  for (int i = 1; i <= q; ++i) read(l[i], r[i]), mx = std::max({mx, l[i], r[i]});
  if (mx > 1e9) lim = 38;
  if (mx <= 1e9) Sub1::solve();
  else Sub2::solve();
}

int32_t main() {
#ifdef ORZXKR
  freopen("in.txt", "r", stdin);
  freopen("out.txt", "w", stdout);
#endif
  int T = 1;
  // std::cin >> T;
  while (T--) dickdreamer();
  std::cerr << 1.0 * clock() / CLOCKS_PER_SEC << "s\n";
  return 0;
}
```