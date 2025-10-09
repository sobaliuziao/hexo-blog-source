---
title: 'Trie学习笔记'
date: 2020-12-20 21:57:00
---

# Trie树

Trie树（字典树），是一种查询快速，省空间（相对而言）的一种数据结构。

## 引入

上[百度](https://www.baidu.com/)搜东西，我们发现搜索“洛谷”会出现二十多页的结果。我们知道，百度是一个十分强大的搜索引擎，而且信息量巨大，但我们搜索东西总会非常快得搜索出结果，而且还十分准确。而他们就是运用了Trie实现的。

---

## Trie思想

我们发现，“洛”、“洛谷”、“洛谷强”都有共同的前缀，这时候我们就将前缀“洛”存储成一个节点，然后就变成“谷”，“谷强”，然后再将“谷”存一个，如此往复。如图：

![graph.png](https://cdn.luogu.com.cn/upload/image_hosting/geem6lk6.png)

但是如果是：“洛”，“洛谷”，“洛神赋”的情况，很明显就不能用链来存储，于是就想到了用一个树来存，像这样：

![](https://cdn.luogu.com.cn/upload/image_hosting/w32yxq6y.png)

于是，每个重复的字母都不会被重复存储。

## 模板代码

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 5;

int n, m, tot;
string s;

int node[N * 5][26];
bool exist[N * 5 * 26];

void insert (string s) {
  int len = s.size();
  int now = 1;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';// 当前字母
    if (node[now][k] == 0) node[now][k] = ++tot;//如果此时没有节点，就新建节点
    now = node[now][k];
  }
  exist[now] = true;//标记，表示此时的now对应有结果
  return ;
}

bool search (string s) {
  int len = s.size();
  int now = 1;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';
    if (node[now][k] == 0) return false;//如果此时没有结果，则直接返回false
    now = node[now][k];
  }
  return exist[now];//这里的exist意义和上面的一样，表示此时的now有没有结果
}

int main() {
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> s;
    insert(s);
  }
  cin >> m;
  for (int i = 1; i <= m; ++i) {
    cin >> s;
    puts(search(s) == true ? "Yes" : "No");
  }
  return 0;
} 
```

代码注意点：

1. Trie数组空间要开到 $\text{字符串个数}\times \text{不同的字符个数}$。

2. 代码中的 ```tot``` 和 ```now``` 的初始值必须相同，例如：我们定义 ```tot``` 初始为```0```，那么 ```now``` 初始也得为0。

## 例题

- [P2580 于是他错误的点名开始了](https://www.luogu.com.cn/problem/P2580)

Trie板子题，插入删除没啥变化，只用把 ```exist``` 数组定为 ```int``` 类型，插入时将 ```exist[now]++```，为了节省空间，我们询问时如果出现 ```OK``` 才插入。

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 5;

int n, m, tot;
string s;

int node[N * 5][26];
int exist[N * 5 * 26];

void insert (string s) {
  int len = s.size();
  int now = 1;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';
    if (node[now][k] == 0) node[now][k] = ++tot;
    now = node[now][k];
  }
  exist[now]++;
  return ;
}

string search (string s) {
  int len = s.size();
  int now = 1;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';
    if (node[now][k] == 0) return "WRONG";
    now = node[now][k];
  }
  if (exist[now] == 0) return "WRONG";
  else if (exist[now] == 1) return "OK";
  else return "REPEAT";
}

int main() {
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> s;
    insert(s);
  }
  cin >> m;
  for (int i = 1; i <= m; ++i) {
    cin >> s;
    string res = search(s);
    cout << res << endl;
    if (res == "OK") insert(s);
  }
  return 0;
} 
```

- [P3879 [TJOI2010]阅读理解](https://www.luogu.com.cn/problem/P3879)

Trie的模板改了一下，```exist```数组从二维增到了三维，增加的那一维度就是文章号，其余的均一样。但这题 ```#11``` 数据点MLE，这也是没办法。

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 5e3 + 5;

int n, m, L, tot;
string s;
int res[N], node[1005][N][26];
bool exist[1005][N * 26];

void insert (int Case, string s) {
  int len = s.size();
  int now = 0;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';
    if (node[Case][now][k] == 0) node[Case][now][k] = ++tot;
    now = node[Case][now][k];
  }
  exist[Case][now] = true;
}

bool search (int Case, string s) {
  int len = s.size();
  int now = 0;
  for (int i = 0; i < len; ++i) {
    int k = s[i] - 'a';
    if (node[Case][now][k] == 0) return false;
    now = node[Case][now][k];
  }
  return exist[Case][now];
}

int main() {
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> L;
    for (int j = 1; j <= L; ++j) {
      cin >> s;
      insert(i, s);
    }
  }
  cin >> m;
  for (int i = 1; i <= m; ++i) {
    cin >> s;
    int cnt = 0;
    for (int j = 1; j <= n; ++j) {
      if (search(j, s) == true) res[++cnt] = j;
    }
    for (int j = 1; j <= cnt; ++j) {
      if (j != 1) printf(" ");
      printf("%d", res[j]);
    }
    cout << endl;
  }
  return 0;
}
```

---

# 01 Trie

## 引入

我们如果要给定两个数组 ```a``` 和 ```b```，均有 $n$ 个数，我们固定 ```a``` 不动，让 ```b``` 自由排列，使排列后的 ```b[i] xor a[i]``` 的值最大，求字典序最小的答案。

### 方法一

暴力枚举 ```b``` 的排列，取最大值即可，时间复杂度 $O(n!\times n)$，随便就卡死了。

### 方法二 - 01 Trie

本质上是一种贪心。我们发现：

> 二进制高位尽量不同，异或出的值就会越大。

有了这个性质，就发现我们处理二进制位就行了。发现，此时只要求二进制高位开始的第 $i$ 位有相同的或者是没相同的即可。于是，便发现可以用Trie来维护。

时间复杂度： $O(n\log \max(a_i,b_i))$，在 ```int``` 范围内，即可理解为 $O(n\log n)$，时间复杂度极其优秀，空间也就 $O(2\times n\log n)$。

## 例题

- [CF923C Perfect Security](https://www.luogu.com.cn/problem/CF923C)

01 Trie板子，直接上代码：

```cpp
#include <bits/stdc++.h>

const int N = 3e5 + 5;

struct Trie {
  int count, son[2];
} Tree[N * 35 * 2] ;

int n, tot = 1;
int a[N], b[N];

void insert (int x) {
  int now = 1;
  Tree[now].count++;
  for (int i = 30; i >= 0; --i) {
    int key = x >> i & 1;//取x从右往左数第i位
    if (Tree[now].son[key] == 0) Tree[now].son[key] = ++tot;
    now = Tree[now].son[key];
    Tree[now].count++;
  }
  return ;
}

int search (int x) {
  int result = 0, now = 1;
  for (int i = 30; i >= 0; --i) {
    int key = x >> i & 1;
    if (Tree[Tree[now].son[key]].count == 0) key ^= 1;
    result = (result << 1) + key;
    now = Tree[now].son[key];
    Tree[now].count--;
  }
  return x ^ result;
}

int main() {
  std::cin >> n;
  for (int i = 1; i <= n; ++i) {
    std::cin >> a[i];
  }
  for (int i = 1; i <= n; ++i) {
    std::cin >> b[i];
    insert(b[i]);
  }
  for (int i = 1; i <= n; ++i) {
    std::cout << search(a[i]) << " ";
  }
  return 0;
}
```

- [P4551 最长异或路径](https://www.luogu.com.cn/problem/P4551)

我们任取两点 $u,v(u\neq v)$，令 $(u,v)$ 的公共祖先为 $k$，$1\to k$ 上经过的边权分别为 $w_1,w_2,...,w_t$，$k\to u$ 的简单路径上的边权分别为 $p_1,p_2,...,p_f$，$k\to v$ 的简单路径上的边权分别为 $q_1,q_2,...,q_g$。

那么
$dis(u)=w_1\oplus w_2\oplus,....,\oplus w_t\oplus p_1\oplus p_2\oplus,...,\oplus p_f$，
$dis(v)=w_1\oplus w_2\oplus,....,\oplus w_t\oplus q_1\oplus q_2\oplus,...,\oplus q_g$，此时 $dis(u)\oplus dis(v)=p_1\oplus p_2\oplus,...,\oplus p_f\oplus q_1\oplus q_2\oplus,...,\oplus q_g$，此时发现就等于我们要求的简单路径的异或值。此时我们只要让 $dis(u)\oplus dis(v)$ 的值最小即可，用01Trie维护就行了。

代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5 + 5; 

struct edge {
  int to, w;
} ;
vector <edge> G[N];

int n, ans, tot = 1;
int u, v, w;
int dis[N], vis[N];

int Tree[N * 31][2];

void addEdge (int u, int v, int w) {
  G[u].push_back((edge){v, w}); 
}

void Prework (int k) {//取出dis(k)的值
  for (vector <edge> :: iterator it = G[k].begin(); it != G[k].end(); ++it) {
    int to = it -> to, v = it -> w;
    if (vis[to] == 1) continue ;
    dis[to] = dis[k] ^ v;
    vis[to] = 1;
    Prework(to);
  }
  return ;
}

void insert (int k) {//01Trie板子
  int now = 1, key;
  for (int i = 31; ~i; --i) {
    key = k >> i & 1;
    if (Tree[now][key] == 0) Tree[now][key] = ++tot;
    now = Tree[now][key];
  }
  return ;
}

int search (int k) {//01Trie板子
  int now = 1, res = 0, key;
  for (int i = 31; ~i; --i) {
    key = k >> i & 1;
    key ^= 1;
    if (Tree[now][key] == 0) key ^= 1;
    res = (res << 1) + key;
    now = Tree[now][key];
  }
  return res;
}

int main() {
  cin >> n;
  for (int i = 1; i <= n - 1; ++i) {
    cin >> u >> v >> w;
    addEdge(u, v, w), addEdge(v, u, w);
  }
  vis[1] = 1;
  Prework(1);
  for (int i = 1; i <= n; ++i) {
    insert(dis[i]);
    if (i != 1) ans = max(ans, dis[i] ^ search(dis[i]));
  }
  cout << ans << endl;
  return 0;
}
```

- [P3369 【模板】普通平衡树](https://www.luogu.com.cn/problem/P3369)

~~惊不惊喜，意不意外，让你用01Trie维护平衡树~~

1. 插入

01Trie板子即可，但要记录  $\text{size}$ 表示插入时这一位被经过的次数。代码：

```cpp
void Insert (int k) {
  int now = 1, key;
  for (int i = MAXBIT; ~i; --i) {
    key = k >> i & 1;
    if (Tree[now][key] == 0) Tree[now][key] = ++tot;
    now = Tree[now][key];
    Size[now]++;
  }
  Exist[now]++;
  return ;
}
```

2 删除

跟插入实现差不多，代码：

```cpp
void Delete (int k) {
  int now = 1, key;
  for (int i = MAXBIT; ~i; --i) {
    key = k >> i & 1;
    now = Tree[now][key];
    Size[now]--;
  }
  Exist[now]--;
  return ;
}
```

3. 查询 $k$ 的排名

对于 $k$ 的第 $i$ 位，如果为 $1$ ，计数器就加 ```Size[lson(now)]```，否则就不加，最后输出计数器+1即可。代码：

```cpp
int Rank (int k) {
  int now = 1, res = 0, key;
  for (int i = MAXBIT; ~i; --i) {
    key = k >> i & 1;
    if (key == 1) res += Size[Tree[now][0]];
    now = Tree[now][key];
  }
  return res + 1;
}
```

4. 查询排名为 $k$ 的数

首先实现 ```Count(k)``` 函数，表示数 $k$ 的出现次数。

实现 ```GetKth(k)``` 时。

- 如果 $k$ 的第 $i$ 位为 $0$

	继续向下转移即可
- 如果 $k$ 的第 $i$ 位为 $1$

先用 $k$ 减去 ```Size[lson(now)]```，计数器```|=```$2^i$，再转移即可。

代码：

```cpp
int GetKth (int k) {
  int now = 1, key, res = 0;
  for (int i = MAXBIT; ~i; --i) {
    key = k >> i & 1;
    if (k <= Size[Tree[now][0]]) now = Tree[now][0];
    else {
      k -= Size[Tree[now][0]];
      res |= (1 << i);
      now = Tree[now][1];
    }
  }
  return res;
}
```

- 查询前驱 & 后继

分别取 ```GetKth(Rank(k)-1)``` 和 ```GetKth(Rank(k)+Count(k))```，代码：

```cpp
int GetPre (int k) {
  int res;
  Insert(k);
  res = GetKth(Rank(k) - 1);
  Delete(k);
  return res;
}
int GetNext (int k) {
  int res;
  Insert(k);
  res = GetKth(Rank(k) + Count(k));
  Delete(k);
  return res;
}
````

完整代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, opt, x;

namespace Trie {
  const int N = 1e5 + 5;
  const int MAXBIT = 23;
  int tot = 1, Tree[N * MAXBIT][2], Exist[N * MAXBIT * 2], Size[N * MAXBIT * 2];
  
  void Insert (int k) {
    int now = 1, key;
    for (int i = MAXBIT; ~i; --i) {
      key = k >> i & 1;
      if (Tree[now][key] == 0) Tree[now][key] = ++tot;
      now = Tree[now][key];
      Size[now]++;
    }
    Exist[now]++;
    return ;
  }
  void Delete (int k) {
    int now = 1, key;
    for (int i = MAXBIT; ~i; --i) {
      key = k >> i & 1;
      now = Tree[now][key];
      Size[now]--;
    }
    Exist[now]--;
    return ;
  }
  int Count (int k) {
    int now = 1, key;
    for (int i = MAXBIT; ~i; --i) {
      key = k >> i & 1;
      now = Tree[now][key];
      if (now == 0) return 0;
    }
    return Exist[now];
  }
  int Rank (int k) {
    int now = 1, res = 0, key;
    for (int i = MAXBIT; ~i; --i) {
      key = k >> i & 1;
      if (key == 1) res += Size[Tree[now][0]];
      now = Tree[now][key];
    }
    return res + 1;
  }
  int GetKth (int k) {
    int now = 1, key, res = 0;
    for (int i = MAXBIT; ~i; --i) {
      key = k >> i & 1;
      if (k <= Size[Tree[now][0]]) now = Tree[now][0];
      else {
        k -= Size[Tree[now][0]];
        res |= (1 << i);
        now = Tree[now][1];
      }
    }
    return res;
  }
  int GetPre (int k) {
    int res;
    Insert(k);
    res = GetKth(Rank(k) - 1);
    Delete(k);
    return res;
  }
  int GetNext (int k) {
    int res;
    Insert(k);
    res = GetKth(Rank(k) + Count(k));
    Delete(k);
    return res;
  }
}

namespace Solution {
  static int BASE = 1e7;
  void Solve (int opt, int x) {
    switch (opt) {
      case 1: Trie::Insert(x + BASE); break;
      case 2: if (Trie::Count(x + BASE) != 0) Trie::Delete(x + BASE); break;
      case 3: printf("%d\n", Trie::Rank(x + BASE)); break;
      case 4: printf("%d\n", Trie::GetKth(x) - BASE); break;
      case 5: printf("%d\n", Trie::GetPre(x + BASE) - BASE); break;
      default: printf("%d\n", Trie::GetNext(x + BASE) - BASE); break;
    }
  }
}

int main() {
  cin >> n;
  for (int i = 1; i <= n; ++i) {
    cin >> opt >> x;
    Solution::Solve(opt, x);
  }
  return 0;
}
```

# The end