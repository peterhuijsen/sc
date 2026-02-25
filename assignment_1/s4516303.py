import sys
import string
from hashlib import sha256
from typing import Callable, Any

level, input_file = int(sys.argv[1]), sys.argv[2]
with open(input_file, "r") as f:
    lines = [l.strip().split(",") for l in f.readlines()]

def calculate_combinations(characters: list[str], previous_combinations: list[str]) -> list[str]:
    return [previous + character for previous in previous_combinations for character in characters] 

def simple_crack_hashes(hashes: list[Any], characters: list[str], lengths: tuple[int, int], check_func: Callable[[list[Any], str], list[tuple[str, str]]]) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    combinations = [""]

    # check whether the last generated combinations already hit the maximum length of the passwords
    while len(combinations[-1]) < lengths[1]:
        combinations = calculate_combinations(characters, combinations)

        if len(combinations[0]) < lengths[0]:
            continue
        
        for combination in combinations:

            found.extend(check_func(hashes, combination))
            
    return found

def simple_check_function(hashes: list[str], combination: str) -> list[tuple[str, str]]:
    attempt_hash = sha256(combination.encode("utf-8")).hexdigest()
    return [(h, combination) for h in hashes if h == attempt_hash]


def salted_check_function(hashes: list[tuple[str, str]], combination: str) -> list[tuple[str, str]]:
    found = []
    for hash, salt in hashes:
        attempt_hash = sha256(combination.encode("utf-8") + salt.encode("utf-8")).hexdigest()
        if hash == attempt_hash:
            found.append((hash, combination))

    return found


def mutation_check_function(hashes: list[tuple[str, str]], combination: str) -> list[tuple[str, str]]:
    found = []
    for hash, salt in hashes:
        attempt_hash = sha256(combination.encode("utf-8") + salt.encode("utf-8")).hexdigest()
        if hash == attempt_hash:
            found.append((hash, combination))

    return found


def level_1(csv: list[list[str]]) -> None:
    characters = [str(c) for c in range(10)]
    hashes = [row[1] for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hashes, 
        characters=characters, 
        lengths=(4, 4),
        check_func=simple_check_function 
    )
    
    # works but prolly slow for large csvs
    for row in csv[1:]:
        match = next(iter([m[1] for m in matches if m[0] == row[1]]), None)
        print(f"{row[0]}, {match}")
        
        
def level_2(csv: list[list[str]]) -> None:
    characters = list[str](string.ascii_lowercase)
    hashes = [row[1] for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hashes, 
        characters=characters, 
        lengths=(3, 5),
        check_func=simple_check_function 
    )
    
    for row in csv[1:]:
        match = next(iter([m[1] for m in matches if m[0] == row[1]]), None)
        print(f"{row[0]}, {match}")

def level_3(csv: list[list[str]]) -> None:
    characters = list[str](string.ascii_lowercase)
    hash_salts = [(row[2], row[1]) for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hash_salts, 
        characters=characters, 
        lengths=(3, 5),
        check_func=salted_check_function 
    )
    
    for row in csv[1:]:
        match = next(iter([m[1] for m in matches if m[0] == row[2]]), None)
        print(f"{row[0]}, {match}")

def level_4(csv: list[list[str]]) -> None:
    characters = ["Margrave", "Whalebones", "Muskroots", "Atmometry", "Fourdriniers", "Porrecting", "Pericynthions", "Misfeasors", "Histiology", "Parochin", "Knockwurst", "Rubeolar", "Ensampling", "Plugless", "Cornerback", "Grapplers", "Coronachs", "Waughted", "Catarhine", "Skidpans", "Fleshmongers", "Provenance", "Trollied", "Selaginellas", "Creepages", "Humectated", "Cercopids", "Unproclaimed", "Bourtrees", "Thalamic", "Inerasably", "Panspermatist", "Reheatings", "Changeless", "Karabiners", "Nonexempt", "Hypoplasties", "Shirtier", "Stablenesses", "Eavesdrop", "Recommittal", "Parrotier", "Obtemperates", "Preprimaries", "Freebooting", "Biggetiest", "Reaffixing", "Alcoholisms", "Cartwheels", "Underreported"]
    hashes = [row[1] for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hashes, 
        characters=characters, 
        lengths=(30, 50),
        check_func=simple_check_function 
    )
    
    for row in csv[1:]:
        match = next(iter([m[1] for m in matches if m[0] == row[1]]), None)
        print(f"{row[0]}, {match}")

def level_5(csv: list[list[str]]) -> None:
    mutations = [*[str(c) for c in range(10)], *[string.ascii_letters]]
    characters = list[str](string.ascii_lowercase)
    hashes = [row[1] for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hashes, 
        characters=characters, 
        lengths=(3, 5),
        check_func=simple_check_function 
    )

    for row in csv[1:]:
        previous_password = next(iter([m for m in matches if m[0] == row[1]]))[1]
        hash = row[2]

        result = None
        for mutation in mutations:
            mutated_previous_password = previous_password + mutation
            attempt_hash = sha256(mutated_previous_password.encode("utf-8")).hexdigest()
            if hash == attempt_hash:
                result = mutated_previous_password
                break

        print(f"{row[0]}, {result}")
        
def solve_level(level: int, csv: list[list[str]]) -> None:
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

solve_level(level, lines)