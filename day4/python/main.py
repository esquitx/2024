'''
Q : how many times does XMAS appear???
!! not to find location
'''

def read_data(filename = '../input.txt') -> list:
    with open(filename, 'r') as f:
        data = f.readlines()

    return [list(line.strip()) for line in data]

def is_valid_position(data, x, y):
    return 0 <= x < len(data) and 0 <= y < len(data[0])

def part1(data):
    WORD = 'XMAS'
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    
    found = set() # avoid duplicates
    count = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'X':
                for move in MOVES:
                    x, y = i, j
                    positions = [(x, y)]
                    
                    for letter_idx in range(1, len(WORD)):
                        x, y = x + move[0], y + move[1]
                        if not is_valid_position(data, x, y) or data[x][y] != WORD[letter_idx]:
                            break
                        positions.append((x, y))
                    else:  
                        # if not tracked already, add
                        if tuple(positions) not in found:
                            found.add(tuple(positions))
                            count += 1
    return count

def part2(data):
    count = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if not is_valid_position(data, i, j) or data[i][j] != 'A':
                continue
                
            #
            # !! X pattern can appear rotated
            patterns = [
                # Original
                [(i-1, j-1, 'M'), (i+1, j-1, 'M'), (i-1, j+1, 'S'), (i+1, j+1, 'S')],
                # Rotated 90°
                [(i-1, j-1, 'M'), (i-1, j+1, 'M'), (i+1, j-1, 'S'), (i+1, j+1, 'S')],
                # Rotated 180°
                [(i-1, j-1, 'S'), (i+1, j-1, 'S'), (i-1, j+1, 'M'), (i+1, j+1, 'M')],
                # Rotated 270°
                [(i-1, j-1, 'S'), (i-1, j+1, 'S'), (i+1, j-1, 'M'), (i+1, j+1, 'M')]
            ]
            
            # Check each possible pattern
            for pattern in patterns:
                valid = True
                for x, y, char in pattern:
                    if not is_valid_position(data, x, y) or data[x][y] != char:
                        valid = False
                        break
                if valid:
                    count += 1
                    
    return count

if __name__ == '__main__':
    data = read_data('../input.txt')
    
    # print('X', data.count('X'))
    # print('M', data.count('M'))
    # print('A', data.count('A'))
    # print('S', data.count('S'))

    print('PART 1: ', part1(data))
    print('PART 2: ', part2(data))
