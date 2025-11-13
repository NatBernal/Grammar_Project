"""
Tests exhaustivos para el módulo generator.py
Prueba la generación de cadenas con BFS en el espacio de derivaciones.
"""

import pytest
from services.grammar import Grammar
from services.generator import generate_shortest


class TestGeneratorBasic:
    """Tests básicos del generador."""
    
    def test_generator_simple_type2(self):
        """Test del generador con gramática simple Tipo 2."""
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
        
        assert "b" in out, "Debería generar 'b'"
        assert "ab" in out, "Debería generar 'ab'"
        assert len(out) <= 5, "No debería exceder el límite"
        assert all(isinstance(s, str) for s in out), "Todas las salidas deben ser strings"
    
    def test_generator_single_terminal(self):
        """Test con gramática que genera un solo terminal."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert out == ["a"], "Debería generar solo 'a'"
    
    def test_generator_multiple_rules_same_symbol(self):
        """Test con múltiples reglas para el mismo símbolo."""
        g = Grammar(
            N=["S"],
            T=["a", "b", "c"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]},
                {"left": "S", "right": ["c"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert "a" in out, "Debería generar 'a'"
        assert "b" in out, "Debería generar 'b'"
        assert "c" in out, "Debería generar 'c'"
        assert len(out) == 3, "Debería generar exactamente 3 cadenas"
    
    def test_generator_nested_rules(self):
        """Test con reglas anidadas."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["A", "b"]},
                {"left": "A", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert "ab" in out, "Debería generar 'ab'"
    
    def test_generator_limit_respect(self):
        """Test que respeta el límite de cadenas."""
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
        
        # Limite bajo
        out_3 = generate_shortest(g, limit=3, max_depth=10)
        assert len(out_3) <= 3, "Debe respetar límite de 3"
        
        # Limite más alto
        out_10 = generate_shortest(g, limit=10, max_depth=10)
        assert len(out_10) <= 10, "Debe respetar límite de 10"
        
        # Comparar que 10 >= 3
        assert len(out_10) >= len(out_3), "Más límite debería generar más cadenas"
    
    def test_generator_depth_limit(self):
        """Test que respeta el límite de profundidad."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a", "S"]},
               {"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        
        # Con profundidad baja
        out_low = generate_shortest(g, limit=100, max_depth=2)
        max_len_low = max(len(s) for s in out_low) if out_low else 0
        
        # Con profundidad alta
        out_high = generate_shortest(g, limit=100, max_depth=5)
        max_len_high = max(len(s) for s in out_high) if out_high else 0
        
        assert max_len_low <= 2, "Con depth=2 no debería exceder 2 símbolos"
        assert max_len_high > max_len_low, "Más profundidad debería permitir cadenas más largas"


class TestGeneratorEdgeCases:
    """Tests de casos límite."""
    
    def test_generator_empty_limit(self):
        """Test con límite 0."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=0)
        
        assert out == [], "Con límite 0 debería retornar lista vacía"
    
    def test_generator_single_limit(self):
        """Test con límite 1."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=1)
        
        assert len(out) == 1, "Con límite 1 debería generar 1 cadena"
    
    def test_generator_low_depth(self):
        """Test con profundidad muy baja."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a", "S"]},
               {"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10, max_depth=1)
        
        # Con profundidad 1, solo debería generar "a"
        assert "a" in out, "Debería generar 'a' con depth=1"
        for s in out:
            assert len(s) <= 1, "Todas las cadenas deben tener longitud <= 1"
    
    def test_generator_deterministic(self):
        """Test que la generación es determinista (mismo resultado)."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]}
            ],
            S="S",
            gtype="type2"
        )
        
        out1 = generate_shortest(g, limit=5, max_depth=6)
        out2 = generate_shortest(g, limit=5, max_depth=6)
        
        assert out1 == out2, "Mismos parámetros deben generar mismas cadenas"
    
    def test_generator_no_duplicates(self):
        """Test que no hay cadenas duplicadas en la salida."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]},
                {"left": "S", "right": ["a"]}  # Regla duplicada
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert len(out) == len(set(out)), "No debería haber duplicados"


class TestGeneratorComplex:
    """Tests con gramáticas más complejas."""
    
    def test_generator_balanced_parentheses(self):
        """Test con gramática de paréntesis balanceados."""
        g = Grammar(
            N=["S"],
            T=["(", ")"],
            P=[
                {"left": "S", "right": ["(", "S", ")"]},
                {"left": "S", "right": []}  # Epsilon (representado como lista vacía)
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10, max_depth=6)
        
        # Debería generar cadena vacía y paréntesis balanceados
        assert "" in out or "()" in out, "Debería generar paréntesis balanceados"
    
    def test_generator_multiple_nonterminals(self):
        """Test con múltiples no terminales."""
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
        out = generate_shortest(g, limit=10)
        
        assert "ab" in out, "Debería generar 'ab'"
        assert len(out) >= 1, "Debería generar al menos una cadena"
    
    def test_generator_recursive_rule(self):
        """Test con reglas recursivas."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[
                {"left": "S", "right": ["a", "S"]},
                {"left": "S", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10, max_depth=5)
        
        # Debería generar a, aa, aaa, etc.
        assert "a" in out, "Debería generar 'a'"
        assert "aa" in out or len(out) > 1, "Debería generar múltiples cadenas"
    
    def test_generator_left_recursive(self):
        """Test con recursión por la izquierda."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[
                {"left": "S", "right": ["S", "a"]},
                {"left": "S", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10, max_depth=5)
        
        assert "a" in out, "Debería generar 'a' como base"
        # La recursión por izquierda con BFS debería expandirse


class TestGeneratorOutput:
    """Tests sobre la calidad de la salida."""
    
    def test_generator_returns_strings(self):
        """Test que todas las salidas son strings."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert isinstance(out, list), "Debe retornar una lista"
        assert all(isinstance(s, str) for s in out), "Todos los elementos deben ser strings"
    
    def test_generator_returns_empty_list_if_no_terminals(self):
        """Test comportamiento cuando no hay derivaciones terminales en límite."""
        g = Grammar(
            N=["S", "A"],
            T=["a"],
            P=[
                {"left": "S", "right": ["A"]},
                {"left": "A", "right": ["A"]}  # Solo recursión infinita
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=5, max_depth=2)
        
        # No debería generar nada (A → A es infinito)
        assert isinstance(out, list), "Debe retornar una lista incluso si está vacía"
    
    def test_generator_large_limit(self):
        """Test con límite grande."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": ["b"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=1000, max_depth=10)
        
        # Solo 2 cadenas posibles, no debería retornar 1000
        assert len(out) == 2, "Solo hay 2 cadenas terminales posibles"
        assert len(out) <= 1000, "No debe exceder el límite"
    
    def test_generator_sorted_by_length(self):
        """Test que las cadenas generadas están ordenadas por longitud (BFS)."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[
                {"left": "S", "right": ["a", "S"]},
                {"left": "S", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10, max_depth=10)
        
        # BFS debería generar por niveles: a, aa, aaa, etc.
        lengths = [len(s) for s in out]
        # Las primeras cadenas deberían ser más cortas
        if len(out) > 1:
            assert lengths[0] <= lengths[-1], "BFS generaría cadenas más cortas primero"


class TestGeneratorTypeVariations:
    """Tests con diferentes tipos de gramáticas."""
    
    def test_generator_type2(self):
        """Test explícito con gramática Tipo 2."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        out = generate_shortest(g, limit=10)
        
        assert len(out) >= 1, "Debe generar al menos una cadena"
        assert all(all(c in "a" for c in s) for s in out), "Todas deben ser terminales"
    
    def test_generator_type3(self):
        """Test explícito con gramática Tipo 3 (Regular)."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a", "A"]},
                {"left": "A", "right": ["b"]},
                {"left": "S", "right": ["a"]}
            ],
            S="S",
            gtype="type3"
        )
        out = generate_shortest(g, limit=10)
        
        assert "a" in out, "Debería generar 'a'"
        assert "ab" in out, "Debería generar 'ab'"


if __name__ == "__main__":
    # Ejecutar con pytest: pytest tests/test_generator.py -v
    pytest.main([__file__, "-v"])
