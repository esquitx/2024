import os

WIDTH = 101
HEIGHT = 103

def read_data(filename='../input.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()

    robots = []
    for line in lines: 
        pos, v = line.strip().split(' ')
        
        # Remove 'p=' and 'v=' prefixes and split by comma
        x, y = map(int, pos[2:].split(','))
        vx, vy = map(int, v[2:].split(','))

        robots.append({
            'pos': (x, y),
            'v': (vx, vy)
        })
    
    return robots

def get_quadrant(pos):

    x, y = pos
    mid_x = WIDTH // 2
    mid_y = HEIGHT // 2

    if x == mid_x or y == mid_y:
        return 0
    if x < mid_x:
        return 1 if y < mid_y else 3
    else:
        return 2 if y < mid_y else 4

 
def calculate_safety_score(robots):
    quadrant_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        quadrant = get_quadrant(robot['pos'])
        quadrant_counts[quadrant] += 1
    return quadrant_counts[1] * quadrant_counts[2] * quadrant_counts[3] * quadrant_counts[4]

def part1(data):
    for _ in range(100):
        for robot in data:
            x, y = robot['pos']
            vx, vy = robot['v']
            robot['pos'] = ((x + vx) % WIDTH, (y + vy) % HEIGHT)

    return calculate_safety_score(data)

def save_grid_to_file(robots, iteration, output_dir='output'):

    os.makedirs(output_dir, exist_ok=True)
    
    # grid representation according to example
    grid = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for robot in robots:
        x, y = robot['pos']
        if grid[y][x] == '.':
            grid[y][x] = '1'
        else: 
            grid[y][x] = str(int(grid[y][x]) + 1)
    
    # save file
    with open(f'{output_dir}/{iteration:03d}.txt', 'w') as f:
        f.write('-' * (WIDTH + 2) + '\n')
        for row in grid:
            f.write('|' + ''.join(row) + '|\n')
        f.write('-' * (WIDTH + 2) + '\n')

def has_overlaps(robots):
    positions = set()
    for robot in robots:
        pos = robot['pos']
        if pos in positions:
            return True
        positions.add(pos)
    return False

def part2(data):
    # IDEA 4 - the developers probably worked from the christmas tree, simulated all possible configurations
    # gave everyone a different starting point (hinted by wrong solution saying it was someone elses solution)
    # So we try to find that unique position in which all guards are in a different position

    # f there is only one, we are probably right. Otherwise, on to IDEA 5 :/

    for i in range(WIDTH*HEIGHT):
        for robot in data:
            x, y = robot['pos']
            vx, vy = robot['v']
            robot['pos'] = ((x + vx) % WIDTH, (y + vy) % HEIGHT)
        
        if not has_overlaps(data):
            save_grid_to_file(data, i+1)
            return f"Unique iteration found at {i+1}"
    
    return "FAILURE - All configurations have overlaps you midwit"

if __name__ == '__main__':
    data = read_data('../input.txt')
    print('PART 1 - SOLUTION' , part1(data))
    # since we iterate over all positions, no need to update data to initial state
    print('PART 1 - SOLUTION', part2(data))