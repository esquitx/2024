def read_data(filename='../input.txt'):
    with open(filename , 'r') as f:
        return f.read().split(' ')




def blink(stone):
    if stone == '0':
        return ['1']

    elif len(stone) % 2 == 0:
        mid = len(stone) // 2
        return [str(int(stone[0:mid])), str(int(stone[mid:]))]
    
    else: 
        return [str(int(stone)*2024)]
    

def part1(data):
    for _ in range(25):
        data = [blink(stone) for stone in data]
        data = [item for sublist in data for item in sublist]
    return len(data)


def part2(data):

    # Same as part1, but have to get clever with the tracking of the counts
    # !! WE ONLY WANT THE NUMBER OF STONES !!
    # i.e. the positions are irrelevant, so we have to keep track of the counts

    # IDEA : keep track only of the three types of stones?
    # PROBLEM : in other, we need to know the value of the stone to know which type it is

    stone_counts = {}
    for stone in data:
        stone_counts[stone] = stone_counts.get(stone, 0) + 1
    
    for _ in range(75):
        new_counts = {}
        for stone, count in stone_counts.items():
            if stone == '0':
                new_counts['1'] = new_counts.get('1', 0) + count
            elif len(stone) % 2 == 0:
                mid = len(stone) // 2
                left = str(int(stone[0:mid]))
                right = str(int(stone[mid:]))
                new_counts[left] = new_counts.get(left, 0) + count
                new_counts[right] = new_counts.get(right, 0) + count
            else:
                new_val = str(int(stone) * 2024)
                new_counts[new_val] = new_counts.get(new_val, 0) + count
        
        stone_counts = new_counts
    
    return sum(stone_counts.values())


if __name__ == '__main__':
    
    
    data = read_data()

    print('PART 1 - SOLUTION: ', part1(data))
    print('PART 2 - SOLUTION: ', part2(data))