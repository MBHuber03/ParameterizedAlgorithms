from Bib2 import GrafoListaAdj
from parameterizedAlgorithm import paramAlgorithm
from edgeCliqueCoverBF import edgeCliqueCoverBF
from graph_deepcopy import graph_deepcopy
import sys


def removeVertex(G, r):
    for v in G.V():
        p = G.L[v]
        ant = None
        while p is not None:  # Removendo da lista encadeada de cada vértice vizinho.
            if p.Viz == r:
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


def reduction1(
    G, k
):  # Se G possui um vértice isolado v, então a nova instância é (G - v, k)
    remove = []
    for v in G.V():
        p = G.L[v]
        if p is None:
            # print(f'Reduction 1: removendo vertice isolado {v}.')
            remove.append(v)
            # removeVertex(G, v)
            # return G, k, True
    if remove:
        for v in remove:
            G = removeVertex(G, v)
        return G, k, True
    return G, k, False


def removeEdge(G, u, v):
    def removeNeighbor(G, u, v):
        p = G.L[u]
        ant = None
        while p is not None:
            if p.Viz == v:
                if ant is None:
                    G.L[u] = p.Prox
                else:
                    ant.Prox = p.Prox
                break
            p = p.Prox

    removeNeighbor(G, u, v)
    removeNeighbor(G, v, u)
    G.m -= 1

    return G


def reduction2(G, k):  # Se há uma aresta isolada, remover aresta e decrementar k por 1
    for v in G.V():
        p = G.L[v]
        if (
            p is not None and p.Prox is None
        ):  # vértice forma apenas uma aresta, ou seja, d(p) = 1
            w = p.Viz
            pw = G.L[w]
            wprox = pw.Prox
            if wprox is None:  # o vizinho forma aresta apenas com p
                removeEdge(G, v, w)
                # print(f"Reduction 2: aresta {v} {w} removida.")
                return G, k - 1, True
    return G, k, False


def reduction3(G, k):  # Se há uma aresta uv em que N[u] = N[v], então remover v.
    remove = []
    for u in G.V():
        p = G.L[u]
        vizinhos_u = set(G.N(u))
        vizinhos_u = vizinhos_u.union(set([u]))
        while p is not None:
            v = p.Viz
            vizinhos_v = set(G.N(v)).union(set([v]))

            if vizinhos_u == vizinhos_v:
                remove.append(v)
                # removeVertex(G, v)
                # print(f"Reduction 3: vertice com N[u] = N[v] {v} removido.")
                # return G, k, True

            p = p.Prox

    if remove:
        remove.sort(reverse=True)
        for v in remove:
            G = removeVertex(G, v)
        return G, k, True

    return G, k, False


def condition(G, k):
    if G.n <= 2**k:
        return None
    else:
        return False


def imprimirGrafo(G):
    for v in G.V():
        print(f"{v}:", end=" ")
        p = G.L[v]
        while p:
            print(p.Viz, end=" ")
            p = p.Prox
        print()


def LerGrafo(file):
    G = GrafoListaAdj()

    while True:
        line = file.readline().strip()
        if line == "end":
            return None
        elif line != "":
            break

    n = int(line)
    print(f"n: {n}")
    line = file.readline().strip()
    m = int(line)
    print(f"m: {m}")
    G.DefinirN(n)
    for _ in range(m):
        line = file.readline().strip()
        u, v = line.split()
        u, v = int(u), int(v)
        # print(f'u: {u}, v: {v}')
        G.AdicionarAresta(u, v)
    print(k)
    return G


def tamGrafo(G):
    return G.n


reductions = []
reductions.append(reduction1)
reductions.append(reduction2)
filename = sys.argv[1]
outputFolder = sys.argv[2]
instances = []
k_values = []
kfile = sys.argv[3]

# Reading k values from kfile.
with open(kfile, "r") as kf:
    for line in kf:
        k = int(line.strip())
        k_values.append(k)


def openInput(filename):
    with open(filename, "r") as file:
        while True:
            I = LerGrafo(file)
            if I is None:
                break
            for k in k_values:
                yield (graph_deepcopy(I), k)


paramAlgorithm(
    openInput(filename),
    tamGrafo,
    edgeCliqueCoverBF,
    reductions,
    condition,
    imprimirGrafo,
    1800,
    outputFolder,
)
