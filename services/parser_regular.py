from typing import List, Dict, Tuple
from services.grammar import Grammar

def parse_regular(grammar: Grammar, w: List[str]) -> Tuple[bool, List]:
    """
    Parser simple para Gramáticas Regulares (Tipo 3).
    
    Asume formato:
    - A → aB (terminal seguido de no terminal)
    - A → a  (solo terminal)
    
    Retorna: (aceptada, derivación)
    derivación es una lista de tuplas (símbolo_actual, producción_usada)
    """
    if not w:
        # Verificar si hay producción S → ε
        for p in grammar.P:
            if p["left"] == grammar.S and len(p["right"]) == 0:
                return True, [(grammar.S, "S → ε")]
        return False, []
    
    derivation = []
    current_symbol = grammar.S
    idx = 0
    
    while idx < len(w):
        token = w[idx]
        found = False
        
        # Buscar producción aplicable
        for p in grammar.P:
            if p["left"] == current_symbol:
                right = p["right"]
                
                # Caso: A → a (producción terminal)
                if len(right) == 1 and right[0] == token and right[0] in grammar.T:
                    if idx == len(w) - 1:  # Último token
                        derivation.append((current_symbol, f"{p['left']} → {token}"))
                        return True, derivation
                
                # Caso: A → aB (terminal + no terminal)
                elif len(right) == 2 and right[0] == token and right[0] in grammar.T:
                    if right[1] in grammar.N:
                        derivation.append((current_symbol, f"{p['left']} → {right[0]}{right[1]}"))
                        current_symbol = right[1]
                        idx += 1
                        found = True
                        break
        
        if not found:
            return False, derivation
    
    return False, derivation


def validate_regular_grammar(grammar: Grammar) -> bool:
    """
    Verifica que la gramática sea realmente Tipo 3 (Regular).
    
    Formato válido:
    - A → aB (lineal derecha)
    - A → a
    - A → ε (opcional)
    """
    for p in grammar.P:
        right = p["right"]
        
        # ε-producción
        if len(right) == 0:
            continue
        
        # Producción terminal: A → a
        if len(right) == 1:
            if right[0] not in grammar.T:
                return False
        
        # Producción lineal: A → aB
        elif len(right) == 2:
            if right[0] not in grammar.T or right[1] not in grammar.N:
                return False
        else:
            return False
    
    return True