from collections import deque

def read_data(filename='../input.txt'):
    with open(filename) as f:
        return [list(line.strip()) for line in f.read().splitlines()]


def print_data(data):
    for line in data:
        print(''.join(line))


MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def part1(data):

    # find start and end
    start = end = None
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'S':
                start = (i, j)
            elif data[i][j] == 'E':
                end = (i, j)
            if start and end:
                break
        if start and end:
            break

    # BFS - again
    queue = deque([(start, 0)])
    visited = {start}
    path_distances = {start: 0}
    
    while queue:
        pos, steps = queue.popleft()
        if pos == end:
            break

        for dx, dy in MOVES:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < len(data) and 
                0 <= new_y < len(data[0]) and 
                (new_x, new_y) not in visited and
                data[new_x][new_y] != '#'):
                
                queue.append(((new_x, new_y), steps + 1))
                visited.add((new_x, new_y))
                path_distances[(new_x, new_y)] = steps + 1

    jumps = 0
    for pos in path_distances:
        i, j = pos
        current_dist = path_distances[pos]
        
        # Check possible jumps
        for move1 in MOVES + [(0, 0)]: # add (0, 0) to simulate only using one cheat second
            for move2 in MOVES:
                jump_x, jump_y = i + move1[0] + move2[0], j + move1[1] + move2[1]
                jump_pos = (jump_x, jump_y)
                
                if (jump_pos in path_distances and 
                    path_distances[jump_pos] - current_dist > 100): # add only if savings bigger than 100. wtf??
                    jumps += 1

    return jumps

def part2(data):
    # find start and end
    start = end = None
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'S':
                start = (i, j)
            elif data[i][j] == 'E':
                end = (i, j)
            if start and end:
                break
        if start and end:
            break

    # BFS for normal path distances
    queue = deque([(start, 0)])
    visited = {start}
    path_distances = {start: 0}
    
    while queue:
        pos, steps = queue.popleft()
        if pos == end:
            break

        for dx, dy in MOVES:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if (0 <= new_x < len(data) and 
                0 <= new_y < len(data[0]) and 
                (new_x, new_y) not in visited and
                data[new_x][new_y] != '#'):
                queue.append(((new_x, new_y), steps + 1))
                visited.add((new_x, new_y))
                path_distances[(new_x, new_y)] = steps + 1

    jumps = 0
    for pos in path_distances:
        i, j = pos
        current_dist = path_distances[pos]
        
        # Check possible jumps
        for move1 in MOVES + [(0, 0)]:  
            for move2 in MOVES:
                jump_x, jump_y = i + move1[0] + move2[0], j + move1[1] + move2[1]
                jump_pos = (jump_x, jump_y)
                
                if (0 <= jump_x < len(data) and 
                    0 <= jump_y < len(data[0]) and 
                    jump_pos in path_distances and
                    data[jump_x][jump_y] != '#'):
                    
                    if path_distances[jump_pos] - current_dist >= 20:  # change 100 to 20
                        jumps += 1

    return jumps


if __name__ == '__main__':
    
    data = read_data('../input.txt')
    
    #
    print(part1(data))
    print(part2(data))