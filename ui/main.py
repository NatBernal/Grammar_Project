import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, scrolledtext
from services.grammar import Grammar
from services.parser_cyk import cyk_parse, reconstruct_tree, is_cnf
from services.parser_regular import parse_regular, validate_regular_grammar
from services.generator import generate_shortest
from services.tree import TreeNode


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="morph")
        self.title("Analizador Sintáctico de Gramáticas - By Mile, Steven y Nata")
        self.geometry("1000x550")
        self.grammar = None
        self.current_tree = None  # Inicializar el árbol
        self._build_ui()

    def _build_ui(self):
        """Construye la interfaz completa."""
        # Frame principal con notebook (tabs)
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Crear notebook para organizar funcionalidades con altura fija
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # TAB 1: Definir/Cargar Gramática
        tab_grammar = ttk.Frame(notebook, padding="10")
        notebook.add(tab_grammar, text="Gramática")
        self._build_grammar_tab(tab_grammar)

        # TAB 2: Parser (Análisis)
        tab_parser = ttk.Frame(notebook, padding="10")
        notebook.add(tab_parser, text="Parser")
        self._build_parser_tab(tab_parser)

        # TAB 3: Generador de Cadenas
        tab_generator = ttk.Frame(notebook, padding="10")
        notebook.add(tab_generator, text="Generador")
        self._build_generator_tab(tab_generator)

        # Barra de estado
        self.status_bar = ttk.Label(self, text="Listo", relief="sunken", padding="5")
        self.status_bar.pack(fill="x", side="bottom")

    def _build_grammar_tab(self, parent):
        """Tab para definir y cargar gramáticas."""
        # Frame superior: botones
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            top_frame, 
            text="📂 Cargar Gramática (JSON)", 
            command=self.load_grammar,
            bootstyle="info"
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="💾 Guardar Gramática", 
            command=self.save_grammar,
            bootstyle="success"
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="➕ Nueva Gramática", 
            command=self.new_grammar_dialog,
            bootstyle="primary"
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="✓ Validar", 
            command=self.validate_grammar,
            bootstyle="warning"
        ).pack(side="left", padx=5)

        # Frame central: mostrar gramática
        label = ttk.Label(parent, text="Gramática Actual:", font=("Arial", 11, "bold"))
        label.pack(anchor="w")
        
        self.grammar_display = scrolledtext.ScrolledText(
            parent, 
            height=20, 
            font=("Courier", 10),
            wrap="word"
        )
        self.grammar_display.pack(fill="both", expand=True, pady=5)
        self.grammar_display.insert("1.0", "No hay gramática cargada. Use 'Cargar' o 'Nueva Gramática'.")
        self.grammar_display.config(state="disabled")

    def _build_parser_tab(self, parent):
        """Tab para parsear cadenas."""
        # Frame de entrada con título
        input_frame_outer = ttk.Frame(parent)
        input_frame_outer.pack(fill="x", pady=(0, 10))
        ttk.Label(input_frame_outer, text="Entrada", font=("Arial", 11, "bold")).pack(anchor="w", padx=5, pady=(5, 0))
        
        input_frame = ttk.Frame(parent, padding="10")
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Cadena:").grid(row=0, column=0, sticky="w")
        self.entry_parse = ttk.Entry(input_frame, width=60)
        self.entry_parse.grid(row=0, column=1, padx=10, sticky="ew")

        ttk.Button(
            input_frame, 
            text="🔍 Parsear", 
            command=self.parse_string,
            bootstyle="info"
        ).grid(row=0, column=2)

        input_frame.columnconfigure(1, weight=1)

        # Tipo de parser
        parser_frame = ttk.Frame(input_frame)
        parser_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="w")
        
        ttk.Label(parser_frame, text="Algoritmo:").pack(side="left", padx=(0, 10))
        self.parser_var = ttk.StringVar(value="auto")
        ttk.Radiobutton(parser_frame, text="Auto-detectar", variable=self.parser_var, value="auto").pack(side="left", padx=5)
        ttk.Radiobutton(parser_frame, text="CYK (Tipo 2)", variable=self.parser_var, value="cyk").pack(side="left", padx=5)
        ttk.Radiobutton(parser_frame, text="Regular (Tipo 3)", variable=self.parser_var, value="regular").pack(side="left", padx=5)

        # Frame de resultado con botón en la parte superior
        result_frame_outer = ttk.Frame(parent)
        result_frame_outer.pack(fill="both", expand=True)
        
        # Frame para el título y el botón en la misma línea
        title_frame = ttk.Frame(result_frame_outer)
        title_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        ttk.Label(title_frame, text="Resultado del Análisis", font=("Arial", 11, "bold")).pack(side="left")
        
        self.export_tree_btn = ttk.Button(
            title_frame, 
            text="💾 Exportar Árbol", 
            command=self.export_tree,
            bootstyle="success",
            state="disabled"  # Inicialmente deshabilitado
        )
        self.export_tree_btn.pack(side="right", padx=5)
        
        result_frame = ttk.Frame(result_frame_outer, padding="10")
        result_frame.pack(fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, 
            height=15, 
            font=("Courier", 10)
        )
        self.result_text.pack(fill="both", expand=True)
        
        # Configurar tags para colores
        self._configure_text_tags()

    def _configure_text_tags(self):
        """Configura los tags de color para el texto de resultados."""
        # Tag para encabezados
        self.result_text.tag_config("header", foreground="#2c3e50", font=("Arial", 11, "bold"))
        
        # Tag para éxito (verde)
        self.result_text.tag_config("success", foreground="#27ae60", font=("Courier", 10, "bold"))
        
        # Tag para rechazo (rojo)
        self.result_text.tag_config("error", foreground="#e74c3c", font=("Courier", 10, "bold"))
        
        # Tag para información (azul)
        self.result_text.tag_config("info", foreground="#3498db", font=("Courier", 10))
        
        # Tag para separadores
        self.result_text.tag_config("separator", foreground="#95a5a6", font=("Courier", 10))
        
        # Tag para nodos del árbol
        self.result_text.tag_config("tree_node", foreground="#8e44ad", font=("Courier", 10, "bold"))
        
        # Tag para terminales del árbol
        self.result_text.tag_config("tree_terminal", foreground="#16a085", font=("Courier", 10))
        
        # Tag para derivaciones
        self.result_text.tag_config("derivation", foreground="#2980b9", font=("Courier", 10))

    def _build_generator_tab(self, parent):
        """Tab para generar cadenas."""
        # Controles
        control_frame_outer = ttk.Frame(parent)
        control_frame_outer.pack(fill="x", pady=(0, 10))
        ttk.Label(control_frame_outer, text="Parámetros", font=("Arial", 11, "bold")).pack(anchor="w", padx=5, pady=(5, 0))
        
        control_frame = ttk.Frame(control_frame_outer, padding="10")
        control_frame.pack(fill="x")

        ttk.Label(control_frame, text="Número de cadenas:").grid(row=0, column=0, sticky="w", padx=5)
        self.gen_limit = ttk.Spinbox(control_frame, from_=1, to=50, width=10)
        self.gen_limit.set(10)
        self.gen_limit.grid(row=0, column=1, padx=5)

        ttk.Label(control_frame, text="Profundidad máxima:").grid(row=0, column=2, sticky="w", padx=5)
        self.gen_depth = ttk.Spinbox(control_frame, from_=5, to=30, width=10)
        self.gen_depth.set(12)
        self.gen_depth.grid(row=0, column=3, padx=5)

        ttk.Button(
            control_frame, 
            text="⚡ Generar Cadenas", 
            command=self.generate_strings,
            bootstyle="primary"
        ).grid(row=0, column=4, padx=10)

        # Frame de resultado con botón en la parte superior
        result_frame_outer = ttk.Frame(parent)
        result_frame_outer.pack(fill="both", expand=True)
        
        # Frame para el título y el botón en la misma línea
        title_frame = ttk.Frame(result_frame_outer)
        title_frame.pack(fill="x", padx=5, pady=(5, 0))
        
        ttk.Label(title_frame, text="Cadenas Generadas", font=("Arial", 11, "bold")).pack(side="left")
        
        ttk.Button(
            title_frame, 
            text="💾 Exportar Cadenas", 
            command=self.export_strings,
            bootstyle="success"
        ).pack(side="right", padx=5)
        
        result_frame = ttk.Frame(result_frame_outer, padding="10")
        result_frame.pack(fill="both", expand=True)

        self.gen_text = scrolledtext.ScrolledText(
            result_frame, 
            height=20, 
            font=("Courier", 10)
        )
        self.gen_text.pack(fill="both", expand=True)

    # ============ MÉTODOS DE GRAMÁTICA ============

    def _traducir_tipo_gramatica(self, tipo):
        """Traduce el tipo de gramática a español."""
        traducciones = {
            "type0": "Tipo 0 (Sin restricciones)",
            "type1": "Tipo 1 (Sensible al contexto)",
            "type2": "Tipo 2 (Libre de contexto / GLC)",
            "type3": "Tipo 3 (Regular)"
        }
        return traducciones.get(tipo, tipo)
    
    def load_grammar(self):
        """Carga una gramática desde archivo JSON."""
        path = filedialog.askopenfilename(
            title="Cargar Gramática",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        
        try:
            self.grammar = Grammar.load(path)
            self.update_grammar_display()
            tipo_texto = self._traducir_tipo_gramatica(self.grammar.type)
            self.status_bar.config(text=f"✓ Gramática cargada: {path}")
            messagebox.showinfo("Éxito", f"Gramática cargada correctamente.\nTipo: {tipo_texto}\nSímbolo inicial: {self.grammar.S}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la gramática:\n{str(e)}")

    def save_grammar(self):
        """Guarda la gramática actual a archivo JSON."""
        if not self.grammar:
            messagebox.showwarning("Advertencia", "No hay gramática para guardar.")
            return
        
        path = filedialog.asksaveasfilename(
            title="Guardar Gramática",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        
        try:
            self.grammar.save(path)
            self.status_bar.config(text=f"✓ Gramática guardada: {path}")
            messagebox.showinfo("Éxito", "Gramática guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")

    def new_grammar_dialog(self):
        """Abre diálogo para crear una nueva gramática."""
        dialog = ttk.Toplevel(self)
        dialog.title("Nueva Gramática")
        dialog.geometry("900x600")
        dialog.resizable(True, True)
        dialog.minsize(700, 500)
        
        # Frame principal con padding
        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill="both", expand=True)

        # Tipo
        ttk.Label(main_frame, text="Tipo de Gramática:").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        type_var = ttk.StringVar(value="type2")
        ttk.Radiobutton(main_frame, text="Tipo 2 (GLC)", variable=type_var, value="type2").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(main_frame, text="Tipo 3 (Regular)", variable=type_var, value="type3").grid(row=0, column=2, sticky="w", padx=5)

        # Símbolo inicial
        ttk.Label(main_frame, text="Símbolo Inicial (S):").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        s_entry = ttk.Entry(main_frame, width=30)
        s_entry.insert(0, "S")
        s_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)

        # No terminales
        ttk.Label(main_frame, text="No Terminales (separados por coma):").grid(row=2, column=0, sticky="w", padx=5, pady=8)
        n_entry = ttk.Entry(main_frame, width=30)
        n_entry.insert(0, "S,A,B")
        n_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)

        # Terminales
        ttk.Label(main_frame, text="Terminales (separados por coma):").grid(row=3, column=0, sticky="w", padx=5, pady=8)
        t_entry = ttk.Entry(main_frame, width=30)
        t_entry.insert(0, "a,b")
        t_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5)

        # Producciones
        ttk.Label(main_frame, text="Producciones (una por línea, formato: A->aB):").grid(row=4, column=0, sticky="nw", padx=5, pady=8)
        p_text = scrolledtext.ScrolledText(main_frame, height=10, width=40, font=("Courier", 10))
        p_text.insert("1.0", "S->AB\nA->a\nB->b")
        p_text.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5)
        
        # Configurar pesos de grid para que se adapte al redimensionamiento
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        def create_grammar():
            try:
                S = s_entry.get().strip()
                N = [x.strip() for x in n_entry.get().split(",")]
                T = [x.strip() for x in t_entry.get().split(",")]
                
                # Parsear producciones
                P = []
                for line in p_text.get("1.0", "end").strip().split("\n"):
                    if "->" not in line:
                        continue
                    left, right = line.split("->")
                    left = left.strip()
                    right_symbols = list(right.strip())  # Cada carácter es un símbolo
                    P.append({"left": left, "right": right_symbols})
                
                self.grammar = Grammar(N, T, P, S, type_var.get())
                self.update_grammar_display()
                self.status_bar.config(text="✓ Nueva gramática creada")
                messagebox.showinfo("Éxito", "Gramática creada correctamente.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear gramática:\n{str(e)}")

        # Frame para botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=15)
        
        ttk.Button(button_frame, text="Crear", command=create_grammar, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="danger").pack(side="left", padx=5)

    def validate_grammar(self):
        """Valida la gramática actual."""
        if not self.grammar:
            messagebox.showwarning("Advertencia", "No hay gramática para validar.")
            return
        
        is_valid = self.grammar.validate()
        
        msg = "✓ La gramática es VÁLIDA.\n\n"
        if is_valid:
            # Verificar tipo específico
            if self.grammar.type == "type2":
                if is_cnf(self.grammar):
                    msg += "• Está en Forma Normal de Chomsky (CNF)\n"
                else:
                    msg += "• NO está en CNF (puede necesitar normalización para CYK)\n"
            elif self.grammar.type == "type3":
                if validate_regular_grammar(self.grammar):
                    msg += "• Es una gramática regular válida\n"
                else:
                    msg += "• ADVERTENCIA: No cumple formato regular estándar\n"
        else:
            msg = "✗ La gramática NO es válida.\n\nVerifique:\n"
            msg += "• S debe estar en N\n"
            msg += "• Lado izquierdo de producciones debe estar en N\n"
            msg += "• Símbolos del lado derecho deben estar en N o T\n"
        
        messagebox.showinfo("Validación", msg)

    def update_grammar_display(self):
        """Actualiza la visualización de la gramática."""
        self.grammar_display.config(state="normal")
        self.grammar_display.delete("1.0", "end")
        
        if self.grammar:
            self.grammar_display.insert("end", str(self.grammar))
        else:
            self.grammar_display.insert("end", "No hay gramática cargada.")
        
        self.grammar_display.config(state="disabled")

    # ============ MÉTODOS DE PARSER ============

    def parse_string(self):
        """Parsea una cadena de entrada."""
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Cargue una gramática primero.")
            return
        
        text = self.entry_parse.get().strip()
        if not text:
            messagebox.showwarning("Advertencia", "Ingrese una cadena para parsear.")
            return
        
        # Limpiar estado anterior
        self.current_tree = None
        self.export_tree_btn.config(state="disabled")
        
        # Convertir la cadena en tokens (cada carácter es un token)
        tokens = list(text)
        self.result_text.delete("1.0", "end")
        
        try:
            parser_type = self.parser_var.get()
            
            # Auto-detectar
            if parser_type == "auto":
                parser_type = "regular" if self.grammar.type == "type3" else "cyk"
            
            self._insert_with_tag("Cadena de entrada: ", "info")
            self.result_text.insert("end", f"\"{text}\"\n")
            
            self._insert_with_tag("Tokens: ", "info")
            self.result_text.insert("end", f"{tokens}\n")
            
            self._insert_with_tag("Algoritmo: ", "info")
            self.result_text.insert("end", f"{parser_type.upper()}\n\n")
            
            if parser_type == "cyk":
                self._parse_cyk(tokens)
            else:
                self._parse_regular(tokens)
                
        except NotImplementedError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el parsing:\n{str(e)}")

    def _insert_with_tag(self, text, tag):
        """Helper para insertar texto con un tag específico."""
        self.result_text.insert("end", text, tag)

    def _parse_cyk(self, tokens):
        """Parser CYK para Tipo 2."""
        acept, back = cyk_parse(self.grammar, tokens)
        
        if acept:
            self._insert_with_tag("Resultado: ✓ CADENA ACEPTADA\n\n", "success")
            
            try:
                # Reconstruir árbol
                tree_struct = reconstruct_tree(back, 0, len(tokens), self.grammar.S)
                
                def build(node):
                    symbol, children = node
                    child_nodes = []
                    for c in children:
                        if isinstance(c, tuple):
                            child_nodes.append(build(c))
                        else:
                            child_nodes.append(TreeNode(c))
                    return TreeNode(symbol, child_nodes)
                
                self.current_tree = build(tree_struct)
                
                # Habilitar botón de exportar
                self.export_tree_btn.config(state="normal")
                
                # Mostrar árbol con estilo

                self._insert_with_tag("\nÁrbol de derivación:\n", "header")
                
                # Insertar árbol con colores
                self._insert_tree_colored(self.current_tree)
                
            except Exception as e:
                print(f"ERROR al construir árbol: {e}")
                import traceback
                traceback.print_exc()
                self._insert_with_tag(f"\n⚠️ Error al construir el árbol: {e}\n", "error")
                self.current_tree = None
                self.export_tree_btn.config(state="disabled")
        else:
            self._insert_with_tag("Resultado: ✗ CADENA RECHAZADA\n\n", "error")
            self._insert_with_tag("❌ La cadena no pertenece al lenguaje generado por la gramática.\n", "info")
            self._insert_with_tag("   No se puede construir un árbol de derivación.\n", "info")
            self.current_tree = None
            self.export_tree_btn.config(state="disabled")

    def _insert_tree_colored(self, node, indent=0, is_last=True, prefix=""):
        """Inserta el árbol con colores en el texto."""
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        
        # Insertar prefijo
        self._insert_with_tag(prefix + connector, "separator")
        
        # Insertar símbolo con color
        if node.is_leaf():
            self._insert_with_tag(f'"{node.symbol}"', "tree_terminal")
        else:
            self._insert_with_tag(f'[{node.symbol}]', "tree_node")
        
        self.result_text.insert("end", "\n")
        
        # Procesar hijos
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            if isinstance(child, TreeNode):
                self._insert_tree_colored(child, indent + 1, is_last_child, prefix + extension)
            else:
                # Nodo terminal
                child_connector = "└── " if is_last_child else "├── "
                self._insert_with_tag(prefix + extension + child_connector, "separator")
                self._insert_with_tag(f'"{child}"', "tree_terminal")
                self.result_text.insert("end", "\n")

    def _parse_regular(self, tokens):
        """Parser para gramáticas regulares."""
        acept, derivation = parse_regular(self.grammar, tokens)
        
        if acept:
            self._insert_with_tag("Resultado: ✓ CADENA ACEPTADA\n\n", "success")
            
            if derivation:
                
                # Construir árbol de derivación desde los pasos
                try:
                    self.current_tree = self._build_tree_from_derivation(derivation, tokens)
                    
                    if self.current_tree:
                        
                        # Habilitar botón de exportar
                        self.export_tree_btn.config(state="normal")
                        
                        # Mostrar árbol
                        self._insert_with_tag("Árbol de derivación:\n", "header")
                        
                        self._insert_tree_colored(self.current_tree)
                    else:
                        self.export_tree_btn.config(state="disabled")
                        
                except Exception as e:
                    print(f"ERROR al construir árbol regular: {e}")
                    import traceback
                    traceback.print_exc()
                    self.current_tree = None
                    self.export_tree_btn.config(state="disabled")
            else:
                self.current_tree = None
                self.export_tree_btn.config(state="disabled")
        else:
            self._insert_with_tag("Resultado: ✗ CADENA RECHAZADA\n\n", "error")
            
            if derivation:
                self._insert_with_tag("Pasos de derivación:\n", "header")
                
                for i, (symbol, prod) in enumerate(derivation, 1):
                    self._insert_with_tag(f"Paso {i}: ", "info")
                    self._insert_with_tag(f"{prod}\n", "derivation")
            
            self.current_tree = None
            self.export_tree_btn.config(state="disabled")
    
    def _build_tree_from_derivation(self, derivation, tokens):
        """Construye un árbol de derivación desde los pasos de una gramática regular."""
        if not derivation:
            return None
        
        # Las gramáticas regulares tienen derivaciones lineales
        # Cada paso es (símbolo_actual, producción_aplicada)
        # Ejemplo: S → aA, A → aA, A → b
        
        # Comenzar con el símbolo inicial
        root_symbol = self.grammar.S
        current_node = TreeNode(root_symbol)
        root = current_node
        
        token_index = 0
        
        for step_num, (symbol, production) in enumerate(derivation):
            # Parsear la producción (ej: "S → aA" o "A → b")
            if " → " in production:
                left, right = production.split(" → ")
                right = right.strip()
                
                children = []
                
                # Procesar cada símbolo del lado derecho
                i = 0
                while i < len(right):
                    char = right[i]
                    
                    # Verificar si es un terminal
                    if char in self.grammar.T:
                        # Es un terminal
                        if token_index < len(tokens):
                            children.append(TreeNode(tokens[token_index]))
                            token_index += 1
                        else:
                            children.append(TreeNode(char))
                    elif char in self.grammar.N:
                        # Es un no terminal
                        # Si no es el último paso, será expandido después
                        if step_num < len(derivation) - 1:
                            next_node = TreeNode(char)
                            children.append(next_node)
                            current_node = next_node  # Este será expandido en el siguiente paso
                        else:
                            # Último paso, puede ser un no terminal final o epsilon
                            children.append(TreeNode(char))
                    
                    i += 1
                
                # Asignar hijos al nodo actual
                if step_num == 0:
                    root.children = children
                else:
                    current_node.children = children
        
        return root

    def export_tree(self):
        """Exporta el árbol de derivación como archivo de texto."""
        if self.current_tree is None:
            messagebox.showwarning("Advertencia", "No hay árbol para exportar.\nPrimero debe parsear una cadena aceptada con CYK.")
            return
        
        path = filedialog.asksaveasfilename(
            title="Guardar Árbol",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.current_tree.to_text())
            messagebox.showinfo("Éxito", f"Árbol exportado:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")

    # ============ MÉTODOS DE GENERADOR ============

    def generate_strings(self):
        """Genera cadenas usando BFS."""
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Cargue una gramática primero.")
            return
        
        try:
            limit = int(self.gen_limit.get())
            depth = int(self.gen_depth.get())
            
            # Limpiar resultados anteriores
            self.gen_text.delete("1.0", "end")
            
            strings = generate_shortest(self.grammar, limit=limit, max_depth=depth)

            for i, s in enumerate(strings, 1):
                self.gen_text.insert("end", f"{i:2d}. \"{s}\" (longitud: {len(s)})\n")
            
            if len(strings) < limit:
                self.gen_text.insert("end", f"\n⚠ Solo se generaron {len(strings)} cadenas (puede aumentar profundidad).\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas:\n{str(e)}")

    def export_strings(self):
        """Exporta las cadenas generadas a archivo."""
        content = self.gen_text.get("1.0", "end").strip()

        # Si no hay texto, no hay nada que exportar
        if not content:
            messagebox.showwarning("Advertencia", "No hay cadenas para exportar.")
            return
        
        # Filtrar líneas vacías
        lines = [line for line in content.splitlines() if line.strip() != ""]
        if not lines:
            messagebox.showwarning("Advertencia", "No hay cadenas para exportar.")
            return
        content_to_save = "\n".join(lines) + "\n"

        path = filedialog.asksaveasfilename(
            title="Exportar Cadenas",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content_to_save)
            messagebox.showinfo("Éxito", "Cadenas exportadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()