import sys
from hashlib import sha256

level, input_file = int(sys.argv[1]), sys.argv[2]
with open(input_file, "r") as f:
    lines = [l.strip().split(",") for l in f.readlines()]

def solve_level(level, csv):
    match level:
        case 1:
            return level_1(csv)
        case 2:
            return level_2(csv)
        case 3:
            return level_3(csv)
        case 4:
            return level_4(csv)
        case 5:
            return level_5(csv)
        case _:
            raise ValueError(f"Level {level} not found")

def level_1(csv):
    pass

def level_2(csv):
    pass

def level_3(csv):
    pass

def level_4(csv):
    pass

def level_5(csv):
    pass