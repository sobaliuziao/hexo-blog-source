---
title: trick 题集合
date: 2025-08-28 15:45:00
---

[P9062](https://www.cnblogs.com/Scarab/p/18823374)：平面最近点对可以考虑按照 $x$ 和 $y$ 分别分块。

[20250616 模拟赛 T2](https://www.cnblogs.com/Scarab/p/18931559)：做的操作跟数与数之间的大小有关，且最后要最优化答案的题可以考虑枚举每个 $v$，将 $x$ 变为 $[x\geq v]$ 再做。

[CF2122G](https://www.cnblogs.com/Scarab/p/18998928)：欧拉数 $A(n,k)$ 算 $n$ 阶排列有 $k$ 个下降位置的排列数量是有公式的。

[CF2097F](https://www.cnblogs.com/Scarab/p/19009292)：一个图的最大流不好做的话可以考虑转最小割。

[CF2089E](https://www.cnblogs.com/Scarab/p/19015550)：dfs 树上背包不好合并，考虑按照 dfs 序倒着做。

[CF2077E](https://www.cnblogs.com/Scarab/p/19017131)：对于跟下标奇偶性有关的题考虑设 $b_i=(-1)^ia_i$ 后再考虑。

[CF1456E](https://www.cnblogs.com/Scarab/p/19033128)：要求最大化序列相邻数的权值之和可以考虑区间 dp。对于最大化两两异或结果之和考虑往从高位到低位考虑，没卡边界的可以删掉。

[CF2062G](https://www.cnblogs.com/Scarab/p/19034044)：对于排列的交换问题可以把 $(i,p_i)$ 看成一个点，每次操作看成同时移动一对点。

[QOJ7324](https://www.cnblogs.com/Scarab/p/19036738)：删掉两条 dfs 树非割边使得连通状态改变的条件是覆盖它们的非树边集合相同。

[QOJ1814](https://www.cnblogs.com/Scarab/p/19044080)：如果操作条件很复杂，考虑用不变的东西去刻画它。

[P7603](https://www.cnblogs.com/Scarab/p/19044700)：折半警报器考虑设置阈值到每个控制的位置，达到阈值就重构。

[P9041](https://www.cnblogs.com/Scarab/p/19045318)：要求多路径点不交就考虑 LGV 引理。

[QOJ2214](https://www.cnblogs.com/Scarab/p/19047476)：动态维护强连通分量考虑整体二分每个边第一次出现在强连通分量内部的时间。

[QOJ2373](https://www.cnblogs.com/Scarab/p/19047997)：对于交互题询问一些数的差考虑找到最小/最大值，然后以这个位置为基准点询问。

[CF1764G3](https://www.cnblogs.com/Scarab/p/19048808)：对于一些交互题考虑特殊/边界情况！！！

[CF1764H](https://www.cnblogs.com/Scarab/p/19053585)：区间赋值成某个元素考虑倒着做，计算每个位置的存活时间。

[ABC311H](https://www.cnblogs.com/Scarab/p/19057649)：树形背包做 $\min$ 加卷积可以考虑从上往下转移，将合并转成插入，往状态里面传数组。然后先继承重儿子的结果，往轻儿子转移时状态加入当前结果。

P6856：滑动窗口问题可以按照窗口长度 $k$ 分块，将问题转化成前后缀之间的合并。

ARC120F：对于计数题枚举中间位置算贡献的题，如果要求总个数固定，且左右之间没有影响，可以考虑将链连成环再做。

[P9036](https://www.cnblogs.com/Scarab/p/19058645)：对于一些图上 NPC 问题可以考虑删点。

[GYM103428C](https://www.cnblogs.com/Scarab/p/19059596)：对于存在性 01 背包的题，可以考虑用均摊暴力找到所有有贡献的位置，找 $a_i=1,a_{i+x}=0$ 的位置可以用哈希处理。

[CF1025G](https://www.cnblogs.com/Scarab/p/19059668)：对于操作比较复杂且没有明显的操作方向的询问期望操作时间的题，可以尝试用鞅与停时定理做。

[QOJ4424](https://www.cnblogs.com/Scarab/p/19062781)：对于置换环上分裂的问题，如果需要暴力找到一个位置进行操作，然后分裂置换环，可以考虑从两边同时找，即一边跳 $pre$，一边跳 $nxt$，用分裂后小环环长次数来找到这个位置，也就是启发式分裂的思想。

[yukicoder3054](https://yukicoder.me/problems/no/3054)：求一堆判定问题的总和可以考虑将 $[x]$ 拆成类似 $a+b-c$ 的形式，这样可以方便求总和。

[CF480E](https://www.cnblogs.com/Scarab/p/19076070)：对于求一个矩阵内最大的连续正方形不包含关键点的题有个想法是设 $len_{i,j}$ 表示以 $(i,j)$ 为右端点的线段的最长长度，使得这个线段里没有任何点不能选。那么判断一个是否存在一个以 $(x,y)$ 为右上角的正方形边长为 $k$ 的条件即为 $\forall i\in[x,x+k-1],len_{i,y}\geq k$。

[CF1326F1](https://codeforces.com/problemset/problem/1326/F1)：对于一个规模较小，但是直接指数过不了且支持合并的题，可以考虑用 meet in the middle 优化。

[CF1326F2](https://www.cnblogs.com/Scarab/p/19076110)：对于规模较小，状态数很多，但是状态可以表示为若干个数的和，且这些数能够随意交换顺序的题可以用拆分数优化状态。

[P13693](https://www.cnblogs.com/Scarab/p/19094956)：对于 $\text{mex}$ 区间问题，极短 $\text{mex}$ 区间的数量是 $O(n)$ 的。

[QOJ5092](https://www.cnblogs.com/Scarab/p/19112036)：对于两个人轮流选，且都想要最大化自己的权值的问题可以把权值看成第一个人减去第二个人。对于一类策略不明显，可以找一些形如“选了 $x$ 后必须接着选 $y$”的策略，把这些连着的点合并起来，直到转化成策略很明显的状态。

[QOJ5421](https://www.cnblogs.com/Scarab/p/19116929)：对于 $(\max,+)$ 卷积的 dp 题，首先要考虑它是不是凸的，要是是凸的就能直接归并差分数组了。