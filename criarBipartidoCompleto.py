def criarGrafo(n): # Criar grafo bipartido completo.
	k = 4
	alpha = (n - k) // 2

	conjuntoA = list(range(alpha + 1, alpha + k + 1))
	conjuntoB = list(range(1, n + 1))

	arestas = []
	for u in conjuntoA:
		for v in conjuntoB:
				if v not in conjuntoA:
					arestas.append((u, v))

	with open("input2.txt", "a") as file:        
		file.write(f'{n}\n') # Escrever número de vértices.

		# Escrever número de arestas.
		file.write(f'{len(arestas)}\n')
		for u, v in arestas:
			file.write(f'{u} {v}\n')
		file.write("\n")

#n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140]
n = [10, 20, 30, 40, 50]

for i in range(len(n)):     
	criarGrafo(n[i])