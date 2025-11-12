import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from services.grammar import Grammar
from services.parser_cyk import cyk_parse, reconstruct_tree, is_cnf
from services.parser_regular import parse_regular, validate_regular_grammar
from services.generator import generate_shortest
from services.tree import TreeNode


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Analizador Sintáctico de Gramáticas - UPTC")
        self.geometry("1100x700")
        self.grammar = None
        self.configure(bg="#f0f0f0")
        self._build_ui()

    def _build_ui(self):
        """Construye la interfaz completa."""
        # Frame principal con notebook (tabs)
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Crear notebook para organizar funcionalidades
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        # TAB 1: Definir/Cargar Gramática
        tab_grammar = ttk.Frame(notebook, padding="10")
        notebook.add(tab_grammar, text="📝 Gramática")
        self._build_grammar_tab(tab_grammar)

        # TAB 2: Parser (Análisis)
        tab_parser = ttk.Frame(notebook, padding="10")
        notebook.add(tab_parser, text="🔍 Parser")
        self._build_parser_tab(tab_parser)

        # TAB 3: Generador de Cadenas
        tab_generator = ttk.Frame(notebook, padding="10")
        notebook.add(tab_generator, text="⚡ Generador")
        self._build_generator_tab(tab_generator)

        # Barra de estado
        self.status_bar = tk.Label(
            self, 
            text="No hay gramática cargada", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="#e0e0e0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _build_grammar_tab(self, parent):
        """Tab para definir y cargar gramáticas."""
        # Frame superior: botones
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(
            top_frame, 
            text="📂 Cargar Gramática (JSON)", 
            command=self.load_grammar
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="💾 Guardar Gramática", 
            command=self.save_grammar
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="➕ Nueva Gramática", 
            command=self.new_grammar_dialog
        ).pack(side="left", padx=5)

        ttk.Button(
            top_frame, 
            text="✓ Validar", 
            command=self.validate_grammar
        ).pack(side="left", padx=5)

        # Frame central: mostrar gramática
        ttk.Label(parent, text="Gramática Actual:", font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.grammar_display = scrolledtext.ScrolledText(
            parent, 
            height=25, 
            font=("Courier", 10),
            bg="#ffffff",
            wrap=tk.WORD
        )
        self.grammar_display.pack(fill="both", expand=True, pady=5)
        self.grammar_display.insert("1.0", "No hay gramática cargada. Use 'Cargar' o 'Nueva Gramática'.")
        self.grammar_display.config(state="disabled")

    def _build_parser_tab(self, parent):
        """Tab para parsear cadenas."""
        # Frame de entrada
        input_frame = ttk.LabelFrame(parent, text="Entrada", padding="10")
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Cadena (tokens separados por espacio):").grid(row=0, column=0, sticky="w")
        self.entry_parse = ttk.Entry(input_frame, width=60, font=("Arial", 10))
        self.entry_parse.grid(row=0, column=1, padx=10, sticky="ew")

        ttk.Button(
            input_frame, 
            text="🔍 Parsear", 
            command=self.parse_string
        ).grid(row=0, column=2)

        input_frame.columnconfigure(1, weight=1)

        # Tipo de parser
        parser_frame = ttk.Frame(input_frame)
        parser_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="w")
        
        ttk.Label(parser_frame, text="Algoritmo:").pack(side="left", padx=(0, 10))
        self.parser_var = tk.StringVar(value="auto")
        ttk.Radiobutton(parser_frame, text="Auto-detectar", variable=self.parser_var, value="auto").pack(side="left", padx=5)
        ttk.Radiobutton(parser_frame, text="CYK (Tipo 2)", variable=self.parser_var, value="cyk").pack(side="left", padx=5)
        ttk.Radiobutton(parser_frame, text="Regular (Tipo 3)", variable=self.parser_var, value="regular").pack(side="left", padx=5)

        # Frame de resultado
        result_frame = ttk.LabelFrame(parent, text="Resultado del Análisis", padding="10")
        result_frame.pack(fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, 
            height=20, 
            font=("Courier", 10),
            bg="#f9f9f9"
        )
        self.result_text.pack(fill="both", expand=True)

        # Botón para exportar árbol
        ttk.Button(
            result_frame, 
            text="💾 Exportar Árbol", 
            command=self.export_tree
        ).pack(pady=(5, 0))

    def _build_generator_tab(self, parent):
        """Tab para generar cadenas."""
        # Controles
        control_frame = ttk.LabelFrame(parent, text="Parámetros", padding="10")
        control_frame.pack(fill="x", pady=(0, 10))

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
            command=self.generate_strings
        ).grid(row=0, column=4, padx=10)

        # Resultados
        result_frame = ttk.LabelFrame(parent, text="Cadenas Generadas", padding="10")
        result_frame.pack(fill="both", expand=True)

        self.gen_text = scrolledtext.ScrolledText(
            result_frame, 
            height=20, 
            font=("Courier", 10),
            bg="#f9f9f9"
        )
        self.gen_text.pack(fill="both", expand=True)

        # Botón exportar
        ttk.Button(
            result_frame, 
            text="💾 Exportar Cadenas", 
            command=self.export_strings
        ).pack(pady=(5, 0))

    # ============ MÉTODOS DE GRAMÁTICA ============

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
            self.status_bar.config(text=f"✓ Gramática cargada: {path}")
            messagebox.showinfo("Éxito", f"Gramática cargada correctamente.\nTipo: {self.grammar.type}\nSímbolo inicial: {self.grammar.S}")
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
        dialog = tk.Toplevel(self)
        dialog.title("Nueva Gramática")
        dialog.geometry("500x450")
        dialog.transient(self)
        dialog.grab_set()

        # Tipo
        ttk.Label(dialog, text="Tipo de Gramática:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        type_var = tk.StringVar(value="type2")
        ttk.Radiobutton(dialog, text="Tipo 2 (GLC)", variable=type_var, value="type2").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(dialog, text="Tipo 3 (Regular)", variable=type_var, value="type3").grid(row=0, column=2, sticky="w")

        # Símbolo inicial
        ttk.Label(dialog, text="Símbolo Inicial (S):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        s_entry = ttk.Entry(dialog, width=30)
        s_entry.insert(0, "S")
        s_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10)

        # No terminales
        ttk.Label(dialog, text="No Terminales (separados por coma):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        n_entry = ttk.Entry(dialog, width=30)
        n_entry.insert(0, "S,A,B")
        n_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10)

        # Terminales
        ttk.Label(dialog, text="Terminales (separados por coma):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        t_entry = ttk.Entry(dialog, width=30)
        t_entry.insert(0, "a,b")
        t_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10)

        # Producciones
        ttk.Label(dialog, text="Producciones (una por línea, formato: A->aB):").grid(row=4, column=0, sticky="nw", padx=10, pady=5)
        p_text = tk.Text(dialog, height=10, width=40)
        p_text.insert("1.0", "S->AB\nA->a\nB->b")
        p_text.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10)

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

        ttk.Button(dialog, text="Crear", command=create_grammar).grid(row=5, column=1, pady=10)
        ttk.Button(dialog, text="Cancelar", command=dialog.destroy).grid(row=5, column=2, pady=10)

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
        
        tokens = text.split()
        self.result_text.delete("1.0", "end")
        
        try:
            parser_type = self.parser_var.get()
            
            # Auto-detectar
            if parser_type == "auto":
                parser_type = "regular" if self.grammar.type == "type3" else "cyk"
            
            self.result_text.insert("end", f"═══════════════════════════════════════\n")
            self.result_text.insert("end", f"ANÁLISIS SINTÁCTICO\n")
            self.result_text.insert("end", f"═══════════════════════════════════════\n\n")
            self.result_text.insert("end", f"Cadena: {text}\n")
            self.result_text.insert("end", f"Tokens: {tokens}\n")
            self.result_text.insert("end", f"Parser: {parser_type.upper()}\n\n")
            
            if parser_type == "cyk":
                self._parse_cyk(tokens)
            else:
                self._parse_regular(tokens)
                
        except NotImplementedError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el parsing:\n{str(e)}")

    def _parse_cyk(self, tokens):
        """Parser CYK para Tipo 2."""
        acept, back = cyk_parse(self.grammar, tokens)
        
        self.result_text.insert("end", "─────────────────────────────────────\n")
        self.result_text.insert("end", f"RESULTADO: {'✓ ACEPTADA' if acept else '✗ RECHAZADA'}\n")
        self.result_text.insert("end", "─────────────────────────────────────\n\n")
        
        if acept:
            self.result_text.insert("end", f"Backpointers generados: {len(back)}\n\n")
            
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
            
            self.result_text.insert("end", "ÁRBOL DE DERIVACIÓN:\n")
            self.result_text.insert("end", "═══════════════════════════════════════\n")
            self.result_text.insert("end", self.current_tree.to_text())
        else:
            self.result_text.insert("end", "No se puede generar árbol para cadena rechazada.\n")
            self.current_tree = None

    def _parse_regular(self, tokens):
        """Parser para gramáticas regulares."""
        acept, derivation = parse_regular(self.grammar, tokens)
        
        self.result_text.insert("end", "─────────────────────────────────────\n")
        self.result_text.insert("end", f"RESULTADO: {'✓ ACEPTADA' if acept else '✗ RECHAZADA'}\n")
        self.result_text.insert("end", "─────────────────────────────────────\n\n")
        
        if derivation:
            self.result_text.insert("end", "PASOS DE DERIVACIÓN:\n")
            for i, (symbol, prod) in enumerate(derivation, 1):
                self.result_text.insert("end", f"{i}. {prod}\n")
        
        self.current_tree = None

    def export_tree(self):
        """Exporta el árbol de derivación a archivo de texto."""
        if not hasattr(self, 'current_tree') or not self.current_tree:
            messagebox.showwarning("Advertencia", "No hay árbol para exportar.")
            return
        
        path = filedialog.asksaveasfilename(
            title="Exportar Árbol",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.current_tree.to_text())
            messagebox.showinfo("Éxito", "Árbol exportado correctamente.")
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
            
            self.gen_text.delete("1.0", "end")
            self.gen_text.insert("end", f"Generando hasta {limit} cadenas (profundidad máx: {depth})...\n\n")
            
            strings = generate_shortest(self.grammar, limit=limit, max_depth=depth)
            
            self.gen_text.insert("end", f"═══════════════════════════════════════\n")
            self.gen_text.insert("end", f"CADENAS GENERADAS: {len(strings)}\n")
            self.gen_text.insert("end", f"═══════════════════════════════════════\n\n")
            
            for i, s in enumerate(strings, 1):
                self.gen_text.insert("end", f"{i:2d}. \"{s}\" (longitud: {len(s)})\n")
            
            if len(strings) < limit:
                self.gen_text.insert("end", f"\n⚠ Solo se generaron {len(strings)} cadenas (puede aumentar profundidad).\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas:\n{str(e)}")

    def export_strings(self):
        """Exporta las cadenas generadas a archivo."""
        content = self.gen_text.get("1.0", "end").strip()
        if not content or "CADENAS GENERADAS" not in content:
            messagebox.showwarning("Advertencia", "No hay cadenas para exportar.")
            return
        
        path = filedialog.asksaveasfilename(
            title="Exportar Cadenas",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Éxito", "Cadenas exportadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()