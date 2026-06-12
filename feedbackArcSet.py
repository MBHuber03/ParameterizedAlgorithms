from Bib2 import GrafoListaAdj
from feedbackarcsetFB import feedbackArcSet as bruteForce
from parameterizedAlgorithm import paramAlgorithm
from graph_deepcopy import graph_deepcopy
import sys


def reverse(p):
    if p == p.e.no1:
        p2 = p.e.no2
    else:
        p2 = p.e.no1

    if p.Tipo == "+":
        p.Tipo = "-"
    else:
        p.Tipo = "+"

    if p2.Tipo == "+":
        p2.Tipo = "-"
    else:
        p2.Tipo = "+"


def reduction1(D, k):
    c = {}
    for u, v in D.E():
        c[(u, v)] = 0
        c[(v, u)] = 0

    for v in D.V():
        p = D.L[v]
        while p != None:
            if p.Tipo == "+":
                u = p.Viz
                p2 = D.L[u]
                while p2 != None:
                    if p2.Tipo == "+":
                        w = p2.Viz
                        if D.EhAresta(w, v):
                            c[(v, u)] += 1
                            c[(u, v)] += 1
                            if (c[(u, v)]) >= k + 1:
                                reverse(p)
                                return D, k - 1, True

                    p2 = p2.Prox
            p = p.Prox
    return D, k, False


def removeVertex(D, r):
    for v in D.V():
        p = D.L[v]
        ant = None
        while p != None:  # Removendo da lista encadeada de cada vértice vizinho.
            if p.Viz == r:
                D.m -= 1
                if ant is None:
                    D.L[v] = p.Prox
                    p = D.L[v]
                else:
                    ant.Prox = p.Prox
                    p = p.Prox
            else:
                if p.Viz > r:
                    p.Viz -= 1
                ant = p
                p = p.Prox
    del D.L[r]
    D.n -= 1

    return D


def reduction2(D, k):
    c = [False] * (D.n + 1)

    for v in D.V():
        p = D.L[v]
        while p != None:
            if p.Tipo == "+":
                u = p.Viz
                p2 = D.L[u]
                while p2 != None:
                    if p2.Tipo == "+":
                        w = p2.Viz
                        if D.EhAresta(w, v):
                            c[u] = True
                            c[v] = True
                            c[w] = True
                    p2 = p2.Prox
            p = p.Prox

    someVertexRemoved = False
    verticesToRemove = []

    for v in D.V():
        if c[v] == False:
            verticesToRemove.append(v)
            someVertexRemoved = True

    verticesToRemove.sort(reverse=True)

    for v in verticesToRemove:
        D = removeVertex(D, v)

    return D, k, someVertexRemoved


def kernelMaxSize(D, k):
    if D.n <= k**2 + 2 * k:
        return None
    else:
        return False


def LerGrafo(file):
    D = GrafoListaAdj(orientado=True)

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
    D.DefinirN(n)
    for _ in range(m):
        line = file.readline().strip()
        u, v = line.split()
        u, v = int(u), int(v)
        # print(f'u: {u}, v: {v}')
        D.AdicionarAresta(u, v)
    return D


def imprimirDigrafo(D):
    for v in D.V():
        print(f"{v}:", end=" ")
        p = D.L[v]
        while p:
            if p.Tipo == "+":
                print(p.Viz, end=" ")
            p = p.Prox
        print()


def tamDigrafo(D):
    return D.n


reductions = []
reductions.append(reduction1)
reductions.append(reduction2)
filename = sys.argv[1]
outputFolder = sys.argv[2]
kfile = sys.argv[3]
instances = []
k_values = []

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
    tamDigrafo,
    bruteForce,
    reductions,
    kernelMaxSize,
    imprimirDigrafo,
    3600,
    outputFolder,
)
