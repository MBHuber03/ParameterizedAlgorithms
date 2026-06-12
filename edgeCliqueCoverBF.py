from itertools import combinations
import gc

def encontrar_cliques_maximais(G):
    """
    Encontra todas as cliques maximais no grafo G usando o algoritmo Bron-Kerbosch.

    Args:
        G: O objeto grafo com os métodos G.V() e a estrutura G.L[u].

    Returns:
        Uma lista de listas, onde cada lista interna é uma clique maximal.
    """

    cliques_maximais = []

    def bron_kerbosch(R, P, X):
        """
        Função recursiva do algoritmo Bron-Kerbosch.

        R: Clique atual (conjunto de vértices).
        P: Vértices candidatos a adicionar (conjunto de vértices).
        X: Vértices excluídos (conjunto de vértices).
        """

        # Caso base: Se P e X estiverem vazios, R é uma clique maximal.
        if not P and not X:
            # R é uma clique maximal, a adicionamos à lista de resultados
            cliques_maximais.append(list(R))
            return

        # PIVOTAMENTO: Escolher um pivô u em P ∪ X para otimizar.
        # Escolher o vértice u em P ∪ X que tem o maior número de vizinhos em P.
        # O objetivo é minimizar o número de chamadas recursivas.
        # Sem otimização por pivotamento, usa-se P:
        # P_list = list(P)

        # Implementação com pivotamento (mais eficiente)
        P_uniao_X = P.union(X)
        if not P_uniao_X:
            # Caso P e X vazios já é tratado acima, mas por segurança.
            if not P and not X:
                cliques_maximais.append(list(R))
            return

        # Encontra o pivô u (o vértice em P ∪ X que elimina mais chamadas)
        # Escolhe o vértice que tem o maior número de vizinhos em P
        pivo = max(P_uniao_X, key=lambda v: len(set(G.N(v)).intersection(P)))

        # P_sem_vizinhos_do_pivo = P \ N(pivo)
        N_pivo = set(G.N(pivo))
        P_sem_vizinhos_do_pivo = P.difference(N_pivo)

        # Itera sobre P \ N(pivo)
        for v in list(P_sem_vizinhos_do_pivo):
            # N(v) é o conjunto de vizinhos de v
            N_v = set(G.N(v))

            # Chama recursivamente:
            # R' = R ∪ {v}
            # P' = P ∩ N(v)
            # X' = X ∩ N(v)
            bron_kerbosch(R.union({v}), P.intersection(N_v), X.intersection(N_v))

            # Move v de P para X para evitar encontrar a mesma clique novamente
            P.remove(v)
            X.add(v)

    # Conjunto inicial de todos os vértices do grafo
    V = set(G.V())
    #print("Iniciando o calculo das cliques maximais...")
    # Chamada inicial:
    # R: vazio (a clique atual está vazia)
    # P: todos os vértices (todos são candidatos iniciais)
    # X: vazio (nenhum foi excluído inicialmente)
    try:
        bron_kerbosch(set(), V, set())
    except Exception as e:
        cliques_maximais = None
        gc.collect()
        raise e
    #print("Cliques maximais calculadas...")


    return cliques_maximais


def edgeCliqueCoverBF(G, k, stop):
    """
    Algoritmo de Força Bruta para o Problema de Decisão Edge Clique Cover.

    Pergunta: O grafo G pode ser coberto por no máximo k cliques?
    """
    setE = set(G.E())

    # 1. Obter todas as arestas que precisam ser cobertas
    if not G.E():
        return True  # Grafo sem arestas, cobertura trivial com 0 cliques.

    existeClique = False
    try:
        comb = combinations(encontrar_cliques_maximais(G), k)
    except:
        comb = None
        return None

    while True:
        try:
            subconjunto_cliques = next(comb)
        except StopIteration:
            break
        except:
            comb = None
            return None
            
        if stop.is_set():
            return None
        existeClique = True
        arestas_cobertas = set()

        # Para cada clique na combinação atual
        for clique in subconjunto_cliques:
            # O clique é uma tupla de vértices (ex: ('a', 'b', 'c'))
            # Ele cobre todas as arestas entre seus vértices.
            for u_idx in range(len(clique)):
                for v_idx in range(u_idx + 1, len(clique)):
                    u = clique[u_idx]
                    v = clique[v_idx]
                    aresta = tuple(sorted((u, v)))
                    arestas_cobertas.add(aresta)

        # Verifica se todas as arestas foram cobertas
        if arestas_cobertas == setE:
            # Encontrou uma cobertura de tamanho <= k
            # print(f"Cobertura encontrada com {num_cliques} cliques: {subconjunto_cliques}")
            return True

    # Se nenhuma combinação de tamanho <= k cobriu todas as arestas
    return not existeClique
