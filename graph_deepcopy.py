from Bib1 import entrada
from Bib2 import GrafoListaAdj
from collections import deque, defaultdict

def graph_deepcopy(G):
    if G.orientado == True:
        graph_copy = GrafoListaAdj(orientado=True)
    else:
        graph_copy = GrafoListaAdj()
    graph_copy.DefinirN(G.n)
   
    queue = deque()
    #visited = [False] * (G.n + 1)
    #visited[1] = True

    # Colocando as arestas na ordem do arquivo original.
    current_u = None
    buffer = []

    for u, v in G.E():
        if current_u is None:
            current_u = u

        if u != current_u:
            for e in reversed(buffer):
                graph_copy.AdicionarAresta(e[0], e[1])

            buffer.clear()
            current_u = u

        buffer.append((u, v))

    for e in reversed(buffer):
        graph_copy.AdicionarAresta(e[0], e[1])

    return graph_copy
