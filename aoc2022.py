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

#####################################
### Day 1: Calorie Counting
#####################################

from heapq import nlargest, heappush

class Day1CalorieCounting(object):
    def __init__(self, data:str):
        self.data:List[Optional[int]] = [x and int(x) or None
                                         for x in data.split("\n")]

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
                 "10000\n"
    solution1 = Day1CalorieCounting(input1)
    assert solution1.part1() == 24000
    assert solution1.part2() == 45000
    print("✅ Part 1\n✅ Part 2\n")

#####################################
### Day 2: Rock Paper Scissors
#####################################

class Day2RockPaperScissors(object):
    def __init__(self, data:str):
        self.data = [x for x in data.strip().split("\n")]

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
    assert solution2.part1() == 15
    assert solution2.part2() == 12
    print("✅ Part 1\n✅ Part 2\n")

#####################################
### Day 3: Rucksack Reorganization
#####################################

class Day3RucksackReorganization(object):
    def __init__(self, data:str):
        self.data:List[str] = data.strip().split("\n")

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
    assert solution3.part1() == 157
    assert solution3.part2() == 70
    print("✅ Part 1\n✅ Part 2\n")


#####################################
### Day 4: Camp Cleanup
#####################################

import re

class Day4CampCleanup(object):
    def __init__(self, data:str):
        self.data:List[str] = data.strip().split("\n")

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
    assert solution.part1() == 2
    assert solution.part2() == 4
    print("✅ Part 1\n✅ Part 2\n")
