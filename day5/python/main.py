'''

IDEA  . Guardar los valores que tienen que ir antes, construir lista con el orden, ir consultando a partir del orden

X | Y -> if both X and Y are in the list, X must be before Y

before : "NUMBER" : [LIST OF NUMBERS THAT HAVE TO APPEAR AFTER "NUMBER"]
'''

def read_data(file='../input.txt'):
    '''
    X | Y for the first n lines
    --> blank line <--
    rules
    '''

    rules = {}
    tests = []
    isRule = True
    
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                isRule = False
                continue
            if isRule:
                x, y = line.strip().split('|')
                x, y = x.strip(), y.strip()
                if x not in rules:
                    rules[x] = set()
                rules[x].add(y)
            else:
                tests.append(line.strip().split(','))

    return rules, tests

def is_valid(test, rules_dict):
    for i, num in enumerate(test[::-1]):
        if num in rules_dict:
            required_after = rules_dict[num]
            # Get numbers that should appeart after (the 'Y's)
            numbers_before = set(test[:-i-1])
            # Check if any required "after" number appears before by calculating intersection
            if required_after & numbers_before:
                return False
    return True

def part1(rules, tests):
    sum = 0
    for test in tests:
        if is_valid(test, rules):
            # Get middle number from valid sequence
            middle_idx = len(test) // 2
            sum += int(test[middle_idx])

    return sum

def sort(sequence, rules):
    """custom insertion sort to respect rules"""

    sequence = sequence.copy()  # being nice to the original s
    for i in range(1, len(sequence)):
        current = sequence[i]
        j = i - 1
        # Move violation elements froward
        while j >= 0:
            # Check if current element must come after j
            if sequence[j] in rules and current in rules[sequence[j]]:
                break
            # Check if j must come after current element
            if current in rules and sequence[j] in rules[current]:
                sequence[j + 1] = sequence[j]
                j -= 1
            else:
                break
        sequence[j + 1] = current
    
    return sequence

def part2(rules, tests):
    sum = 0
    for test in tests:
        if not is_valid(test, rules):
            arranged = sort(test, rules)
            middle_idx = len(arranged) // 2
            sum += int(arranged[middle_idx])
    return sum

if __name__ == '__main__':
    rules, test = read_data()
    
    print('PART 1 - SOLUTION : ', part1(rules, test))
    print('PART 2 - SOLUTION : ', part2(rules, test))


