from itertools import combinations

def parse_operation(line):
    # Split into inputs and output
    inputs, output = line.split(' -> ')
    
    # Parse the operation part
    parts = inputs.split()
    
    if len(parts) == 3:  # Binary operation (e.g., "x AND y")
        return (parts[0], parts[2], parts[1], output)
    else:  # Single operation with XOR
        return (parts[0], parts[2], 'OR', output) if 'OR' in line else (parts[0], parts[2], 'XOR', output)

def read_data(filename='../input.txt'):
    initial_values = {}
    operations = []

    with open(filename) as f:
        lines = f.readlines()
        
    # Read initial values
    for line in lines:
        if not line.strip():
            break
        var, val = line.strip().split(': ')
        initial_values[var] = int(val)
        
    # Read operations into structured format
    for line in lines[len(initial_values) + 1:]:
        if line.strip():
            operations.append(parse_operation(line.strip()))
            
    return initial_values, operations


def part1(data):
    initial_values, operations = data
    current_values = initial_values.copy()
    
    def process_operation(op1, op2, operation, output):
        # Get values, using 0 if not yet calculated
        val1 = current_values.get(op1, None)
        val2 = current_values.get(op2, None)
        
        if val1 is None or val2 is None:
            return False
        else: 
            # Apply the operation
            if operation == 'AND':
                result = val1 & val2
            elif operation == 'OR':
                result = val1 | val2
            elif operation == 'XOR':
                result = val1 ^ val2
        
            current_values[output] = result
            return True
    
    # Keep processing until all operations are completed
    while len(current_values) < len(initial_values) + len(operations):
        for operation in operations:
            process_operation(*operation)
    
    # Get all z-gates in reverse sorted order and combine their values into binary
    z_gates = sorted([k for k in current_values.keys() if k.startswith('z')], reverse=True)
    binary = ''.join('1' if current_values[gate] else '0' for gate in z_gates)
    
    # Convert binary to decimal
    return int(binary, 2)

def part2(data):
    initial_values, operations = data
    
    def furthest_made(operations):
        ops = {}
        for x1, x2, res, op in operations:
            ops[(frozenset([x1, x2]), op)] = res
        
        def get_res(x1, x2, op):
            return ops.get((frozenset([x1, x2]), op), None)
        
        carries = {}
        correct = set()
        prev_intermediates = set()
        
        try:
            for i in range(45):
                pos = f"0{i}" if i < 10 else str(i)
                predigit = get_res(f"x{pos}", f"y{pos}", "XOR")
                precarry1 = get_res(f"x{pos}", f"y{pos}", "AND")
                
                if i == 0:
                    if predigit != "z00":
                        return 0, correct
                    carries[i] = precarry1
                    continue
                
                digit = get_res(carries[i - 1], predigit, "XOR")
                if digit != f"z{pos}":
                    return i - 1, correct
                
                correct.add(carries[i - 1])
                correct.add(predigit)
                for wire in prev_intermediates:
                    correct.add(wire)
                
                precarry2 = get_res(carries[i - 1], predigit, "AND")
                carry_out = get_res(precarry1, precarry2, "OR")
                carries[i] = carry_out
                prev_intermediates = {precarry1, precarry2}
                
        except Exception:
            return i - 1, correct
            
        return 44, correct

    swaps = set()
    base, base_used = furthest_made(operations)
    
    for _ in range(4):
        found_swap = False
        for i, j in combinations(range(len(operations)), 2):
            x1_i, x2_i, res_i, op_i = operations[i]
            x1_j, x2_j, res_j, op_j = operations[j]
            
            if "z00" in (res_i, res_j) or res_i in base_used or res_j in base_used:
                continue
                
            # Try swap
            operations[i], operations[j] = (x1_i, x2_i, res_j, op_i), (x1_j, x2_j, res_i, op_j)
            attempt, attempt_used = furthest_made(operations)
            
            if attempt > base:
                swaps.add((res_i, res_j))
                base, base_used = attempt, attempt_used
                found_swap = True
                break
            
            # Revert swap
            operations[i], operations[j] = (x1_i, x2_i, res_i, op_i), (x1_j, x2_j, res_j, op_j)
            
        if not found_swap:
            break

    return ",".join(sorted(sum(swaps, start=tuple())))


if __name__ == '__main__':
    data = read_data('../test.txt')
    print(part1(data))
    print(part2(data))