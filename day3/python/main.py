import re 


def read_data():
    with open('../input.txt') as f:
        data = f.read().replace('\n', '')
    
    return [data]



def part1(data):
    
    pattern = r'mul\((\d{1,3}),\s*(\d{1,3})\)'
    matches = []
    for line in data:
        matches.extend(re.findall(pattern, line))


    sum = 0
    for match in matches:
        sum += int(match[0]) * int(match[1])
    
    return sum




def part2(data):

    do_sections = []
    for line in data:
        parts = line.split('do()')
        # Reached this point, each part looks like this 
        # blah-blah-don't()-blah-blah-blah-don't()-[...]
        for part in parts:
            # We need to get the first part i.e content up to the first don't
            # So we split the part by don't and take the first part
            first_part = part.split('don\'t()')[0]
            do_sections.append(first_part)

    sum = part1(do_sections)
    return sum



if __name__ == '__main__':
    data = read_data()

    #
    print("PART 1")
    print("SOLUTION: ", part1(data))
    #
    print("PART 2")
    print("SOLUTION: ", part2(data))
