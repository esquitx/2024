from heapq import heappush, heappop

def read_data(filename='../input.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [list(line.strip()) for line in lines]


# MOVE ONLY FORWARD - COST 1
# ROTATE CLOCKWISE OR COUNTERCLOCKWISE - COST 1000
ROTATIONS = {
    (0, 1) : [(1, 0), (-1, 0)],
    (1, 0) : [(0, -1), (0, 1)],
    (0, -1) : [(1, 0), (-1, 0)],
    (-1, 0) : [(0, -1), (0, 1)]
}
MOVE = (0, 1)
ROTATE_L = ROTATIONS[MOVE][0]
ROTATE_R = ROTATIONS[MOVE][1]
#

def part1(data):
    # find S and E positions
    start = end = None
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'S':
                start = (i, j)
            elif data[i][j] == 'E':
                end = (i, j)

            # break if both are found
            if start and end:
                break
    
    # priority queue: (cost, position, direction)
    queue = [(0, start, MOVE)]
    # visited: (position, direction)
    visited = set()
    
    while queue:

        # we check for minimum cost first
        cost, pos, direction = heappop(queue)
        
        # if reached the end, return min cost
        if pos == end:
            return cost
            
        state = (pos, direction)
        if state in visited:
            continue
        visited.add(state)
        
        # move forward
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if (0 <= new_pos[0] < len(data) and 
            0 <= new_pos[1] < len(data[0]) and 
            data[new_pos[0]][new_pos[1]] != '#'):
            heappush(queue, (cost + 1, new_pos, direction))
        
        # rotate left + rotate right
        for new_dir in ROTATIONS[direction]:
            new_pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
            if (0 <= new_pos[0] < len(data) and 
                0 <= new_pos[1] < len(data[0]) and 
                data[new_pos[0]][new_pos[1]] != '#'):
                heappush(queue, (cost + 1001, new_pos, new_dir))
    
    return -1

# have to fucking redo this shit for part 2
def find_optimal_paths(data, start, end):
    queue = [(0, start, MOVE, [(start, MOVE)])]
    visited = {}  # (pos, dir) -> cost
    all_end_paths = []  # store ALL paths that reach the end
    
    while queue:
        cost, pos, direction, path = heappop(queue)
        
        state = (pos, direction)
        if state in visited and visited[state] < cost:
            continue
        visited[state] = cost
        
        if pos == end:
            all_end_paths.append((cost, path))
            continue
            
        for next_dir in [direction] + ROTATIONS[direction]:
            new_pos = (pos[0] + next_dir[0], pos[1] + next_dir[1])
            if (0 <= new_pos[0] < len(data) and 
                0 <= new_pos[1] < len(data[0]) and 
                data[new_pos[0]][new_pos[1]] != '#'):
                new_cost = cost + (1 if next_dir == direction else 1001)
                new_path = path + [(new_pos, next_dir)]
                heappush(queue, (new_cost, new_pos, next_dir, new_path))
    
    # Find minimum cost from all paths
    min_cost = min(cost for cost, _ in all_end_paths) if all_end_paths else float('inf')
    
    
    optimal_positions = set()
    for cost, path in all_end_paths:
        if cost == min_cost:
            for pos, _ in path:
                optimal_positions.add(pos)
    
    return min_cost, optimal_positions

# helper function to visualize
def print_path(data, positions):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if (i,j) in positions and data[i][j] != 'S' and data[i][j] != 'E':
                print('O', end='')
            else:
                print(data[i][j], end='')
        print()

def part2(data):
    # find S and E positions
    start = end = None
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'S':
                start = (i, j)
            elif data[i][j] == 'E':
                end = (i, j)
            if start and end:
                break
    
    min_cost, positions = find_optimal_paths(data, start, end)
    
    print("\nOptimal path visualization:")
    print_path(data, positions)
    print()
    
    return len(positions) if min_cost != float('inf') else 0

if __name__ == '__main__':

    # Part 1
    data = read_data('../input.txt')

    print(part1(data))
    
    # Part 2
    print(part2(data))