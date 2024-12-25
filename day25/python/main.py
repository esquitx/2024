def find_heights(block, type):

    width = len(block[0])
    height = len(block)
    heights = []
    
    for col in range(width):
        found = False
        if type == 'K':  
            for row in range(height-1, -1, -1):
                if block[row][col] == '.':
                    heights.append(height - 1 - row -1)
                    found = True
                    break
            if not found:
                heights.append(0)
        else:  # lock (find first '#' from top)
            for row in range(height):
                if block[row][col] == '.':
                    heights.append(row-1)
                    found = True
                    break
            if not found:
                heights.append(0)
    return heights

def read_data(filename='../input.txt'):
    with open(filename) as f:
        raw_blocks = f.read().strip().split('\n\n')

    blocks = [block.split('\n') for block in raw_blocks]
    keys = []
    locks = []

    for block in blocks:
        height = len(block)  # Get height of block
        if all(char == '.' for char in block[0]):
            heights = find_heights(block, 'K')  # key
            keys.append((heights, height))
        else:
            heights = find_heights(block, 'L')  # lock
            locks.append((heights, height))
    
    return keys, locks

def part1(data):
    keys, locks = data
    total = 0
    
    for key, key_height in keys:
        for lock, lock_height in locks:
            if key_height != lock_height:
                continue
            
            
            # Check if heights sum to block height - 1 at each position
          
            if all(k + l < key_height - 1  for k, l in zip(key, lock)):
              
                total += 1
    
    return total

def part2(data):
    pass

if __name__ == '__main__':
    data = read_data('../input.txt')
    print(part1(data))
    print(part2(data))