#!/usr/bin/env python3

import re
import os
import math
import requests
from time import sleep
from datetime import datetime
from heapq import heappush, heappop
from collections import Counter, defaultdict
from functools import cache, reduce
from operator import mul
import numpy as np

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
    tab = defaultdict(int)
    for stone in data:
        tab[stone] = 1
    for i in range(75):
        step = defaultdict(int)
        for stone, count in tab.items():
            if stone == 0:
                step[1] += count
            elif (digits := int(1+math.log10(stone))) % 2 == 0:
                power = pow(10, digits // 2)
                step[int(stone // power)] += count
                step[int(stone % power)] += count
            else:
                step[stone * 2024] += count
        tab = step
        if (i + 1) == 25:
            silver = sum(tab.values())
        if (i + 1) == 75:
            gold = sum(tab.values())
    return (silver, gold)
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
        for edge in edges:
            y1, x1 = edge[0]
            y2, x2 = edge[1]
            # horizontal segments
            if y1 == y2:
                if ((y1, x1-1), (y2, x2-1)) in edges: # left most
                    continue
                sides += 1
            # vertical segments
            if x1 == x2:
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


def Day13(data):
    silver = 0; gold = 0
    data = data.strip().splitlines()
    games = []
    for i in range(0, len(data), 4):
        a = tuple(map(int,re.findall(r"(\d+)", data[i+0])))
        b = tuple(map(int,re.findall(r"(\d+)", data[i+1])))
        goal = tuple(map(int,re.findall(r"(\d+)", data[i+2])))
        games.append((a, b, goal))
    @cache
    def dfs(x1, y1, x2, y2, gx, gy):
        if gx < 0 or gy < 0:
            return math.inf
        if gx == 0 and gy == 0:
            return 0
        return min(
            3+dfs(x1, y1, x2, y2, gx - x1, gy - y1),
            1+dfs(x1, y1, x2, y2, gx - x2, gy - y2)
        )
    for ((x1, y1), (x2,y2), (gx,gy)) in games:
        dist = dfs(x1, y1, x2, y2, gx, gy)
        silver += dist if dist != math.inf else 0
    return (silver, gold)


def Day13(data):
    silver = 0; gold = 0
    data = data.strip().splitlines()
    games = []
    for i in range(0, len(data), 4):
        if not data[i]: continue
        a = tuple(map(int,re.findall(r"(\d+)", data[i+0])))
        b = tuple(map(int,re.findall(r"(\d+)", data[i+1])))
        goal = tuple(map(int,re.findall(r"(\d+)", data[i+2])))
        games.append((a, b, goal))
    for ((x1, y1), (x2,y2), (gx,gy)) in games:
        # silver
        solution = np.linalg.solve([[x1, x2], [y1, y2]], [gx, gy])
        a_presses, b_presses = np.round(solution).astype(int)
        x = x1 * a_presses + x2 * b_presses
        y = y1 * a_presses + y2 * b_presses
        # verify
        if gx == x and gy == y:
            silver += 3 * a_presses + b_presses
        # gold
        offset = 10000000000000
        solution = np.linalg.solve([[x1, x2], [y1, y2]], [gx+offset, gy+offset])
        a_presses, b_presses = np.round(solution).astype(int)
        x = x1 * a_presses + x2 * b_presses
        y = y1 * a_presses + y2 * b_presses
        # verify
        if (gx+offset) == x and (gy+offset) == y:
            gold += 3 * a_presses + b_presses
    return (silver, gold)
data = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400\n
Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176\n
Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450\n
Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
print("Day 13:", end="")
assert Day13(data) == (480,875318608908), "❌"; print(" ⭐ ⭐")


def Day14(data):
    silver = 0; gold = 0
    cols = 11; rows = 7
    data = data.strip().splitlines()
    bots, vels = [], []
    for idx, line in enumerate(data):
        pos = tuple(map(int, line.split(" ")[0][2:].split(",")))
        vel = tuple(map(int, line.split(" ")[1][2:].split(",")))
        bots.append(pos)
        vels.append(vel)
    def count_quads():
        quads = defaultdict(int)
        for bot in bots:
            x, y = bot
            if x == cols // 2 or y == rows // 2:
                continue
            quads[(x > cols // 2, y > rows // 2)] += 1
        return quads.values()
    for i in range(10000):
        for idx in range(len(bots)):
            x, y = bots[idx]
            dx, dy = vels[idx]
            x = (x + dx) % cols
            y = (y + dy) % rows
            bots[idx] = (x, y)
        if i == 99:
            silver = reduce(mul, count_quads())
        elif i > 99 and len(bots) == len(set(bots)):
            gold = i + 1; break
    return (silver, gold)
data = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
print("Day 14:", end="")
assert Day14(data) == (12, 105), "❌"; print(" ⭐ ⭐")


def Day15(data):
    silver = 0; gold = 0
    dirs = { '<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0) }
    matrix = []
    moves = []
    for line in data.strip().splitlines():
        if line == "\n":
            continue
        elif line.startswith("#"):
            matrix.append(list(line))
        else:
            moves.extend(dirs[x] for x in line)
    cols = len(matrix[0])
    rows = len(matrix)
    walls = set()
    boxes = set()
    robot = tuple()
    for y in range(rows):
        for x in range(cols):
            if matrix[y][x] == "#":
                walls.add((y,x))
            elif matrix[y][x] == "O":
                boxes.add((y,x))
            elif matrix[y][x] == "@":
                robot = (y,x)
    def try_move(y, x, dy, dx):
        if (y+dy, x+dx) in walls:
            return False
        if (y+dy, x+dx) in boxes:
            return try_move(y+dy, x+dx, dy, dx)
        return True
    def push(y, x, dy, dx):
        if (y,x) in walls:
            return
        if (y,x) in boxes:
            push(y+dy, x+dx, dy, dx)
            boxes.remove((y,x))
            boxes.add((y+dy, x+dx))
    for dy, dx in moves:
        y, x = robot
        if try_move(y, x, dy, dx):
            robot = (y+dy, x+dx)
            push(y+dy, x+dx, dy, dx)
    for y, x in boxes:
        silver += (100 * y) + x
    return (silver, gold)
data = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########\n
<^^>>>vv<v>>v<<
"""
print("Day 15:", end="")
assert Day15(data) == (2028, 0), "❌"; print(" ⭐ ⭐")

def Day16(data):
    silver = inf; gold = set()
    matrix = [list(x) for x in data.strip().splitlines()]
    walls = set()
    start, goal = tuple(), tuple()
    curr = tuple()
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == "#":
                walls.add((y,x))
            elif matrix[y][x] == "S":
                start = (y,x)
            elif matrix[y][x] == "E":
                goal = (y,x)
    visited = set()
    scores = {}
    minheap = [(1, (0,1), start, [start, goal])]
    while minheap:
        score, (py,px), (y, x), path = heappop(minheap)
        for dy, dx in ((0,1), (1,0), (0,-1), (-1,0)):
            ny, nx = y + dy, x + dx
            if (ny, nx) == goal and score <= silver:
                silver = score
                gold = gold | set(path)
                continue
            if (ny, nx) in walls:
                continue
            if (ny, nx) in visited and score > 1000 + scores[(ny, nx)]:
                continue
            visited.add((ny, nx))
            scores[(ny, nx)] = min(scores.get((ny, nx), math.inf), score)
            curpath = path + [(ny, nx)]
            cost = 1 if (dy,dx) == (py, px) else 1001
            heappush(minheap, (score + cost, (dy, dx), (ny, nx), curpath))
    return (silver, len(gold))
data = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
print("Day 16:", end="")
assert Day16(data) == (7036, 45), "❌"; print(" ⭐")


def Day17(data):
    DEBUG = False
    data = data.strip().splitlines()
    reg = { "pc": 0 }
    program = []
    for line in data:
        if line.startswith("Register"):
            reg[line.split(":")[0].split()[-1]] = int(line.split(":")[1])
        elif line.startswith("Program"):
            program = list(map(int, line.split(":")[1].split(",")))
    def combo(num):
        reg_digit = { 4: "A", 5: "B", 6: "C" }
        return num if num <= 3 else reg[reg_digit[num]]
    def adv(op): # 0
        cop = combo(op)
        if DEBUG: print("adv", cop)
        reg["A"] = reg["A"] // (1 << cop)
        reg["pc"] += 2
    def bxl(op): # 1
        if DEBUG: print("bxl", op)
        reg["B"] ^= op
        reg["pc"] += 2
    def bst(op): # 2
        cop = combo(op)
        if DEBUG: print("bst", cop, cop & 0b111)
        reg["B"] = cop & 0b111
        reg["pc"] += 2
    def jnz(op): # 3
        if DEBUG: print("jnz", op)
        if reg["A"] == 0:
            reg["pc"] += 2
            return
        reg["pc"] = op
    def bxc(op): # 4
        if DEBUG: print("bxc", op)
        reg["B"] ^= reg["C"]
        reg["pc"] += 2
    def out(op): # 5
        cop = combo(op)
        if DEBUG: print("out", cop, cop & 0b111)
        reg["pc"] += 2
        return str(cop & 0b111)
    def bdv(op): # 6
        cop = combo(op)
        if DEBUG: print("bdv", cop)
        reg["B"] = reg["A"] // (1 << cop)
        reg["pc"] += 2
    def cdv(op): # 7
        cop = combo(op)
        if DEBUG: print("cdv", cop)
        reg["C"] = reg["A"] // (1 << cop)
        reg["pc"] += 2
    INSTR = { 0: adv, 1: bxl, 2: bst, 3: jnz, \
              4: bxc, 5: out, 6: bdv, 7: cdv }
    output = []
    while reg["pc"] < len(program):
        instr = program[reg["pc"]]
        op = program[reg["pc"]+1]
        if out := INSTR[instr](op):
            output.append(out)
        if DEBUG: print(reg)
        if DEBUG: input()
    return (",".join(output))
data = """
Register A: 729
Register B: 0
Register C: 0\n
Program: 0,1,5,4,3,0
"""
print("Day 17:", end="")
assert Day17(data) == ("4,6,3,5,6,3,5,2,1,0"), "❌"; print(" ⭐")


def Day18(data):
    silver = 0; gold = 0
    lines = [line.split(",") for line in data.strip().splitlines()]
    allwalls = [(int(y),int(x)) for x,y in lines]
    start, goal = (0,0), (6,6)
    cols, rows = 7, 7
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    for i in range(len(allwalls)):
        walls = set(allwalls[:i])
        heap = [(manhattan(start, goal), 0, start)]
        visited = set()
        while heap:
            score, steps, (y, x) = heappop(heap)
            if (y, x) == goal:
                if i == 12:
                    silver = steps
                break
            for dy, dx in ((1,0), (0,1), (-1,0), (0,-1)):
                ny, nx = y + dy, x + dx
                if (ny, nx) in visited:
                    continue
                if not (0 <= ny < rows and 0 <= nx < cols):
                    continue
                if (ny, nx) in walls:
                    continue
                visited.add((ny, nx))
                heappush(heap, (manhattan((ny, nx), goal), steps + 1, (ny, nx)))
        if not heap:
            gold = ",".join(map(str,allwalls[i-1]))
            return (silver, gold)
data = """
5,4\n4,2\n4,5\n3,0\n2,1\n6,3\n2,4
1,5\n0,6\n3,3\n2,6\n5,1\n1,2\n5,5
2,5\n6,5\n1,4\n0,4\n6,4\n1,1\n6,1
1,0\n0,5\n1,6\n2,0
"""
print("Day 18:", end="")
assert Day18(data) == (22, '1,6'), "❌"; print(" ⭐ ⭐")


def Day22(data):
    silver = 0; gold = 0
    data = [int(x) for x in data.strip().splitlines()]
    freq = defaultdict(int)
    def mix(secret, value):
        return secret ^ value
    def prune(secret):
        return secret % 16777216
    for secret in data:
        change = [num % 10]
        prices = [0]
        seen = set()
        for _ in range(2000):
            secret = mix(secret, secret << 6)
            secret = prune(secret)
            secret = mix(secret, secret >> 5)
            secret = prune(secret)
            secret = mix(secret, secret << 11)
            secret = prune(secret)
            if len(prices) > 3:
                prices.pop(0)
                change.pop(0)
            prices.append(num % 10)
            change.append(prices[-1] - prices[-2])
            if len(change) == 4 and tuple(change) not in seen:
                freq[tuple(change)] += prices[-1]
                seen.add(tuple(change))
        silver += num
    return silver, max(freq.values())
data = """
1
2
3
2024
"""
print("Day 22:", end="")
assert Day22(data) == (37990510, 23), "❌"; print(" ⭐ ⭐")
