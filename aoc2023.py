#!/usr/bin/env python3

import re
import requests
from os import system
from time import sleep
from datetime import datetime

print()
print("##########################")
print("### ⭐🎄 AOC 2023 🎄⭐ ###")
print("##########################")
print()

SESSION = ""

def get_input(session, year, day):
    cookies = {"session": session}
    request = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    return request.text

data = get_input(SESSION, 2023, 1)

print("Day 1:", end="")

data = "1abc2\n" +\
       "pqr3stu8vwx\n" +\
       "a1b2c3d4e5f\n"+\
       "treb7uchet\n"

def Day1Part1(data):
    total = 0
    for num in data.splitlines():
        num = re.sub(r"[a-z]", "", num)
        total += int(f"{num[0]}{num[-1]}") if num else 0
    return total
assert Day1Part1(data) == 142, "❌"; print(" ⭐", end="")

data = "two1nine\n" +\
       "eightwothree\n" +\
       "abcone2threexyz\n" +\
       "xtwone3four\n" +\
       "4nineeightseven2\n" +\
       "zoneight234\n" +\
       "7pqrstsixteen"

def Day1Part2(data):
    DIGITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    total = 0
    forward_trie = {}
    backward_trie = {}
    def add_word(trie, word):
        curr = trie
        for c in word:
            curr = curr.setdefault(c, {})
        curr["*"] = "*"
    def search_word(trie, word):
        digit = ""
        curr = trie
        for c in word:
            digit += c
            if c not in curr:
                return False
            curr = curr[c]
            if "*" in curr:
                return digit
        return digit if "*" in curr else False
    def get_first(line, trie, reverse=False):
        for i, c in enumerate(line):
            if c.isdigit():
                return int(c)
            if digit := search_word(trie, line[i:]):
                if not reverse:
                    return DIGITS.index(digit) 
                else:
                    return DIGITS.index(digit[::-1])
        return None
    for digit in DIGITS:
        add_word(forward_trie, digit)
        add_word(backward_trie, digit[::-1])
    for line in data.splitlines():
        first_digit = get_first(line, forward_trie)
        last_digit = get_first(line[::-1], backward_trie, True)
        total += first_digit * 10 + last_digit
    return total
assert Day1Part2(data) == 281, "❌"; print(" ⭐\n")

print("🎄 Day 2:", end="")

data = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n" +\
       "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n" +\
       "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n" +\
       "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n" +\
       "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

def Day2Part1(data):
    total = 0
    for game in re.finditer(r'Game (\d+): (.+)', data):
        counts = defaultdict(int)
        number, rounds = game.groups()
        cubes = re.findall(r'(\d+) (\w+)', rounds)
        for amount, color in cubes:
            counts[color] = max(counts[color], int(amount))
        if counts["red"] <= 12 and counts["green"] <= 13 and counts["blue"] <= 14:
            total += int(number)
    return total
assert Day2Part1(data) == 8, "❌"; print(" ⭐", end="")

data = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n" +\
       "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n" +\
       "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n" +\
       "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n" +\
       "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

def Day2Part2(data):
    total = 0
    for game in re.finditer(r'Game (\d+): (.+)', data):
        counts = defaultdict(int)
        number, rounds = game.groups()
        cubes = re.findall(r'(\d+) (\w+)', rounds)
        for amount, color in cubes:
            counts[color] = max(counts[color], int(amount))
        total += counts['red'] * counts['green'] * counts['blue']
    return total
assert Day2Part2(data) == 2286, "❌"; print(" ⭐\n")

print("🎄 Day 3:", end="")

data = "467..114..\n" +\
       "...*......\n" +\
       "..35..633.\n" +\
       "......#...\n" +\
       "617*......\n" +\
       ".....+.58.\n" +\
       "..592.....\n" +\
       "......755.\n" +\
       "...$.*....\n" +\
       ".664.598.."

def Day3Part1(data):
    total = 0
    lines = data.splitlines()
    width, height = len(lines[0]), len(lines)
    grid = [list(line) for line in lines]
    def is_valid(y, x):
        def is_touching(dy, dx):
            ny, nx = y + dy, x + dx
            return 0 <= ny < height and 0 <= nx < width \
                and grid[ny][nx] not in '.0123456789'
        adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        return any(is_touching(dy, dx) for dy, dx in adjacent)
    for y in range(height):
        number, valid = "", False
        for x in range(width):
            char = grid[y][x]
            if char.isdigit():
                valid |= is_valid(y, x)
                number += char
            else:
                if number and valid:
                    total += int(number)
                number, valid = "", False
        if number and valid:
            total += int(number)
    return total
assert Day3Part1(data) == 4361, "❌"; print(" ⭐", end="")

def Day3Part2(data):
    total = 0
    valid_numbers = defaultdict(list)
    lines = data.splitlines()
    width, height = len(lines[0]), len(lines)
    grid = [list(line) for line in lines]
    def get_star(y, x):
        def is_touching(dy, dx):
            ny, nx = y + dy, x + dx
            if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] == '*':
                return (ny, nx)
            return None
        adjacent = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        position = [is_touching(dy, dx) for dy, dx in adjacent]
        return next(iter([x for x in position if x is not None]), None)
    for y in range(height):
        number, valid = "", False
        for x in range(width):
            char = grid[y][x]
            if char.isdigit():
                valid = valid or get_star(y, x)
                number += char
            else:
                if number and valid:
                    valid_numbers[valid].append(number)
                number, valid = "", False
        if number and valid:
            valid_numbers[valid].append(number)
    return sum(int(x[0]) * int(x[1]) for x in valid_numbers.values() if len(x) == 2)
assert Day3Part2(data) == 467835, "❌"; print(" ⭐\n")
