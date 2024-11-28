import os
import heapq
import time

class DisjointSet:
    def __init__(self, vertices):
        self.vertices = vertices
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, vertex):
        if self.parent[vertex] != vertex:
            self.parent[vertex] = self.find(self.parent[vertex])
        return self.parent[vertex]

    def union(self, vertex1, vertex2):
        root1 = self.find(vertex1)
        root2 = self.find(vertex2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1

def dijkstra(grafo, inicio, destino):
    distancias = {node: float('inf') for node in grafo}
    predecessores = {node: None for node in grafo}
    distancias[inicio] = 0
    fila_prioridade = [(0, inicio)]

    while fila_prioridade:
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)
        if distancia_atual > distancias[no_atual]:
            continue

        for vizinho, peso in grafo[no_atual]:
            distancia = distancia_atual + peso
            if distancia < distancias[vizinho]:
                distancias[vizinho] = distancia
                predecessores[vizinho] = no_atual
                heapq.heappush(fila_prioridade, (distancia, vizinho))

    # Reconstruir o caminho mínimo
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]
    caminho.reverse()

    return caminho, distancias[destino]
