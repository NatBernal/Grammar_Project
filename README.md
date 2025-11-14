# 📚 Analizador Sintáctico de Gramáticas Formales

**Universidad Pedagógica y Tecnológica de Colombia - UPTC**  
**Asignatura:** Lenguajes Formales  
**Proyecto:** Parser y Generador para Gramáticas Tipo 2 y 3

---

## ✨ Características

### 🎨 Interfaz Moderna

- **Tema Bootstrap oscuro** (morph) para un aspecto profesional y moderno
- Diseño responsivo con interfaz intuitive
- Barra de estado con mensajes de retroalimentación
- Botones con estilos Bootstrap (info, success, primary, warning, danger)

### 🔤 Soporte de Gramáticas

- **Tipo 2 (GLC):** Gramáticas Libres de Contexto con soporte CNF
- **Tipo 3 (Regulares):** Gramáticas regulares
- Carga/guardado en formato JSON
- Validación automática de gramáticas

### ⚙️ Análisis Sintáctico

- **Algoritmo CYK:** Para gramáticas libres de contexto en CNF
- **Parser Regular:** Para gramáticas regulares (DFA simulation)
- Auto-detección del tipo de gramática y algoritmo
- Generación de árboles de derivación

### 🔧 Generación de Cadenas

- Generador BFS con límites de profundidad y cantidad
- Obtención de cadenas más cortas del lenguaje
- Exportación de resultados a archivos

### 🧪 Testing Completo

- **47 pruebas unitarias** con cobertura completa
- Tests para parser CYK, parser regular, generador y gramática
- Validación de casos normales y edge cases

---

## 📋 Tabla de Contenidos

1. [Requisitos](#requisitos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Instalación](#instalación)
4. [Ejecución](#ejecución)
5. [Uso de la Aplicación](#uso-de-la-aplicación)
6. [Ejemplos](#ejemplos)
7. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Requisitos

### Software Necesario

- **Python 3.8 o superior** ([Descargar Python](https://www.python.org/downloads/))
- **tkinter** (incluido con Python en Windows y macOS)
- **ttkbootstrap 1.6.0+** (se instala automáticamente con requirements.txt)

### Verificar Instalación

Abre una terminal/CMD y ejecuta:

```bash
python --version
# Debe mostrar: Python 3.8.x o superior

python -m tkinter
# Debe abrir una ventana de prueba de tkinter
```

Si `tkinter` no está instalado:

**En Ubuntu/Debian:**

```bash
sudo apt-get install python3-tk
```

**En Fedora:**

```bash
sudo dnf install python3-tkinter
```

**En macOS/Windows:** tkinter viene incluido por defecto.

---

## 📁 Estructura del Proyecto

```
project/
├── services/
│   ├── __init__.py
│   ├── grammar.py         # Modelo de gramática + persistencia JSON
│   ├── parser_cyk.py      # Parser CYK para Gramáticas Libres de Contexto
│   ├── parser_regular.py  # Parser para Gramáticas Regulares
│   ├── generator.py       # Generador de cadenas (BFS)
│   └── tree.py            # Estructura de árbol de derivación
├── ui/
│   ├── __init__.py
│   └── main.py            # Interfaz gráfica (Tkinter)
├── tests/
│   ├── test_parser.py     # Tests unitarios
│   └── test_generator.py  # Tests del generador
├── examples/
│   ├── ejemplo_cnf.json       # Gramática en CNF
│   ├── ejemplo_regular.json   # Gramática regular
│   └── ejemplo_aritmetico.json # Expresiones aritméticas
├── requirements.txt
└── README.md
```

---

## 💿 Instalación

### Paso 1: Clonar/Descargar el Proyecto

Si tienes Git:

```bash
git clone <URL_DEL_REPOSITORIO>
cd project
```

O descarga el ZIP y descomprímelo.

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:

- **ttkbootstrap** - Framework moderno con tema Bootstrap (morph theme)
- Cualquier otra dependencia necesaria

---

## ▶️ Ejecución

### Opción 1: Ejecutar Interfaz Gráfica (Recomendado)

Desde la raíz del proyecto:

```bash
python run.py
```

Se abrirá una ventana con interfaz moderna con **tema oscuro Bootstrap**:

- **Interfaz moderna y profesional** con tema "morph" de ttkbootstrap
- **Botones con estilos Bootstrap** (colores info, success, primary, warning, danger)
- **Barra de estado** para mensajes de retroalimentación
- **Tres pestañas funcionales** con diseño optimizado

O si estás en la carpeta `ui`:

```bash
cd ui
python main.py
```

### Opción 2: Ejecutar Tests

Para verificar que todo funciona:

```bash
pytest tests/
```

O ejecutar los tests específicos:

```bash
python tests/test_parser.py
python tests/test_generator.py
```

Deberías ver:

```
✅ test_generator_simple pasado
✅ test_cnf_check pasado
✅ test_cyk_simple pasado
✅ test_grammar_validation pasado
... (47 tests total)

🎉 Todos los tests pasaron correctamente
```

### Opción 3: Usar como Módulo

```python
from services.grammar import Grammar
from services.parser_cyk import cyk_parse
from services.generator import generate_shortest

# Cargar gramática
g = Grammar.load("examples/ejemplo_cnf.json")

# Parsear cadena
aceptada, back = cyk_parse(g, ["a", "b"])
print(f"¿Aceptada?: {aceptada}")

# Generar cadenas
cadenas = generate_shortest(g, limit=10)
print(f"Cadenas generadas: {cadenas}")
```

---

## 📖 Uso de la Aplicación

### 1️⃣ Pestaña "📝 Gramática"

#### **Cargar Gramática Existente**

1. Click en **[📂 Cargar Gramática (JSON)]**
2. Selecciona un archivo `.json` (ejemplos en carpeta `examples/`)
3. La gramática se mostrará en el área de texto

#### **Crear Nueva Gramática**

1. Click en **[➕ Nueva Gramática]**
2. En el diálogo:
   - Selecciona tipo: **Tipo 2** o **Tipo 3**
   - Ingresa símbolo inicial (ej: `S`)
   - Ingresa no terminales separados por coma (ej: `S,A,B`)
   - Ingresa terminales separados por coma (ej: `a,b`)
   - Define producciones (una por línea):
     ```
     S->AB
     A->a
     B->b
     ```
3. Click en **[Crear]**

#### **Validar Gramática**

1. Click en **[✓ Validar]**
2. Se mostrará si:
   - La gramática es válida
   - Está en CNF (necesario para CYK)
   - Es regular válida

#### **Guardar Gramática**

1. Click en **[💾 Guardar Gramática]**
2. Elige ubicación y nombre del archivo
3. Se guardará en formato JSON

---

### 2️⃣ Pestaña "🔍 Parser"

#### **Parsear una Cadena**

1. Ingresa la cadena en el campo de texto
   - **Importante:** Separa tokens con espacios
   - Ejemplo: `a b` para la cadena "ab"
   - Ejemplo: `id + id * id` para expresiones
2. Selecciona algoritmo:
   - **Auto-detectar:** Usa el tipo de la gramática
   - **CYK:** Para Tipo 2 (debe estar en CNF)
   - **Regular:** Para Tipo 3
3. Click en **[🔍 Parsear]**

#### **Resultado**

- Muestra si la cadena fue **✓ ACEPTADA** o **✗ RECHAZADA**
- Si fue aceptada (y usas CYK), muestra el **Árbol de Derivación**
- Para gramáticas regulares, muestra los **Pasos de Derivación**

#### **Exportar Árbol**

1. Después de parsear una cadena aceptada
2. Click en **[💾 Exportar Árbol]**
3. Se guardará como archivo `.txt`

---

### 3️⃣ Pestaña "⚡ Generador"

#### **Generar Cadenas**

1. Configura parámetros:
   - **Número de cadenas:** Cuántas generar (máx 50)
   - **Profundidad máxima:** Límite de expansión
2. Click en **[⚡ Generar Cadenas]**
3. Se mostrarán las cadenas **más cortas** generadas por BFS

#### **Exportar Cadenas**

1. Después de generar cadenas
2. Click en **[💾 Exportar Cadenas]**
3. Se guardará como archivo `.txt`

---

## 📝 Ejemplos

### Ejemplo 1: Gramática Simple en CNF

**Archivo:** `examples/ejemplo_cnf.json`

```json
{
  "type": "type2",
  "N": ["S", "A", "B"],
  "T": ["a", "b"],
  "S": "S",
  "P": [
    { "left": "S", "right": ["A", "B"] },
    { "left": "A", "right": ["a"] },
    { "left": "B", "right": ["b"] }
  ]
}
```

**Lenguaje:** L = {ab}

**Probar:**

- Cadena: `a b` → ✓ Aceptada
- Cadena: `a a` → ✗ Rechazada

---

### Ejemplo 2: Gramática Regular

**Archivo:** `examples/ejemplo_regular.json`

```json
{
  "type": "type3",
  "N": ["S", "A"],
  "T": ["a", "b"],
  "S": "S",
  "P": [
    { "left": "S", "right": ["a", "A"] },
    { "left": "A", "right": ["b", "A"] },
    { "left": "A", "right": ["b"] }
  ]
}
```

**Lenguaje:** L = {ab+} (a seguida de una o más b's)

**Probar:**

- `a b` → ✓ Aceptada
- `a b b` → ✓ Aceptada
- `a b b b` → ✓ Aceptada
- `a a` → ✗ Rechazada

---

### Ejemplo 3: Expresiones Aritméticas (CNF)

**Archivo:** `examples/ejemplo_aritmetico.json`

```json
{
  "type": "type2",
  "N": ["E", "T", "F", "P1", "M1"],
  "T": ["id", "+", "*"],
  "S": "E",
  "P": [
    { "left": "E", "right": ["E", "P1"] },
    { "left": "E", "right": ["T"] },
    { "left": "P1", "right": ["+", "T"] },
    { "left": "T", "right": ["T", "M1"] },
    { "left": "T", "right": ["F"] },
    { "left": "M1", "right": ["*", "F"] },
    { "left": "F", "right": ["id"] }
  ]
}
```

**Lenguaje:** Expresiones aritméticas simples

**Probar:**

- `id` → ✓ Aceptada
- `id + id` → ✓ Aceptada
- `id * id + id` → ✓ Aceptada

---

## 🐛 Solución de Problemas

### ❌ Error: "No module named 'services'"

**Causa:** Estás ejecutando desde la carpeta incorrecta.

**Solución:**

```bash
# Asegúrate de estar en la raíz del proyecto
cd /ruta/al/project
python ui/main.py
```

O agrega el path:

```python
import sys
sys.path.append('..')
```

---

### ❌ Error: "La gramática debe estar en CNF para usar CYK"

**Causa:** Intentas usar CYK con una gramática que no está en Forma Normal de Chomsky.

**Solución:**

1. Valida la gramática: Click en **[✓ Validar]**
2. Si no está en CNF, debes:
   - Convertirla manualmente a CNF
   - O usar un parser diferente

**Conversión manual a CNF (ejemplo):**

❌ **Original:** `S → aSb`

✅ **CNF:**

```
S → A1 B1
A1 → a
B1 → S1
S1 → S B2
B2 → b
```

---

### ❌ Error: "tkinter no está instalado"

**Solución en Linux:**

```bash
sudo apt-get install python3-tk
```

---

### ❌ La aplicación no muestra resultados al parsear

**Verificar:**

1. ¿Cargaste una gramática? (debe decir en la barra de estado)
2. ¿Separaste tokens con espacios? (`a b` no `ab`)
3. ¿La gramática está en CNF si usas CYK?

---

### ❌ El generador no produce cadenas

**Causas posibles:**

1. **Profundidad insuficiente:** Aumenta "Profundidad máxima" a 20-30
2. **Gramática recursiva infinita:** Verifica que existan producciones terminales
3. **Bug de indentación:** Asegúrate de usar el `generator.py` corregido

---

## 📚 Referencias

- **Teoría de Autómatas** - Hopcroft, Motwani, Ullman
- **Algoritmo CYK:** [Wikipedia](https://en.wikipedia.org/wiki/CYK_algorithm)
- **Forma Normal de Chomsky:** [Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)

---

## 👥 Autores

**UPTC - Ingeniería de Sistemas**  
Proyecto de Lenguajes Formales

---

## 📄 Licencia

Este proyecto es para uso académico en la UPTC.
