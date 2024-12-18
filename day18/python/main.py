from heapq import heappush, heappop
import math
from collections import deque

def read_data(filename='../input.txt'):

    with open(filename) as f:
        positions = [tuple(map(int, line.strip().split(','))) for line in f]

    return positions


# GRID_SIZE = 6
GRID_SIZE = 70

# SIZE = 12
SIZE = 1024

MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_path(start, goal, forbidden):
    queue = deque([(start, [start])])
    visited = {start}
    forbidden = set(forbidden)
    
    while queue:
        pos, path = queue.popleft()
        
        if pos == goal:
            return path
            
        for dx, dy in MOVES:
            next_pos = (pos[0] + dx, pos[1] + dy)
            
            if (next_pos not in visited and 
                next_pos not in forbidden and
                0 <= next_pos[0] <= GRID_SIZE and 
                0 <= next_pos[1] <= GRID_SIZE):
                
                visited.add(next_pos)
                queue.append((next_pos, path + [next_pos]))
    
    return None


def print_grid(forbidden, path):

    for j in range(GRID_SIZE):
        for i in range(GRID_SIZE):
            if (i, j) in forbidden:
                print('#', end='')
            elif (i, j) in path:
                print('O', end='')
            else:
                print('.', end='')
        print()

def part1(data):
    forbidden_positions = set(data[:SIZE])
    start = (0, 0)
    goal = (GRID_SIZE, GRID_SIZE)
    
    path = find_path(start, goal, forbidden_positions)

    if path:
        #print_grid(forbidden_positions, path)
        return len(path) - 1
    
    return -1

def part2(data):
    
    # ATTEMPT 1 : BRUTEFORCE
    test_for = 1
    while find_path((0, 0), (GRID_SIZE, GRID_SIZE), set(data[:test_for])):
        test_for += 1

    return data[test_for - 1]

    return 
if __name__ == '__main__':
    data = read_data('../input.txt')
    print(part1(data))
    print(part2(data))