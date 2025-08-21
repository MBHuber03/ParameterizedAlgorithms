from Bib1 import entrada
from Bib2 import GrafoListaAdj
import random
import time
import itertools
import matplotlib.pyplot as plt

def reduction1(G): # Se G possui um vértice isolado v, então a nova instância é (G - v, k)
    for v in G.V():
        p = G.L[v]
        if p == None:
            print(f'Reduction1: removendo vertice isolado {v}')
            removerVertice(G, v)
            return True
    return False

def grau(G, v):
    count = 0
    p = G.L[v]
    while p:
        count += 1
        p = p.Prox
    return count

def reduction2(G, k): # Se G possui um vértice com grau de pelo menos k + 1, então a nova instância é (G - v, k - 1).
    for v in G.V():
        d = grau(G, v)
        if (d >= (k + 1)):
            print(f'Reduction2: removendo vertice {v} com grau {d}')
            removerVertice(G, v)
            return True, k - 1
    return False, k

def removerVertice(G, r):
    for v in G.V():
        p = G.L[v]
        ant = None
        while(p != None): # Removendo da lista encadeada de cada vértice vizinho.
            if (p.Viz == r):
                G.m -= 1
                if ant is None:
                    G.L[v] = p.Prox
                    p = G.L[v]
                else:
                    ant.Prox = p.Prox
                    p = p.Prox
            else:
                if p.Viz > r:
                    p.Viz -= 1
                ant = p
                p = p.Prox   
    
    del G.L[r]
    G.n -= 1

def vertexCover(G, k):
    """
    Determines if a graph G has a vertex cover of size k using a brute-force approach.

    Args:
        G: The graph object, structured with G.L[v] as an adjacency list where
           each node has 'Viz' (neighbor index) and 'Prox' (next node pointer).
        k: The desired size of the vertex cover.

    Returns:
        True if G has a vertex cover of size k, False otherwise.
    """

    # Generate all possible subsets of vertices of size k

    if G.m == 0:
        return True
        
    for cover_candidate in itertools.combinations(G.V(), k):
        # Check if the current cover_candidate is a valid vertex cover
        is_valid_cover = True
        
        # Iterate through all vertices to check if their edges are covered
        for u in G.V():
            current_node = G.L[u]
            while current_node:
                v = current_node.Viz
                
                # An edge (u, v) is covered if either u or v is in the cover_candidate
                if u not in cover_candidate and v not in cover_candidate:
                    is_valid_cover = False
                    break # This cover_candidate is not valid, move to the next
                current_node = current_node.Prox
            if not is_valid_cover:
                break
        
        if is_valid_cover:
            return True # Found a valid vertex cover of size k

    return False # No vertex cover of size k found

def imprimirGrafo(G):
    for v in G.V():
        print(f'{v}:', end=' ')
        p = G.L[v]
        while p:
            print(p.Viz, end=' ')
            p = p.Prox
        print()

def LerGrafo():
	G = GrafoListaAdj()
	n = int(entrada())
	m = int(entrada())
	G.DefinirN(n)
	for _ in range(m):
		u,v = entrada().split()
		u,v = int(u), int(v)
		G.AdicionarAresta(u, v)
	return G

def vertexCoverParam(G, k):
    a1, a2 = True, True
    while (a1 or a2):
        a1 = reduction1(G)
        a2, k = reduction2(G, k)
        
    imprimirGrafo(G)
    
    print(f'G.n = {G.n}')
    print(f'G.m = {G.m}')
    print(f'k = {k}')
    if G.n <= k**2 + k and G.m <= k**2:
        return vertexCover(G, k)
    else:
        return False    


T1 = []
T2 = []
while (True):
	try:
		G1 = LerGrafo()
	except:
		break
	G2 = LerGrafo()
	print(f'\nn: {G1.n}')
	k = 4
	print(f'k: {k}')

	# Calculando o tempo do vertex cover força-bruta.
	inicio1 = time.time()
	result1 = vertexCover(G2, k)
	fim1 = time.time()
	tempo1 = fim1 - inicio1
	T1.append((G1.n, tempo1))
	print(f'Vertex Cover Força-Bruta: {result1}')

	# Calculando o tempo do vertex cover parametrizado.
	inicio2 = time.time()
	result2 = vertexCoverParam(G2, k)
	fim2 = time.time()
	tempo2 = fim2 - inicio2
	T2.append((G2.n, tempo2))
	print(f'Vertex Cover Parametrizado: {result2}')
     
	if result1 != result2:
		print("Error!")
		exit()

# Plotando o gráfico comparando os tempos.
valoresN = [i[0] for i in T1]
temposForcaBruta = [i[1] for i in T1]
temposParam = [i[1] for i in T2]

plt.plot(valoresN, temposForcaBruta, label='Força-Bruta', marker='o')
plt.plot(valoresN, temposParam, label='Parametrizado', marker='s')
plt.xlabel('n (número de vértices)')
plt.ylabel('tempos (segundos)')
plt.title('Força-Bruta vs Parametrizado')
plt.legend()
plt.grid(True)
plt.show()