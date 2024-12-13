COST_A = 3
COST_B = 1

def read_data(filename='../input.txt'):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    cases = []
    for case in range(0, len(lines), 4):
        case_data = lines[case:case+3]  # Only need 3 lines per case
        
        button_a = case_data[0].strip().split(': ')[1].split(',')
        button_b = case_data[1].strip().split(': ')[1].split(',')
        prize = case_data[2].strip().split(': ')[1].split(',')
        
        cases.append({
            'button_a': {
                'x': int(button_a[0][2:]),
                'y': int(button_a[1][3:])
            },
            'button_b': {
                'x': int(button_b[0][2:]),
                'y': int(button_b[1][3:])
            },
            'prize': {
                'x': int(prize[0][2:]),
                'y': int(prize[1][3:])
            }
        })
    
    return cases

# GCD + BEZOUT

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def bezout(a, b):
    if b == 0:
        return a, 1, 0
    
    d, x1, y1 = bezout(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return d, x, y

def bezout_2d(vec_a, vec_b, target):
    """
    Solve for system of equations:
    a*vec_a[0] + b*vec_b[0] = target[0]
    a*vec_a[1] + b*vec_b[1] = target[1]
    """

    # Check determinant to see if system has a solution
    det = vec_a[0]*vec_b[1] - vec_a[1]*vec_b[0]
    if det == 0:
        return None
    
    # SOLVE system of equation using CRAMER
    a = (target[0]*vec_b[1] - target[1]*vec_b[0]) / det
    b = (vec_a[0]*target[1] - vec_a[1]*target[0]) / det
    
    # Check if solution is integer
    if not (a.is_integer() and b.is_integer()):
        return None
    
    a, b = int(a), int(b)
    
    # Check if solution is non-negative
    if a < 0 or b < 0:
        return None
        
    return (a, b)

def part1(data):
    total_cost = 0
    
    for _, case in enumerate(data):
        # print(f"\nCase {i + 1}:")
        vec_a = (case['button_a']['x'], case['button_a']['y'])
        vec_b = (case['button_b']['x'], case['button_b']['y'])
        target = (case['prize']['x'], case['prize']['y'])
        
        # print(f"Target: {target}")
        # print(f"Button A vector: {vec_a}")
        # print(f"Button B vector: {vec_b}")
        
        solution = bezout_2d(vec_a, vec_b, target)
        
        if solution is None:
            #print("No solution exists")
            # SKIP if no solution, not added to cost
            continue
            
        moves_a, moves_b = solution
        cost = COST_A * moves_a + COST_B * moves_b
        # print(f"Solution: {moves_a} moves of A, {moves_b} moves of B")
        # print(f"Verification: ({moves_a}*{vec_a[0]} + {moves_b}*{vec_b[0]}, {moves_a}*{vec_a[1]} + {moves_b}*{vec_b[1]}) = {target}")
        # print(f"Cost: {cost}")
        
        total_cost += cost
    
    return total_cost

def part2(data):
    total_cost = 0
    
    for i, case in enumerate(data):
        # print(f"\nCase {i + 1}:")
        vec_a = (case['button_a']['x'], case['button_a']['y'])
        vec_b = (case['button_b']['x'], case['button_b']['y'])
        target = (case['prize']['x'] + 10000000000000, case['prize']['y'] + 10000000000000)
        
        # print(f"Target: {target}")
        # print(f"Button A vector: {vec_a}")
        # print(f"Button B vector: {vec_b}")
        
        solution = bezout_2d(vec_a, vec_b, target)
        
        if solution is None:
            #print("No solution exists")
            # SKIP if no solution, not added to cost
            continue
            
        moves_a, moves_b = solution
        cost = COST_A * moves_a + COST_B * moves_b
        # print(f"Solution: {moves_a} moves of A, {moves_b} moves of B")
        # print(f"Verification: ({moves_a}*{vec_a[0]} + {moves_b}*{vec_b[0]}, {moves_a}*{vec_a[1]} + {moves_b}*{vec_b[1]}) = {target}")
        # print(f"Cost: {cost}")
        
        total_cost += cost
    
    return total_cost

if __name__ == '__main__':
    data = read_data('../input.txt')


    # Part 1
    print('PART 1 - SOLUTION : ', part1(data))
    
    # Part 2
    print('PART 2 - SOLUTION : ', part2(data))