def read_data(filename='../input.txt'):
    matrix = []
    with open(filename, 'r') as f:
        for line in f:
            matrix.append([int(char) for char in line.strip()])

    return matrix

def score(matrix, start):
    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    i, j = start
    visited = set()
    score = 0

    def valid_move(matrix, i, j, prev_value):
        return (0 <= i < len(matrix) and 
                0 <= j < len(matrix[0]) and 
                (i, j) not in visited and 
                matrix[i][j] == prev_value + 1)

    
    to_visit = [(i, j, 0)]  # Trails always start with height 0
    while to_visit:
        curr_i, curr_j, curr_value = to_visit.pop()

        # already visited skip
        if (curr_i, curr_j) in visited:
            continue
        # If not, mark as visited
        else: 
            visited.add((curr_i, curr_j))
        
        # Reached a 9, increment score and continue
        if matrix[curr_i][curr_j] == 9:
            score += 1
            continue
        
        # posible moves 
        for di, dj in MOVES:
            # Candidate futute positions
            next_i, next_j = curr_i + di, curr_j + dj
            # if the move is okay, move
            if valid_move(matrix, next_i, next_j, curr_value):
                to_visit.append((next_i, next_j, matrix[next_i][next_j]))

    return score
   

def part1(data):
    total_score = 0
    # Find 0s, then find score for every zero
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 0:
                total_score += score(data, (i, j))

    return total_score


def rating(matrix, start):

    MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    i, j = start
    paths = 0 # Number of paths is = rating
    visited = set() # keep track of visisted

    # Same as in score
    def valid_move(matrix, i, j, prev_value):
        return (0 <= i < len(matrix) and 
                0 <= j < len(matrix[0]) and 
                (i, j) not in visited and 
                matrix[i][j] == prev_value + 1)

    # Use DFS to find all paths
    def dfs(curr_i, curr_j, curr_value):
        
        nonlocal paths # This allows us to access the paths variable from the outer scope

        # Basic BFS, with stop condition reaching a 9 ->
        if matrix[curr_i][curr_j] == 9:
            paths += 1
            return
        
        visited.add((curr_i, curr_j))
        
        for di, dj in MOVES:
            next_i, next_j = curr_i + di, curr_j + dj
            if valid_move(matrix, next_i, next_j, curr_value):
                dfs(next_i, next_j, matrix[next_i][next_j])
        
        visited.remove((curr_i, curr_j))
        # <-

    # Call it in the starting points with value 0
    dfs(i, j, 0)
    return paths


def part2(data):
    total_rating = 0
    # Find 0s, then find score for every zero
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 0:
                total_rating += rating(data, (i, j))

    return total_rating


if __name__ == '__main__':

    data = read_data()


    print('PART 1 - SOLUTION : ', part1(data))

    print('PART 2 - SOLUTION : ', part2(data))