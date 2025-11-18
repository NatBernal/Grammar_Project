from typing import List, Dict, Tuple
from services.grammar import Grammar

def detect_grammar_direction(grammar: Grammar) -> str:
    """
    Detecta si la gramática es lineal derecha, izquierda o mixta.
    
    Returns:
        'right': Lineal derecha (A → aB)
        'left': Lineal izquierda (A → Ba)
        'mixed': Contiene ambos tipos
        'invalid': No es regular
    """
    has_right = False
    has_left = False
    
    for p in grammar.P:
        right = p["right"]
        
        # ε o terminal simple, válido para ambos
        if len(right) == 0:
            continue  # Producción epsilon
        
        if len(right) == 1:
            # A → a (terminal) o A → ε (epsilon representado como string)
            if right[0] in grammar.T or right[0] == 'ε' or right[0] == 'epsilon':
                continue
            # A → B (unit production, válida para regulares)
            elif right[0] in grammar.N:
                continue
            else:
                return 'invalid'
        
        if len(right) == 2:
            # Lineal derecha: A → aB (terminal, no terminal)
            if right[0] in grammar.T and right[1] in grammar.N:
                has_right = True
            # Lineal izquierda: A → Ba (no terminal, terminal)
            elif right[0] in grammar.N and right[1] in grammar.T:
                has_left = True
            else:
                return 'invalid'
        else:
            return 'invalid'
    
    if has_right and has_left:
        return 'mixed'
    elif has_right:
        return 'right'
    elif has_left:
        return 'left'
    else:
        return 'right'  # Default si solo tiene A → a

def parse_regular(grammar: Grammar, w: List[str]) -> Tuple[bool, List]:
    """
    Parser universal para Gramáticas Regulares (Tipo 3).
    Auto-detecta dirección y procesa apropiadamente.
    
    Soporta:
    - Gramáticas lineales derechas: A → aB, A → a, A → ε
    - Gramáticas lineales izquierdas: A → Ba, A → a, A → ε
    
    Retorna: (aceptada, derivación)
    derivación es una lista de tuplas (símbolo_actual, producción_usada)
    """
    # Caso especial: cadena vacía
    if not w:
        for p in grammar.P:
            if p["left"] == grammar.S:
                if len(p["right"]) == 0 or (len(p["right"]) == 1 and p["right"][0] in ['ε', 'epsilon']):
                    epsilon_symbol = 'ε' if len(p["right"]) == 0 else p["right"][0]
                    return True, [(grammar.S, f"S → {epsilon_symbol}")]
        return False, []
    
    direction = detect_grammar_direction(grammar)
    
    if direction == 'invalid':
        return False, [("Error", "Gramática no es regular")]
    
    if direction == 'mixed':
        return False, [("Error", "Gramática mixta (izquierda + derecha) no soportada")]
    
    if direction == 'left':
        return parse_left_linear(grammar, w)
    else:
        return parse_right_linear(grammar, w)

def parse_right_linear(grammar: Grammar, w: List[str]) -> Tuple[bool, List]:
    """
    Parser para gramáticas lineales DERECHAS.
    Procesa de IZQUIERDA a DERECHA.
    
    Formato: A → aB, A → a, A → ε, A → B
    """
    derivation = []
    current_symbol = grammar.S
    idx = 0
    
    # Resolver unit productions al inicio (S → A)
    max_unit_steps = 100  # Prevenir ciclos infinitos
    unit_steps = 0
    while unit_steps < max_unit_steps:
        found_unit = False
        for p in grammar.P:
            if p["left"] == current_symbol:
                right = p["right"]
                # Unit production: A → B
                if len(right) == 1 and right[0] in grammar.N:
                    derivation.append((current_symbol, f"{p['left']} → {right[0]}"))
                    current_symbol = right[0]
                    found_unit = True
                    unit_steps += 1
                    break
        if not found_unit:
            break
    
    while idx < len(w):
        token = w[idx]
        found = False
        
        # Buscar producción aplicable
        for p in grammar.P:
            if p["left"] == current_symbol:
                right = p["right"]
                
                # Caso: A → a (producción terminal)
                if len(right) == 1 and right[0] == token and right[0] in grammar.T:
                    derivation.append((current_symbol, f"{p['left']} → {token}"))
                    idx += 1
                    
                    # Si es el último token, verificar si alcanzamos estado final
                    if idx == len(w):
                        return True, derivation
                    
                    # Si no es el último, no deberíamos aceptar
                    return False, derivation
                
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
    
    # Después de procesar todos los tokens, verificar si el estado actual acepta epsilon
    for p in grammar.P:
        if p["left"] == current_symbol:
            right = p["right"]
            # Verificar producción epsilon
            if len(right) == 0 or (len(right) == 1 and right[0] in ['ε', 'epsilon']):
                epsilon_symbol = 'ε' if len(right) == 0 else right[0]
                derivation.append((current_symbol, f"{current_symbol} → {epsilon_symbol}"))
                return True, derivation
            # Verificar unit production que lleve a epsilon
            elif len(right) == 1 and right[0] in grammar.N:
                # Buscar epsilon transitivamente
                next_symbol = right[0]
                derivation.append((current_symbol, f"{current_symbol} → {next_symbol}"))
                for p2 in grammar.P:
                    if p2["left"] == next_symbol:
                        r2 = p2["right"]
                        if len(r2) == 0 or (len(r2) == 1 and r2[0] in ['ε', 'epsilon']):
                            epsilon_symbol = 'ε' if len(r2) == 0 else r2[0]
                            derivation.append((next_symbol, f"{next_symbol} → {epsilon_symbol}"))
                            return True, derivation
    
    return False, derivation

def parse_left_linear(grammar: Grammar, w: List[str]) -> Tuple[bool, List]:
    """
    Parser para gramáticas lineales IZQUIERDAS.
    Procesa de DERECHA a IZQUIERDA.
    
    Formato: A → Ba, A → a, A → ε, A → B
    
    Ejemplo:
        Gramática: S → Ab, A → a
        Cadena: "ab"
        
        Paso 1: Desde el final, token='b', buscar producción que termine en 'b'
        Paso 2: Encontrar S → Ab, cambiar estado a A
        Paso 3: Token='a', buscar A → a
    """
    derivation = []
    current_symbol = grammar.S
    idx = len(w) - 1  # Empezar desde el FINAL
    
    # Resolver unit productions al inicio (S → A)
    max_unit_steps = 100
    unit_steps = 0
    while unit_steps < max_unit_steps:
        found_unit = False
        for p in grammar.P:
            if p["left"] == current_symbol:
                right = p["right"]
                # Unit production: A → B
                if len(right) == 1 and right[0] in grammar.N:
                    derivation.append((current_symbol, f"{p['left']} → {right[0]}"))
                    current_symbol = right[0]
                    found_unit = True
                    unit_steps += 1
                    break
        if not found_unit:
            break
    
    while idx >= 0:
        token = w[idx]
        found = False
        
        # Buscar producción aplicable
        for p in grammar.P:
            if p["left"] == current_symbol:
                right = p["right"]
                
                # Caso: A → a (producción terminal)
                if len(right) == 1 and right[0] == token and right[0] in grammar.T:
                    derivation.append((current_symbol, f"{p['left']} → {token}"))
                    idx -= 1
                    
                    # Si es el primer token, verificar si alcanzamos estado final
                    if idx < 0:
                        derivation.reverse()
                        return True, derivation
                    
                    # Si no es el primero, no deberíamos aceptar
                    derivation.reverse()
                    return False, derivation
                
                # Caso: A → Ba (no terminal + terminal)
                elif len(right) == 2 and right[1] == token and right[1] in grammar.T:
                    if right[0] in grammar.N:
                        derivation.append((current_symbol, f"{p['left']} → {right[0]}{right[1]}"))
                        current_symbol = right[0]  # Transición al no terminal
                        idx -= 1  # Avanzar hacia la IZQUIERDA
                        found = True
                        break
        
        if not found:
            derivation.reverse()
            return False, derivation
    
    # Después de procesar todos los tokens, verificar si el estado actual acepta epsilon
    for p in grammar.P:
        if p["left"] == current_symbol:
            right = p["right"]
            # Verificar producción epsilon
            if len(right) == 0 or (len(right) == 1 and right[0] in ['ε', 'epsilon']):
                epsilon_symbol = 'ε' if len(right) == 0 else right[0]
                derivation.append((current_symbol, f"{current_symbol} → {epsilon_symbol}"))
                derivation.reverse()
                return True, derivation
            # Verificar unit production que lleve a epsilon
            elif len(right) == 1 and right[0] in grammar.N:
                next_symbol = right[0]
                derivation.append((current_symbol, f"{current_symbol} → {next_symbol}"))
                for p2 in grammar.P:
                    if p2["left"] == next_symbol:
                        r2 = p2["right"]
                        if len(r2) == 0 or (len(r2) == 1 and r2[0] in ['ε', 'epsilon']):
                            epsilon_symbol = 'ε' if len(r2) == 0 else r2[0]
                            derivation.append((next_symbol, f"{next_symbol} → {epsilon_symbol}"))
                            derivation.reverse()
                            return True, derivation
    
    derivation.reverse()
    return False, derivation

def validate_regular_grammar(grammar: Grammar) -> bool:
    """
    Verifica que la gramática sea realmente Tipo 3 (Regular).
    
    Formato válido:
    - Lineal derecha: A → aB, A → a
    - Lineal izquierda: A → Ba, A → a
    - ε-producción: A → ε (opcional)
    
    No se permiten gramáticas mixtas.
    """
    direction = detect_grammar_direction(grammar)
    return direction in ['right', 'left']