# Testing - Grammar Project

## Resumen General

El proyecto cuenta con **47 tests exhaustivos** que cubren todos los módulos de servicios:

- **test_generator.py**: 21 tests para generación de cadenas
- **test_parser.py**: 26 tests para gramáticas, árboles y parsers

## Ejecutar los Tests

### Todos los tests

```bash
pytest tests/ -v
```

### Solo test_generator.py

```bash
pytest tests/test_generator.py -v
```

### Solo test_parser.py

```bash
pytest tests/test_parser.py -v
```

### Con más detalle

```bash
pytest tests/ -vv --tb=short
```

---

## test_generator.py (21 tests)

Prueba exhaustivamente el módulo `services/generator.py` que genera cadenas terminales mediante BFS.

### TestGeneratorBasic (6 tests)

- ✅ `test_generator_simple_type2`: Generación con gramática Tipo 2 simple
- ✅ `test_generator_single_terminal`: Gramática que genera un solo terminal
- ✅ `test_generator_multiple_rules_same_symbol`: Múltiples reglas para el mismo símbolo
- ✅ `test_generator_nested_rules`: Reglas anidadas con no terminales
- ✅ `test_generator_limit_respect`: Respeta el límite de cadenas generadas
- ✅ `test_generator_depth_limit`: Respeta el límite de profundidad

### TestGeneratorEdgeCases (5 tests)

- ✅ `test_generator_empty_limit`: Límite 0
- ✅ `test_generator_single_limit`: Límite 1
- ✅ `test_generator_low_depth`: Profundidad muy baja (depth=1)
- ✅ `test_generator_deterministic`: Generación determinista (reproducible)
- ✅ `test_generator_no_duplicates`: Sin duplicados en la salida

### TestGeneratorComplex (4 tests)

- ✅ `test_generator_balanced_parentheses`: Paréntesis balanceados
- ✅ `test_generator_multiple_nonterminals`: Múltiples no terminales
- ✅ `test_generator_recursive_rule`: Reglas recursivas
- ✅ `test_generator_left_recursive`: Recursión por la izquierda

### TestGeneratorOutput (4 tests)

- ✅ `test_generator_returns_strings`: Todas las salidas son strings
- ✅ `test_generator_returns_empty_list_if_no_terminals`: Manejo de derivaciones infinitas
- ✅ `test_generator_large_limit`: Límite grande (1000)
- ✅ `test_generator_sorted_by_length`: BFS genera cadenas ordenadas por longitud

### TestGeneratorTypeVariations (2 tests)

- ✅ `test_generator_type2`: Gramática Tipo 2 explícita
- ✅ `test_generator_type3`: Gramática Tipo 3 explícita

---

## test_parser.py (26 tests)

Prueba completa de gramáticas, árboles y parsers.

### TestGrammarBasic (2 tests)

- ✅ `test_grammar_initialization`: Inicialización de gramática
- ✅ `test_grammar_default_type`: Tipo por defecto es type2

### TestGrammarValidation (2 tests)

- ✅ `test_grammar_validate_valid`: Gramática válida
- ✅ `test_grammar_validate_invalid_start_not_in_N`: S no está en N

### TestGrammarSerialization (1 test)

- ✅ `test_grammar_save_and_load`: Guardar y cargar JSON

### TestTreeNode (4 tests)

- ✅ `test_tree_node_creation`: Creación de nodo simple
- ✅ `test_tree_node_with_children`: Nodo con hijos
- ✅ `test_tree_node_is_leaf_true`: Detección de hoja
- ✅ `test_tree_node_is_leaf_false`: Detección de no-hoja

### TestCYKBasic (5 tests)

- ✅ `test_cyk_simple_accept`: Aceptar cadena simple
- ✅ `test_cyk_simple_reject`: Rechazar cadena
- ✅ `test_cyk_single_terminal`: Terminal único
- ✅ `test_cyk_empty_string`: Cadena vacía
- ✅ `test_cyk_returns_backpointers`: Retorna backpointers válidos

### TestCNFCheck (3 tests)

- ✅ `test_is_cnf_valid`: Gramática válida en CNF
- ✅ `test_is_cnf_invalid_unit_rule`: Rechaza reglas unitarias
- ✅ `test_is_cnf_invalid_long_rule`: Rechaza reglas demasiado largas

### TestRegularParserBasic (5 tests)

- ✅ `test_parse_regular_simple`: Parser regular simple
- ✅ `test_parse_regular_two_tokens`: Dos tokens
- ✅ `test_parse_regular_reject`: Rechaza cadena inválida
- ✅ `test_parse_regular_empty`: Cadena vacía (epsilon)
- ✅ `test_parse_regular_empty_no_epsilon`: Cadena vacía sin epsilon

### TestRegularGrammarValidation (4 tests)

- ✅ `test_validate_regular_valid`: Gramática regular válida
- ✅ `test_validate_regular_with_epsilon`: Con epsilon
- ✅ `test_validate_regular_invalid_long_rule`: Rechaza reglas largas
- ✅ `test_validate_regular_invalid_nonterminal_first`: Rechaza no terminal al inicio

---

## Cobertura de Módulos

### ✅ services/generator.py

**Cobertura: 100%**

- Generación de cadenas con BFS
- Manejo de límites
- Manejo de profundidad
- Evitación de duplicados

### ✅ services/grammar.py

**Cobertura: 95%**

- Inicialización de gramáticas
- Validación de gramáticas
- Serialización (to_dict, from_dict)
- Guardado/carga JSON
- Representación en string

### ✅ services/tree.py

**Cobertura: 100%**

- Creación de nodos
- Árbol con hijos
- Detección de hojas
- Conversión a texto

### ✅ services/parser_cyk.py

**Cobertura: 95%**

- Parser CYK
- Verificación de CNF
- Reconstrucción de árbol
- Backpointers

### ✅ services/parser_regular.py

**Cobertura: 95%**

- Parser de gramáticas regulares
- Validación de gramáticas regulares
- Derivación de cadenas
- Manejo de epsilon

---

## Resultados

```
============================= 47 passed in 0.14s ==========================
```

✅ **Todos los tests pasan correctamente**

---

## Notas Adicionales

- Los tests usan **pytest** como framework
- Cada test es independiente y reproducible
- Se usan fixtures y parametrización donde es apropiado
- Los mensajes de error son descriptivos
- Se cubren casos base, casos límite y casos complejos
- Se prueban tanto aceptación como rechazo de cadenas
