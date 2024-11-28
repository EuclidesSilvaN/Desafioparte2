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

def kruskal(grafo):
    arvore_minima = []
    arestas = []
    for vertice in grafo:
        for vizinho, peso in grafo[vertice]:
            arestas.append((peso, vertice, vizinho))
    arestas.sort()

    conjunto_disjunto = DisjointSet(grafo.keys())

    for aresta in arestas:
        peso, vertice1, vertice2 = aresta
        if conjunto_disjunto.find(vertice1) != conjunto_disjunto.find(vertice2):
            arvore_minima.append(aresta)
            conjunto_disjunto.union(vertice1, vertice2)

    custo_total = sum(aresta[0] for aresta in arvore_minima)  # Cálculo do custo total da árvore geradora mínima
    return arvore_minima, custo_total

def prim(grafo):
    arvore_minima = []
    visitados = set()
    no_inicio = list(grafo.keys())[0]
    visitados.add(no_inicio)
    arestas = [(peso, no_inicio, vizinho) for vizinho, peso in grafo[no_inicio]]

    while arestas:
        arestas.sort()
        peso, vertice1, vertice2 = arestas.pop(0)
        if vertice2 not in visitados:
            visitados.add(vertice2)
            arvore_minima.append((peso, vertice1, vertice2))
            arestas.extend((p, vertice2, vizinho) for vizinho, p in grafo[vertice2] if vizinho not in visitados)

    custo_total = sum(aresta[0] for aresta in arvore_minima)  # Cálculo do custo total da árvore geradora mínima
    return arvore_minima, custo_total
