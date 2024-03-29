#!/usr/bin/env python3
# ./aoc2022.py && python3 -m mypy aoc2022.py --strict

#####################################
### ⭐🎄 Advent of Code 2022 🎄⭐ ###
#####################################

### types

from typing import List, Dict, Optional, Set, Any, Tuple, Iterator, cast

### utility

import requests
from os import system
from time import sleep
from datetime import datetime

def get_input(session:str, year:int, day:int) -> str:
    cookies:Dict[str,str] = {"session": session}
    request = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    return request.text

SESSION = ""
data15 = get_input(SESSION, 2022, 15)

#####################################
### Day 1: Calorie Counting
#####################################

from heapq import nlargest, heappush

class Day1CalorieCounting(object):
    def __init__(self, data:str):
        self.data:List[Optional[int]] = [x and int(x) or None
                                         for x in data.splitlines()]

    def part1(self) -> int:
        largest:int = -1
        running_total:int = 0
        for calorie in self.data:
            if calorie:
                running_total += calorie
                largest = max(running_total, largest)
            else:
                running_total = 0
        return largest

    def part2(self) -> int:
        heap:List[int] = []
        running_total:int = 0
        for calorie in self.data:
            if calorie:
                running_total += calorie
            else:
                heappush(heap, running_total)
                running_total = 0
        return sum(nlargest(3, heap))

if __name__ == "__main__":
    print("\n⭐🎄 AOC 2022 🎄⭐\n")
    print("[ Day 1 ]:")
    input1:str = "1000\n" +\
                 "2000\n" +\
                 "3000\n\n" +\
                 "4000\n\n" +\
                 "5000\n" +\
                 "6000\n\n" +\
                 "7000\n" +\
                 "8000\n" +\
                 "9000\n\n" +\
                 "10000\n\n"
    solution1 = Day1CalorieCounting(input1)
    assert solution1.part1() == 24000, "❌ Part 1"; print("✅ Part 1")
    assert solution1.part2() == 45000, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 2: Rock Paper Scissors
#####################################

class Day2RockPaperScissors(object):
    def __init__(self, data:str):
        self.data = data.strip().splitlines()

    def part1(self) -> int:
        def score(outcome:str) -> int:
            match outcome:
                # rock
                case "A X": return 1+3
                case "B X": return 1+0
                case "C X": return 1+6
                # paper
                case "A Y": return 2+6
                case "B Y": return 2+3
                case "C Y": return 2+0
                # scissors
                case "A Z": return 3+0
                case "B Z": return 3+6
                case "C Z": return 3+3
                case _:
                    raise ValueError(f"invalid outcome: {outcome}")
        return sum([score(x) for x in self.data])

    def part2(self) -> int:
        def score(outcome:str) -> int:
            match outcome:
                # lose
                case "C X": return 0+2
                case "A X": return 0+3
                case "B X": return 0+1
                # draw
                case "A Y": return 1+3
                case "B Y": return 2+3
                case "C Y": return 3+3
                # win
                case "C Z": return 1+6
                case "A Z": return 2+6
                case "B Z": return 3+6
                case _:
                    raise ValueError(f"invalid outcome: {outcome}")
        return sum([score(x) for x in self.data])

if __name__ == "__main__":
    print("[ Day 2 ]:")
    input2:str = "A Y\n" +\
                 "B X\n" +\
                 "C Z\n"
    solution2 = Day2RockPaperScissors(input2)
    assert solution2.part1() == 15, "❌ Part 1"; print("✅ Part 1")
    assert solution2.part2() == 12, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 3: Rucksack Reorganization
#####################################

class Day3RucksackReorganization(object):
    def __init__(self, data:str):
        self.data:List[str] = data.strip().splitlines()

    def part1(self) -> int:
        def find_common(compartment:List[str]) -> int:
            half:int = int(len(compartment)/2)
            common:Set[str] = set(compartment[:half]) & set(compartment[half:])
            return self.priority_value(common.pop())
        return sum(map(find_common, self.data)) # type:ignore

    def part2(self) -> int:
        triplets:List[List[str]] = [self.data[i:i+3]
                                    for i in range(0, len(self.data), 3)]
        def find_common(group:List[str]) -> int:
            first, second, third = cast(Tuple[str,str,str], group)
            common:Set[str] = set(first) & set(second) & set(third)
            return self.priority_value(common.pop())
        return sum(map(find_common, triplets))

    @staticmethod
    def priority_value(letter:str) -> int:
        if letter.islower():
            return ord(letter)-96
        else:
            return ord(letter)-38

if __name__ == "__main__":
    print("[ Day 3 ]:")
    input3:str = "vJrwpWtwJgWrhcsFMMfFFhFp\n" +\
                 "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\n" +\
                 "PmmdzqPrVvPwwTWBwg\n" +\
                 "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\n" +\
                 "ttgJtRGJQctTZtZT\n" +\
                 "CrZsJsPPZsGzwwsLwLmpwMDw\n"
    solution3 = Day3RucksackReorganization(input3)
    assert solution3.part1() == 157, "❌ Part 1"; print("✅ Part 1")
    assert solution3.part2() == 70,  "❌ Part 2"; print("✅ Part 2\n")


#####################################
### Day 4: Camp Cleanup
#####################################

import re

class Day4CampCleanup(object):
    def __init__(self, data:str):
        self.data:List[str] = data.strip().splitlines()

    def part1(self) -> int:
        def overlaps(pair:str) -> int:
            s1, e1, s2, e2 = cast(Tuple[int,int,int,int], map(int, re.findall(r"\d+", pair)))
            set1:Set[int] = {*range(s1, e1+1)}
            set2:Set[int] = {*range(s2, e2+1)}
            return 1 if set1 & set2 in [set1, set2] else 0
        return sum(map(overlaps, self.data))

    def part2(self) -> int:
        def overlaps(pair:str) -> int:
            s1, e1, s2, e2 = cast(Tuple[int,int,int,int], map(int, re.findall(r"\d+", pair)))
            set1:Set[int] = {*range(s1, e1+1)}
            set2:Set[int] = {*range(s2, e2+1)}
            return 1 if set1 & set2 else 0
        return sum(map(overlaps, self.data))

if __name__ == "__main__":
    print("[ Day 4 ]:")
    input4:str = "2-4,6-8\n" +\
                 "2-3,4-5\n" +\
                 "5-7,7-9\n" +\
                 "2-8,3-7\n" +\
                 "6-6,4-6\n" +\
                 "2-6,4-8\n"
    solution = Day4CampCleanup(input4)
    assert solution.part1() == 2, "❌ Part 1"; print("✅ Part 1")
    assert solution.part2() == 4, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 5: Supply Stacks
#####################################

from copy import deepcopy

class Day5SupplyStacks(object):
    def __init__(self, input:str):
        data:List[str] = input.splitlines()
        rows:List[str] = []
        self.moves:List[List[int]] = []
        self.stacks:List[List[str]]

        for line in data:
            if "[" in line:
                rows.insert(0,line)
            elif line.startswith("move"):
                numbers:List[str] = re.findall(r"\d+", line)
                self.moves.append(list(map(int, numbers)))

        self.stacks = self.stackify([re.findall(r"\[([A-Z])\]|\s{3}\s", x) for x in rows])

    def part1(self) -> str:
        stacks:List[List[str]] = deepcopy(self.stacks)
        def move(stacks:List[List[str]], count:int, source:int, dest:int) -> None:
            for _ in range(count):
                stacks[dest-1].append(stacks[source-1].pop())
        for count, source, dest in self.moves:
            move(stacks, count, source, dest)
        return "".join([x[-1] for x in stacks])

    def part2(self) -> str:
        stacks:List[List[str]] = deepcopy(self.stacks)
        def move(stacks:List[List[str]], count:int, source:int, dest:int) -> None:
            value:List[str] = [stacks[source-1].pop() for _ in range(count)]
            stacks[dest-1] += reversed(value)
        for count, source, dest in self.moves:
            move(stacks, count, source, dest)
        return "".join([x[-1] for x in stacks])

    @staticmethod
    def stackify(row:List[List[str]]) -> List[List[str]]:
        stacks:List[List[str]] = [[] for _ in range(len(row[0]))]
        for column in row:
            for index, value in enumerate(column):
                if value:
                    stacks[index].append(value)
        return stacks


if __name__ == "__main__":
    print("[ Day 5 ]:")
    input5:str= "    [D]    \n" +\
                "[N] [C]    \n" +\
                "[Z] [M] [P]\n" +\
                " 1   2   3 \n" +\
                "\n" +\
                "move 1 from 2 to 1\n" +\
                "move 3 from 1 to 3\n" +\
                "move 2 from 2 to 1\n" +\
                "move 1 from 1 to 2\n"

    solution5 = Day5SupplyStacks(input5)
    assert solution5.part1() == "CMZ", "❌ Part 1"; print("✅ Part 1")
    assert solution5.part2() == "MCD", "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 6: Tuning Trouble
#####################################

class Day6TuningTrouble(object):
    def __init__(self, data:str):
        self.data:str = data

    def find_window(self, minimum:int) -> int:
        for left in range(len(self.data)-minimum):
            window = set(self.data[left:left+minimum])
            if len(window) == minimum:
                return left + minimum
        return -1

    def part1(self) -> int:
        return self.find_window(4)

    def part2(self) -> int:
        return self.find_window(14)

if __name__ == "__main__":
    print("[ Day 6 ]:")
    input6:str = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    solution6 = Day6TuningTrouble(input6)
    assert solution6.part1() == 11, "❌ Part 1"; print("✅ Part 1")
    assert solution6.part2() == 26, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 7: No Space Left On Device
#####################################

from collections import deque

class Folder:
    def __init__(self, name:str):
        self.name:str = name
        self.size:int = 0
        self.parent:Optional[Folder] = None
        self.children:Dict[str,Folder] = {}

class Day7NoSpaceLeftOnDevice(object):
    def __init__(self, data:str):
        self.root:Folder = Folder("root")
        self.root.children["/"] = Folder("/")
        current:Optional[Folder] = self.root
        commands:deque[str] = deque(data.strip().splitlines())
        while commands and current:
            command:List[str] = commands.popleft().split(" ")
            match command:
                case ["$", "cd", folder]:
                    if folder == "..":
                        current = current.parent
                    else:
                        current = current.children[folder]
                case ["$", "ls"]:
                    while commands and not commands[0].startswith("$"):
                        match commands.popleft().split(" "):
                            case ["dir", folder]:
                                node:Folder = Folder(folder)
                                node.parent = current
                                current.children[folder] = node
                            case [size, _]:
                                current.size += int(size)
                                parent = current.parent
                                while parent:
                                    parent.size += int(size)
                                    parent = parent.parent

    def part1(self) -> int:
        total:int = 0
        queue:deque[Folder] = deque([self.root])
        while len(queue) > 0:
            node:Folder = queue.popleft()
            if node.size < 100000:
                total += node.size
            for child in node.children.values():
                queue.append(child)
        return total

    def part2(self) -> int:
        required:int = 30000000 - (70000000 - self.root.children["/"].size)
        smallest:int = 70000000
        queue:deque[Folder] = deque([self.root])
        while len(queue) > 0:
            node:Folder = queue.popleft()
            if node.size >= required and node.size < smallest:
                smallest = node.size
            for child in node.children.values():
                queue.append(child)
        return smallest

if __name__ == "__main__":
    print("[ Day 7 ]:")
    input7:str = "$ cd /\n" +\
                 "$ ls\n" +\
                 "dir a\n" +\
                 "14848514 b.txt\n" +\
                 "8504156 c.dat\n" +\
                 "dir d\n" +\
                 "$ cd a\n" +\
                 "$ ls\n" +\
                 "dir e\n" +\
                 "29116 f\n" +\
                 "2557 g\n" +\
                 "62596 h.lst\n" +\
                 "$ cd e\n" +\
                 "$ ls\n" +\
                 "584 i\n" +\
                 "$ cd ..\n" +\
                 "$ cd ..\n" +\
                 "$ cd d\n" +\
                 "$ ls\n" +\
                 "4060174 j\n" +\
                 "8033020 d.log\n" +\
                 "5626152 d.ext\n" +\
                 "7214296 k\n"
    solution7 = Day7NoSpaceLeftOnDevice(input7)
    assert solution7.part1() == 95437,    "❌ Part 1"; print("✅ Part 1")
    assert solution7.part2() == 24933642, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 8: Treetop Tree House
#####################################

class Day8TreetopTreeHouse(object):
    def __init__(self, data: str):
        self.data:List[List[int]] = [[int(x) for x in y] \
            for y in data.strip().splitlines()]
        self.length:int = len(self.data)
        self.width:int = len(self.data[0])

    def part1(self) -> int:
        tallest:int
        visible:Set[str] = set()
        for y in range(self.length):
            tallest = -1
            for x in range(self.width):
                if (height := self.data[y][x]) > tallest:
                    visible.add(f"{x},{y}")
                    tallest = height
        for y in range(self.length):
            tallest = -1
            for x in range(self.width - 1, -1, -1):
                if (height := self.data[y][x]) > tallest:
                    visible.add(f"{x},{y}")
                    tallest = height
        for x in range(self.width):
            tallest = -1
            for y in range(self.length):
                if (height := self.data[y][x]) > tallest:
                    visible.add(f"{x},{y}")
                    tallest = height
        for x in range(self.width):
            tallest = -1
            for y in range(self.length - 1, -1, -1):
                if (height := self.data[y][x]) > tallest:
                    visible.add(f"{x},{y}")
                    tallest = height
        return len(visible)

    def part2(self) -> int:
        def get_score(x:int, y:int) -> int:
            up = down = left = right = 0
            size = self.data[y][x]
            for i in range(x-1, -1, -1):
                left += 1
                if self.data[y][i] >= size:
                    break
            for i in range(x+1, self.length):
                right += 1
                if self.data[y][i] >= size:
                    break
            for i in range(y-1, -1, -1):
                up += 1
                if self.data[i][x] >= size:
                    break
            for i in range(y+1, self.width):
                down += 1
                if self.data[i][x] >= size:
                    break
            return up*left*down*right
        return max(get_score(x, y) \
                   for x in range(self.length) \
                   for y in range(self.width))

if __name__ == "__main__":
    print("[ Day 8 ]:")
    input8: str = "30373\n" +\
                  "25512\n" +\
                  "65332\n" +\
                  "33549\n" +\
                  "35390\n"
    solution8 = Day8TreetopTreeHouse(input8)
    assert solution8.part1() == 21, "❌ Part 1"; print("✅ Part 1")
    assert solution8.part2() == 8,  "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 9: Rope Bridge
#####################################

class Day9RopeBridge(object):
    def __init__(self, data: str):
        self.data:List[Tuple[str,int]]= [(x,int(y)) for x,y in \
                [z.split() for z in data.strip().splitlines()]]

    def part1(self, start:complex) -> int:
        head:complex = start
        tail:complex = start
        moves:Set[complex] = set([start])

        for move in self.data:
            match move:
                case ('U', units): movement = 0 + -1j
                case ('D', units): movement = 0 + 1j
                case ('L', units): movement = -1 + 0j
                case ('R', units): movement = 1 + 0j
            for _ in range(units):
                prev = head
                head += movement
                distance = (head - tail)
                if abs(distance.real) <= 1 and \
                        abs(distance.imag) <= 1:
                    continue
                elif head.real == tail.real or \
                     head.imag == tail.imag:
                    tail += movement
                else:
                    tail = prev
                moves.add(tail)
        return len(moves)

    def part2(self, start:complex) -> int:
        rope:List[complex] = [start] * 10
        moves:Set[complex] = set([start])
        for direction, units in self.data:
            match direction:
                case 'U': movement = 0 + -1j
                case 'D': movement = 0 + 1j
                case 'L': movement = -1 + 0j
                case 'R': movement = 1 + 0j
            for _ in range(units):
                # move head
                rope[0] += movement
                for i in range(1, len(rope)):
                    head = rope[i-1]
                    distance = (rope[i] - head)
                    if abs(distance.real) <= 1 and abs(distance.imag) <= 1:
                        continue
                    # update the position
                    if rope[i].real == head.real:
                        # x == x | move vertically
                        if rope[i].imag < head.imag:
                            rope[i] += (0 + 1j)
                        else:
                            rope[i] -= (0 + 1j)
                    elif rope[i].imag == head.imag:
                        # x == x | move horizontally
                        if rope[i].real < head.real:
                            rope[i] += (1 + 0j)
                        else:
                            rope[i] -= (1 + 0j)
                    else:
                        # move diagonally
                        if rope[i].real < head.real:
                            rope[i] += (1 + 0j)
                        else:
                            rope[i] -= (1 + 0j)
                        if rope[i].imag < head.imag:
                            rope[i] += (0 + 1j)
                        else:
                            rope[i] -= (0 + 1j)
                moves.add(rope[9])
                # self.draw_graph(start, rope)
        return len(moves)

    @staticmethod
    def draw_graph(start:complex, rope:List[complex]) -> None:
        for y in range(30):
            for x in range(30):
                curr = complex(x,y)
                if curr in rope:
                    if rope.index(curr) == 0:
                        print("H", end="")
                    else:
                        print(rope.index(curr), end="")
                elif curr == start:
                    print("s", end="")
                else:
                    print(".", end="")
            print()
        print()
        input()

if __name__ == "__main__":
    print("[ Day 9 ]:")
    input9:str = "R 5\n" +\
                 "U 8\n" +\
                 "L 8\n" +\
                 "D 3\n" +\
                 "R 17\n" +\
                 "D 10\n" +\
                 "L 25\n" +\
                 "U 20\n"

    solution9 = Day9RopeBridge(input9)
    assert solution9.part1(11 + 20j) == 88, "❌ Part 1"; print("✅ Part 1")
    assert solution9.part2(11 + 15j) == 36, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 10: Cathode-Ray Tube
#####################################

class Day10CathodeRayTube(object):
    def __init__(self, data: str):
        self.commands = deque([x for x in \
            [z.split() for z in data.strip().splitlines()]])

    def process(self) -> Tuple[int, str]:
        cursor:List[int] = [0,1,2]
        screen:List[str] = ["#"]+["."]*239
        signal:int = 0
        cycle:int = 1
        reg:Dict[str,int] = { "x": 1 }

        def next_cycle() -> None:
            nonlocal cycle, reg, screen, cursor, signal
            if cycle in cursor:
                screen[cycle] = "#"
            cycle += 1
            if cycle % 40 == 0:
                cursor = [x + 40 for x in cursor]
            if cycle in [20, 60, 100, 140, 180, 220]:
                signal += cycle * reg["x"]

        while self.commands:
            op = self.commands.popleft()
            match op:
                case ["noop"]:
                    next_cycle()
                case ["addx", num]:
                    next_cycle()
                    reg["x"] += int(num)
                    cursor = [x + int(num) for x in cursor]
                    next_cycle()

        return signal, "".join(screen)

        def print_screen():
            nonlocal cursor, screen, reg
            print(cycle, reg)
            for y in range(6):
                for x in range(40):
                    if (y*40)+x in cursor:
                        print("X", end="")
                    else:
                        print(screen[(y*40)+x], end="")
                print()

if __name__ == "__main__":
    print("[ Day 10 ]:")
    input10:str = "addx 15\n" +\
                  "addx -11\n" +\
                  "addx 6\n" +\
                  "addx -3\n" +\
                  "addx 5\n" +\
                  "addx -1\n" +\
                  "addx -8\n" +\
                  "addx 13\n" +\
                  "addx 4\n" +\
                  "noop\n" +\
                  "addx -1\n" +\
                  "addx 5\n" +\
                  "addx -1\n" +\
                  "addx 5\n" +\
                  "addx -1\n" +\
                  "addx 5\n" +\
                  "addx -1\n" +\
                  "addx 5\n" +\
                  "addx -1\n" +\
                  "addx -35\n" +\
                  "addx 1\n" +\
                  "addx 24\n" +\
                  "addx -19\n" +\
                  "addx 1\n" +\
                  "addx 16\n" +\
                  "addx -11\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 21\n" +\
                  "addx -15\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx -3\n" +\
                  "addx 9\n" +\
                  "addx 1\n" +\
                  "addx -3\n" +\
                  "addx 8\n" +\
                  "addx 1\n" +\
                  "addx 5\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx -36\n" +\
                  "noop\n" +\
                  "addx 1\n" +\
                  "addx 7\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 2\n" +\
                  "addx 6\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 7\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "addx -13\n" +\
                  "addx 13\n" +\
                  "addx 7\n" +\
                  "noop\n" +\
                  "addx 1\n" +\
                  "addx -33\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 2\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 8\n" +\
                  "noop\n" +\
                  "addx -1\n" +\
                  "addx 2\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "addx 17\n" +\
                  "addx -9\n" +\
                  "addx 1\n" +\
                  "addx 1\n" +\
                  "addx -3\n" +\
                  "addx 11\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx -13\n" +\
                  "addx -19\n" +\
                  "addx 1\n" +\
                  "addx 3\n" +\
                  "addx 26\n" +\
                  "addx -30\n" +\
                  "addx 12\n" +\
                  "addx -1\n" +\
                  "addx 3\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx -9\n" +\
                  "addx 18\n" +\
                  "addx 1\n" +\
                  "addx 2\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 9\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx -1\n" +\
                  "addx 2\n" +\
                  "addx -37\n" +\
                  "addx 1\n" +\
                  "addx 3\n" +\
                  "noop\n" +\
                  "addx 15\n" +\
                  "addx -21\n" +\
                  "addx 22\n" +\
                  "addx -6\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "addx 2\n" +\
                  "addx 1\n" +\
                  "noop\n" +\
                  "addx -10\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "addx 20\n" +\
                  "addx 1\n" +\
                  "addx 2\n" +\
                  "addx 2\n" +\
                  "addx -6\n" +\
                  "addx -11\n" +\
                  "noop\n" +\
                  "noop\n" +\
                  "noop\n"

    solution10 = Day10CathodeRayTube(input10)
    solution10_part1, solution10_part2 = solution10.process()
    assert solution10_part1 == 13140, "❌ Part 1"; print("✅ Part 1")
    screen_test = "##..##..##..##..##..##..##..##..##..##.." +\
                  "###...###...###...###...###...###...###." +\
                  "####....####....####....####....####...." +\
                  "#####.....#####.....#####.....#####....." +\
                  "######......######......######......####" +\
                  "#######.......#######.......#######....."
    assert solution10_part2 == screen_test, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 11: Monkey in the Middle
#####################################

import re
from collections import deque
from functools import reduce
from operator import mul

class Monkey:
    def __init__(self) -> None:
        self.items:deque[int] = deque()
        self.inspect_count:int = 0
        self.op:List[str] = []
        self.test:int = 0
        self.pass_node:int = 0
        self.fail_node:int = 0

class Day11MonkeyInTheMiddle(object):
    def __init__(self, text:str):
        self.monkies = []

        def readlines(data:str) -> Iterator[str]:
            i = 0
            lines = data.strip().splitlines()
            while i < len(lines):
                yield lines[i]
                i += 1
            yield None # type: ignore

        lines = readlines(text)

        while (line := next(lines)) != None:
            if line.startswith("Monkey"):
                monkey = Monkey()
                monkey.items = deque(map(int, re.findall("\d{1,}", next(lines))))
                monkey.op = re.search("Operation: new = (.*)", next(lines))[1].split(" ") # type: ignore
                monkey.test = int(re.search("\d{1,}", next(lines))[0]) # type: ignore
                monkey.pass_node = int(re.search("\d{1,}", next(lines))[0]) # type: ignore
                monkey.fail_node = int(re.search("\d{1,}", next(lines))[0]) # type: ignore
                self.monkies.append(monkey)

    def part1(self) -> int:
        monkies = deepcopy(self.monkies)
        def process_monkey(monkey:Monkey) -> None:
            while monkey.items:
                new:int
                old:int = monkey.items.popleft()
                match monkey.op:
                    case ["old", "*", "old"]: new = old * old
                    case ["old", "*", num]:   new = old * int(num)
                    case ["old", "+", num]:   new = old + int(num)
                monkey.inspect_count += 1
                new = new // 3
                if new % monkey.test == 0:
                    monkies[monkey.pass_node].items.append(new)
                else:
                    monkies[monkey.fail_node].items.append(new)
        for _ in range(20):
            for monkey in monkies:
                process_monkey(monkey)
        return reduce(mul, (sorted([monkey.inspect_count \
            for monkey in monkies], reverse=True)[:2]))

    def part2(self) -> int:
        monkies = deepcopy(self.monkies)
        def process_monkey(monkey:Monkey) -> None:
            while monkey.items:
                new:int
                old:int = monkey.items.popleft()
                match monkey.op:
                    case ["old", "*", "old"]: new = old * old
                    case ["old", "*", num]:   new = old * int(num)
                    case ["old", "+", num]:   new = old + int(num)
                monkey.inspect_count += 1
                # new = new % 9699690
                new = new % 96577
                if new % monkey.test == 0:
                    monkies[monkey.pass_node].items.append(new)
                else:
                    monkies[monkey.fail_node].items.append(new)
        for _ in range(10000):
            for monkey in monkies:
                process_monkey(monkey)
        return reduce(mul, (sorted([monkey.inspect_count \
            for monkey in monkies], reverse=True)[:2]))

if __name__ == "__main__":
    print("[ Day 11 ]:")
    input11:str = "Monkey 0:\n" +\
                  "  Starting items: 79, 98\n" +\
                  "  Operation: new = old * 19\n" +\
                  "  Test: divisible by 23\n" +\
                  "    If true: throw to monkey 2\n" +\
                  "    If false: throw to monkey 3\n\n" +\
                  "Monkey 1:\n" +\
                  "  Starting items: 54, 65, 75, 74\n" +\
                  "  Operation: new = old + 6\n" +\
                  "  Test: divisible by 19\n" +\
                  "    If true: throw to monkey 2\n" +\
                  "    If false: throw to monkey 0\n\n" +\
                  "Monkey 2:\n" +\
                  "  Starting items: 79, 60, 97\n" +\
                  "  Operation: new = old * old\n" +\
                  "  Test: divisible by 13\n" +\
                  "    If true: throw to monkey 1\n" +\
                  "    If false: throw to monkey 3\n\n" +\
                  "Monkey 3:\n" +\
                  "  Starting items: 74\n" +\
                  "  Operation: new = old + 3\n" +\
                  "  Test: divisible by 17\n" +\
                  "    If true: throw to monkey 0\n" +\
                  "    If false: throw to monkey 1\n\n"
    solution11 = Day11MonkeyInTheMiddle(input11)
    assert solution11.part1() == 10605, "❌ Part 1"; print("✅ Part 1")
    assert solution11.part2() == 2713310158, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 12: Hill Climbing Algorithm
#####################################

from heapq import heappop, heappush

class Day12HillClimbingAlgorithm(object):
    def __init__(self, data:str):
        self.maze = [[*x] for x in data.strip().splitlines()]
        self.height, self.width = len(self.maze), len(self.maze[0])
        self.start = self.end = (0,0)

        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == "S":
                    self.start = (x,y)
                    self.maze[y][x] = "a"
                if self.maze[y][x] == "E":
                    self.end = (x,y)
                    self.maze[y][x] = "{"

    def part1(self) -> int:
        path:Dict[Tuple[int,int],Optional[Tuple[int,int]]] = {self.start:None}
        costs:Dict[Tuple[int,int],int] = {self.start: 0}
        queue:List[Tuple[int, Tuple[int,int]]] = [(0, self.start)]
        while queue:
            cost, current = heappop(queue)
            x, y = current
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                mx, my = x + dx, y + dy
                if not (0 <= mx < self.width and 0 <= my < self.height):
                    continue
                if (mx, my) in costs:
                    continue
                if ord(self.maze[my][mx]) - ord(self.maze[y][x]) > 1:
                    continue
                heappush(queue, (cost + 1, (mx, my)))
                costs[(mx, my)] = cost + 1
                path[(mx, my)] = current
        return costs[self.end]

    def part2(self) -> int:
        self.start, self.end = self.end, self.start
        visited:Set[Tuple[int,int]] = set()
        queue:deque[Tuple[Tuple[int,int], int]] = deque([(self.start, 0)])
        while queue:
            [x, y], steps = queue.popleft()
            if self.maze[y][x] == 'a':
                return steps
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                mx, my = x + dx, y + dy
                if not (0 <= mx < self.width and 0 <= my < self.height):
                    continue
                if (mx, my) in visited:
                    continue
                if ord(self.maze[y][x]) - ord(self.maze[my][mx]) > 1:
                    continue
                queue.append(((mx, my), steps + 1))
                visited.add((mx, my))
        return -1

if __name__ == "__main__":
    print("[ Day 12 ]:")
    input12:str = "Sabqponm\n" +\
                  "abcryxxl\n" +\
                  "accszExk\n" +\
                  "acctuvwj\n" +\
                  "abdefghi\n"
    solution12 = Day12HillClimbingAlgorithm(input12)
    assert solution12.part1() == 31, "❌ Part 1"; print("✅ Part 1")
    assert solution12.part2() == 29, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 13: Distress Signal
#####################################

from functools import cmp_to_key
from collections import deque

class Day13DistressSignal(object):
    def __init__(self, text:str):
        self.data = [eval(x) for x in text.strip().splitlines() if x != ""]

    def part1(self) -> int:
        it = iter(self.data)
        pairs = list(zip(it, it))
        score = 0
        index = 0
        for l1, l2 in pairs:
            index += 1
            if compare := self.compare_lists(l1, l2):
                score += index
        return score

    def part2(self) -> int:
        self.data += [[[2]]]
        self.data += [[[6]]]

        def sort_lists(l1:List[int], l2:List[int]) -> int:
            result = self.compare_lists(l1, l2)
            if result == None: return -1
            elif result: return -1
            else: return 1

        self.data = sorted(self.data, key=cmp_to_key(sort_lists))
        return (self.data.index([[2]]) + 1) * \
            (self.data.index([[6]]) + 1)

    def compare_lists(self, l1:List[int], l2:List[int]) -> Optional[bool]:
        list1, list2 = deque(l1), deque(l2)
        while list1 and list2:
            item1 = list1.popleft()
            item2 = list2.popleft()
            match item1, item2:
                case int(),  int():
                    if item1 == item2:
                        continue
                    return item1 < item2
                case list(), list():
                    result = self.compare_lists(item1, item2)
                    if result is None:
                        continue
                    return result
                case int(),  list():
                    result = self.compare_lists([item1], item2)
                    if result is None:
                        continue
                    return result
                case list(), int():
                    result = self.compare_lists(item1, [item2])
                    if result is None:
                        continue
                    return result
        if not list1 and list2:
            return True
        if list1 and not list2:
            return False
        return None


if __name__ == "__main__":
    print("[ Day 13 ]:")
    input13:str = "[1,1,3,1,1]\n" +\
                  "[1,1,5,1,1]\n\n" +\
                  "[[1],[2,3,4]]\n" +\
                  "[[1],4]\n\n" +\
                  "[9]\n" +\
                  "[[8,7,6]]\n\n" +\
                  "[[4,4],4,4]\n" +\
                  "[[4,4],4,4,4]\n\n" +\
                  "[7,7,7,7]\n" +\
                  "[7,7,7]\n\n" +\
                  "[]\n" +\
                  "[3]\n\n" +\
                  "[[[]]]\n" +\
                  "[[]]\n\n" +\
                  "[1,[2,[3,[4,[5,6,7]]]],8,9]\n" +\
                  "[1,[2,[3,[4,[5,6,0]]]],8,9]\n\n"
    solution13 = Day13DistressSignal(input13)
    assert solution13.part1() == 13,  "❌ Part 1"; print("✅ Part 1")
    assert solution13.part2() == 140, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 14: Regolith Reservoir
#####################################

import re

class Day14RegolithReservoir(object):
    def __init__(self, text:str):
        self.sand:Set[Tuple[int,int]] = set()
        self.ground:Set[Tuple[int,int]]  = set()
        self.has_floor:bool = False
        self.start:Tuple[int,int] = (500, 0)

        # parse
        data = text.strip().splitlines()
        paths = [[list(map(int,y.split(","))) for y in
          re.findall("\d+,\d+", x)] for x in data]

        # get width and height
        flatten = [x for sub in paths for x in sub]
        xs, ys = list(zip(*flatten))
        xs = sorted([*xs]) # type:ignore
        ys = sorted([*ys]) # type:ignore
        self.height, self.width = ys[-1] + 2, xs[-1] + 2

        # add paths
        for lines in paths:
            x1, y1 = lines.pop(0)
            self.ground.add((x1,y1))
            while lines:
                x2, y2 = lines.pop(0)
                while x1 != x2 or y1 != y2:
                    if   x1 < x2: x1 += 1
                    elif x1 > x2: x1 -= 1
                    elif y1 < y2: y1 += 1
                    elif y1 > y2: y1 -= 1
                    self.ground.add((x1,y1))

    def is_falling(self, x:int, y:int) -> bool:
        if self.has_floor:
            return (y != self.height) and \
                   (x, y) not in self.ground and \
                   (x, y) not in self.sand
        return (x, y) not in self.ground and \
               (x, y) not in self.sand

    def count_sand(self, has_floor:bool) -> int:
        x, y = self.start
        self.sand = set()
        self.has_floor = has_floor

        while True:
            if not has_floor and y == self.height:
                return len(self.sand) # part 1
            elif self.is_falling(x,  y+1): y += 1
            elif self.is_falling(x-1,y+1): x, y = x-1, y+1
            elif self.is_falling(x+1,y+1): x, y = x+1, y+1
            elif (x, y) == self.start:
                return len(self.sand) + 1 # part 2
            else:
                self.sand.add((x, y))
                x, y = self.start

    def part1(self) -> int:
        return self.count_sand(False)

    def part2(self) -> int:
        return self.count_sand(True)

    def draw_cave(self) -> None:
        for y in range(40, 49):
            for x in range(518, 600):
                if (x,y) in self.ground: print("#", end="")
                elif (x,y) in self.sand: print("o", end="")
                else: print(".", end="")
            print()
        input()

if __name__ == "__main__":
    print("[ Day 14 ]:")
    input14 = "498,4 -> 498,6 -> 496,6\n" +\
              "503,4 -> 502,4 -> 502,9 -> 494,9"
    solution14 = Day14RegolithReservoir(input14)
    assert solution14.part1() == 24, "❌ Part 1"; print("✅ Part 1")
    assert solution14.part2() == 93, "❌ Part 2"; print("✅ Part 2\n")

#####################################
### Day 15: Beacon Exclusion Zone
#####################################

import re

class Day15BeaconExclusionZone(object):
    def __init__(self, text:str):
        self.sensors = []
        self.beacons = []
        self.distances = []

        # parse input
        data = text.strip().splitlines()
        pairs = [[tuple(map(int,y)) \
          for y in re.findall("(\-?\d+), y=(\-?\d+)", x)] \
          for x in data]

        # get sensors and beacons
        for sensor, beacon in pairs:
            self.sensors.append(sensor)
            self.beacons.append(beacon)
            x1, y1 = sensor
            x2, y2 = beacon
            self.distances.append(abs(x1 - x2) + abs(y1 - y2))

        # find x,y min and max
        x_ranges = []
        y_ranges = []
        for i, beacon in enumerate(self.beacons):
            x, y = beacon
            x_ranges.append(x + self.distances[i])
            x_ranges.append(x - self.distances[i])
            y_ranges.append(y + self.distances[i])
            y_ranges.append(y - self.distances[i])

        x_ranges.sort()
        y_ranges.sort()

        self.xmin, self.xmax = x_ranges[0], x_ranges[-1]
        self.ymin, self.ymax = y_ranges[0], y_ranges[-1]

    def part1(self) -> int:
        count = 0
        y1 = 10
        for x1 in range(self.xmin, self.xmax):
            if (x1, y1) in self.beacons or \
               (x1, y1) in self.sensors:
                continue
            for i, (x2, y2) in enumerate(self.sensors):
                distance = abs(x1 - x2) + abs(y1 - y2)
                if distance <= self.distances[i]:
                    count += 1
                    break
        return count

    def part2(self) -> int:
        points = set()
        intersecs = set()

        def add_point(x:int, y:int) -> None:
            if 0 <= x < 20 and 0 <= y <= 20:
                if (x,y) in points:
                    intersecs.add((x, y))
                else:
                    points.add((x, y))

        for i, sensor in enumerate(self.sensors):
            print(" > sensor", i)
            x, y = sensor
            d = self.distances[i] + 1
            for i in range(0, d+1):
                add_point(x+d-i, y+i)
                add_point(x+d-i, y-i)
                add_point(x-d+i, y+i)
                add_point(x-d+i, y-i)

        for i, sensor in enumerate(self.sensors):
            print(" > sensor", i)
            x1, y1 = sensor
            remove = set()
            for x2, y2 in intersecs:
                distance = abs(x1 - x2) + abs(y1 - y2)
                if distance <= self.distances[i]:
                    remove.add((x2, y2))
            for point in remove:
                intersecs.remove(point)

        x, y = intersecs.pop() or (0,0)
        return (x * 4000000) + y

if __name__ == "__main__":
    print("[ Day 15 ]:")
    input15:str = "Sensor at x=2, y=18: closest is at x=-2, y=15\n" +\
                  "Sensor at x=9, y=16: closest beacon is at x=10, y=16\n" +\
                  "Sensor at x=13, y=2: closest beacon is at x=15, y=3\n" +\
                  "Sensor at x=12, y=14: beacon is at x=10, y=16\n" +\
                  "Sensor at x=10, y=20: closest beacon is at x=10, y=16\n" +\
                  "Sensor at x=14, y=17: closest beacon is at x=10, y=16\n" +\
                  "Sensor at x=8, y=7: closest beacon is at x=2, y=10\n" +\
                  "Sensor at x=2, y=0: closest beacon is at x=2, y=10\n" +\
                  "Sensor at x=0, y=11: closest beacon is at x=2, y=10\n" +\
                  "Sensor at x=20, y=14: closest beacon is at x=25, y=17\n" +\
                  "Sensor at x=17, y=20: closest beacon is at x=21, y=22\n" +\
                  "Sensor at x=16, y=7: closest beacon is at x=15, y=3\n" +\
                  "Sensor at x=14, y=3: closest beacon is at x=15, y=3\n" +\
                  "Sensor at x=20, y=1: closest beacon is at x=15, y=3\n"
    solution15 = Day15BeaconExclusionZone(input15)
    assert solution15.part1() == 26, "❌ Part 1"; print("✅ Part 1")
    assert solution15.part2() == 56000011, "❌ Part 2"; print("✅ Part 2\n")
