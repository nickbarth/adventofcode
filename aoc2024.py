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
                i += 1
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
