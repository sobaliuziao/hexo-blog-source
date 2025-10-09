---
title: CF571E Geometric Progressions 题解
date: 2024-08-06 15:37:00
---

##  Description

- 给定 $n$ 以及 $n$ 个正整数对 $a_i, b_i$。
- 第 $i$ 对 $a_i, b_i$ 确定了一个序列 $\{a_i, a_i b_i, a_i b_i^2, a_i b_i^3, \ldots \}$。
- 询问最小的在 $n$ 个序列中都有出现的数，或者判断不存在。
- $n \le 100$，$a_i, b_i \le {10}^9$，答案对 ${10}^9 + 7$ 取模。

## Solution

设答案为 $k$，注意到答案很大，考虑分解质因数，设 $cnt_p(x)$ 表示 $x$ 的质因数分解有多少个 $p$，每次合并两个集合。

合并时有 $3$ 种情况：空集、只有一个数的集合、有无穷个数的集合。

考虑如何合并。设最终的数可以表示为 $a_ib_i^{k_i}$，那么一定满足 $cnt_p(a_i)+k_icnt_p(b_i)=cnt_p(a_j)+k_jcnt_p(b_j)$。对于所有 $p$，如果 $cnt_p(b_i)$ 和 $cnt_p(b_j)$ 都为 $0$，就只用判断 $cnt_p(a_i)$ 是否等于 $cnt_p(a_j)$。

如果 $cnt_p(b_i)$ 和 $cnt_p(b_j)$ 只有一个 $0$，那么就可以唯一确定 $k$ 了，求出来然后判断即可。

如果都不是 $0$，那么一定为关于 $k_i$ 和 $k_j$ 的不定方程，如果有 $\geq 2$ 种不同的方程就能唯一确定 $k$。否则就可以通过 exgcd 把 $(a_i,b_i)$ 和 $(a_j,b_j)$ 合并，设 $x$ 为 $k_i$ 的最小正整数解，结果就为 $\left(a_ib_i^x,\prod p^{\text{lcm}{\left\{cnt_p(b_i),cnt_p(b_j)\right\}}}\right)$。

这里由于 $cnt_p(b_i)\leq 30$，所以所有 $cnt$ 的 lcm 不会爆 `long long`，对于乘法用 `int128` 即可。

时间复杂度：还不会算。

## Code

```cpp
#include <bits/stdc++.h>

#define int int64_t

using i128 = __int128_t;
using pii = std::pair<int, int>;

const int kMaxN = 105, kMod = 1e9 + 7;

int n;
int a[kMaxN], b[kMaxN];
std::vector<int> pri, va[kMaxN], vb[kMaxN];

constexpr int qpow(int bs, int64_t idx = kMod - 2) {
  int ret = 1;
  for (; idx; idx >>= 1, bs = (int64_t)bs * bs % kMod)
    if (idx & 1)
      ret = (int64_t)ret * bs % kMod;
  return ret;
}

inline int add(int x, int y) { return (x + y >= kMod ? x + y - kMod : x + y); }
inline int sub(int x, int y) { return (x >= y ? x - y : x - y + kMod); }
inline void inc(int &x, int y) { (x += y) >= kMod ? x -= kMod : x; }
inline void dec(int &x, int y) { (x -= y) < 0 ? x += kMod : x; }

bool isprime(int x) {
  for (int i = 2; i * i <= x; ++i)
    if (x % i == 0)
      return 0;
  return 1;
}

i128 exgcd(i128 a, i128 b, i128 &x, i128 &y) {
  if (!b) { x = 1, y = 0; return a; }
  i128 d = exgcd(b, a % b, y, x);
  y -= a / b * x;
  return d;
}

pii merge(std::pair<i128, i128> a, std::pair<i128, i128> b) {
  if (!~a.second || !~b.second) return {0, -1};
  if (a == b) return a;
  if (!~a.first) return b;
  if (!~b.first) return a;
  if (a.second > b.second) std::swap(a, b);
  if (!a.second && !b.second) {
    if (a.first == b.first) return {0, -1};
    else return a;
  } else if (!a.second) {
    if (a.first >= b.first && (a.first - b.first) % b.second == 0) return a;
    else return {0, -1};
  }
  i128 x, y;
  // a.second * x + a.first = b.second * y + b.first
  // a.second * x - b.second * y = b.first - a.first
  i128 d = exgcd(a.second, b.second, x, y);
  if ((a.first - b.first) % d != 0) return {0, -1};
  y = -y;
  // a.second * x - b.second * y = d
  x *= (b.first - a.first) / d, y *= (b.first - a.first) / d;
  // a.second * x - b.second * y = b.first - a.first
  a.second /= d, b.second /= d;
  int tmp = (b.first - a.first) / d;
  // a.second * x - b.second * y = tmp
  assert(a.second * x - b.second * y == tmp);
  assert((a.second * x * d + a.first - b.first) % (b.second * d) == 0);
  x = (x % b.second + b.second) % b.second;
  if (a.second * x - tmp < 0) {
    int to = (tmp + a.second - 1) / a.second;
    assert(x < to);
    int det = (to - x + b.second - 1) / b.second;
    x += det * b.second;
  }
  int val = a.second * x * d + a.first, lcm = a.second * b.second * d;
  // std::cerr << "heige " << a.first << ' ' << a.second * d << ' ' << b.first << ' ' << b.second * d << ' ' << val << ' ' << lcm << '\n';
  assert((val - b.first) % (b.second * d) == 0);
  return {val, lcm};
}

std::vector<int> getp(int x) {
  std::vector<int> vec;
  for (int i = 2; i * i <= x; ++i) {
    if (x % i == 0) {
      vec.emplace_back(i);
      for (; x % i == 0; x /= i) {}
    }
  }
  if (x > 1) vec.emplace_back(x);
  return vec;
}

int getcnt(int a, int p) {
  int cnt = 0;
  for (; a % p == 0; a /= p) ++cnt;
  return cnt;
}

int getval(std::vector<int> v) {
  int ret = 1;
  for (int i = 0; i < (int)v.size(); ++i)
    ret = 1ll * ret * qpow(pri[i], v[i]) % kMod;
  return ret;
}

bool check(std::vector<int> v) {
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j < (int)pri.size(); ++j) {
      if (v[j] < va[i][j]) return 0;
      if (!vb[i][j] && v[j] != va[i][j] || vb[i][j] && (v[j] - va[i][j]) % vb[i][j] != 0) return 0;
    }
  }
  return 1;
}

bool equal(std::tuple<int, int, int> a, std::tuple<int, int, int> b) {
  return ((i128)std::get<0>(a) * std::get<1>(b) == (i128)std::get<1>(a) * std::get<0>(b))
      && ((i128)std::get<1>(a) * std::get<2>(b) == (i128)std::get<2>(a) * std::get<1>(b));
}

std::pair<int, int> calc(std::tuple<i128, i128, i128> a, std::tuple<i128, i128, i128> b) {
  auto [a1, a2, a3] = a;
  auto [b1, b2, b3] = b;
  i128 kk = a2 * b1 - a1 * b2, vv = a3 * b1 - b3 * a1;
  if (!kk) return {-1, -1};
  if (kk && (vv / kk) * kk != vv) return {-1, -1};
  i128 y = vv / kk;
  if (y < 0) return {-1, -1};
  kk = a1, vv = a3 - a2 * y;
  if (!kk) kk = b1, vv = b3 - b2 * y;
  if (!kk && vv || kk && (vv / kk) * kk != vv) return {-1, -1};
  i128 x = vv / kk;
  assert(a1 * x + a2 * y == a3 && b1 * x + b2 * y == b3);
  if (x < 0 || y < 0) return {-1, -1};
  else return {x, y};
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i] >> b[i];
    auto tmp1 = getp(a[i]), tmp2 = getp(b[i]);
    for (auto x : tmp1) pri.emplace_back(x);
    for (auto x : tmp2) pri.emplace_back(x);
  }
  std::sort(pri.begin(), pri.end()), pri.erase(std::unique(pri.begin(), pri.end()), pri.end());
  for (int i = 1; i <= n; ++i) {
    va[i].resize(pri.size()), vb[i].resize(pri.size());
    for (int j = 0; j < (int)pri.size(); ++j) {
      va[i][j] = getcnt(a[i], pri[j]);
      vb[i][j] = getcnt(b[i], pri[j]);
    }
  }
  for (int i = 1; i < n; ++i) {
    bool fl = 0;
    std::tuple<int, int, int> now = {-1, -1, -1};
    for (int j = 0; j < (int)pri.size(); ++j) {
      int x = vb[i][j], y = -vb[i + 1][j], z = va[i + 1][j] - va[i][j];
      if (!x && !y) {
        if (z) return void(std::cout << "-1\n");
      } else if (!x) {
        int tmp = z / y;
        if (tmp * y != z || tmp < 0) return void(std::cout << "-1\n");
        std::vector<int> vec(pri.size());
        for (int k = 0; k < (int)pri.size(); ++k)
          vec[k] = va[i + 1][k] + vb[i + 1][k] * tmp;
        if (check(vec)) return void(std::cout << getval(vec) << '\n');
      } else if (!y) {
        int tmp = z / x;
        if (tmp * x != z || tmp < 0) return void(std::cout << "-1\n");
        std::vector<int> vec(pri.size());
        for (int k = 0; k < (int)pri.size(); ++k)
          vec[k] = va[i][k] + vb[i][k] * tmp;
        if (check(vec)) return void(std::cout << getval(vec) << '\n');
      }
      if (!fl) fl = 1, now = {x, y, z};
      else {
        if (!equal(now, {x, y, z})) {
          auto p = calc(now, {x, y, z});
          if (!~p.first && !~p.second) return void(std::cout << "-1\n");
          else {
            std::vector<int> vec(pri.size());
            for (int k = 0; k < (int)pri.size(); ++k) {
              vec[k] = va[i][k] + vb[i][k] * p.first;
            }
            if (check(vec)) return void(std::cout << getval(vec) << '\n');
            else return void(std::cout << "-1\n");
          }
        }
      }
    }
    for (int j = 0; j < (int)pri.size(); ++j) {
      auto p = merge({va[i][j], vb[i][j]}, {va[i + 1][j], vb[i + 1][j]});
      if (!~p.second) return void(std::cout << "-1\n");
      va[i + 1][j] = p.first, vb[i + 1][j] = p.second;
    }
  }
  std::cout << getval(va[n]) << '\n';
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