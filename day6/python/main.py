def read_data(filename='../input.txt'):
    grid = [list(line.strip()) for line in open(filename)]
    return (
        (len(grid), len(grid[0])),  # dimensions
        {(i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == '#'},  # obstacles
        next((i, j) for i, row in enumerate(grid) for j, c in enumerate(row) if c == '^')  # guard
    )

ROTATE = {(0, 1): (1, 0), (-1, 0): (0, 1), (0, -1): (-1, 0), (1, 0): (0, -1)}

# get path is common to both parts, move to a separate part
def get_path(dims, obstacles, pos, move):
    path, states = [], set()
    while True:
        state = (pos, move)
        if state in states:
            return path, path.index(state)
        states.add(state)
        path.append(state)
        
        next_pos = (pos[0] + move[0], pos[1] + move[1])
        if not (0 <= next_pos[0] < dims[0] and 0 <= next_pos[1] < dims[1]):
            return path, -1
            
        if next_pos in obstacles:
            move = ROTATE[move]
            continue
        pos = next_pos

def solve(dims, obstacles, guard):
    
    # Part 1 - just get the number of visited positions i.e. positions in path
    path, _ = get_path(dims, obstacles, guard, (-1, 0))
    p1 = len({pos for pos, _ in path})
    
    # Check visited (except guard initial position) if there is a path to guard
    visited = {pos for pos, _ in path} - obstacles - {guard}
    p2 = sum(1 for pos in visited if get_path(dims, obstacles | {pos}, guard, (-1, 0))[1] != -1)
    
    return p1, p2

if __name__ == '__main__':

    dims, obstacles, guard = read_data()
    # 11s !!
    p1, p2 = solve(dims, obstacles, guard)
    # 
    print('PART 1 - SOLUTION :', p1)
    #
    print('PART 2 - SOLUTION :', p2)
    #