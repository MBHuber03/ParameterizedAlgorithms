from Bib1 import entrada
from Bib2 import GrafoListaAdj
import time
import itertools
from parameterizedAlgorithm import paramAlgorithm

def reduction1(G, k): # Se G possui um vértice isolado v, então a nova instância é (G - v, k)
	for v in G.V():
		p = G.L[v]
		if p == None:
			#print(f'Reduction1: removendo vertice isolado {v}')
			removerVertice(G, v)
			return G, k, True
	return G, k, False

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
			#print(f'Reduction2: removendo vertice {v} com grau {d}')
			G = removerVertice(G, v)
			return G, k - 1, True
	return G, k, False

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

	return G

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

def condition(G, k):
	if G.n <= k**2 + k and G.m <= k**2:
		return None
	else:
		return False
	
def imprimirGrafo(G):
	for v in G.V():
		print(f'{v}:', end=' ')
		p = G.L[v]
		while p:
			print(p.Viz, end=' ')
			p = p.Prox
		print()

def LerGrafo(file):
	G = GrafoListaAdj()

	while True:
		line = file.readline().strip()
		if line == "end":
			return None
		elif line != '':
			break

	n = int(line)
	print(f'n: {n}')
	line = file.readline().strip()
	m = int(line)
	print(f'm: {m}')
	G.DefinirN(n)
	for _ in range(m):
					line = file.readline().strip()
					u, v = line.split()
					u, v = int(u), int(v)
					#print(f'u: {u}, v: {v}')
					G.AdicionarAresta(u, v)
	return G

def imprimirGrafo(G):
	for v in G.V():
		print(f'{v}:', end=' ')
		p = G.L[v]
		while p:
			print(p.Viz, end=' ')
			p = p.Prox
		print()

def tamGrafo(G):
	return G.n

k = 4
reductions = []
reductions.append(reduction1)
reductions.append(reduction2)
filename = input("Input filename: ")

instances = []
with open(filename, "r") as file:
	while True:
		G = LerGrafo(file)
		if G == None:
			break
		instances.append((G, k))
		
paramAlgorithm(instances, tamGrafo, vertexCover, reductions, condition, imprimirGrafo)