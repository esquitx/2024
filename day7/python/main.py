def read_data(filename='../input.txt'):
    data = []
    with open(filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            sides = line.strip().split(':')
            data.append((int(sides[0]), [int(x) for x in sides[1].strip().split()]))

    return data


def test_line_v1(target, bullets, index=1, current_value=None):
    
    if current_value is None:
        current_value = bullets[0]
        
    if index >= len(bullets):
        return current_value == target
    
    # Try addition path
    if test_line_v1(target, bullets, index + 1, current_value + bullets[index]):
        return True
        
    # Try multiplication path
    if test_line_v1(target, bullets, index + 1, current_value * bullets[index]):
        return True
        
    return False

def test_line_v2(target, bullets, index=1, current_value=None):
    
    if current_value is None:
        current_value = bullets[0]
        
    if index >= len(bullets):
        return current_value == target
    
    # Try addition path
    if test_line_v2(target, bullets, index + 1, current_value + bullets[index]):
        return True
        
    # Try multiplication path
    if test_line_v2(target, bullets, index + 1, current_value * bullets[index]):
        return True

    # concat values - convert to string concatenation then back to int
    concat_value = int(str(current_value) + str(bullets[index]))
    if test_line_v2(target, bullets, index + 1, concat_value):
        return True
 
    return False

def part1(data):
    return sum(target for target, bullets in data if test_line_v1(target, bullets))


def part2(data):
    return sum(target for target, bullets in data if test_line_v2(target, bullets))

if __name__ == '__main__':
    tests = read_data()
   
    print("PART 1 - SOLUTION :", part1(tests))
    print("PART 2 - SOLUTION :", part2(tests))