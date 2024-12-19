'''
Solution for Day 19
'''

def read_data(filename='../input.txt'):
    with open(filename) as f:
        lines = f.readlines();
        available = [x.strip() for x in lines[0].split(',')]
        sequences = [line.strip() for line in lines[2:]]

        return available, sequences

def can_make_sequence(target, available):

    # dp approach - thank you KTH!

    n = len(target)
    can_build = [False] * (n + 1)
    can_build[0] = True # can always build empty string


    for i in range(1, n+1):
        for sequence in available:
            if len(sequence) <= i:
                if target[i-len(sequence):i] == sequence and can_build[i-len(sequence)]:
                    can_build[i] = True
                    break

    return can_build[n]

def num_ways_to_build_sequence(target, available):
    
    n = len(target)
    num_ways = [0] * (n + 1)
    num_ways[0] = 1 # can always build empty string

    for i in range(1, n+1):
        for sequence in available:
            if len(sequence) <= i:
                if target[i-len(sequence):i] == sequence:
                    num_ways[i] += num_ways[i-len(sequence)]

    return num_ways[n]

def part1(data):
    available, sequences = data
    return sum(1 for seq in sequences if can_make_sequence(seq, available))


def part2(data):
    available, sequences = data 
    return sum(num_ways_to_build_sequence(seq, available) for seq in sequences)

if __name__ == '__main__':

    data = read_data('../input.txt')

    # print(data)
    print(part1(data))
    print(part2(data))