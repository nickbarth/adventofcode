#!/usr/bin/env python3

import re
import os
import requests
from time import sleep
from datetime import datetime
from heapq import heappush, heappop
from collections import Counter

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
assert (11, 31) == Day1(data), "❌"; print(" ⭐ ⭐")

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
    socks = set()
    for ry, rx in positions:
        if (ry,rx) in rocks:
            continue
        rocks.add((ry,rx))
        if not walk(sy,sx,0):
            gold += 1
            socks.add((ry,rx))
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
assert Day6(data) == (41, 6), "❌"; print(" ⭐ ⭐")

