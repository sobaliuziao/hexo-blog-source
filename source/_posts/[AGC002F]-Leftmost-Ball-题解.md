---
title: '[AGC002F] Leftmost Ball 题解'
date: 2023-10-19 20:19:00
---

## Description

给你 $n$ 种颜色的球，每种颜色的球有 $k$ 个，把这 $n\times k$ 个球排成一排，把每一种颜色的最左边出现的球涂成白色（初始球不包含白色），求有多少种不同的颜色序列，答案对 $10^9+7$ 取模。

$1\leq n, k\leq 2000$。

## Solution

思考怎样的序列是满足条件的。

假设第 $i$ 个白球的位置为 $p_i$。

那么如果存在一个 $i$，使得 $[1,p_i-1]$ 中出现了 $\geq i$ 种彩球，那么这些球显然找不到它的最左边的白球，自然就不合法了。

否则把每种彩球**第一次**出现的位置排序后把白球顺次染成排序后的颜色即可还原序列。

然后就是计数了。

设 $f_{i,j}$ 表示当前放了 $i$ 个白球，$j$ **种**彩球的合法方案数。

考虑每次在当前没放球的最左边的位置放球。

如果这个位置放白球，那么 $f_{i+1,j}\leftarrow f_{i,j}$。

如果这个位置放彩球，首先要选择这个位置的颜色，为 $n-j$ 种，然后在剩余 $nk-j(k-1)-1$ 个位置放剩下的 $k-2$ 种彩球，方案数就是 $(n-j)\times C_{nk-j(k-1)-1}^{k-2}$，所以 $f_{i,j+1}\leftarrow f_{i,j}\times (n-j)\times C_{nk-j(k-1)-1}^{k-2}$。

---

容易发现这样转移是对的。

首先由于是按顺序放球，所以一定不会算重。然后由于每次放球时，它放的位置都是当前能放的最左边的，所以每次放白球时它左边的彩球数一定是确定的，就是当前所有的彩球数，所以只要 $j\leq i$ 就可以满足 $f_{i,j}$ 状态合法。

时间复杂度：$O(n^2+nk)$。

## Code

<details>
<summary>Code</summary>

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 2e3 + 5, kMod = 1e9 + 7;

namespace Modular {
template<class T>
T qpow(T bs, T idx, T kMod) {
  bs %= kMod;
  int ret = 1;
  for (; idx; idx >>= 1, bs = 1ll * bs * bs % kMod)
    if (idx & 1)
      ret = 1ll * ret * bs % kMod;
  return ret;
}
int inv(int x, int kMod) {
  x %= kMod;
  if (!x) { std::cerr << "inv error\n"; return 0; }
  return qpow(x, kMod - 2, kMod);
}
template<class T, const T kMod>
T add(T x, T y) {
  if (x + y >= kMod) return x + y - kMod;
  else return x + y;
}

template<class T, const T kMod>
T sub(T x, T y) {
  if (x - y < 0) return x - y + kMod;
  else return x - y;
}

template<class T, const T kMod>
struct Mint {
  T x;

  Mint() { x = 0; }
  template<class _T> Mint(_T _x) { x = _x; }

  friend Mint operator +(Mint m1, Mint m2) { return Mint(Modular::add<T, kMod>(m1.x, m2.x)); }
  friend Mint operator -(Mint m1, Mint m2) { return Mint(Modular::sub<T, kMod>(m1.x, m2.x)); }
  friend Mint operator *(Mint m1, Mint m2) { return Mint(1ll * m1.x * m2.x % kMod); }
  friend Mint operator /(Mint m1, Mint m2) { return Mint(1ll * m1.x * inv(m2.x, kMod) % kMod); }
  Mint operator +=(Mint m2) { return x = Modular::add<T, kMod>(x, m2.x); }
  Mint operator -=(Mint m2) { return x = Modular::sub<T, kMod>(x, m2.x); }
  Mint operator *=(Mint m2) { return x = 1ll * x * m2.x % kMod; }
  Mint operator /=(Mint m2) { return x = 1ll * x * inv(m2.x, kMod) % kMod; }

  template<class _T> friend Mint operator +(Mint m1, _T m2) { return Mint(Modular::add<T, kMod>(m1.x, m2 % kMod)); }
  template<class _T> friend Mint operator -(Mint m1, _T m2) { return Mint(Modular::sub<T, kMod>(m1.x, m2 % kMod)); }
  template<class _T> friend Mint operator *(Mint m1, _T m2) { return Mint(1ll * m1.x * m2 % kMod); }
  template<class _T> friend Mint operator /(Mint m1, _T m2) { return Mint(1ll * m1.x * inv(m2, kMod) % kMod); }
  template<class _T> Mint operator +=(_T m2) { return x = Modular::add<T, kMod>(x, m2); }
  template<class _T> Mint operator -=(_T m2) { return x = Modular::sub<T, kMod>(x, m2); }
  template<class _T> Mint operator *=(_T m2) { return x = 1ll * x * m2 % kMod; }
  template<class _T> Mint operator /=(_T m2) { return x = 1ll * x * inv(m2, kMod) % kMod; }
  template<class _T> friend Mint operator +(_T m1, Mint m2) { return Mint(Modular::add<T, kMod>(m1 % kMod, m2.x)); }
  template<class _T> friend Mint operator -(_T m1, Mint m2) { return Mint(Modular::sub<T, kMod>(m1 % kMod, m2)); }
  template<class _T> friend Mint operator *(_T m1, Mint m2) { return Mint(1ll * m1 * m2.x % kMod); }
  template<class _T> friend Mint operator /(_T m1, Mint m2) { return Mint(1ll * m1 * inv(m2.x, kMod) % kMod); }
  friend Mint operator -(Mint &m1) { return Mint(m1.x == 0 ? (kMod - 1) : (m1.x - 1)); }
  friend Mint operator --(Mint &m1) { return m1 = Mint(m1.x == 0 ? (kMod - 1) : (m1.x - 1)); }
  friend Mint operator ++(Mint &m1) { return m1 = Mint(m1.x == (kMod - 1) ? 0 : (m1.x + 1)); }
  friend bool operator ==(Mint m1, Mint m2) { return m1.x == m2.x; }

  friend std::istream &operator >>(std::istream &is, Mint &m) {
    int x;
    is >> x;
    m = Mint(x);
    return is;
  }
  friend std::ostream &operator <<(std::ostream &os, Mint m) {
    os << m.x;
    return os;
  }
};
} // namespace Modular

using mint = Modular::Mint<int, kMod>;

int n, k;
mint f[kMaxN][kMaxN], fac[kMaxN * kMaxN], ifac[kMaxN * kMaxN], inv[kMaxN * kMaxN];

void prework() {
  fac[0] = ifac[0] = fac[1] = ifac[1] = inv[1] = 1;
  for (int i = 2; i <= n * k; ++i) {
    inv[i] = (kMod - kMod / i) * inv[kMod % i];
    fac[i] = i * fac[i - 1];
    ifac[i] = inv[i] * ifac[i - 1];
  }
}

mint C(int m, int n) {
  if (m < n || m < 0 || n < 0) return 0;
  return fac[m] * ifac[n] * ifac[m - n];
}

void dickdreamer() {
  std::cin >> n >> k;
  if (k == 1) { std::cout << "1\n"; return; }
  prework();
  f[0][0] = 1;
  for (int i = 1; i <= n; ++i) {
    for (int j = 0; j <= i; ++j) {
      f[i][j] = f[i - 1][j];
      if (j) f[i][j] += f[i][j - 1] * (n - j + 1) * C(n * k - (j - 1) * (k - 1) - i - 1, k - 2);
    }
  }
  std::cout << f[n][n] << '\n';
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
