import sys
import string
from hashlib import sha256

level, input_file = int(sys.argv[1]), sys.argv[2]
with open(input_file, "r") as f:
    lines = [l.strip().split(",") for l in f.readlines()]

def calculate_combinations(characters, previous_combinations):
    # We append each character for each previous combination.
    return [previous + character for previous in previous_combinations for character in characters] \
        if len(previous_combinations) > 0 \
        else characters
    
def simple_crack_hashes(hashes, characters, lengths, check_func):
    found = []
    combinations = []
    while len(combinations[-1] if len(combinations) > 0 else []) < lengths[1]:
        combinations = calculate_combinations(characters, combinations)
        for combination in combinations:
            # Skip any combinations which aren't checked.
            if len(combination) < lengths[0]:
                continue

            found.extend(check_func(hashes, combination))
            
    return found

def simple_check_function(hashes, combination):
    attempt_hash = sha256(combination.encode("utf-8")).hexdigest()
    return [(h, combination) for h in hashes if h == attempt_hash]

def salted_check_function(hashes, combination):
    found = []
    for hash, salt in hashes:
        attempt_hash = sha256(combination.encode("utf-8") + salt.encode("utf-8")).hexdigest()
        if hash == attempt_hash:
            found.append((hash, combination))

    return found

def mutation_check_function(hashes, combination):
    found = []
    for hash, salt in hashes:
        attempt_hash = sha256(combination.encode("utf-8") + salt.encode("utf-8")).hexdigest()
        if hash == attempt_hash:
            found.append((hash, combination))

    return found

def level_1(csv):
    characters = [str(c) for c in range(10)]
    hashes = [row[1] for row in csv[1:]]
    matches = simple_crack_hashes(
        hashes=hashes, 
        characters=characters, 
        lengths=(4, 4),
        check_func=simple_check_function 
    )
    
    for row in csv[1:]:
        match = next(iter([m[1] for m in matches if m[0] == row[1]]), None)
        print(f"{row[0]}, {match}")
        
def level_2(csv):
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

def level_3(csv):
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

def level_4(csv):
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

def level_5(csv):
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

solve_level(level, lines)