def read_data(filename='../input.txt'):
    with open(filename, 'r') as f:
        numbers = f.readline().strip()
    
    encoded = []
    for i, number in enumerate(numbers):
        if i % 2 == 0:
            encoded.extend([str(i // 2)] * int(number))
        else: 
            encoded.extend(['.'] * int(number))

    return encoded


def part1(data):
    
    j = 0
    for i in range(len(data) -1, -1, -1):
        while j < i:
            if data[j] == '.':
                data[j], data[i] = data[i], data[j]
                # print(''.join(data))
                break
            j += 1

    return sum(int(number) * i for i, number in enumerate(data) if number != '.')


def part2(data):

    i = len(data) - 1
    j = 0
    while i > j:

        # If we find a dot, continue
        if (data[i] == '.'):
            i -= 1 
            continue 
        
        # Decide block size
        block_size = 0
        while data[i-block_size] == data[i]:
            block_size += 1
        
        while j < i - block_size:

            free_space = 0
            while data[j+free_space] == '.':
                free_space += 1

            # if enough space, swap
            if free_space >= block_size:
                data[j:j+block_size] = data[i-block_size+1:i+1]
                data[i-block_size+1:i+1] = ['.'] * block_size
                #print(''.join(data))
                break
            else: 
                j += max(1, free_space)
        
        j = 0
        i -= block_size
    return sum(int(number) * i for i, number in enumerate(data) if number != '.')
    

if __name__ == '__main__':
    
    #
    data = read_data('../input.txt')
    #print(data)
    #
    print('PART 1 - SOLUTION: ', part1(data))
    data = read_data('../input.txt')

    #
    print('PART 2 - SOLUTION: ', part2(data))