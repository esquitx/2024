def read_data(filename='../input.txt'):
    with open(filename, 'r') as file:
        content = file.read()
    # Split content into map and moves
    map_text, moves_text = content.strip().split('\n\n')
    warehouse_map = map_text.split('\n')
    warehouse_map = [list(row) for row in warehouse_map]
    moves = moves_text.replace('\n', '')
    return warehouse_map, moves


MOVES = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

def move_robot(warehouse_map, move):
    robot = None
    # find robot position
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '@':
                robot = (i, j)
                break
    
    if not robot:
        return

    new_x, new_y = robot[0] + MOVES[move][0], robot[1] + MOVES[move][1]

    # Check if move is valid (not hitting a wall)
    if warehouse_map[new_x][new_y] == '#':
        return

    # If next position is empty, just move there
    if warehouse_map[new_x][new_y] == '.':
        warehouse_map[robot[0]][robot[1]] = '.'
        warehouse_map[new_x][new_y] = '@'
        return

    # If next position has a box, try to push the entire block
    if warehouse_map[new_x][new_y] == 'O':
        box_positions = []
        next_positions = []
        check_x, check_y = new_x, new_y
        
        # Find all connected boxes in the direction of movement
        while check_x < len(warehouse_map) and check_y < len(warehouse_map[0]) and warehouse_map[check_x][check_y] == 'O':
            box_positions.append((check_x, check_y))
            next_x = check_x + MOVES[move][0]
            next_y = check_y + MOVES[move][1]
            if next_x >= len(warehouse_map) or next_y >= len(warehouse_map[0]) or warehouse_map[next_x][next_y] == '#':
                return  # Can't push if we hit a wall
            next_positions.append((next_x, next_y))
            check_x = next_x
            check_y = next_y

        # Move all boxes one position
        for pos_x, pos_y in box_positions:
            warehouse_map[pos_x][pos_y] = '.'
            
        for next_x, next_y in next_positions:
            warehouse_map[next_x][next_y] = 'O'
        
        # Move robot
        warehouse_map[robot[0]][robot[1]] = '.'
        warehouse_map[new_x][new_y] = '@'

def move_robot_wide(warehouse_map, move):
    # Find robot position
    robot = None
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '@':
                robot = (i, j)
                break
    
    if not robot:
        return

    new_x, new_y = robot[0] + MOVES[move][0], robot[1] + MOVES[move][1]

    # Check if move is valid
    if new_x >= len(warehouse_map) or new_y >= len(warehouse_map[0]) or warehouse_map[new_x][new_y] == '#':
        return

    # If next position is empty, just move there
    if warehouse_map[new_x][new_y] == '.':
        warehouse_map[robot[0]][robot[1]] = '.'
        warehouse_map[new_x][new_y] = '@'
        return

    # If next position has a box part
    if warehouse_map[new_x][new_y] in ['[', ']']:
        # For horizontal moves
        if move in ['<', '>']:
            # Collect all contiguous wide boxes in the row before attempting to move
            forward = 1 if move == '>' else -1
            row = warehouse_map[new_x]
            # Find all segments of wide boxes
            segments = []
            checked = set()
            idx = new_y
            while 0 <= idx < len(row):
                if idx in checked or row[idx] not in ['[', ']']:
                    idx += 1
                    continue
                start = idx
                while start > 0 and row[start - 1] == '[':
                    start -= 1
                end = idx
                while end < len(row) - 1 and row[end + 1] == ']':
                    end += 1
                segments.append((start, end))
                checked.update(range(start, end + 1))
                idx = end + 1
            
            # Check space for entire segment set
            boundary = segments[-1][1] if move == '>' else segments[0][0]
            if boundary + forward < 0 or boundary + forward >= len(row) or row[boundary + forward] == '#':
                return
            
            # Move boxes in reverse order if moving right, forward if left
            if move == '>':
                for (s, e) in reversed(segments):
                    row[e + 1] = ']'
                    row[s] = '.'
            else:
                for (s, e) in segments:
                    row[s - 1] = '['
                    row[e] = '.'
        else:
            # Handle vertical moves for wide boxes
            next_x = new_x + MOVES[move][0]
            if next_x < 0 or next_x >= len(warehouse_map):
                return

            # Find all boxes in the column that need to move
            if warehouse_map[new_x][new_y] == '[':
                if not (warehouse_map[next_x][new_y] == '.' and warehouse_map[next_x][new_y+1] == '.'):
                    return
                warehouse_map[next_x][new_y] = '['
                warehouse_map[next_x][new_y+1] = ']'
                warehouse_map[new_x][new_y] = '.'
                warehouse_map[new_x][new_y+1] = '.'
            else:  # ']'
                if not (warehouse_map[next_x][new_y] == '.' and warehouse_map[next_x][new_y-1] == '.'):
                    return
                warehouse_map[next_x][new_y] = ']'
                warehouse_map[next_x][new_y-1] = '['
                warehouse_map[new_x][new_y] = '.'
                warehouse_map[new_x][new_y-1] = '.'

        # Move robot
        warehouse_map[robot[0]][robot[1]] = '.'
        warehouse_map[new_x][new_y] = '@'

def part1(data):

    warehouse_map, moves = data
 
    for move in moves: 
        move_robot(warehouse_map, move)

    # find boxes positions
    boxes = []
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == 'O':
                boxes.append((i, j))
    
    return sum([100*x + y for x, y in boxes])

def part2(data):
    
    from collections import defaultdict
    warehouse_map, directions = data

    # Transform map to make boxes double width
    m = len(warehouse_map)
    n = len(warehouse_map[0])
    grid = [['.']*(2*n) for _ in range(m)]
    
    # Initialize the grid
    robot = None
    for i in range(m):
        for j in range(n):
            if warehouse_map[i][j] == '#':
                grid[i][2*j] = grid[i][2*j+1] = '#'
            elif warehouse_map[i][j] == 'O':
                grid[i][2*j] = '['
                grid[i][2*j+1] = ']'
            elif warehouse_map[i][j] == '@':
                grid[i][2*j] = '@'
                robot = (i, 2*j)

    for d in directions[:]:
        i, j = robot
        
        if d == '<':
            k = j-1
            while grid[i][k] == ']':
                k -= 2
            if grid[i][k] == '.':
                for l in range(k, j):
                    grid[i][l] = grid[i][l+1]
                robot = (i, j-1)

        elif d == '>':
            k = j+1
            while grid[i][k] == '[':
                k += 2
            if grid[i][k] == '.':
                for l in reversed(range(j+1, k+1)):
                    grid[i][l] = grid[i][l-1]
                robot = (i, j+1)

        elif d == '^':
            queue = {(i-1, j)}
            rows = defaultdict(set)
            while queue:
                x, y = queue.pop()
                match grid[x][y]:
                    case '#':
                        break
                    case ']':
                        rows[x] |= {y-1, y}
                        queue |= {(x-1, y), (x-1, y-1)}
                    case '[':
                        rows[x] |= {y, y+1}
                        queue |= {(x-1, y), (x-1, y+1)}
                    case '.':
                        rows[x].add(y)
            else:
                for x in sorted(rows):
                    for y in rows[x]:
                        grid[x][y] = grid[x+1][y] if y in rows[x+1] else '.'
                robot = (i-1, j)

        elif d== 'v':
            queue = {(i+1, j)}
            rows = defaultdict(set)
            while queue:
                x, y = queue.pop()
                match grid[x][y]:
                    case '#':
                        break
                    case ']':
                        rows[x] |= {y-1, y}
                        queue |= {(x+1, y), (x+1, y-1)}
                    case '[':
                        rows[x] |= {y, y+1}
                        queue |= {(x+1, y), (x+1, y+1)}
                    case '.':
                        rows[x].add(y)
            else:
                for x in sorted(rows, reverse=True):
                    for y in rows[x]:
                        grid[x][y] = grid[x-1][y] if y in rows[x-1] else '.'
                robot = (i+1, j)

    total = 0
    for i in range(m):
        for j in range(n*2):
            if grid[i][j] == '[':
                total += 100*i + j

    return total

if __name__ == '__main__':
    data = read_data('../test3.txt')
    print('PART 1- SOLUTION: ', part1(data))
    data = read_data('../input.txt')
    print('PART 2- SOLUTION: ', part2(data))