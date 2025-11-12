from collections import deque
from services.grammar import Grammar

def generate_shortest(grammar: Grammar, limit: int = 10, max_depth: int = 12):
    """Genera cadenas terminales por BFS en el espacio de derivaciones.
    
    Args:
        grammar: Gramática a usar
        limit: cuántas cadenas terminales devolver
        max_depth: longitud máxima de la sentencial (cantidad de símbolos)
    
    Returns:
        Lista de cadenas generadas (strings)
    """
    results = []
    start = [grammar.S]
    q = deque()
    q.append(start)
    visited = set()
    visited.add(tuple(start))  # Marcar el inicio como visitado

    while q and len(results) < limit:
        sent = q.popleft()
        
        # ¿Toda terminal?
        if all(sym in grammar.T for sym in sent):
            s = "".join(sent)
            if s not in results:
                results.append(s)
            continue  # No expandir cadenas terminales

        # Evitar sentencias demasiado largas
        if len(sent) > max_depth:
            continue

        # Expandir el PRIMER no terminal (derivación leftmost)
        for i, sym in enumerate(sent):
            if sym in grammar.N:
                # Aplicar todas las producciones posibles para este no terminal
                for p in grammar.P:
                    if p["left"] == sym:
                        new_sent = sent[:i] + p["right"] + sent[i+1:]
                        key = tuple(new_sent)
                        if key not in visited:
                            visited.add(key)
                            q.append(new_sent)
                break  # Solo expandir el primer no terminal
    
    return results  # ✅ CORRECTO: fuera del while