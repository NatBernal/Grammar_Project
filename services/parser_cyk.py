from collections import defaultdict, deque
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

def convert_to_cnf(grammar: Grammar) -> Grammar:
    """
    Conversión mínima a CNF:
    - Reemplaza terminales en RHS de longitud>1 por variables nuevas.
    - Descompone producciones largas en binarias.
    - Elimina unit-productions (A -> B) propagando las producciones de B en A.
    Nota: no implementa eliminación completa de epsilons generales; si hay epsilons se lanza NotImplementedError.
    """
    # Rechazar epsilons globales (simplificación)
    for p in grammar.P:
        if len(p.get("right", [])) == 0:
            raise NotImplementedError("Conversión a CNF no soporta epsilons en esta implementación.")

    newN = set(grammar.N)
    newP = [ {"left": p["left"], "right": list(p["right"])} for p in grammar.P ]

    # 1) Reemplazar terminales en reglas de longitud >=2 por nuevas variables
    term_map = {}
    term_counter = 0
    for p in list(newP):
        if len(p["right"]) >= 2:
            new_right = []
            for sym in p["right"]:
                if sym in grammar.T:
                    if sym not in term_map:
                        # crear nuevo no-terminal para este terminal
                        nt = f"@T{term_counter}"
                        term_counter += 1
                        while nt in newN:
                            nt = f"@T{term_counter}"
                            term_counter += 1
                        term_map[sym] = nt
                        newN.add(nt)
                        newP.append({"left": nt, "right": [sym]})
                    new_right.append(term_map[sym])
                else:
                    new_right.append(sym)
            p["right"] = new_right

    # 2) Descomponer producciones largas (>2) en binarias
    bin_counter = 0
    updatedP = []
    for p in newP:
        left = p["left"]
        right = p["right"]
        if len(right) <= 2:
            updatedP.append({"left": left, "right": right})
        else:
            cur_left = left
            for i in range(len(right) - 2):
                new_nt = f"@X{bin_counter}"
                bin_counter += 1
                while new_nt in newN:
                    new_nt = f"@X{bin_counter}"
                    bin_counter += 1
                newN.add(new_nt)
                updatedP.append({"left": cur_left, "right": [right[i], new_nt]})
                cur_left = new_nt
            updatedP.append({"left": cur_left, "right": [right[-2], right[-1]]})

    # 3) Eliminar unit-productions (A -> B) propagando RHS de B a A
    prods_by_left = defaultdict(list)
    for p in updatedP:
        prods_by_left[p["left"]].append(p["right"])

    finalP = []
    for A in list(newN):
        # recorrido BFS de unit-links desde A
        queue = deque([A])
        seen = set([A])
        while queue:
            B = queue.popleft()
            for rhs in prods_by_left.get(B, []):
                # unit production
                if len(rhs) == 1 and rhs[0] in newN:
                    C = rhs[0]
                    if C not in seen:
                        seen.add(C)
                        queue.append(C)
                else:
                    # no-unit production -> A -> rhs
                    finalP.append({"left": A, "right": rhs})

    # eliminar duplicados
    unique = []
    seen_set = set()
    for p in finalP:
        tup = (p["left"], tuple(p["right"]))
        if tup not in seen_set:
            seen_set.add(tup)
            unique.append(p)

    return Grammar(list(newN), grammar.T, unique, grammar.S, grammar.type)


def cyk_parse(grammar: Grammar, w: List[str]) -> Tuple[bool, Dict]:
    """CYK parse.
    Retorna: (aceptada_bool, backpointer_dict)
    backpointer_dict contiene claves (i,len,A) -> ('term', token) o (split, B, C)
    """
    # Si no está en CNF, intentar convertir automáticamente
    if not is_cnf(grammar):
        try:
            grammar = convert_to_cnf(grammar)
        except NotImplementedError as e:
            raise NotImplementedError("La gramática debe estar en CNF o convertible (sin epsilons). " + str(e))

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

    aceptada = grammar.S in T[0][n] if n > 0 else False
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