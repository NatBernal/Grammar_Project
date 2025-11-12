from services.grammar import Grammar
from services.generator import generate_shortest
from services.parser_cyk import cyk_parse, is_cnf

def test_generator_simple():
    """Test del generador con gramática simple."""
    g = Grammar(
        N=["S"],
        T=["a", "b"],
        P=[
            {"left": "S", "right": ["a", "S"]}, 
            {"left": "S", "right": ["b"]}
        ],
        S="S",
        gtype="type2"
    )
    out = generate_shortest(g, limit=5, max_depth=6)
    
    print("Cadenas generadas:", out)
    assert "b" in out, "Debería generar 'b'"
    assert "ab" in out, "Debería generar 'ab'"
    # Otras cadenas esperadas: "aab", "aaab", etc.
    print("✅ test_generator_simple pasado")


def test_cnf_check():
    """Test de verificación de CNF."""
    # Gramática en CNF: S → AB | a, A → a, B → b
    g_cnf = Grammar(
        N=["S", "A", "B"],
        T=["a", "b"],
        P=[
            {"left": "S", "right": ["A", "B"]},
            {"left": "S", "right": ["a"]},
            {"left": "A", "right": ["a"]},
            {"left": "B", "right": ["b"]}
        ],
        S="S",
        gtype="type2"
    )
    
    assert is_cnf(g_cnf), "Esta gramática debería estar en CNF"
    print("✅ test_cnf_check pasado")


def test_cyk_simple():
    """Test del parser CYK con gramática simple en CNF."""
    # Gramática: S → AB, A → a, B → b
    # Acepta: "ab"
    g = Grammar(
        N=["S", "A", "B"],
        T=["a", "b"],
        P=[
            {"left": "S", "right": ["A", "B"]},
            {"left": "A", "right": ["a"]},
            {"left": "B", "right": ["b"]}
        ],
        S="S",
        gtype="type2"
    )
    
    # Cadena aceptada
    acept, back = cyk_parse(g, ["a", "b"])
    assert acept, "Debería aceptar 'ab'"
    
    # Cadena rechazada
    acept2, _ = cyk_parse(g, ["a", "a"])
    assert not acept2, "No debería aceptar 'aa'"
    
    print("✅ test_cyk_simple pasado")


def test_grammar_validation():
    """Test de validación de gramática."""
    # Gramática válida
    g_valid = Grammar(
        N=["S"],
        T=["a"],
        P=[{"left": "S", "right": ["a"]}],
        S="S"
    )
    assert g_valid.validate(), "Gramática válida debería pasar validación"
    
    # Gramática inválida (S no está en N)
    g_invalid = Grammar(
        N=["A"],
        T=["a"],
        P=[{"left": "A", "right": ["a"]}],
        S="S"  # S no está en N
    )
    assert not g_invalid.validate(), "Gramática inválida no debería pasar"
    
    print("✅ test_grammar_validation pasado")


if __name__ == "__main__":
    test_generator_simple()
    test_cnf_check()
    test_cyk_simple()
    test_grammar_validation()
    print("\n🎉 Todos los tests pasaron correctamente")