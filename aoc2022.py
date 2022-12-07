#!/usr/bin/env python3
# ./aoc2022.py && python3 -m mypy aoc2022.py --strict

#####################################
### ⭐🎄 Advent of Code 2022 🎄⭐ ###
#####################################

### types

from typing import List, Dict, Optional, Set, Any, Tuple, cast

### utility

import requests

def get_input(session:str, year:int, day:int) -> str:
    cookies:Dict[str,str] = {"session": session}
    request = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    return request.text

SESSION = ""
data7 = get_input(SESSION, 2022, 7)

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
        self.data = [x for x in data.strip().splitlines()]

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

class Node:
    def __init__(self, name:str):
        self.name:str = name
        self.size:int = 0
        self.parent:Optional[Node] = None
        self.children:Dict[str,Node] = {}

class Day7NoSpaceLeftOnDevice(object):
    def __init__(self, data:str):
        self.root:Node = Node("root")
        self.root.children["/"] = Node("/")
        current:Optional[Node] = self.root
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
                                node:Node = Node(folder)
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
        queue:deque[Node] = deque([self.root])
        while len(queue) > 0:
            node:Node = queue.popleft()
            if node.size < 100000:
                total += node.size
            for child in node.children.values():
                queue.append(child)
        return total

    def part2(self) -> int:
        required:int = 30000000 - (70000000 - self.root.children["/"].size)
        smallest:int = 70000000
        queue:deque[Node] = deque([self.root])
        while len(queue) > 0:
            node:Node = queue.popleft()
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
