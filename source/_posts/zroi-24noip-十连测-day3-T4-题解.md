---
title: zroi 24noip 十连测 day3 T4 题解
date: 2024-09-15 20:44:00
---

## Description

食蜂操祈有一个栈，她意识到有些排列是可以用这个栈进行排序的。

具体来说，她会以如下方法排序：

- 准备一个空序列。
- 每一步，食蜂操祈可以将排列的第一个数取出，并压入栈中；或将栈顶的数弹出，并放置于序列尾。
- 重复执行以上操作，直到序列中有 $n$ 个数，这 $n$ 个数应当递增。

显然，不是所有的排列都可以用这种方法排序。

食蜂操祈还有一个长度为 $n$ 的排列 $A$，她想知道，有多少长度同样为 $n$ 的排列 $B$，满足其可以用上述方式排序，并且 $B$ 的字典序大于等于 $A$。

对 $998244353$ 取模。

## Solution

考虑什么样序列是合法的。

设 $pos_i$ 表示 $i$ 在序列中的出现位置。那么要让 $1$ 出现在栈顶，就要先把 $[1,pos_1]$ 加到栈里，并且由于栈里的数一定是从栈顶到栈底递增，所以 $[1,pos_1]$ 的数要递减。

要是 $2$ 出现在 $1$ 之前，就先不管。否则一定要满足 $[1,pos_2]$ 去掉 $1$ 后递减。同理可以得到判定条件：一个序列合法当且仅当对于所有 $i$，把 $[1,pos_i]$ 中 $<i$ 的数去掉后，剩余的数递减。即不存在 $i<j<k$ 满足 $a_k<a_i<a_j$。

注意到要求所有字典序大于等于 $A$ 的序列数是一定要钦定一个前缀和 $A$ 相同的，并枚举第一个和 $A$ 不同的位填了什么，后面随便填。这样做是要快速求给定前缀的合法方案数，所以只有上面的那个结论是不够的。

容易发现在**值域**上把没填的数构成的连续段拿出来，那么如果当前位不在第一个连续段则必然不合法。所以填数的过程一定是先把第一个连续段填了，再填第二个，以此类推。

考虑只有一个连续段时的方案数。设 $C_n$ 表示长度为 $n$ 的合法排列数。枚举 $a_1$ 的值 $x$，则贡献为 $C_{x-1}C_{n-x}$。于是 $C_n=\sum_{i=1}^{n}{C_{i-1}C_{n-i}}$，这就是卡特兰数的形式，可以快速计算。如果有多个连续段，方案数就是每个连续段的卡特兰数乘起来。

---

现在加上字典序大于等于 $A$ 的限制，先枚举 $A$ 和 $B$ 的 LCP 以及第一个不同的位 $B$ 填的数，用数据结构维护连续段和方案数即可做到 $O(n^2)$。

考虑优化。

由于第一个不同的位 $B$ 填的数一定是当前第一个连续段的一个从 $A_i+1$ 开始后缀，并且每次操作后会从 $A_i$ 这里分裂，所以可以用启发式分裂的方式。如果 $>A_i$ 的数比 $\leq A_i$ 的数少，则直接枚举后缀。否则枚举前缀，并用总答案减去前缀的答案。

时间复杂度：$O(n\log n)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e6 + 5, kMod = 998244353;

int n;
int a[kMaxN], fac[kMaxN], ifac[kMaxN], inv[kMaxN], cat[kMaxN], icat[kMaxN];

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

int C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * fac[m] * ifac[n] % kMod * ifac[m - n] % kMod;
}

int IC(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return 1ll * ifac[m] * fac[n] % kMod * fac[m - n] % kMod;
}

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = inv[1] = 1;
  for (int i = 2; i <= 2 * n; ++i) {
    inv[i] = 1ll * (kMod - kMod / i) * inv[kMod % i] % kMod;
    fac[i] = 1ll * i * fac[i - 1] % kMod;
    ifac[i] = 1ll * inv[i] * ifac[i - 1] % kMod;
  }

  for (int i = 0; i <= n; ++i) {
    cat[i] = 1ll * C(2 * i, i) * inv[i + 1] % kMod;
    icat[i] = 1ll * IC(2 * i, i) * (i + 1) % kMod;
  }
}

void dickdreamer() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) std::cin >> a[i];
  prework();
  int now = cat[n], ans = 0;
  std::set<std::pair<int, int>> st;
  st.emplace(1, n);
  for (int i = 1; i <= n; ++i) {
    auto p = *st.begin();
    int L = p.first, R = p.second;
    if (a[i] >= L && a[i] <= R) {
      int cnt = 0;
      if (a[i] - L >= R - a[i]) {
        for (int j = a[i] + 1; j <= R; ++j)
          inc(cnt, 1ll * now * icat[R - L + 1] % kMod * cat[j - L] % kMod * cat[R - j] % kMod);
      } else {
        cnt = now;
        for (int j = L; j <= a[i]; ++j)
          dec(cnt, 1ll * now * icat[R - L + 1] % kMod * cat[j - L] % kMod * cat[R - j] % kMod);
      }
      inc(ans, cnt);
    }

    if (a[i] > R) {
      now = 0; break;
    } else if (a[i] == L) {
      now = 1ll * now * icat[R - L + 1] % kMod, st.erase({L, R});
      if (L < R) now = 1ll * now * cat[R - L] % kMod, st.emplace(L + 1, R);
    } else {
      now = 1ll * now * icat[R - L + 1] % kMod, st.erase({L, R});
      if (L < a[i]) now = 1ll * now * cat[a[i] - L] % kMod, st.emplace(L, a[i] - 1);
      if (a[i] < R) now = 1ll * now * cat[R - a[i]] % kMod, st.emplace(a[i] + 1, R);
    }
  }
  inc(ans, now);
  std::cout << ans << '\n';
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