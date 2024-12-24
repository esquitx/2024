def read_data(filename='../input.txt'):
    connections = []
    with open(filename) as f:
        lines = f.readlines()
        connections.extend([line.strip().split('-') for line in lines])
    return connections

def part1(data):
    
    # Create a dictionary of connections i.e. undirected graph
    connections = {}
    for connection in data:
        a, b = connection
        if a not in connections:
            connections[a] = []
        if b not in connections:
            connections[b] = []
        connections[a].append(b)
        connections[b].append(a)
    
    # Count groups of three interconnected computers
    groups = 0
    visited = set()

    for node in connections:
        neighbors = connections[node]
        # Check pairs of neighbors
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                # If neighbors are connected to each other, we found a group
                if neighbors[j] in connections[neighbors[i]]:
                    # Create a sorted tuple of the group to avoid counting duplicates
                    group = tuple(sorted([node, neighbors[i], neighbors[j]]))
                    if group not in visited:
                        groups += 1
                        visited.add(group)

    # find groups that contain a computer with name starting with t
    groups_with_t = 0
    for group in visited:
        if any([computer.startswith('t') for computer in group]):
            groups_with_t += 1
    
    return groups_with_t


def part2(data):
    # Create a dictionary of connections i.e. undirected graph
    connections = {}
    for connection in data:
        a, b = connection
        if a not in connections:
            connections[a] = []
        if b not in connections:
            connections[b] = []
        connections[a].append(b)
        connections[b].append(a)

    def find_max_clique(graph):
        def bron_kerbosch(r, p, x, max_clique):
            if len(p) == 0 and len(x) == 0:
                if len(r) > len(max_clique[0]):
                    max_clique[0] = r.copy()
                return

            pivot = max((len(set(graph[v]) & p) for v in p | x), default=0)
            pivot_vertex = next((v for v in p | x if len(set(graph[v]) & p) == pivot), None)

            for v in p - set(graph.get(pivot_vertex, [])):
                new_r = r | {v}
                new_p = p & set(graph[v])
                new_x = x & set(graph[v])
                bron_kerbosch(new_r, new_p, new_x, max_clique)
                p = p - {v}
                x = x | {v}

        max_clique = [set()]
        bron_kerbosch(set(), set(graph.keys()), set(), max_clique)
        return max_clique[0]

    largest_clique = find_max_clique(connections)
    return ",".join(sorted(largest_clique))

if __name__ == '__main__':
    data = read_data('../input.txt')
    # print(data)
    print(part1(data))
    print(part2(data))