# Analizador Sintáctico de Gramáticas Formales

**Universidad Pedagógica y Tecnológica de Colombia - UPTC**  
**Asignatura:** Lenguajes Formales  
**Proyecto:** Parser y Generador para Gramáticas Tipo 2 y 3  
**Autores:** Mileth Martinez, Steven León y Natalia Bernal

---

## Características

### Interfaz

- **Tema Bootstrap claro** (morph) para un aspecto profesional y moderno
- Diseño intuitivo y organizadadp por pestañas
- Barra de estado con mensajes de retroalimentación en tiempo real
- Botones con estilos Bootstrap (info, success, primary, warning, danger)
- **Visualización con colores** en resultados de análisis y árboles de derivación

### Soporte de Gramáticas

- **Tipo 2 (GLC):** Gramáticas Libres de Contexto con soporte CNF
- **Tipo 3 (Regulares):** Gramáticas regulares
- Carga/guardado en formato JSON
- Validación automática de gramáticas
- Diálogo intuitivo para crear gramáticas desde cero

### Análisis Sintáctico

- **Algoritmo CYK:** Para gramáticas libres de contexto en CNF(Chomsky Normal Form: reglas solo de tipo A→BC o A→a)
- **Parser Regular:** Para gramáticas regulares (simulación de DFA)
- Auto-detección del tipo de gramática y algoritmo
- Generación de árboles de derivación con visualización coloreada
- Exportación de árboles a archivos de texto

### Generación de Cadenas

- Generador BFS con límites de profundidad y cantidad
- Obtención de cadenas más cortas del lenguaje
- Visualización ordenada por longitud
- Exportación de resultados a archivos

---

## Requisitos

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

**En macOS/Windows:** tkinter viene incluido por defecto.

---

## Estructura del Proyecto

```
project/
├── services/                    # Lógica de negocio
│   ├── __init__.py
│   ├── grammar.py              # Modelo de gramática + persistencia JSON
│   ├── parser_cyk.py           # Parser CYK para Gramáticas Libres de Contexto
│   ├── parser_regular.py       # Parser para Gramáticas Regulares
│   ├── generator.py            # Generador de cadenas (BFS)
│   └── tree.py                 # Estructura de árbol de derivación
│
├── ui/                          # Interfaz de usuario (modular)
│   ├── __init__.py
│   ├── main.py                 # Clase principal App + lógica de negocio UI
│   ├── grammar_tab.py          # Construcción de pestaña Gramática
│   ├── parser_tab.py           # Construcción de pestaña Parser
│   ├── generator_tab.py        # Construcción de pestaña Generador
│   └── utils.py                # Utilidades (guardar archivos, tags de color)
│
├── examples/                    # Ejemplos de gramáticas
│   ├── ejemplo_cnf.json        # Gramática en CNF
│   ├── ejemplo_regular.json    # Gramática regular
│   └── ejemplo_aritmetico.json # Expresiones aritméticas
│
├── run.py                       # Script principal de ejecución
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

---

## Instalación

### Paso 1: Clonar/Descargar el Proyecto

Si tienes Git:

```bash
git clone https://github.com/NatBernal/Grammar_Project
cd Grammar_Project
```

O descarga el ZIP y descomprímelo.

### Paso 2: Crear Entorno Virtual (Opcional)

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

## Ejecución

Desde la raíz del proyecto ejecute:

```bash
python run.py
```

Se abrirá una ventana con interfaz de la aplicación.

Además a continuación encontrará comandos útiles:

```bash
    python run.py           # Inicia la interfaz gráfica
    python run.py test      # Ejecuta los tests unitarios (47 tests)
    python run.py check     # Verifica el entorno
    python run.py help      # Muestra ayuda
```

---

## Uso de la Aplicación

### 1 Pestaña "Gramática"

#### **Cargar Gramática Existente**

1. Click en **[📂 Cargar Gramática (JSON)]**
2. Selecciona un archivo `.json` (ejemplos en carpeta `examples/`)
3. La gramática se mostrará en el área de texto
4. La barra de estado indicará el tipo de gramática cargada

#### **Crear Nueva Gramática**

1. Click en **[➕ Nueva Gramática]**
2. En el diálogo:
   - Selecciona tipo: **Tipo 2 (GLC)** o **Tipo 3 (Regular)**
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
   - Traducción del tipo al español

#### **Guardar Gramática**

1. Click en **[💾 Guardar Gramática]**
2. Elige ubicación y nombre del archivo
3. Se guardará en formato JSON

---

### 2️ Pestaña "🔍 Parser"

#### **Parsear una Cadena**

1. Ingresa la cadena en el campo de texto
   - **Para gramáticas simples:** Escribe la cadena directamente (ej: `aaaabb`)
   - **Para tokens compuestos:** Separa con espacios (ej: `id + id * id`)
2. Selecciona algoritmo:
   - **Auto-detectar:** Usa el tipo de la gramática (recomendado)
   - **CYK:** Para Tipo 2 (debe estar en CNF)
   - **Regular:** Para Tipo 3
3. Click en **[🔍 Parsear]**

#### **Resultado**

Se mostrará con colores:

- **Verde:** ✓ CADENA ACEPTADA
- **Rojo:** ✗ CADENA RECHAZADA
- **Azul:** Información de entrada (cadena, tokens, algoritmo)
- **Morado:** Nodos no terminales del árbol `[S]`
- **Verde azulado:** Nodos terminales del árbol `"a"`

Si la cadena fue aceptada:

- **Para CYK:** Muestra el árbol de derivación completo
- **Para Regular:** Muestra el árbol de derivación lineal

#### **Exportar Árbol**

1. Después de parsear una cadena aceptada
2. El botón **[💾 Exportar Árbol]** se habilitará automáticamente
3. Click para guardar como archivo `.txt`

---

### 3️ Pestaña "Generador"

#### **Generar Cadenas**

1. Configura parámetros:
   - **Número de cadenas:** Cuántas generar (máx 50)
   - **Profundidad máxima:** Límite de expansión (recomendado: 12-20)
2. Click en **[⚡ Generar Cadenas]**
3. Se mostrarán las cadenas **más cortas** generadas por BFS
4. Cada cadena incluye su longitud

Ejemplo de salida:

```
 1. "ab" (longitud: 2)
 2. "aabb" (longitud: 4)
 3. "aaabbb" (longitud: 6)
```

#### **Exportar Cadenas**

1. Después de generar cadenas
2. Click en **[💾 Exportar Cadenas]**
3. Se guardará como archivo `.txt`

---

## 🏗️ Arquitectura del Código

### Diseño Modular

El proyecto está organizado siguiendo el patrón de separación de responsabilidades:

#### **Capa de Servicios (`services/`)**

- Contiene la lógica de negocio pura
- Independiente de la interfaz gráfica
- Reutilizable y testeable

#### **Capa de Interfaz (`ui/`)**

- **`main.py`**: Clase principal `App` que coordina toda la aplicación
  - Gestiona el estado (gramática, árbol actual)
  - Implementa toda la lógica de negocio de la UI
  - Se comunica con los servicios
- **`grammar_tab.py`**: Construye la pestaña de gramática
  - Función `build_grammar_tab(app, parent)`
  - Crea widgets y los enlaza a `app`
- **`parser_tab.py`**: Construye la pestaña de parser
  - Función `build_parser_tab(app, parent)`
  - Configura visualización con colores
- **`generator_tab.py`**: Construye la pestaña de generador
  - Función `build_generator_tab(app, parent)`
- **`utils.py`**: Funciones auxiliares
  - `save_text_to_file()`: Guardar contenido
  - `configure_result_text_tags()`: Configurar colores

### Flujo de Datos

```
Usuario → UI (main.py) → Services → Resultados → UI
```

**Ejemplo de parseo:**

1. Usuario ingresa cadena en `parser_tab.py`
2. `parser_tab.py` llama a `app.parse_string()`
3. `main.py` procesa y llama a `cyk_parse()` o `parse_regular()`
4. `services/` retorna resultados
5. `main.py` actualiza la interfaz con colores

---

## Solución de Problemas

### Error: "La gramática debe estar en CNF para usar CYK"

**Causa:** Intentas usar CYK con una gramática que no está en Forma Normal de Chomsky.

**Solución:**

1. Valida la gramática: Click en **[✓ Validar]**
2. Si no está en CNF, debes convertirla manualmente o usar parser regular

**Forma Normal de Chomsky requiere:**

- Producciones de la forma: `A → BC` (dos no terminales)
- O: `A → a` (un terminal)
- No producciones epsilon (excepto S)

---

### Error: "tkinter no está instalado"

**Solución en Linux:**

```bash
sudo apt-get install python3-tk
```

---

### La aplicación no muestra resultados al parsear

**Verificar:**

1. ¿Cargaste una gramática? (debe decir en la barra de estado)
2. ¿La gramática está en CNF si usas CYK?
3. ¿Los tokens coinciden con los terminales de la gramática?

---

### El árbol no se exporta

**Causa:** El botón de exportar está deshabilitado.

**Solución:**

- Solo se habilita después de parsear una cadena **aceptada**
- Verifica que la cadena fue aceptada (texto en verde)

---

### El generador no produce cadenas

**Causas posibles:**

1. **Profundidad insuficiente:** Aumenta "Profundidad máxima" a 20-30
2. **Gramática recursiva infinita:** Verifica que existan producciones terminales
3. **Gramática sin cadenas cortas:** Algunas gramáticas solo generan cadenas largas

---

## Referencias

- **Teoría de Autómatas** - Hopcroft, Motwani, Ullman
- **Algoritmo CYK:** [Wikipedia](https://en.wikipedia.org/wiki/CYK_algorithm)
- **Forma Normal de Chomsky:** [Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
- **ttkbootstrap:** [Documentación oficial](https://ttkbootstrap.readthedocs.io/)

---

## 👥 Autores

**UPTC - Ingeniería de Sistemas**  
**Mileth Martinez, Steven León y Natalia Bernal**  
Proyecto de Lenguajes Formales

---

## 📄 Licencia

Este proyecto es para uso académico en la UPTC.
