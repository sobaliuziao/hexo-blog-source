---
title: P5123 [USACO18DEC]Cowpatibility G 题解
date: 2022-01-24 14:32:00
---

## P5123 [USACO18DEC]Cowpatibility G

这题正着直接做显然不行，所以要反着容斥做。

记录 $f_i$ 表示从第 $1\sim i-1$ 头奶牛中可以和第 $i$ 头奶牛和谐共处的头数。

$f_i=\text{有1个数与 i 中的匹配的个数}-\text{有2个数与 i 中的匹配的个数}+\text{有3个数与 i 中的匹配的个数}-\text{有4个数与 i 中的匹配的个数}+\text{有5个数与 i 中的匹配的个数}$ 。

这个匹配的个数显然可以用 $5$ 个 $\text{map+tuple}$ 记，每次算完 $f_i$ 就将 $i$ 这头牛的信息加入 $\text{map}$ 即可。

时间复杂度：$O(64\cdot n\log n)$，不开 $O2$ 过不了。

<details>
<summary>代码</summary>
	
```cpp
#include <bits/stdc++.h>

using namespace std;

using ll = long long;

const int kMaxN = 5e4 + 5;

map <tuple <int>, int> mp1;
map <tuple <int, int>, int> mp2;
map <tuple <int, int, int>, int> mp3;
map <tuple <int, int, int, int>, int> mp4;
map <tuple <int, int, int, int, int>, int> mp5;
int n;
int s[6], a, b, c, d, e;
ll ans;

int main() {
  scanf("%d", &n);
  for (int i = 1; i <= n; ++i) {
    scanf("%d%d%d%d%d", &s[1], &s[2], &s[3], &s[4], &s[5]);
    sort(s + 1, s + 6);
    a = s[1], b = s[2], c = s[3], d = s[4], e = s[5];
    ans += i - 1;
    ans -= mp1[make_tuple(a)] + mp1[make_tuple(b)] + mp1[make_tuple(c)] + mp1[make_tuple(d)]
         + mp1[make_tuple(e)];
    ans += mp2[make_tuple(a, b)] + mp2[make_tuple(a, c)] + mp2[make_tuple(a, d)] + mp2[make_tuple(a, e)]
         + mp2[make_tuple(b, c)] + mp2[make_tuple(b, d)] + mp2[make_tuple(b, e)] + mp2[make_tuple(c, d)]
         + mp2[make_tuple(c, e)] + mp2[make_tuple(d, e)];
    ans -= mp3[make_tuple(a, b, c)] + mp3[make_tuple(a, b, d)] + mp3[make_tuple(a, b, e)]
         + mp3[make_tuple(a, c, d)] + mp3[make_tuple(a, c, e)] + mp3[make_tuple(a, d, e)]
         + mp3[make_tuple(b, c, d)] + mp3[make_tuple(b, c, e)] + mp3[make_tuple(b, d, e)]
         + mp3[make_tuple(c, d, e)];
    ans += mp4[make_tuple(a, b, c, d)] + mp4[make_tuple(a, b, c, e)] + mp4[make_tuple(a, b, d, e)]
         + mp4[make_tuple(a, c, d, e)] + mp4[make_tuple(b, c, d, e)];
    ans -= mp5[make_tuple(a, b, c, d, e)];
    ++mp1[make_tuple(a)], ++mp1[make_tuple(b)], ++mp1[make_tuple(c)], ++mp1[make_tuple(d)], 
    ++mp1[make_tuple(e)];
    ++mp2[make_tuple(a, b)], ++mp2[make_tuple(a, c)], ++mp2[make_tuple(a, d)], ++mp2[make_tuple(a, e)], 
    ++mp2[make_tuple(b, c)], ++mp2[make_tuple(b, d)], ++mp2[make_tuple(b, e)], ++mp2[make_tuple(c, d)], 
    ++mp2[make_tuple(c, e)], ++mp2[make_tuple(d, e)];
    ++mp3[make_tuple(a, b, c)], ++mp3[make_tuple(a, b, d)], ++mp3[make_tuple(a, b, e)], 
    ++mp3[make_tuple(a, c, d)], ++mp3[make_tuple(a, c, e)], ++mp3[make_tuple(a, d, e)], 
    ++mp3[make_tuple(b, c, d)], ++mp3[make_tuple(b, c, e)], ++mp3[make_tuple(b, d, e)], 
    ++mp3[make_tuple(c, d, e)];
    ++mp4[make_tuple(a, b, c, d)], ++mp4[make_tuple(a, b, c, e)], ++mp4[make_tuple(a, b, d, e)], 
    ++mp4[make_tuple(a, c, d, e)], ++mp4[make_tuple(b, c, d, e)];
    ++mp5[make_tuple(a, b, c, d, e)];
  }
  printf("%lld\n", ans);
  cerr << 1.0 * clock() / CLOCKS_PER_SEC << 's' << endl;
  return 0;
}
```
</details>