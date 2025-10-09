---
title: P9353 [JOI 2023 Final] Modern Machine 题解
date: 2024-10-20 21:10:00
---

## Description

Bitaro 生日这天收到了一个 JOI 机作为生日礼物。JOI 机由一个球，$N$ 条光带和 $M$ 个按钮组成。光带从 $1$ 到 $N$ 编号。当 Bitaro 打开开关时，光带 $i\ (1\le i\le N)$ 会发出颜色 $C_i$ 的光（蓝光 $(\texttt{B})$ 或红光 ($\texttt{R})$）。按钮从 $1$ 到 $M$ 编号。如果 Bitaro 按下按钮 $j\ (1\le j\le M)$，将发生如下事情。

1. 把球放置在光带 $A_j$ 上。
2. 光带 $A_j$ 变成红色（不管它原来是什么颜色）
3. 进行如下操作，直到球被移除。
	令 $p$ 为球目前所在的光带编号。
	- 如果光带 $p$ 是蓝色，
    	光带 $p$ 变为红色。在此之后，如果 $p=1$，这个球就被移除。否则，球移向光带 $p-1$。
	- 如果光带 $p$ 是红色，
		光带 $p$ 变为蓝色。在此之后，如果 $p=N$，这个球就被移除。否则，球移向光带 $p+1$。

Bitaro 对 JOI 机十分感兴趣。他计划进行 $Q$ 次实验。在第 $k\ (1\le k\le Q)$ 次实验中，在 Bitaro 开启电源后，他将按 $L_k,L_k+1,\ldots R_k$ 的顺序按下这些开关。在 Bitaro 按下一个开关后，他将等到球被移除后再按下下一个开关。

给定 JOI 机和实验的情况，写一个程序计算对于每个实验，当实验结束后红色的光带有多少。

注：每次实验之间互相独立。

## Solution

先考虑怎么暴力地求出答案。

结论是对于一个在第 $i$ 个位置的操作，一定是把前 $i$ 个蓝球染红或者后 $n-i+1$ 个红球染蓝。证明就考虑最终状态只和最后一次将前缀染红或后缀染蓝的位置有关。

假设最后一次是将前缀染红。在 $[1,i-1]$ 这些位置中碰到红色会变向，$[i,n]$ 碰到蓝色会变向，设 $[1,i-1]$ 中有 $k$ 个红色，$i-1-k$ 个蓝色，那么左边变 $k$ 次向，右边则有 $k+1$ 次，所以右边会把 $k+1$ 个蓝色染红，左边 $i-1-k$ 个，加起来就是将前 $i$ 个蓝色染红。对于后缀染蓝是同理的。

由于这两种操作不能同时发生，所以只需要通过红/蓝球的个数即可判断选择哪个。

---

然后考虑第子任务 4,5 怎么做。

设当前前 $t$ 个是红，操作位置为 $i$，由于 $i$ 初始的颜色会有影响所以需要分类讨论：

如果 $i\leq t$ 且 $i\leq n-t$，则 $t\leftarrow t+i$，否则 $t\leftarrow t-(n-i+1)$。

如果 $i>t$ 且 $i\leq n-t-1$，则 $t\leftarrow t+i+1$，否则 $t\leftarrow t-(n-i)$。

写成简洁的形式：

$$
f_i(t)=
\begin{cases}
(t+i)\bmod (n+1)\ \ \ \ \ \ \ \ \ \ \ \ &(i\leq t)\\
(t+i+1)\bmod (n+1)\ \ \ \ \ \ \ \ \ \ \ \ &(i> t)
\end{cases}
$$

注意到这是个分段函数并且段数是 $O(操作序列大小)$ 的，所以线段树暴力维护分段函数即可，时间复杂度：$O\left(M\log^2N+Q\log N\right)$

---

对于一般情况，操作任意时刻一定是子任务 4,5 或者一段前缀红，后缀蓝，中间不变的形态。

为了简化写法，先在所有蓝之前或者末尾分个段和所有红之后或者开头分个段，这样每次将前 $i$ 个蓝变红就只需要让红的前缀段的指针往后挪 $i$ 个，红变蓝同理。

假设当前红色的前缀长度为 $r$，蓝色的后缀长度为 $b$，考虑找到第一个前后缀汇合的时刻。

那么在这个时刻之前，假设操作位置 $i\leq r$，如果前 $i$ 个蓝染红，则 $r\leftarrow r+i$，否则就汇合了。如果 $i\geq n-b+1$，后 $n-i+1$ 个红染蓝则 $b\leftarrow b+n-i$，否则也汇合了。

如果 $r+1\leq i\leq n-b$ 就不好做了，但是注意到这样的 $i$ 是很少的，因为每次操作至少会让 $r/b$ 中的一个翻倍，所以只有 $O(\log N)$ 个。

但是要快速找到在中间的操作仍然是不好做的，因为前后缀的长度是一直在变化的。这时可以设不超过 $r$ 的最大 $2$ 的幂次为 $x$，不超过 $b$ 的最大幂次为 $y$，对于 $x+1\leq i\leq n-y$ 的操作仍然会让 $x,y$ 中的至少一个翻倍，这样的操作仍然只有 $O(\log N)$ 个。

于是就可以预处理了，设 $nxt_{x,y,k}$ 表示在 $r$ 为 $x$，$b$ 为 $y$ 的情况下，$a_k$ 后面的第一个在 $[x+1,n-y]$ 内的操作下标，$sumr_{x,y,k}$ 和 $sumb_{x,y,k}$ 表示在 $r$ 为 $x$，$b$ 为 $y$ 的情况下前 $k$ 个操作对 $r/b$ 的贡献。

询问时如果在 $nxt$ 之前都无法汇合则跳到 nxt，更新 $r$ 和 $b$ 并算上 $nxt$ 的贡献，否则二分出第一个汇合的时刻即可。

时间复杂度：$O\left((M+Q)\log^2 N\right)$。

## Code

```cpp
#include <bits/stdc++.h>

// #define int int64_t

const int kMaxN = 1.2e5 + 5, kLog = 18;

int n, m, q, cr, cb;
int a[kMaxN], nxt[kLog][kLog][kMaxN], rx[kMaxN], bx[kMaxN], lg[kMaxN], prer[kMaxN];
int64_t sumr[kLog][kLog][kMaxN], sumb[kLog][kLog][kMaxN];
std::string s;

struct SGT {
  std::vector<std::pair<int, int>> v[kMaxN * 4];

  int func(int x, int val) {
    auto it = std::upper_bound(v[x].begin(), v[x].end(), std::pair<int, int>(val, 1e9)) - 1;
    return val + it->second;
  }

  void pushup(int x) {
    int ls = (x << 1), rs = (x << 1 | 1);
    for (int i = 0; i < (int)v[ls].size(); ++i) {
      auto [L, val] = v[ls][i];
      int R = (i + 1 == (int)v[ls].size() ? n + 1 : v[ls][i + 1].first);
      auto itl = std::lower_bound(v[rs].begin(), v[rs].end(), std::pair<int, int>(L + val, -1e9));
      auto itr = std::lower_bound(v[rs].begin(), v[rs].end(), std::pair<int, int>(R + val, -1e9));
      v[x].emplace_back(L, 0);
      for (auto it = itl; it != itr; ++it) {
        v[x].emplace_back(it->first - val, 0);
      }
    }
    std::sort(v[x].begin(), v[x].end());
    v[x].erase(std::unique(v[x].begin(), v[x].end()), v[x].end());
    for (auto &[xx, val] : v[x]) {
      val = func(rs, func(ls, xx)) - xx;
    }
  }

  void build(int x, int l, int r) {
    if (l == r) {
      if (n - a[l] > 0) {
        v[x].emplace_back(0, a[l] + 1);
        if (n - a[l] <= a[l] - 1) v[x].emplace_back(n - a[l], a[l] - n);
      } else {
        v[x].emplace_back(0, a[l] - n);
      }
      if (a[l] < n + 1 - a[l]) {
        v[x].emplace_back(a[l], a[l]);
        v[x].emplace_back(n - a[l] + 1, a[l] - (n + 1));
      } else {
        v[x].emplace_back(a[l], a[l] - (n + 1));
      }
      std::sort(v[x].begin(), v[x].end());
      return;
    }
    int mid = (l + r) >> 1;
    build(x << 1, l, mid), build(x << 1 | 1, mid + 1, r);
    pushup(x);
  }

  int query(int x, int l, int r, int ql, int qr, int val) {
    if (l > qr || r < ql) {
      return val;
    } else if (l >= ql && r <= qr) {
      return func(x, val);
    }
    int mid = (l + r) >> 1;
    return query(x << 1 | 1, mid + 1, r, ql, qr, query(x << 1, l, mid, ql, qr, val));
  }
} sgt;

void prework() {
  sgt.build(1, 1, m);

  lg[0] = -1;
  for (int i = 1; i <= 1.2e5; ++i) lg[i] = lg[i >> 1] + 1;

  for (int i = 1; i <= n; ++i) prer[i] = prer[i - 1] + (s[i] == 'R');

  for (int i = 1; i <= n + 1; ++i) {
    if (i == n + 1 || s[i] == 'B') {
      rx[++cr] = i - 1;
    }
  }
  for (int i = n; ~i; --i) {
    if (!i || s[i] == 'R') {
      bx[++cb] = n - i;
    }
  }

  for (int x = 0; x <= lg[n] + 1; ++x) {
    for (int y = 0; y <= lg[n] + 1; ++y) {
      int lenr, lenb;
      if (!x) lenr = 0;
      else lenr = (1 << (x - 1));
      if (!y) lenb = 0;
      else lenb = (1 << (y - 1));
      if (lenr + lenb > n) continue;
      for (int i = 1; i <= m; ++i) {
        sumr[x][y][i] = sumr[x][y][i - 1];
        sumb[x][y][i] = sumb[x][y][i - 1];
        if (a[i] <= lenr) sumr[x][y][i] += a[i];
        else if (n - a[i] + 1 <= lenb) sumb[x][y][i] += n - a[i];
      }
      nxt[x][y][m + 1] = m + 1;
      for (int i = m; i; --i) {
        if (a[i] > lenr && a[i] <= n - lenb) nxt[x][y][i] = i;
        else nxt[x][y][i] = nxt[x][y][i + 1];
      }
    }
  }
}

int getcntr(int l, int r) {
  if (l > r) return 0;
  return prer[r] - prer[l - 1];
}

int getcntb(int l, int r) {
  if (l > r) return 0;
  return (r - l + 1) - (prer[r] - prer[l - 1]);
}

char getch(int x, int nowr, int nowb) {
  assert(x >= 1 && x <= n);
  if (x <= rx[nowr]) return 'R';
  else if (x > n - bx[nowb]) return 'B';
  else return s[x];
}

int solve(int l, int r) {
  int pos = l - 1, nowr = 1, nowb = 1, val = -1;
  for (;;) {
    assert(rx[nowr] + bx[nowb] <= n);
    if (rx[nowr] + bx[nowb] >= n) {
      val = rx[nowr];
      break;
    }
    int x = lg[rx[nowr]] + 1, y = lg[bx[nowb]] + 1;
    int nxtp = std::min(nxt[x][y][pos + 1], r + 1);
    int detr = std::min<int>(sumr[x][y][nxtp - 1] - sumr[x][y][pos], n);
    int detb = std::min<int>(sumb[x][y][nxtp - 1] - sumb[x][y][pos], n);
    if (rx[std::min(nowr + detr, cr)] + bx[std::min(nowb + detb, cb)] < n) {
      nowr += detr, nowb += detb, pos = nxtp;
      if (pos == r + 1) break;
      int cntr = rx[nowr] + getcntr(rx[nowr] + 1, n - bx[nowb]);
      if (getch(a[pos], nowr, nowb) == 'B') ++cntr;
      if (n - cntr >= a[pos]) { // 把前 a[pos] 个 B 变成 R
        if (getch(a[pos], nowr, nowb) == 'B') ++nowr;
        nowr = std::min(nowr + a[pos], cr);
        if (rx[nowr] + bx[nowb] >= n) {
          val = cntr + a[pos];
          break;
        }
      } else { // 把后 n - a[pos] + 1 个 R 变成 B
        assert(cntr >= n - a[pos] + 1);
        if (getch(a[pos], nowr, nowb) == 'B') --nowb;
        nowb = std::min(nowb + n - a[pos] + 1, cb);
        if (rx[nowr] + bx[nowb] >= n) {
          val = cntr - (n - a[pos] + 1);
          break;
        }
      }
    } else {
      int L = pos, R = nxtp, res = pos;
      while (L + 1 < R) {
        int mid = (L + R) >> 1;
        int detr = std::min<int>(sumr[x][y][mid] - sumr[x][y][pos], n);
        int detb = std::min<int>(sumb[x][y][mid] - sumb[x][y][pos], n);
        if (rx[std::min(nowr + detr, cr)] + bx[std::min(nowb + detb, cb)] >= n) R = res = mid;
        else L = mid;
      }
      assert(res > pos);
      int detr = std::min<int>(sumr[x][y][res - 1] - sumr[x][y][pos], n);
      int detb = std::min<int>(sumb[x][y][res - 1] - sumb[x][y][pos], n);
      nowr += detr, nowb += detb;
      assert(nowr <= cr && nowb <= cb && rx[nowr] + bx[nowb] < n);
      int cntr = rx[nowr] + getcntr(rx[nowr] + 1, n - bx[nowb]);
      if (getch(a[res], nowr, nowb) == 'B') ++cntr;
      pos = res;
      if (a[res] <= n - cntr) {
        val = cntr + a[res];
        break;
      } else {
        val = cntr - (n - a[res] + 1);
        break;
      }
    }
  }
  if (val == -1) {
    return rx[nowr] + getcntr(rx[nowr] + 1, n - bx[nowb]);
  } else {
    return sgt.query(1, 1, m, pos + 1, r, val);
  }
}

void dickdreamer() {
  std::cin >> n >> m >> s;
  s = " " + s;
  for (int i = 1; i <= m; ++i) std::cin >> a[i];
  prework();
  std::cin >> q;
  for (int i = 1; i <= q; ++i) {
    int l, r;
    std::cin >> l >> r;
    std::cout << solve(l, r) << '\n';
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