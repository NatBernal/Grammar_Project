from collections import defaultdict
from typing import List, Dict, Tuple
from services.grammar import Grammar

def is_cnf(grammar: Grammar) -> bool:
    """Verifica estructuras básicas de CNF: cada producción es A->BC o A->a.
    No comprueba epsilons ni unit rules exhaustivamente.
    """
    for p in grammar.P:
        left = p.get("left")
        right = p.get("right", [])
        if len(right) == 1:
            # debe ser terminal
            if right[0] not in grammar.T:
                return False
        elif len(right) == 2:
            if right[0] not in grammar.N or right[1] not in grammar.N:
                return False
        else:
            return False
    return True

def cyk_parse(grammar: Grammar, w: List[str]) -> Tuple[bool, Dict]:

    """CYK parse.
    Retorna: (aceptada_bool, backpointer_dict)
    backpointer_dict contiene claves (i,len,A) -> ('term', token) o (split, B, C)
    """
    if not is_cnf(grammar):
        raise NotImplementedError("La gramática debe estar en CNF para usar CYK. Implementa la normalización o usa otra herramienta.")

    prods_term = defaultdict(set)
    prods_bin = defaultdict(set)

    for p in grammar.P:
        left = p["left"]
        right = tuple(p["right"])
        if len(right) == 1 and right[0] in grammar.T:
            prods_term[right[0]].add(left)
        elif len(right) == 2:
            prods_bin[(right[0], right[1])].add(left)

    n = len(w)
    if n == 0:
        # no tratamos epsilon aquí
        return False, {}


    T = [[set() for _ in range(n+1)] for __ in range(n)]
    back = {}


    for i in range(n):
        token = w[i]
        for A in prods_term.get(token, set()):
            T[i][1].add(A)
            back[(i,1,A)] = ("term", token)


    for l in range(2, n+1):
        for i in range(0, n-l+1):
            for s in range(1, l):
                left_set = T[i][s]
                right_set = T[i+s][l-s]
                for B in left_set:
                    for C in right_set:
                        for A in prods_bin.get((B,C), set()):
                            if A not in T[i][l]:
                                T[i][l].add(A)
                                back[(i,l,A)] = (s, B, C)


    aceptada = grammar.S in T[0][n]
    return aceptada, back

def reconstruct_tree(back: Dict, i: int, l: int, A: str) -> Tuple:
    """Reconstruye árbol en estructura recursiva (tupla) usando backpointers.
    Devuelve (A, children)
    """
    key = (i,l,A)
    if key not in back:
        return (A, [])
    val = back[key]
    if val[0] == 'term':
        return (A, [val[1]])
    else:
        s, B, C = val
        left = reconstruct_tree(back, i, s, B)
        right = reconstruct_tree(back, i+s, l-s, C)
        return (A, [left, right])