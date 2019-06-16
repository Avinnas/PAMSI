class Board:
    def __init__(self):
        self.squares = [['A', 'B', 'C', 'D', 'E'], ['F', 'G', 'H', 'I', 'J'], ['K', 'L', 'M', 'N', 'O'],
                        ['P', 'Q', 'R', 'S', 'T'], ['U', 'V', 'W', 'X', 'Y']]
        self.rook_coordinates = (0, 0)
        self.knight_coordinates = (4, 2)
        self.rook_moves = self.find_rook_moves()
        self.graph = self.make_graph()
        visited = dfs((4,2), self.graph)
        nodes = []
        for i in visited:
            x = self.squares[i[0]][i[1]]
            nodes.append(x)
        print("ścieżka", nodes)
        print("***********************************************************")
        path, visited = A_pathfinding(self.graph, (4,2), (1,2))
        print("ALGORYTM A*")
        output=""
        for node in path:
            output += str(visited.index(node)+ 1) + ": "+ self.squares[node[0]][node[1]] + ", "
        print(output)
        print("odwiedzone węzły ", visited)

    def find_rook_moves(self):
        moves = []
        for i in range(5):
            moves.append((i, self.rook_coordinates[1]))
            moves.append((self.rook_coordinates[0], i))
        return moves

    def find_knight_moves(self):
        x, y = self.knight_coordinates[0], self.knight_coordinates[1]
        temp = []

        temp.append((x - 2, y - 1))
        temp.append((x - 2, y + 1))
        temp.append((x - 1, y - 2))
        temp.append((x - 1, y + 2))

        temp.append((x + 1, y - 2))
        temp.append((x + 1, y + 2))
        temp.append((x + 2, y - 1))
        temp.append((x + 2, y + 1))

        moves = [i for i in temp if 5 > i[0] > 0 and 5 > i[1] > 0]
        return moves

    def make_graph(self):
        graph = dict()
        for i in range(1, 5):
            for j in range(1, 5):
                self.knight_coordinates = i, j
                graph[i, j] = self.find_knight_moves()
        return graph

def dfs(first, graph):
    stack = []
    visited = []
    stack.append(first)
    visited.append(first)
    while len(stack):
        visiting = False
        for i in graph[stack[-1]]:
            if i not in visited:
                visited.append(i)
                stack.append(i)
                visiting = True
                break
        if not visiting:
            stack.pop()
    print("******************DFS*************************")
    print("odwiedzone pola    ", visited)
    return visited

def A_pathfinding(graph, first, last):
    visited = [first, ]
    not_visited = []
    h_array = [[999 for i in range(5)] for j in range(5)]
    g_array = [[999 for i in range(5)] for j in range(5)]
    parent_nodes = [[0 for i in range(5)] for j in range(5)]
    h_array[first[0]][first[1]] , g_array[first[0]][first[1]] = 3, 0
    while(1):
        last_visited = visited[-1]
        for node in graph[last_visited]:
            g = distance_manhattan(visited[-1],  node) + g_array[last_visited[0]][last_visited[1]]
            if g < g_array[node[0]][node[1]]:
                parent_nodes[node[0]][node[1]] = last_visited
                g_array[node[0]][node[1]] = g
                h_array[node[0]][node[1]] = distance_manhattan(node, last)
                if node not in not_visited:
                    not_visited.append(node)
        next_node = min_of_f(g_array, h_array, not_visited)
        visited.append(next_node)
        not_visited.remove(visited[-1])
        if visited[-1] == (1, 2):
            break
    current_node = (1,2)
    path = [current_node, ]
    while parent_nodes[current_node[0]][current_node[1]] is not 0:
        path.append(parent_nodes[current_node[0]][current_node[1]])
        current_node = parent_nodes[current_node[0]][current_node[1]]
    path.reverse()
    return path, visited

def distance_manhattan(first, second):
    return abs(first[0]-second[0]) + abs(first[1]-second[1])

def min_of_f(g_array, h_array, not_visited):
    minimum = float("inf")
    for node in not_visited:
        f = g_array[node[0]][node[1]] + h_array[node[0]][node[1]]
        if f < minimum:
            min_node = node
            minimum= f
        elif f == minimum:
            if node[0]< min_node[0]:
                min_node = node
                minimum = f
            elif node[0]==min_node[0] and node[1] < min_node[1]:
                min_node = node
                minimum = f
    return min_node
def main():
    Board()


if __name__ == '__main__':
    main()