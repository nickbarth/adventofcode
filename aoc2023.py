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

def Day1Part1():
    data = "1abc2\n" +\
           "pqr3stu8vwx\n" +\
           "a1b2c3d4e5f\n"+\
           "treb7uchet\n"
    total = 0
    for num in data.splitlines():
        num = re.sub(r"[a-z]", "", num)
        total += int(f"{num[0]}{num[-1]}") if num else 0
    return total
assert Day1Part1() == 142, "❌"; print(" ⭐", end="")

def Day1Part2():
    data = "two1nine\n" +\
           "eightwothree\n" +\
           "abcone2threexyz\n" +\
           "xtwone3four\n" +\
           "4nineeightseven2\n" +\
           "zoneight234\n" +\
           "7pqrstsixteen"
    total = 0
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    newlines = []
    for line in data.splitlines():
        for digit in digits:
            line = line.replace(digit, digit[0] + str(digits.index(digit)) + digit[-1])
        newlines.append(line)
    for line in newlines:
        num = re.sub(r"[a-z]", "", line)
        total += int(f"{num[0]}{num[-1]}") if num else 0
    return total
assert Day1Part2() == 281, "❌"; print(" ⭐\n")
