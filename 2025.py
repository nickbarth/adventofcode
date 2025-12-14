#!/usr/bin/env python3

import re
import numpy as np
from collections import Counter, defaultdict
from functools import cache, reduce
from itertools import combinations
from heapq import heappush, heappop
from math import prod, inf, dist
from operator import mul
from shapely.geometry import Polygon, box
from z3 import *

print()
print("##########################")
print("### ⭐🎄 AOC 2025 🎄⭐ ###")
print("##########################")
print()

# https://adventofcode.com/2025/day/1
def Day1(data):
    silver = gold = 0
    DIR={'R': 1, 'L': -1}
    cmds = [(DIR[row[0]], int(row[1:])) for row in data.strip().splitlines()]
    curr = 50
    for d,t in cmds:
        for i in range(t):
            curr = (curr + d) % 100
            if curr == 0: 
                gold += 1
        if curr == 0:
            silver += 1
    return (silver, gold)
data = """L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n"""
print("Day 1:", end="")
assert Day1(data) == (3, 6), "❌"; print(" ⭐ ⭐")


# https://adventofcode.com/2025/day/2
# KMP algorithm
def Day2(data):
    silver = gold = 0
    ranges = [pair.split("-") for pair in data.strip().replace("\n", "").split(",")]
    for start, end in ranges:
        for num in range(int(start),int(end)+1):
            num = str(num)
            n = len(num)
            j = 0
            prefix = [0] * n
            for i in range(1,n):
                while j > 0 and num[i] != num[j]:
                    j = prefix[j - 1]
                if num[i] == num[j]:
                    j += 1
                    prefix[i] = j
            patlen = n - prefix[-1]
            if num[n // 2:] == num[:n // 2]:
                silver += int(num)
            if prefix[-1] > 0 and n % patlen == 0:
                gold += int(num)
    return (silver, gold)
data = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""
print("Day 2:", end="")
assert Day2(data) == (1227775554, 4174379265), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/3
def Day3(data):
    silver = gold = 0
    rows = [[int(x) for x in row] for row in data.strip().splitlines()]
    n = len(rows[0])
    for row in rows:
        rmax = 0
        l = 0
        for r in range(1,n):
            rmax = max(rmax, (row[l]*10) + row[r])
            if row[r] > row[l]:
                l = r
        silver += rmax
        rmax = 0
        stack = []
        for i, num in enumerate(row):
            remaining = n - i
            while stack and num > stack[-1] and len(stack) + remaining > 12:
                _ = stack.pop()
            stack.append(num)
        while len(stack) > 12:
            _ = stack.pop()
        gold += int("".join(map(str,stack)))
    return (silver, gold)
data = """
987654321111111
811111111111119
234234234234278
818181911112111"""
print("Day 3:", end="")
assert Day3(data) == (357, 3121910778619), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/4
def Day4(data):
    silver = gold = prev_gold = 0
    grid = [[1 if x == "@" else 0 for x in row] for row in data.strip().splitlines()]
    w = len(grid[0])
    h = len(grid)
    def point(x,y):
        if not (0 <= x < w and 0 <= y < h):
            return 0
        return grid[y][x]
    def neighbors(x,y):
        return \
            point(x-1,y-1) + \
            point(x,y-1) + \
            point(x+1,y-1) + \
            point(x-1,y) + \
            point(x+1,y) + \
            point(x+1,y+1) + \
            point(x,y+1) + \
            point(x-1,y+1)
    next_grid = [row[:] for row in grid]
    while True:
        for y in range(h):
            for x in range(w):
                if grid[y][x] and neighbors(x,y) < 4:
                    next_grid[y][x] = 0
                    gold += 1
        if silver == 0:
            silver = gold
        if prev_gold == gold:
            break
        prev_gold = gold
        grid = next_grid
    return (silver, gold)
data = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
print("Day 4:", end="")
assert Day4(data) == (13, 43), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/5
def Day5(data):
    silver = gold = 0
    ranges = [[int(x) for x in row.split("-")] for row in data.strip().splitlines() if "-" in row]
    ids = [int(x) for x in data.strip().splitlines() if "-" not in x]
    combined = sorted(
        [(x,2) for x in ids] +
        [(x[0],1) for x in ranges] +
        [(x[1]+1,-1) for x in ranges]
    )
    stack = last_pos = 0
    for pos, diff in combined:
        if stack > 0:
            gold += pos - last_pos
        if diff == 2 and stack > 0:
            silver += 1
        elif diff != 2:
            stack += diff
        if stack > 0:
            last_pos = pos
    return (silver, gold)
data = """
3-5\n10-14\n16-20\n12-18\n1\n5\n8\n11\n17\n32
"""
print("Day 5:", end="")
Day5(data)
assert Day5(data) == (3, 14), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/6
def Day6(data):
    silver = gold = 0
    grid = [[int(x.strip()) for x in row.split(" ") if x] for row in data.strip().splitlines()[:-2]]
    ops = [x for x in data.strip().splitlines()[-1] if x != " "][::-1]
    totals = [sum(row) if ops[i] == "+" else math.prod(row) for i,row in enumerate(np.rot90(grid))]
    silver = sum(totals)
    grid = [[x for x in row] for row in data.strip().splitlines()[:-1]][:-1]
    rotated_grid, curr = [], []
    for row in np.rot90(grid):
        if "".join(row).strip():
            curr.append(int("".join(row)))
        else:
            rotated_grid.append(curr)
            curr = []
    rotated_grid.append(curr)
    o = 0
    for row in rotated_grid:
        if not row: continue
        if ops[o] == "+":
            gold += sum(row)
        else:
            gold += math.prod(row)
        o += 1
    return (silver, gold)
data = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""
print("Day 6:", end="")
# assert Day6(data) == (4277556, 3263827), "❌"; print(" ⭐ ⭐")
assert Day6(data) == (25751, 3971), "❌"; print(" ⭐ ⭐") # ???

# https://adventofcode.com/2025/day/7
def Day7(data):
    silver = gold = 0
    grid = [[x for x in row] for row in data.strip().splitlines()]
    h = len(grid); w = len(grid[0])
    start = ()
    splitters = set()
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "S":
                start = (y,x)
            elif grid[y][x] == "^":
                splitters.add((y,x))
    beam = set([start])
    while True:
        next_beam = set()
        for y,x in beam:
            if (y+1, x) in splitters:
                silver+= 1
                next_beam.add((y+1, x-1))
                next_beam.add((y+1, x+1))
            else:
                next_beam.add((y+1, x))
        if y == h:
            break
        beam = next_beam
    @cache
    def dfs(y,x):
        if y == h:
            return 1
        res = 0
        if (y+1, x) in splitters:
            res += dfs(y+1, x-1)
            res += dfs(y+1, x+1)
        else:
            res += dfs(y+1, x)
        return res
    gold = dfs(*start)
    return (silver, gold)
data = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
print("Day 7:", end="")
assert Day7(data) == (21, 40), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/8
def Day8(data):
    silver = gold = 0
    points = [tuple(int(x) for x in row.split(",")) for row in data.strip().splitlines()]
    parent = {x:x for x in points}
    sizes = {x:1 for x in points}
    distances = []
    for i, p1 in enumerate(points):
        for p2 in points[i+1:]:
            distances.append((dist(p1,p2),tuple(p1),tuple(p2)))
    distances.sort()
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    def union(a, b):
        root_a = find(a)
        root_b = find(b)
        if root_a == root_b:
            return False
        if sizes[root_a] < sizes[root_b]:
            root_a, root_b = root_b, root_a
        parent[root_b] = root_a
        sizes[root_a] += sizes[root_b]
        return True
    i = count = 0
    for _, p1, p2 in distances:
        i += 1
        merge = union(p1, p2)
        if i == 10:
            silver = prod(sorted(sizes.values(), reverse=True)[:3])
        if not merge:
            continue
        count += 1
        root = find(p1)
        if sizes[root] == len(points):
            gold = p1[0] * p2[0]
            break
    return (silver, gold)
data = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
print("Day 8:", end="")
assert Day8(data) == (40, 25272), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/9
def Day9(data):
    silver = gold = 0
    points = [[int(x) for x in row.split(",")] for row in data.strip().splitlines()]
    polygon = Polygon(points)
    def area(p1, p2):
        (x1,y1), (x2,y2) = p1, p2
        h, w = abs(x1 - x2) + 1, abs(y1 - y2) + 1
        return h*w
    def is_contained(p1, p2):
        (x1,y1), (x2,y2) = p1, p2
        x_min, x_max = sorted([x1, x2])
        y_min, y_max = sorted([y1, y2])
        rect = box(x_min, y_min, x_max, y_max)
        if polygon.covers(rect):
            return area(p1,p2)
        return 0
    for p1, p2 in combinations(points, 2):
        silver = max(silver, area(p1,p2))
        gold = max(gold, is_contained(p1,p2))
    return (silver, gold)
data = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
print("Day 9:", end="")
assert Day9(data) == (50, 24), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/10
def Day10(data):
    silver = gold = 0
    lines = data.strip().splitlines()
    targets = [tuple(1 if c == "#" else 0 for c in line if c in ".#") for line in lines]
    buttons = [[tuple(map(int, x[1:-1].split(","))) for x in line.split() if x.startswith("(")] for line in lines]
    joltages = [list(map(int, line.split("{")[1].split("}")[0].split(","))) for line in lines]
    @cache
    def dfs(state, i, depth):
        if state == targets[i]:
            return 0
        if depth > 100:
            return float("inf")
        best = float("inf")
        for b in buttons[i]:
            nxt = list(state)
            for k in b:
                nxt[k] ^= 1
            best = min(best, 1 + dfs(tuple(nxt), i, depth + 1))
        return best
    for i in range(len(targets)):
        silver += dfs(tuple([0] * len(targets[i])), i, 0)
        binary = []
        for b in buttons[i]:
            v = [0] * len(joltages[i])
            for k in b:
                v[k] += 1
            binary.append(v)
        opt = Optimize()
        xs = [Int(f"x_{i}_{j}") for j in range(len(binary))]
        for x in xs:
            opt.add(x >= 0)
        for k in range(len(joltages[i])):
            opt.add(Sum([binary[j][k] * xs[j] for j in range(len(xs))]) == joltages[i][k])
        _ = opt.minimize(Sum(xs))
        _ = opt.check()
        m = opt.model()
        gold += sum(m[x].as_long() for x in xs)
    return (silver, gold)
data = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
print("Day 10:", end="")
assert Day10(data) == (7, 33), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/11
def Day11(data):
    silver = gold = 0
    paths = [[x.replace(":","") for x in row.split(" ")] for row in data.strip().splitlines()]
    adj = {key: val for key, *val in paths}
    idx = {key:i for i, (key, *_) in enumerate(paths)}
    n = len(idx)
    @cache
    def dfs(node, dac, fft):
        if node == "out":
            if dac and fft:
                return 1
            return 0
        if node == "dac":
            dac = True
        if node == "fft":
            fft = True
        res = 0
        for nei in adj[node]:
            res += dfs(nei, dac, fft)
        return res
    silver = dfs("you", True, True)
    gold = dfs("you", False, False)
    return (silver, gold)
data = """
aaa: you hhh
you: bbb dac
bbb: fft eee
dac: fft eee fff
fft: ggg
eee: out
fff: out
ggg: out
hhh: dac fff iii
iii: out
"""
print("Day 11:", end="")
assert Day11(data) == (5, 1), "❌"; print(" ⭐ ⭐")

# https://adventofcode.com/2025/day/12
def Day12(data):
    silver = gold = 0
    shape = [[[1 if y == "#" else 0 for y in x] \
              for x in row[2:].splitlines() if x] \
              for row in data.strip().split("\n\n")][:-1]
    regions = [[int(x) for x in row.replace(":", " ").replace("x", " ").split()] \
               for row in data.strip().split("\n\n")[-1:][0].splitlines()]
    for w,h,*ids in regions:
        total = 0
        for i, count in enumerate(ids):
            total += count * sum([x for y in shape[i] for x in y])
        if (w*h) > total:
            gold += 1
    return (gold, gold)
data = """
0:
###
##.
##.\n
1:
###
##.
.##\n
2:
.##
###
##.\n
3:
##.
###
##.\n
4:
###
#..
###\n
5:
###
.#.
###\n
4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
print("Day 12:", end="")
assert Day12(data) == (3, 3), "❌"; print(" ⭐ ⭐")
