#!/usr/bin/env python3

import re
import os
import requests
from time import sleep
from datetime import datetime
from heapq import heappush, heappop
from collections import Counter
from collections import Counter, defaultdict
from functools import cache

print()
print("##########################")
print("### ⭐🎄 AOC 2024 🎄⭐ ###")
print("##########################")
print()

SESSION = ""

def get_input(session, year, day):
    if f"{year}_{day}.txt" in os.listdir():
        with open(f"{year}_{day}.txt", "r") as f:
            return f.read()
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {
        "cookie": f"session={session}"
    }
    response = requests.get(url, headers=headers)
    print(response)
    with open(f"{year}_{day}.txt", "w") as f:
        f.write(response.text)
    return response.text

data = get_input(SESSION, 2024, 2)

def Day1(data):
    silver = gold = 0
    ha, hb = [], []
    bfreq = Counter()
    for s in data.strip().splitlines():
        a, b = map(int, s.split())
        heappush(ha, a)
        heappush(hb, b)
        bfreq[b] += 1
    while ha:
        a, b = heappop(ha), heappop(hb)
        silver += abs(a - b)
        gold += a * bfreq[a]
    return (silver, gold)
data = """
3   4
4   3
2   5
1   3
3   9
3   3
"""
print("Day 1:", end="")
assert Day1(data) == (11, 31), "❌"; print(" ⭐ ⭐")

def Day2(data):
    silver = gold = 0
    def is_safe(nums):
        for i in range(1, len(nums)):
            if not 1 <= nums[i] - nums[i-1] <= 3:
                return False
        return True
    def remove(nums):
        for i in range(len(nums)):
            if is_safe(nums[:i] + nums[i+1:]):
                return True
        return False
    for line in data.strip().splitlines():
        nums = list(map(int, line.split()))
        if is_safe(nums) or is_safe(list(reversed(nums))):
            silver += 1
            gold += 1
        elif remove(nums) or remove(list(reversed(nums))):
            gold += 1
    return (silver, gold)
data = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
print("Day 2:", end="")
assert Day2(data) == (2,4), "❌"; print(" ⭐ ⭐")

def Day3(data):
    silver = gold = 0
    s = data.strip().replace("\n", "")
    process = True
    for i in range(len(s)):
        if s[i-7:i] == "don't()":
            process = False
        elif s[i-4:i] == "do()":
            process = True
        elif s[i-4:i] == "mul(":
            j = i
            arguments = ""
            x, y = 0, 0
            while s[j].isdigit():
                x = x * 10 + int(s[j])
                j += 1
            if s[j] != ",":
                continue
            j += 1
            while s[j].isdigit():
                y = y * 10 + int(s[j])
                j += 1
            if s[j] == ")":
                silver += x * y
                if process:
                    gold += x * y
            arguments = ""
    return (silver, gold)
data = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
print("Day 3:", end="")
assert Day3(data) == (161,48), "❌"; print(" ⭐ ⭐")

def Day4(data):
    silver = gold = 0
    grid = [list(x) for x in data.strip().splitlines()]
    cols = len(grid[0])
    rows = len(grid)
    crosses = set()
    @cache
    def find(y, x, i, dy, dx):
        word = ["X", "M", "A", "S"]
        ny, nx = y + dy, x + dx
        if not (0 <= ny < rows and 0 <= nx < cols):
            return 0
        if grid[ny][nx] != word[i]:
            return 0
        if word[i] == "S":
            return 1
        return find(ny, nx, i + 1, dy, dx)
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == "X":
                silver += find(y, x, 1, -1, -1) # NW
                silver += find(y, x, 1, -1,  0) # N
                silver += find(y, x, 1, -1,  1) # NE
                silver += find(y, x, 1,  0, -1) # W
                silver += find(y, x, 1,  1, -1) # SW
                silver += find(y, x, 1,  1,  0) # S
                silver += find(y, x, 1,  1,  1) # SE
                silver += find(y, x, 1,  0,  1) # E
            elif grid[y][x] == "M":
                if find(y, x, 2, -1, -1): # NW
                    if (y-1, x-1) in crosses:
                        gold += 1
                    crosses.add((y-1, x-1))
                if find(y, x, 2, -1,  1): # NE
                    if (y-1, x+1) in crosses:
                        gold += 1
                    crosses.add((y-1, x+1))
                if find(y, x, 2,  1, -1): # SW
                    if (y+1, x-1) in crosses:
                        gold += 1
                    crosses.add((y+1, x-1))
                if find(y, x, 2,  1,  1): # SE
                    if (y+1, x+1) in crosses:
                        gold += 1
                    crosses.add((y+1, x+1))
    return (silver, gold)
data = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
print("Day 4:", end="")
assert Day4(data) == (18,9), "❌"; print(" ⭐ ⭐")


def Day5(data):
    silver = gold = 0
    rules = [list(map(int, x.split("|"))) for x in data.strip().splitlines() if x.count("|") == 1]
    lines = [list(map(int, x.split(","))) for x in data.strip().splitlines() if x.count(",") != 0]
    adj = defaultdict(set)
    for a, b in rules:
        adj[b].add(a)
    def toposort(pages):
        page_set = set(pages)
        result = []
        visited = set()
        visiting = set()
        def visit(n):
            if n in visiting:
                return  # cycle
            if n in visited:
                return
            visiting.add(n)
            for m in adj[n]:
                if m in page_set:
                    visit(m)
            visited.add(n)
            visiting.remove(n)
            result.append(n)
        for page in pages:
            if page not in visited:
                visit(page)
        return result
    for pages in lines:
        ordered = toposort(pages)
        if ordered == pages:
            silver += ordered[len(ordered) // 2]
        else:
            gold += ordered[len(ordered) // 2]
    return (silver, gold)
data = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
print("Day 5:", end="")
assert Day5(data) == (143, 123), "❌"; print(" ⭐ ⭐")


def Day6(data):
    silver = gold = 0
    data = data.strip()
    pos = data.replace("\n", "").index("^")
    cols = data.index("\n")
    rows = data.count("\n") + 1
    sy, sx = 0, 0
    rocks = set()
    for i in range(len(data.strip())):
        if data[i] == "#":
            rocks.add((i // (cols + 1), i % (rows + 1)))
        elif data[i] == "^":
            sy, sx = i // (cols + 1), i % (rows + 1)
    dirs = [(-1,0), (0,1), (1,0), (0,-1)]
    def inbounds(y,x):
        return (0 <= y < rows) and (0 <= x < cols)
    def isrock(y,x):
        return (y,x) in rocks
    def walk(y,x,curr):
        positions = set()
        dirpositions = set()
        while True:
            # check seen
            if (curr, y, x) in dirpositions:
                return False
            # update position
            positions.add((y,x))
            dirpositions.add((curr,y,x))
            # new position
            ny, nx = y + dirs[curr][0], x + dirs[curr][1]
            if not inbounds(ny,nx):
                return positions
            # wall turn right
            if isrock(ny,nx):
                dirpositions.add((curr,y,x))
                curr = (curr + 1) % 4
                ny, nx = y + dirs[curr][0], x + dirs[curr][1]
            # corner check
            if isrock(ny,nx):
                dirpositions.add((curr,y,x))
                curr = (curr + 1) % 4
                ny, nx = y + dirs[curr][0], x + dirs[curr][1]
            # update position
            y, x = ny, nx
    positions = walk(sy,sx,0)
    silver = len(positions)
    for ry, rx in positions:
        if (ry,rx) in rocks:
            continue
        rocks.add((ry,rx))
        if not walk(sy,sx,0):
            gold += 1
        rocks.remove((ry,rx))
    return (silver, gold)
data = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
print("Day 6:", end="")
assert Day6(data) == (41, 6), "❌"; print(" ⭐ ⭐")


def Day7(data):
    silver = gold = 0
    for line in data.strip().splitlines():
        target = int(line.split(":")[0])
        numbers = list(map(int, line.split(":")[1].split()))
        def dfs(i, total, isgold):
            if i == len(numbers) and total == target:
                return True
            if i >= len(numbers) or total > target:
                return False
            return dfs(i+1, total + numbers[i], isgold) \
                or dfs(i+1, total * numbers[i], isgold) \
                or (isgold and dfs(i+1, int(str(total) + str(numbers[i])), isgold))
        if dfs(0, 0, False):
            silver += target
            gold += target
        elif dfs(0, 0, True):
            gold += target
    return (silver, gold)
data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
print("Day 7:", end="")
assert Day7(data) == (3749,11387), "❌"; print(" ⭐ ⭐")


def Day8(data):
    silver, gold = set(), set()
    data = [list(x) for x in data.strip().splitlines()]
    cols = len(data[0])
    rows = len(data)
    antenna = defaultdict(set)
    antennas = set()
    for y in range(rows):
        for x in range(cols):
            if data[y][x] == ".":
                continue
            antenna[data[y][x]].add((y,x))
            antennas.add((y,x))
    def propagate_signal(y, x, dy, dx, powered):
        y, x = y + dy, x + dx
        first = True
        while 0 <= y < rows and 0 <= x < cols:
            if first:
                silver.add((y, x))
                first = False
            if (y, x) not in antennas:
                gold.add((y, x))
            if not powered:
                break
            y, x = y + dy, x + dx
    completed = set()
    for key, nodes in antenna.items():
        powered = False
        if len(nodes) > 1:
            powered = True
        for y1,x1 in nodes:
            for y2,x2 in nodes:
                if y1 == y2 and x1 == x2:
                    continue
                if (y1, x1, y2, x2) in completed:
                    continue
                completed.add((y1, x1, y2, x2))
                completed.add((y2, x2, y1, x1))
                propagate_signal(y1, x1, y1-y2, x1-x2, powered)
                propagate_signal(y2, x2, y2-y1, x2-x1, powered)
    return (len(silver), len(gold) + len(antennas))
data = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""
print("Day 8:", end="")
assert Day8(data) == (14,34), "❌"; print(" ⭐ ⭐")

def Day9(data):
    counts = list(map(int, list(data.strip())))
    blocks = []
    block_id = 0
    block_idx = 0
    memory = []
    for i in range(len(counts)):
        if i % 2 == 0:
            memory.extend([block_id] * counts[i])
            blocks.append([block_id, counts[i], block_idx])
            block_id += 1
            block_idx += counts[i]
        else:
            memory.extend(["."] * counts[i])
            block_idx += counts[i]
    silver = memory.copy()
    gold = memory.copy()
    for block_id, size, block_idx in blocks[::-1]:
        # gold memory
        space_index = -1
        empty_space = 0
        for i in range(block_idx):
            if gold[i] == ".":
                empty_space += 1
                if empty_space == size:
                    space_index = i - size + 1
                    break
            else:
                empty_space = 0
                space_index = -1
        if space_index != -1:
            for i in range(size):
                gold[space_index + i] = block_id
                gold[block_idx + i] = "."
        # silver memory
        silver_filled = 0
        for i in range(block_idx):
            if silver[i] == "." or silver[i] == block_id:
                silver[i] = block_id
                silver_filled += 1
            if silver_filled == size:
                break
        for i in range(silver_filled):
            silver[block_idx + size - i - 1] = "."
    silver_checksum = gold_checksum = 0
    for i in range(len(memory)):
        if silver[i] != ".":
            silver_checksum += i * silver[i]
        if gold[i] != ".":
            gold_checksum += i * gold[i]
    return (silver_checksum, gold_checksum)
print("Day 9:", end="")
data = """
2333133121414131402
"""
assert Day9(data) == (1928, 2858), "❌"; print(" ⭐ ⭐")


def Day10(data):
    silver = set(); gold = 0
    grid = [list(map(int,x)) for x in data.strip().splitlines()]
    cols, rows = len(grid[0]), len(grid)
    starts = set()
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 0:
                starts.add((y,x))
    def dfs(y, x, sy, sx):
        curr = grid[y][x]
        if curr == 9:
            silver.add((sy,sx,y,x))
            return 1
        total = 0
        for dy, dx in [(0,1),(1,0),(0,-1),(-1,0)]:
            if 0 <= y+dy < rows and 0 <= x+dx < cols \
            and curr + 1 == grid[y+dy][x+dx]:
                total += dfs(y+dy, x+dx, sy, sx)
        return total
    for y, x in starts:
        gold += dfs(y, x, y, x)
    return (len(silver), gold)
data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
print("Day 10:", end="")
assert Day10(data) == (36, 81), "❌"; print(" ⭐ ⭐")


def Day11(data):
    silver = 0; gold = 0
    data = list(map(int, data.strip().split(" ")))
    @cache
    def turn(n, step):
        if step == 0:
            return 1
        if n == 0:
            return turn(1, step-1)
        elif len(str(n)) % 2 == 0:
            nstr = str(n)
            return turn(int(nstr[:len(nstr)//2]), step-1) + \
                   turn(int(nstr[len(nstr)//2:]), step-1)
        else:
            return turn(n * 2024, step-1)
    for n in data:
        gold += turn(n, 75)
        silver += turn(n, 25)
    return silver, gold
data = """
125 17
"""
print("Day 11:", end="")
assert Day11(data) == (55312, 65601038650482), "❌"; print(" ⭐ ⭐")


def Day12(data):
    silver = 0; gold = 0
    matrix = [list(x) for x in data.strip().splitlines()]
    rows, cols = len(matrix), len(matrix[0])
    areas = defaultdict(set)
    edges = defaultdict(Counter)
    seen = set()
    # record area and edges
    def flood_fill(y, x, sy, sx, idx):
        if not (0 <= y < rows and 0 <= x < cols):
            return
        if (y, x) in seen:
            return
        if matrix[y][x] != matrix[sy][sx]:
            return
        seen.add((y, x))
        areas[idx].add((y, x))
        flood_fill(y+1, x, sy, sx, idx)
        flood_fill(y-1, x, sy, sx, idx)
        flood_fill(y, x+1, sy, sx, idx)
        flood_fill(y, x-1, sy, sx, idx)
    idx = 0
    for y in range(rows):
        for x in range(cols):
            if (y, x) in seen:
                continue
            flood_fill(y, x, y, x, idx)
            idx += 1
    for idx, position in areas.items():
        for y, x in position:
            # forward edge
            edges[idx][((y,x), (y,x+1))] += 1
            edges[idx][((y,x), (y+1,x))] += 1
            edges[idx][((y+1,x), (y+1,x+1))] += 1
            edges[idx][((y,x+1), (y+1,x+1))] += 1
            # backwards edge
            edges[idx][((y,x+1), (y,x))] += 1
            edges[idx][((y+1,x), (y,x))] += 1
            edges[idx][((y+1,x+1), (y+1,x))] += 1
            edges[idx][((y+1,x+1), (y,x+1))] += 1
    # filter non-unique edges
    for idx in edges.keys():
        edge_set = set([edge for edge, count in edges[idx].items() if count == 1])
        edges[idx] = edge_set
    # count sides by segments
    def count_sides(edges, idx):
        sides = 0
        # horizontal segments
        for edge in edges:
            y1, x1 = edge[0]
            y2, x2 = edge[1]
            if y1 == y2: # horizontal only
                if ((y1, x1-1), (y2, x2-1)) in edges: # left most
                    continue
                sides += 1
        # vertical segments
        for edge in edges:
            y1, x1 = edge[0]
            y2, x2 = edge[1]
            if x1 == x2: # vertical only
                if ((y1-1, x1), (y2-1, x2)) in edges: # top most
                    continue
                sides += 1
        return sides // 2
    # calculate perimeter
    for idx, adj in edges.items():
        curr = None
        perimeter = 0
        sides = count_sides(adj, idx)
        while adj:
            if not curr:
                curr = next(iter(adj))
            y, x = curr[1] # end of current edge
            for dy, dx in [(0,1), (1,0), (0,-1), (-1,0)]:
                next_edge = ((y,x), (y+dy, x+dx))
                altr_edge = ((y+dy,x+dx), (y, x))
                if next_edge in adj:
                    curr = next_edge
                    adj.remove(next_edge)
                    adj.remove(altr_edge)
                    perimeter += 1
            curr = None
        silver += perimeter * len(areas[idx])
        gold += sides * len(areas[idx])
    return (silver, gold)
data = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
print("Day 12:", end="")
assert Day12(data) == (1930,1206), "❌"; print(" ⭐ ⭐")
