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
            # Find the complete box (both [ and ])
            box_start = new_y
            if warehouse_map[new_x][new_y] == ']':
                box_start = new_y - 1
            
            # Find all connected boxes in pairs
            boxes = []
            visited = set()
            check_y = box_start
            
            while check_y < len(warehouse_map[0]) - 1 and check_y not in visited:
                visited.add(check_y)
                if (warehouse_map[new_x][check_y] == '[' and 
                    check_y + 1 < len(warehouse_map[0]) and 
                    warehouse_map[new_x][check_y + 1] == ']'):
                    
                    boxes.extend([(new_x, check_y), (new_x, check_y + 1)])
                    
                    # Check if there's another box right after
                    next_check = check_y + 2
                    if (next_check < len(warehouse_map[0]) and 
                        warehouse_map[new_x][next_check] == '['):
                        check_y = next_check
                    else:
                        break
                else:
                    break

            if not boxes:
                return

            # Check if we can move all boxes
            for _, box_y in boxes:
                next_y = box_y + MOVES[move][1]
                if next_y >= len(warehouse_map[0]) or next_y < 0 or warehouse_map[new_x][next_y] == '#':
                    return
                if warehouse_map[new_x][next_y] in ['[', ']'] and (new_x, next_y) not in boxes:
                    return

            # Move all boxes in pairs
            box_pairs = [(boxes[i], boxes[i+1]) for i in range(0, len(boxes), 2)]
            if move == '>':
                box_pairs.reverse()
            
            for (box1_x, box1_y), (box2_x, box2_y) in box_pairs:
                next_y1 = box1_y + MOVES[move][1]
                next_y2 = box2_y + MOVES[move][1]
                warehouse_map[box1_x][box1_y] = '.'
                warehouse_map[box2_x][box2_y] = '.'
                warehouse_map[box1_x][next_y1] = '['
                warehouse_map[box2_x][next_y2] = ']'

        # For vertical moves
        else:
            boxes = []
            if warehouse_map[new_x][new_y] == '[' and new_y + 1 < len(warehouse_map[0]):
                if warehouse_map[new_x][new_y + 1] == ']':
                    boxes = [(new_x, new_y), (new_x, new_y + 1)]
            elif warehouse_map[new_x][new_y] == ']' and new_y > 0:
                if warehouse_map[new_x][new_y - 1] == '[':
                    boxes = [(new_x, new_y - 1), (new_x, new_y)]

            if not boxes:
                return

            # Check if we can move both parts of the box
            next_x = new_x + MOVES[move][0]
            if next_x >= len(warehouse_map) or next_x < 0:
                return
            
            for box_x, box_y in boxes:
                if warehouse_map[next_x][box_y] == '#':
                    return
                if warehouse_map[next_x][box_y] in ['[', ']']:
                    # Check if the next box can be pushed
                    next_next_x = next_x + MOVES[move][0]
                    if (next_next_x >= len(warehouse_map) or next_next_x < 0 or
                        warehouse_map[next_next_x][box_y] == '#' or
                        warehouse_map[next_next_x][box_y] in ['[', ']']):
                        return

            # Move the box
            for box_x, box_y in boxes:
                warehouse_map[box_x][box_y] = '.'
                warehouse_map[next_x][box_y] = '[' if box_y % 2 == 0 else ']'

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
    warehouse_map, moves = data

    # Transform the map to make # and O double in width
    fat_map = [['']*2*len(warehouse_map[0]) for _ in range(len(warehouse_map))]
    for i, row in enumerate(warehouse_map):
        for j, cell in enumerate(row):
            if cell == '#':
                fat_map[i][2*j] = '#'
                fat_map[i][2*j+1] = '#'
            elif cell == 'O':
                fat_map[i][2*j] = '['
                fat_map[i][2*j+1] = ']'
            elif cell == '@':
                fat_map[i][2*j] = '@'
                fat_map[i][2*j+1] = '.'
            else: 
                fat_map[i][2*j] = '.'
                fat_map[i][2*j+1] = '.'

    # Execute moves with wide boxes
    for move in moves:
        move_robot_wide(fat_map, move)
        print('After move', move)
        print('\n'.join([''.join(row) for row in fat_map]))
        print()

    print('\n'.join([''.join(row) for row in fat_map]))
    # Calculate GPS coordinates for wide boxes
    total = 0
    for i, row in enumerate(fat_map):
        for j, cell in enumerate(row):
            if cell == '[' or cell == ']':  # Only count left edge of boxes
                total += i+ 100*j    
    return total

if __name__ == '__main__':
    data = read_data('../test3.txt')
    print('PART 1- SOLUTION: ', part1(data))
    data = read_data('../test3.txt')
    print('PART 2- SOLUTION: ', part2(data))