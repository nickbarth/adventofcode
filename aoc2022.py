### Advent of Code
### 2022

### Utility

import requests

def get_input(session:str, year:int, day:int) -> str:
    cookies:dict = {"session": session}
    request:Response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    return request.text

### Day1CalorieCounting

from heapq import nlargest, heappush

class Day1CalorieCounting(object):
    def __init__(self, data:str):
        self.data:[int,None] = [x and int(x) or None for x in data.split("\n")]

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
        heap:[int] = []
        running_total:int = 0
        for calorie in self.data:
            if calorie:
                running_total += calorie
            else:
                heappush(heap, running_total)
                running_total = 0
        return sum(nlargest(3, heap))

### Day2RockPaperScissors
    
class Day2RockPaperScissors(object):
    def __init__(self, data:str):
        self.data:[[int]] = [x.split(" ") for x in data.strip().split("\n")]

    def part1(self) -> int:
        def score(player1:int, player2:int) -> int:
            outcome:dict = {
                # rock
                "X": { "A": 1+3, "B": 1+0, "C": 1+6 },
                # paper
                "Y": { "A": 2+6, "B": 2+3, "C": 2+0 },
                # scissors
                "Z": { "A": 3+0, "B": 3+6, "C": 3+3 }
            }
            return outcome[player2][player1]
        return sum([score(x,y) for x,y in self.data])

    def part2(self) -> int:
        def score(player1:int, player2:int) -> int:
            outcome:dict = {
                # lose
                "X": { "C": 0+2, "A": 0+3, "B": 0+1 },
                # draw
                "Y": { "A": 1+3, "B": 2+3, "C": 3+3 },
                # win
                "Z": { "C": 1+6, "A": 2+6, "B": 3+6 }
            }
            return outcome[player2][player1]
        return sum([score(x,y) for x,y in self.data])
