import numpy as np
from math import floor
import random
import sys
import time


class Graph:
    number_of_vertices = 0

    def create_random_graph(self, vertices, density):
        if density < 0 or density> 1:
            print("DENSITY MUST BE BETWEEN 0 AND 1")
            sys.exit()
        max_edges = vertices * (vertices - 1) // 2
        number_of_edges = floor(density * max_edges)

        matrix = np.zeros([vertices, vertices], dtype=int)
        if number_of_edges >= vertices - 1:
            edges_left = number_of_edges - vertices + 1
            disconnected_vertices = {i for i in range(1, vertices)}
            last = 0
            # w pętli while : łączenie węzłów tak aby każdy z nich miał przynamniej jedno połączenie
            # usuwa ryzyko powstania węzłów izolowanych

            while len(disconnected_vertices):
                next_element = random.choice(tuple(disconnected_vertices))
                matrix[last][next_element] = matrix[next_element][last] = random.randint(1, 20)
                disconnected_vertices.remove(next_element)
                last = next_element

        else:
            edges_left = number_of_edges
        # tworzenie listy słowników : setów zawierających elementy które nie są połączone z wezłem o danym indeksie
        # np. disconections[0] to set zawierający wezły z którymi nie jest połączony węzeł 0
        disconnections = {i : [j for j in range(vertices) if matrix[i][j]==0 and j!=i] for i in range(vertices)}

        # losowe "narysowanie" pozostałych krawędzi
        suma = 0
        while edges_left:

            node_to_connect = random.choice(tuple(disconnections.keys()))

            next_element = random.choice(disconnections[node_to_connect])

            disconnections[node_to_connect].remove(next_element)
            disconnections[next_element].remove(node_to_connect)

            if not len(disconnections[node_to_connect]):
                disconnections.pop(node_to_connect)
            if not len(disconnections[next_element]):
                disconnections.pop(next_element)

            matrix[node_to_connect][next_element] = matrix[next_element][node_to_connect] = random.randint(1, 20)
            edges_left -= 1

        return matrix



class GraphMatrix(Graph):
    adjacency_matrix = ()

    def __init__(self, vertices, density):
        Graph.number_of_vertices = vertices
        matrix = self.create_random_graph(vertices,density)
        self.adjacency_matrix = tuple(tuple(i) for i in matrix)

    def dijkstra(self, source):
        vertices = self.number_of_vertices
        visited = [source]
        distances = [float("inf") for i in range(vertices)]
        distances[source] = 0
        not_visited = [i for i in range(vertices)]
        not_visited.remove(source)
        while len(not_visited):
            last_visited = visited[-1]
            for i in range(len(self.adjacency_matrix[last_visited])):
                distance_from_source = distances[last_visited] + self.adjacency_matrix[last_visited][i]
                if distances[i] > distance_from_source and self.adjacency_matrix[last_visited][i]:
                    distances[i]= distance_from_source
            next_node = min_distance_node(distances, not_visited)
            visited.append(next_node)
            not_visited.remove(next_node)
        return distances



class GraphList(Graph):
    adjacency_list = ()

    def __init__(self, vertices, density):
        Graph.number_of_vertices = vertices
        matrix = self.create_random_graph(vertices, density)
        self.adjacency_list = tuple(tuple((j, i[j]) for j in range(vertices) if i[j]!=0) for i in matrix)

    def dijkstra(self, source):
        vertices = self.number_of_vertices
        visited = [source]
        distances = [float("inf") for i in range(vertices)]
        distances[source] = 0
        not_visited = [i for i in range(vertices)]
        not_visited.remove(source)
        while len(not_visited):
            last_visited = visited[-1]
            for node in self.adjacency_list[last_visited]:
                distance_from_source = distances[last_visited] + node[1]
                if distances[node[0]] > distance_from_source:
                    distances[node[0]]= distance_from_source
            next_node = min_distance_node(distances, not_visited)
            visited.append(next_node)
            not_visited.remove(next_node)
        return distances

def min_distance_node(distances, not_visited):
    min = float("inf")
    min_index = 0
    for i in range(len(distances)):
        if min > distances[i] and i in not_visited and distances[i]:
            min = distances[i]
            min_index = i
    return min_index


vertices = 400

#
tests = 10
suma = 0
for i in range(tests):
    test2 = GraphMatrix(vertices,1)
    test = GraphList(vertices, 1)
    start= time.time()
    test2.dijkstra(0)
    end = time.time()
    suma = suma + end - start
print(suma/tests)
#start= time.time()
#
#end = time.time()
#print(end - start)

