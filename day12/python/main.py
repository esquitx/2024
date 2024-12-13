def read_data(filename='../input.txt'):
    with open(filename, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]




def part1(data):
    rows, cols = len(data), len(data[0])
    visited = set()
    total_sum = 0
    
    def is_valid(x, y):
        return 0 <= x < cols and 0 <= y < rows
    
    def calculate_perimeter(component):
        perimeter = 0
        for x, y in component:
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                # Count edge as perimeter if it's invalid or different type
                if not is_valid(nx, ny) or (nx, ny) not in component:
                    perimeter += 1
        return perimeter

    def find_component(start_x, start_y):
        component = set()
        to_visit = {(start_x, start_y)}
        element_type = data[start_y][start_x]
        
        while to_visit:
            x, y = to_visit.pop()
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            component.add((x, y))
            
            # Check all 4 MOVES
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (is_valid(nx, ny) and 
                    (nx, ny) not in visited and 
                    data[ny][nx] == element_type):
                    to_visit.add((nx, ny))
        
        return component
    
    # Find all components and calculate metrics
    for y in range(rows):
        for x in range(cols):
            if (x, y) not in visited:
                component = find_component(x, y)
                area = len(component)
                perimeter = calculate_perimeter(component)
                total_sum += area * perimeter
    
    return total_sum

def part2(data):
    rows, cols = len(data), len(data[0])
    visited = set()
    total_sum = 0
    
    def is_valid(x, y):
        return 0 <= x < cols and 0 <= y < rows
    
    def calculate_sides(component):
        sides = 0
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # right, left, down, up
        
        for dx, dy in directions:
            # Track edges for this direction
            edge_cells = set()
            for x, y in component:
                nx, ny = x + dx, y + dy
                if not is_valid(nx, ny) or (nx, ny) not in component:
                    edge_cells.add((x, y))
            
            # Count continuous lines
            while edge_cells:
                start = edge_cells.pop()
                current = start
                # Check perpendicular direction
                pdx, pdy = -dy, dx  # perpendicular direction
                
                # Count this as one side
                sides += 1
                
                # Remove all cells that are part of this continuous line
                while True:
                    next_pos = (current[0] + pdx, current[1] + pdy)
                    if next_pos not in edge_cells:
                        break
                    edge_cells.remove(next_pos)
                    current = next_pos
                
                # Check other direction
                current = start
                while True:
                    next_pos = (current[0] - pdx, current[1] - pdy)
                    if next_pos not in edge_cells:
                        break
                    edge_cells.remove(next_pos)
                    current = next_pos
        
        return sides
    
    def find_component(start_x, start_y):
        component = set()
        to_visit = {(start_x, start_y)}
        element_type = data[start_y][start_x]
        
        while to_visit:
            x, y = to_visit.pop()
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            component.add((x, y))
            
            # Check all 4 MOVES
            for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if (is_valid(nx, ny) and 
                    (nx, ny) not in visited and 
                    data[ny][nx] == element_type):
                    to_visit.add((nx, ny))
        
        return component
    
    # Find all components and calculate metrics
    for y in range(rows):
        for x in range(cols):
            if (x, y) not in visited:
                component = find_component(x, y)
                area = len(component)
                sides = calculate_sides(component)
                # print(sides, 'side(s) in component', component)
                total_sum += area * sides
    
    return total_sum

if __name__ == '__main__':
    data = read_data()
    print('PART 1 - SOLUTION : ', part1(data))
    print('PART 2 - SOLUTION : ', part2(data))