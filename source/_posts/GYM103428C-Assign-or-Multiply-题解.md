---
title: GYM103428C Assign or Multiply 题解
date: 2025-08-26 19:28:00
---

## Description

Zayin 有一个数 $x$，初始时 $x = 1$，还有一个质数 $p$，以及 $n$ 个操作。第 $i$ 个操作必须是以下两种之一：

- $x \leftarrow a_i$ ：将 $x$ 赋值为 $a_i$
- $x \leftarrow x\times a_i$ ：将 $x$ 更新为 $(x \times a_i) \bmod p$

Ziyin 作为调皮的女朋友，可能会**随意打乱操作的顺序**。

Zayin 想知道，在区间 $[0,p-1]$ 内（包括两端），到底有多少个数是**不可能**通过这些操作得到的。你能帮他算出来吗？

$p\leq 2\times 10^5,n\leq 10^6$。

## Solution

先用原根转成加法对 $p-1$ 取模。

考虑把最后一次赋值操作拿出来，那么后面的操作形如在加法操作里找到一个子集，询问可能构成的和有哪些。

有个显然的想法是直接背包，设 $a_i$ 表示 $i$ 是否能够被凑出来，枚举每个加法操作的 $x$，就是让 $a_i\leftarrow a'_{i-x}$。暴力做只能做到 $O\left(\frac{np}{w}\right)$。

注意到我们只需要关心所有当前 $a_i=1$ 且 $a_{i+x}=0$ 的位置，进一步的，我们只需要找到所有 $a_i\neq a_{i+x}$ 的位置，因为将 $i$ 和 $i+x$ 连边后，$01$ 的出现次数和 $10$ 的出现次数是相等的，所以均摊还是对的。

对于找 $a_i\neq a_{i+x}$ 的位置就直接用树状数组维护区间哈希，每次二分即可。

对于最后的赋值操作由于只能选一个，和乘法操作不太一样，所以还需要特殊处理一下。

时间复杂度：$O(n+p^{\frac{5}{4}}+p\log^2p)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

using u64 = uint64_t;

const int kMaxP = 4e5 + 5, kMaxN = 1e6 + 5;

int p, n, rt;
int op[kMaxN], a[kMaxN], g[kMaxP], cnt[kMaxP];
u64 pw[kMaxP * 2];
bool vis[kMaxP];

struct BIT {
  u64 c[kMaxP * 4];
  void upd(int x, u64 v) {
    for (++x; x <= 2 * p + 1; x += x & -x) c[x] += v;
  }
  u64 qry(int x) {
    u64 ret = 0;
    for (++x; x; x -= x & -x) ret += c[x];
    return ret;
  }
  u64 qry(int l, int r) { return l <= r ? (qry(r) - qry(l - 1)) : 0; }
} bit1, bit2;

int findrt(int p) {
  g[0] = -1, g[1] = 0;
  for (int i = 2; i <= p - 1; ++i) {
    bool fl = 1;
    for (int j = 1, mul = i; j < p - 1; ++j, mul = 1ll * mul * i % p) {
      if (mul == 1) { fl = 0; break; }
      g[mul] = j;
    }
    if (fl) return i;
  }
  return 1;
}

int findpos(int lst, int x) {
  int L = lst, R = p - 1, res = p - 1;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (bit1.qry(lst + 1, mid) * pw[x] != bit1.qry(lst + x + 1, mid + x)) R = res = mid;
    else L = mid;
  }
  return res;
}

int findpos1(int lst, int x) {
  int L = lst, R = p - 1, res = p - 1;
  while (L + 1 < R) {
    int mid = (L + R) >> 1;
    if (bit2.qry(lst + 1, mid) * pw[x] != bit1.qry(lst + x + 1, mid + x)) R = res = mid;
    else L = mid;
  }
  return res;
}

void dickdreamer() {
  std::cin >> p >> n; rt = findrt(p);
  int ans = 0; bool fl = 0;
  for (int i = 1; i <= n; ++i) {
    std::cin >> op[i] >> a[i];
    a[i] = g[a[i]];
    if (!~a[i]) ans |= 1;
    if (op[i] == 1) {
      if (~a[i]) ++cnt[a[i]];
    } else {
      fl = 1;
    }
  }
  if (!fl) return void(std::cout << p - 1 << '\n');
  pw[0] = 1;
  for (int i = 1; i <= 2 * p + 1; ++i) pw[i] = 13331ull * pw[i - 1];
  vis[0] = vis[p - 1] = 1, bit1.upd(0, pw[0]), bit1.upd(p - 1, pw[p - 1]);
  for (int i = 1; i < p - 1; ++i) {
    for (int j = 1; j <= cnt[i]; ++j) {
      int now = -1;
      std::vector<int> vec;
      for (; now < p - 1;) {
        now = findpos(now, i);
        if (now < p - 1 && vis[now]) vec.emplace_back(now);
      }
      for (auto x : vec) {
        int r = (x + i) % (p - 1);
        // std::cerr << i << ' ' << p - 1 << ' ' << x << ' ' << r << ' ' << vis[x] << ' ' << vis[r] << '\n';
        assert(vis[x] && !vis[r]);
        vis[r] = vis[r + p - 1] = 1, bit1.upd(r, pw[r]), bit1.upd(r + p - 1, pw[r + p - 1]);
      }
      // std::cerr << "-----------\n";
    }
  }
  for (int i = 0; i <= 2 * p + 1; ++i) bit2.c[i] = bit1.c[i], vis[i] = 0;
  memset(bit1.c, 0, sizeof(bit1.c));
  for (int i = 1; i <= n; ++i) {
    if (op[i] == 1 || !~a[i]) continue;
    int now = -1;
    std::vector<int> vec;
    for (; now < p - 1;) {
      now = findpos1(now, a[i]);
      if (now < p - 1 && !vis[(now + a[i]) % (p - 1)]) vec.emplace_back(now);
    }
    for (auto x : vec) {
      int r = (x + a[i]) % (p - 1);
      assert(!vis[r]);
      // std::cerr << r << '\n';
      vis[r] = vis[r + p - 1] = 1, bit1.upd(r, pw[r]), bit1.upd(r + p - 1, pw[r + p - 1]);
    }
  }
  for (int i = 0; i < p - 1; ++i) ans += vis[i];
  std::cout << p - ans << '\n';
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