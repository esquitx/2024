def read_input(filename="../input.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        data = []
        for line in lines:
            data.append(line)
            levels= [list(map(int, line.split())) for line in data]

        return levels
    
def is_monotonic(level):
    is_increasing = all(level[i] <= level[i+1] for i in range(len(level)-1))
    is_decreasing = all(level[i] >= level[i+1] for i in range(len(level)-1))
    return is_increasing or is_decreasing

def is_increase_valid(level):
    for i in range(len(level)-1):
        diff = abs(level[i] - level[i+1])
        if diff < 1 or diff > 3:
            return False
    return True

def check_shortened_level(level):
    for i in range(len(level)):
        reduced = level[:i] + level[i+1:] 
        if is_monotonic(reduced) and is_increase_valid(reduced):
            return True
    return False

def part1(levels):

    valid_count = 0
    for level in levels:
        if is_monotonic(level) and is_increase_valid(level):
            valid_count += 1

    print("PART 1")
    print("SOLUTION: ", valid_count)

def part2(levels):

    valid_count = 0
    for level in levels: 
        if is_monotonic(level) and is_increase_valid(level):
            valid_count += 1
        else: 
            if check_shortened_level(level):
                valid_count += 1
    
    print("PART 2")
    print("SOLUTION: ", valid_count)

if __name__ == "__main__":
    

    print("Advent of Code 2024 - Day 1\n")

    data = read_input()


    ##
    part1(data)
    ## 
    part2(data)