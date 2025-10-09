---
title: P11647 【MX-X8-T6】「TAOI-3」俄罗斯蓝猫 题解
date: 2025-02-01 14:49:00
---

## Description

有 $n$ 个 $[0, 10^{18}]$ 之间**随机**的整数。可以提出两次询问，每次询问给出不超过 $n-1$ 个二元组 $(x_i,y_i)$。返回 $a_{x_i}+a_{y_i}$ 从小到大排序的结果。

不能询问 $(i,i)$ 或者重复的无序对 $(i,j)$。

要求按顺序返回这 $n$ 个数。$1\leq n\leq 500$。

## Solution

注意到 $n$ 比较小，值域很大且随机，所以在询问得到可以大致通过加减操作确定其是什么，并且正确率很高。设 $s(i,j)=a_i+a_j$。

首先考虑如果知道 $a_1,a_2$，怎么推出后面的数。

注意到 $s(i-1,i)-s(2,i)=a_{i-1}-a_2$，所以如果已经推出 $a_1,a_2,\ldots,a_{i-1}$，可以通过询问 $\left\{(1,2),(2,3),\ldots,(n-1,n)\right\}$ 和 $\left\{(2,3),(2,4),\ldots,(2,n-1)\right\}$ 并从中暴力枚举出满足条件的 $s(i-1,i)$ 和 $s(2,i)$，然后就可以通过 $s(i-1,i)$ 和 $a_{i-1}$ 来求出 $a_i$。

---

那么怎么知道一部分数的值呢。

由于上面的那个做法已经把两次询问都用上了，所以只能并行地去做一些询问来得到 $a_1,a_2$。

考虑确定前 $4$ 个数。

先询问 $\left\{(1,2),(1,3),(1,4),(4,5),(5,6),\ldots,(n-1,n)\right\}$ 和 $\left\{(2,3),(3,4),(2,4),(2,5),(2,6),\ldots,(2,n)\right\}$。

通过首先由于 $s(1,2)+s(3,4)=s(1,3)+s(2,4)=s(1,4)+s(2,3)$，这里有 $3$ 个相等的和，次数一定是最多的，所以可以以此求出 $\left\{s(1,2),s(1,3),s(1,4)\right\}$ 和 $\left\{s(2,3),s(3,4),s(2,4)\right\}$，然后就可以得到 $a_1$ 和 $\left\{a_2,a_3,a_4\right\}$。同时通过之前的 $(4,5)$ 和 $(2,5)$ 可以得到 $a_4-a_2$，所以可以以很大的概率确定 $a_2,a_3,a_4$ 分别是哪个。

然后用上面的做法就可以得到后面的数了。

时间复杂度：$O(n^3)$。

## Code

```cpp
#include <bits/stdc++.h>

#ifdef ORZXKR
#include "grader.cpp"
#endif

using i64 = long long;

std::vector<i64> game(int n);
std::vector<i64> ask(std::vector<int> x,std::vector<int> y);

std::vector<int> work(std::vector<int> vec) {
  for (auto &x : vec) --x;
  return vec;
}

void del(std::vector<i64> &vec, i64 x) {
  std::vector<i64> ret;
  for (auto xx : vec)
    if (xx != x)
      ret.emplace_back(xx);
  vec = ret;
}

std::pair<i64, i64> getpr(std::vector<i64> &vec1, std::vector<i64> &vec2, i64 x) {
  for (auto a : vec1)
    for (auto b : vec2)
      if (a - b == x)
        return {a, b};
  return {-1, -1};
}

std::vector<i64> game(int n) {
  std::vector<i64> arr(n), res1, res2;
  std::vector<int> vec1, vec2, vec3, vec4;
  vec1 = {1, 1, 1}, vec2 = {2, 3, 4};
  for (int i = 4; i <= n - 1; ++i) vec1.emplace_back(i), vec2.emplace_back(i + 1);
  vec3 = {2, 3, 4}, vec4 = {3, 4, 2};
  for (int i = 5; i <= n; ++i) vec3.emplace_back(2), vec4.emplace_back(i);
  res1 = ask(work(vec1), work(vec2)), res2 = ask(work(vec3), work(vec4));
  // get a[1] and {a[2], a[3], a[4]}
  std::map<i64, std::vector<std::pair<i64, i64>>> mp;
  for (auto x : res1)
    for (auto y : res2)
      mp[x + y].emplace_back(x, y);
  std::vector<i64> v234;
  i64 mxv = -1, cc = 0;
  for (auto [x, vec] : mp) {
    if (vec.size() > cc) {
      mxv = x, cc = vec.size();
    }
  }
  i64 sum234 = 0;
  for (auto [x, y] : mp[mxv])
    arr[0] += x, sum234 += y, del(res1, x), del(res2, y);
  assert(sum234 % 2 == 0);
  sum234 /= 2;
  assert(arr[0] >= sum234 && (arr[0] - sum234) % 3 == 0);
  arr[0] = (arr[0] - sum234) / 3;
  for (auto [x, y] : mp[mxv]) v234.emplace_back(x - arr[0]);
  for (int i = 0; i < 3; ++i) {
    for (int j = 0; j < 3; ++j) {
      if (i == j) continue;
      auto pr = getpr(res1, res2, v234[i] - v234[j]);
      if (pr != std::pair<i64, i64>{-1, -1}) {
        arr[3] = v234[i], arr[1] = v234[j], arr[2] = v234[3 - i - j];
      }
    }
  }
  // std::cerr << arr[0] << ' ' << arr[1] << ' ' << arr[2] << ' ' << arr[3] << ' ';
  for (int i = 4; i < n; ++i) {
    auto pr = getpr(res1, res2, arr[i - 1] - arr[1]);
    // assert(pr != std::pair<i64, i64>{-1, -1});
    // assert(pr.first != -1 && pr.second != -1);
    del(res1, pr.first), del(res2, pr.second);
    arr[i] = pr.first - arr[i - 1];
    // std::cerr << arr[i] << ' ';
  }
  // std::cerr << '\n';
  return arr;
}
```