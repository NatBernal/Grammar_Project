"""
Tests exhaustivos para los módulos de servicios:
- grammar.py
- tree.py
- parser_cyk.py
- parser_regular.py
"""

import pytest
import json
import tempfile
import os
from services.grammar import Grammar
from services.tree import TreeNode
from services.parser_cyk import cyk_parse, is_cnf, reconstruct_tree
from services.parser_regular import parse_regular, validate_regular_grammar


# ============ TESTS PARA Grammar ============

class TestGrammarBasic:
    """Tests básicos de la clase Grammar."""
    
    def test_grammar_initialization(self):
        """Test de inicialización de gramática."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[{"left": "S", "right": ["A", "b"]}],
            S="S",
            gtype="type2"
        )
        
        assert g.N == ["S", "A"]
        assert g.T == ["a", "b"]
        assert len(g.P) == 1
        assert g.S == "S"
        assert g.type == "type2"
    
    def test_grammar_default_type(self):
        """Test que el tipo por defecto es type2."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[],
            S="S"
        )
        
        assert g.type == "type2"


class TestGrammarValidation:
    """Tests de validación de gramáticas."""
    
    def test_grammar_validate_valid(self):
        """Test de gramática válida."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S"
        )
        
        assert g.validate() is True
    
    def test_grammar_validate_invalid_start_not_in_N(self):
        """Test de gramática inválida (S no en N)."""
        g = Grammar(
            N=["A"],
            T=["a"],
            P=[{"left": "A", "right": ["a"]}],
            S="S"
        )
        
        assert g.validate() is False


class TestGrammarSerialization:
    """Tests de guardado y carga de gramáticas."""
    
    def test_grammar_save_and_load(self):
        """Test de guardar y cargar gramática."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[{"left": "S", "right": ["A", "b"]}],
            S="S",
            gtype="type2"
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            path = f.name
        
        try:
            g.save(path)
            g2 = Grammar.load(path)
            
            assert g2.N == g.N
            assert g2.T == g.T
            assert g2.P == g.P
            assert g2.S == g.S
            assert g2.type == g.type
        finally:
            if os.path.exists(path):
                os.remove(path)


# ============ TESTS PARA TreeNode ============

class TestTreeNode:
    """Tests para la clase TreeNode."""
    
    def test_tree_node_creation(self):
        """Test creación de nodo."""
        node = TreeNode("S")
        
        assert node.symbol == "S"
        assert node.children == []
    
    def test_tree_node_with_children(self):
        """Test nodo con hijos."""
        child1 = TreeNode("A")
        child2 = TreeNode("B")
        parent = TreeNode("S", [child1, child2])
        
        assert parent.symbol == "S"
        assert len(parent.children) == 2
        assert parent.children[0].symbol == "A"
    
    def test_tree_node_is_leaf_true(self):
        """Test is_leaf para hoja."""
        node = TreeNode("a")
        
        assert node.is_leaf() is True
    
    def test_tree_node_is_leaf_false(self):
        """Test is_leaf para nodo interno."""
        parent = TreeNode("S", [TreeNode("A")])
        
        assert parent.is_leaf() is False


# ============ TESTS PARA Parser CYK ============

class TestCYKBasic:
    """Tests básicos del parser CYK."""
    
    def test_cyk_simple_accept(self):
        """Test CYK aceptar cadena simple."""
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
        
        acept, _ = cyk_parse(g, ["a", "b"])
        assert acept is True
    
    def test_cyk_simple_reject(self):
        """Test CYK rechazar cadena."""
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
        
        acept, _ = cyk_parse(g, ["a", "a"])
        assert acept is False
    
    def test_cyk_single_terminal(self):
        """Test CYK con terminal único."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        
        acept, _ = cyk_parse(g, ["a"])
        assert acept is True
    
    def test_cyk_empty_string(self):
        """Test CYK con cadena vacía."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type2"
        )
        
        acept, _ = cyk_parse(g, [])
        assert acept is False
    
    def test_cyk_returns_backpointers(self):
        """Test que CYK retorna backpointers válidos."""
        g = Grammar(
            N=["S", "A"],
            T=["a"],
            P=[
                {"left": "S", "right": ["A", "A"]},
                {"left": "A", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        
        acept, back = cyk_parse(g, ["a", "a"])
        assert acept is True
        assert len(back) > 0


class TestCNFCheck:
    """Tests para verificación de CNF."""
    
    def test_is_cnf_valid(self):
        """Test de gramática válida en CNF."""
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
        
        assert is_cnf(g) is True
    
    def test_is_cnf_invalid_unit_rule(self):
        """Test de regla unitaria (no CNF)."""
        g = Grammar(
            N=["S", "A"],
            T=["a"],
            P=[
                {"left": "S", "right": ["A"]},
                {"left": "A", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        
        assert is_cnf(g) is False
    
    def test_is_cnf_invalid_long_rule(self):
        """Test de regla demasiado larga."""
        g = Grammar(
            N=["S", "A", "B"],
            T=["a"],
            P=[
                {"left": "S", "right": ["A", "B", "a"]},
                {"left": "A", "right": ["a"]},
                {"left": "B", "right": ["a"]}
            ],
            S="S",
            gtype="type2"
        )
        
        assert is_cnf(g) is False


# ============ TESTS PARA Parser Regular ============

class TestRegularParserBasic:
    """Tests básicos del parser regular."""
    
    def test_parse_regular_simple(self):
        """Test parser regular con gramática simple."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a", "A"]},
                {"left": "A", "right": ["b"]},
                {"left": "S", "right": ["b"]}
            ],
            S="S",
            gtype="type3"
        )
        
        acept, deriv = parse_regular(g, ["b"])
        assert acept is True
        assert len(deriv) >= 1
    
    def test_parse_regular_two_tokens(self):
        """Test parser regular con dos tokens."""
        g = Grammar(
            N=["S", "A"],
            T=["a", "b"],
            P=[
                {"left": "S", "right": ["a", "A"]},
                {"left": "A", "right": ["b"]}
            ],
            S="S",
            gtype="type3"
        )
        
        acept, deriv = parse_regular(g, ["a", "b"])
        assert acept is True
    
    def test_parse_regular_reject(self):
        """Test parser regular rechaza cadena."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type3"
        )
        
        acept, _ = parse_regular(g, ["b"])
        assert acept is False
    
    def test_parse_regular_empty(self):
        """Test parser regular con cadena vacía."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": []}],
            S="S",
            gtype="type3"
        )
        
        acept, deriv = parse_regular(g, [])
        assert acept is True
    
    def test_parse_regular_empty_no_epsilon(self):
        """Test parser regular con vacía pero sin epsilon."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[{"left": "S", "right": ["a"]}],
            S="S",
            gtype="type3"
        )
        
        acept, _ = parse_regular(g, [])
        assert acept is False


class TestRegularGrammarValidation:
    """Tests de validación de gramáticas regulares."""
    
    def test_validate_regular_valid(self):
        """Test validación de gramática regular válida."""
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
        
        assert validate_regular_grammar(g) is True
    
    def test_validate_regular_with_epsilon(self):
        """Test validación con epsilon."""
        g = Grammar(
            N=["S"],
            T=["a"],
            P=[
                {"left": "S", "right": ["a"]},
                {"left": "S", "right": []}
            ],
            S="S",
            gtype="type3"
        )
        
        assert validate_regular_grammar(g) is True
    
    def test_validate_regular_invalid_long_rule(self):
        """Test que rechaza reglas muy largas."""
        g = Grammar(
            N=["S"],
            T=["a", "b"],
            P=[{"left": "S", "right": ["a", "b", "a"]}],
            S="S",
            gtype="type3"
        )
        
        assert validate_regular_grammar(g) is False
    
    def test_validate_regular_invalid_nonterminal_first(self):
        """Test que rechaza no terminal al inicio."""
        g = Grammar(
            N=["S", "A"],
            T=["a"],
            P=[{"left": "S", "right": ["A", "a"]}],
            S="S",
            gtype="type3"
        )
        
        assert validate_regular_grammar(g) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])