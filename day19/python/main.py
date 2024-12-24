'''
Solution for Day 19
'''

def read_data(filename='../input.txt'):
    with open(filename) as f:
        lines = f.readlines();
        available = [x.strip() for x in lines[0].split(',')]
        sequences = [line.strip() for line in lines[2:]]

        return available, sequences

def can_make_sequence(target, available, used=None):
    if used is None:
        used = set()
    
    # If target is empty, we found a valid combination
    if not target:
        return True
    
    # Try each available value
    for i, val in enumerate(available):
        if i not in used and target.startswith(val):
            # Use this value and try to make the rest of the sequence
            used.add(i)
            if can_make_sequence(target[len(val):], available, used):
                return True
            used.remove(i)
    
    return False

def part1(data):
    available, sequences = data
    count = 0
    for seq in sequences:
        if can_make_sequence(seq, available):
            count += 1
    return count

if __name__ == '__main__':

    data = read_data('../test.txt')

    print(data)
    print(part1(data))
    # print(part2(data))