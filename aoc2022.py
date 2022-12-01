### Utility
import requests

def get_input(session:str, year:int, day:int) -> str:
    cookies:dict = {"session": session}
    request:Response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies)
    return request.text

### Day1CalorieCounting
from heapq import nlargest, heappush

class Day1CalorieCounting(object):
    def __init__(self, data:[str]):
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
