from Bib1 import entrada
from Bib2 import GrafoListaAdj
from collections import deque
from itertools import combinations
#import copy
from graph_deepcopy import graph_deepcopy

def removeEdge(D, u, v):
    def removeNeighbor(D, u, v, tipo):
        p = D.L[u]
        ant = None
        while(p != None):
            if (p.Viz == v and p.Tipo == tipo):
                D.m -= 1
                if ant is None:
                    D.L[u] = p.Prox
                else:
                    ant.Prox = p.Prox
                break
            p = p.Prox
    
    removeNeighbor(D, u, v, '+')
    removeNeighbor(D, v, u, '-')

    return D

def eh_dag(D):
    grau_entrada = [0] * (D.n + 1)
    for i in D.V():
        atual = D.L[i]
        while atual:
            if atual.Tipo == '+':
                grau_entrada[atual.Viz] += 1
            atual = atual.Prox

    fila = deque([i for i in D.V() if grau_entrada[i] == 0])
    vertices_processados = 0

    while len(fila) > 0:
        u = fila.popleft()
        vertices_processados += 1
        atual = D.L[u]
        while atual:
            if atual.Tipo == '+':
                v = atual.Viz
                grau_entrada[v] -= 1
                if grau_entrada[v] == 0:
                    fila.append(v)
            atual = atual.Prox

    return vertices_processados == D.n

def feedbackArcSet(D, k, stop):
    """
    Verifica se é possível remover k arestas de um dígrafo D para torná-lo acíclico.
    O algoritmo testa todas as combinações de k arestas.

    Parâmetros:
    - D: O dígrafo, uma instância da classe Digrafo.
    - k: O número de arestas a serem removidas.

    Retorna:
    - True se for possível, False caso contrário.
    """
   
    # Se k for maior que o número total de arestas, não é possível remover
    if k >= D.m:
        return True

    if k < 0:
        return False
        
    arestas = list(D.E())
    
    # Gera todas as combinações de k arestas para remoção
    for combinacao_remover in combinations(arestas, k):
        if stop.is_set():
            return None

        # Cria uma cópia do dígrafo para não modificar o original
        #copia_D = copy.deepcopy(D)
        copia_D = graph_deepcopy(D) 
        # Remove as arestas da combinação
        for u, v in combinacao_remover:
            removeEdge(copia_D, u, v)
        
        # Testa se o dígrafo resultante é acíclico
        if eh_dag(copia_D):
            return True
            
    return False
