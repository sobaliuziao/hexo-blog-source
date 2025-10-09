---
title: min-max 容斥
date: 2024-04-23 20:00:00
---

min-max 容斥也称之为最值反演。

$$Max(S)=\sum_{T\subseteq S,T\neq \varnothing}{(-1)^{|T|-1}\cdot Min(T)}$$

定义 $kMax(S)$ 等于 $S$ 的第 $k$ 大值，那么：

$$kMax(S)=\sum_{T\subseteq S,|T|\geq k}{(-1)^{|T|-k}Min(T)\cdot C_{|T|-1}^{k-1}}$$

$$E\left(Max(S)\right)=\sum_{T\subseteq S}{(-1)^{|T|-1}{E\left(Min(T)\right)}}$$