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
    
def parse_graph(nome_arquivo):
    grafo = {}
    num_nos = 0
    num_arestas = 0

    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if linha.startswith('c') or not linha.strip():
                continue
            if linha.startswith('p'):
                _, _, num_nos, num_arestas = linha.split()
                num_nos = int(num_nos)
                num_arestas = int(num_arestas)
                for no in range(1, num_nos + 1):
                    grafo[str(no)] = []
            elif linha.startswith('a'):
                partes = linha.split()
                if len(partes) == 4:
                    _, u, v, peso = partes
                    u, v, peso = str(u), str(v), float(peso)
                    if u in grafo and v in grafo:
                        grafo[u].append((v, peso))
                        grafo[v].append((u, peso))
                else:
                    print(f"Linha ignorada (formato inválido): {linha.strip()}")
    return grafo, num_nos, num_arestas

# Script principal de execução
if __name__ == "__main__":
    # Encontrar todos os arquivos .gr na pasta data
    pasta_data = "data"
    grafos = [os.path.join(pasta_data, arquivo) for arquivo in os.listdir(pasta_data) if arquivo.endswith('.gr')]

    # Abre arquivo de resultados para escrita
    with open("resultados.txt", "w") as f:
        # Percorre cada grafo encontrado
        for nome_arquivo in grafos:
            print(f"Executando leitura da rota ({os.path.basename(nome_arquivo).split('.')[0]}) com Dijkstra")
            tempo_inicio = time.time()

            # Parseia o grafo do arquivo
            grafo, num_nos, num_arestas = parse_graph(nome_arquivo)

            # Escreve informações básicas do grafo
            f.write(f"Grafo: {nome_arquivo}\n")
            f.write(f"Vértices: {num_nos}, Arestas: {num_arestas}\n\n")

            # Executa Dijkstra a partir do primeiro nó para o último nó
            primeiro_no = list(grafo.keys())[0]
            ultimo_no = list(grafo.keys())[-1]

            caminho, custo = dijkstra(grafo, primeiro_no, ultimo_no)
            tempo_fim = time.time()
            tempo_execucao = tempo_fim - tempo_inicio

            # Escreve os resultados no arquivo
            f.write(f"Dijkstra:\n")
            f.write(f"Caminho mínimo do nó {primeiro_no} ao nó {ultimo_no}: {' -> '.join(caminho)}\n")
            f.write(f"Custo total: {custo:.2f}\n")
            f.write(f"Tempo de execução: {tempo_execucao:.6f} segundos\n")
            f.write("\n" + "="*50 + "\n\n")

            print(f"Concluído para {os.path.basename(nome_arquivo)} em {tempo_execucao:.6f} segundos")

            print(f"Executando leitura da rota ({os.path.basename(nome_arquivo).split('.')[0]}) com Kruskal")
            tempo_inicio = time.time()

            # Executa Kruskal
            arvore_kruskal, custo_kruskal = kruskal(grafo)
            f.write("Árvore Geradora Mínima (Kruskal):\n")
            for aresta in arvore_kruskal:
                f.write(f"{aresta[1]} - {aresta[2]} (peso: {aresta[0]})\n")
            f.write(f"Custo total: {custo_kruskal:.2f}\n")
            f.write("\n")

            tempo_fim = time.time()
            tempo_execucao = tempo_fim - tempo_inicio
            f.write(f"Tempo de execução: {tempo_execucao:.6f} segundos\n")
            f.write("\n" + "="*50 + "\n\n")

            print(f"Concluído para {os.path.basename(nome_arquivo)} com Kruskal em {tempo_execucao:.6f} segundos")

            print(f"Executando leitura da rota ({os.path.basename(nome_arquivo).split('.')[0]}) com Prim")
            tempo_inicio = time.time()

            # Executa Prim
            arvore_prim, custo_prim = prim(grafo)
            f.write("Árvore Geradora Mínima (Prim):\n")
            for aresta in arvore_prim:
                f.write(f"{aresta[1]} - {aresta[2]} (peso: {aresta[0]})\n")
            f.write(f"Custo total da Árvore Geradora Mínima (Prim): {custo_prim:.2f}\n")

            tempo_fim = time.time()
            tempo_execucao = tempo_fim - tempo_inicio
            f.write(f"Tempo de execução: {tempo_execucao:.6f} segundos\n")
            f.write("\n" + "="*50 + "\n\n")

            print(f"Concluído para {os.path.basename(nome_arquivo)} com Prim em {tempo_execucao:.6f} segundos")
