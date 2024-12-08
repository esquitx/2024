def read_data(filename = '../input.txt') -> list:
    
    with open(filename, 'r') as f:
        data = f.readlines()
    
    antennas = {}
    matrix = [list(line.strip()) for line in data]
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char != '.':  # Ignore empty spaces
                antennas.setdefault(char, []).append((x, y))

    return antennas, (len(matrix[0]), len(matrix))

def find_antinodes(ant1, ant2):
    """Calculate positions where distance to ant1 is twice the distance to ant2 or vice versa."""
    antinodes = set()

    # positions
    x1, y1 = ant1
    x2, y2 = ant2
    
    # difference
    dx = x2 - x1
    dy = y2 - y1

    # has to be twice the distance from each antinode than to the antenna
    
    antinodes.add((x1 + 2*dx, y1 + 2*dy))
    antinodes.add((x2 - 2*dx, y2 - 2*dy))
    
    return antinodes

def find_antinodes_v2(ant1, ant2, bounds):
    """Find points that lie on straight lines between antenna pairs (horizontal, vertical, or diagonal)."""
    
    x1, y1 = ant1
    x2, y2 = ant2
    antinodes = set()

    # brute force all positions
    for x in range(bounds[0]):
        for y in range(bounds[1]):
            if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1):
                antinodes.add((x, y))

   
            
    return antinodes

def part1(data):

    antennas, bounds = data
    # Calculate antinodes for all pairs of same frequency
    antinodes = set() 
    for _, positions in antennas.items():
        for ant1 in positions:
            for ant2 in positions:
                if ant1 != ant2:
                    antinodes.update(find_antinodes(ant1, ant2))
    
    # Remove antinodes that are outside the bounds
    antinodes = set(node for node in antinodes if 0 <= node[0] < bounds[0] and 0 <= node[1] < bounds[1])
    # Calculate set of all antenna pos

    return len(antinodes)

def part2(data):
    antennas, bounds = data
    antinodes = set()
    
    for frequency, positions in antennas.items():
        for ant1 in positions: 
            for ant2 in positions:
                if ant1 != ant2:
                    antinodes.update(find_antinodes_v2(ant1, ant2, bounds))

    
    return len(antinodes)

if __name__ == '__main__':

    # data = read_data('../test.txt')
    data = read_data()
    # 
    print('PART 1 - SOLUTION :', part1(data))
    #
    #
    print('PART 2 - SOLUTION :', part2(data))
    #