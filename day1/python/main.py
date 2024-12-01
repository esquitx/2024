def read_input(filename="../input.txt"):
    # Step 1 - read the file and split into columns
    with open(filename, 'r') as file:
        lines = file.readlines()
        column1 = []
        column2 = []
        for line in lines:
            col1, col2 = line.split()
            column1.append(int(col1))
            column2.append(int(col2))

    return column1, column2


def part1():

    column1, column2 = read_input()
    
    # Step 2 - sort the columns
    column1.sort()
    column2.sort()

    # Step 3 - Calculate the sum of the differences
    sum = 0
    for i in range(len(column1)):
        sum += abs(column1[i] - column2[i])

    print("PART 1")
    print("SOLUTION: ", sum)
    print()

def part2(): 

    column1, column2 = read_input()

    # Step 1 - calculate similarity score
    similarity_score = 0
    for element in column1:
        similarity_score += element*column2.count(element)


    print("PART 2")
    print("SOLUTION: ", similarity_score)
    print()

    # Calculate similarity 
if __name__ == '__main__':

    print("Advent of Code 2024 - Day 1\n")

    ##
    part1()
    ## 
    part2()