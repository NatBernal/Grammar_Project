import ttkbootstrap as ttk
from .grammar_tab import build_grammar_tab
from .parser_tab import build_parser_tab
from .generator_tab import build_generator_tab
from .utils import save_text_to_file

# services import (usados por la lógica)
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
        self.current_tree = None
        # variables que se crearán en cada tab
        self.entry_parse = None
        self.parser_var = None
        self.export_tree_btn = None
        self.result_text = None
        self.grammar_display = None
        self.gen_limit = None
        self.gen_depth = None
        self.gen_text = None

        self._build_ui()

    def _build_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill="both", expand=True)

        tab_grammar = ttk.Frame(notebook, padding="10")
        notebook.add(tab_grammar, text="Gramática")
        build_grammar_tab(self, tab_grammar)

        tab_parser = ttk.Frame(notebook, padding="10")
        notebook.add(tab_parser, text="Parser")
        build_parser_tab(self, tab_parser)

        tab_generator = ttk.Frame(notebook, padding="10")
        notebook.add(tab_generator, text="Generador")
        build_generator_tab(self, tab_generator)

        self.status_bar = ttk.Label(self, text="Listo", relief="sunken", padding="5")
        self.status_bar.pack(fill="x", side="bottom")

    # ---------- helpers ----------
    def _traducir_tipo_gramatica(self, tipo):
        traducciones = {
            "type0": "Tipo 0 (Sin restricciones)",
            "type1": "Tipo 1 (Sensible al contexto)",
            "type2": "Tipo 2 (Libre de contexto / GLC)",
            "type3": "Tipo 3 (Regular)"
        }
        return traducciones.get(tipo, tipo)

    def _insert_with_tag(self, text, tag):
        if self.result_text:
            self.result_text.insert("end", text, tag)

    # ---------- Gramática ----------
    def load_grammar(self):
        from tkinter import filedialog, messagebox
        path = filedialog.askopenfilename(title="Cargar Gramática", filetypes=[("JSON files","*.json"), ("All files","*.*")])
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
        from tkinter import filedialog, messagebox
        if not self.grammar:
            messagebox.showwarning("Advertencia", "No hay gramática para guardar.")
            return
        path = filedialog.asksaveasfilename(title="Guardar Gramática", defaultextension=".json", filetypes=[("JSON files","*.json"), ("All files","*.*")])
        if not path:
            return
        try:
            self.grammar.save(path)
            self.status_bar.config(text=f"✓ Gramática guardada: {path}")
            messagebox.showinfo("Éxito", "Gramática guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")

    def new_grammar_dialog(self):
        # reutiliza exactamente la implementación previa para el diálogo.
        # Para no repetir cientos de líneas aquí, llamo a una implementación inline:
        from tkinter import scrolledtext, messagebox, Toplevel
        dialog = Toplevel(self)
        dialog.title("Nueva Gramática")
        dialog.geometry("900x600")
        dialog.resizable(True, True)
        dialog.minsize(700, 500)

        main_frame = ttk.Frame(dialog, padding="15")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Tipo de Gramática:").grid(row=0, column=0, sticky="w", padx=5, pady=8)
        type_var = ttk.StringVar(value="type2")
        ttk.Radiobutton(main_frame, text="Tipo 2 (GLC)", variable=type_var, value="type2").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Radiobutton(main_frame, text="Tipo 3 (Regular)", variable=type_var, value="type3").grid(row=0, column=2, sticky="w", padx=5)

        ttk.Label(main_frame, text="Símbolo Inicial (S):").grid(row=1, column=0, sticky="w", padx=5, pady=8)
        s_entry = ttk.Entry(main_frame, width=30)
        s_entry.insert(0, "S")
        s_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)

        ttk.Label(main_frame, text="No Terminales (separados por coma):").grid(row=2, column=0, sticky="w", padx=5, pady=8)
        n_entry = ttk.Entry(main_frame, width=30)
        n_entry.insert(0, "S,A,B")
        n_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)

        ttk.Label(main_frame, text="Terminales (separados por coma):").grid(row=3, column=0, sticky="w", padx=5, pady=8)
        t_entry = ttk.Entry(main_frame, width=30)
        t_entry.insert(0, "a,b")
        t_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5)

        ttk.Label(main_frame, text="Producciones (una por línea, formato: A->aB):").grid(row=4, column=0, sticky="nw", padx=5, pady=8)
        p_text = scrolledtext.ScrolledText(main_frame, height=10, width=40, font=("Courier", 10))
        p_text.insert("1.0", "S->AB\nA->a\nB->b")
        p_text.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5)

        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        def create_grammar():
            try:
                S = s_entry.get().strip()
                N = [x.strip() for x in n_entry.get().split(",")]
                T = [x.strip() for x in t_entry.get().split(",")]

                P = []
                for line in p_text.get("1.0", "end").strip().split("\n"):
                    if "->" not in line:
                        continue
                    left, right = line.split("->")
                    left = left.strip()
                    right_symbols = list(right.strip())
                    P.append({"left": left, "right": right_symbols})

                self.grammar = Grammar(N, T, P, S, type_var.get())
                self.update_grammar_display()
                self.status_bar.config(text="✓ Nueva gramática creada")
                messagebox.showinfo("Éxito", "Gramática creada correctamente.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear gramática:\n{str(e)}")

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=15)

        ttk.Button(button_frame, text="Crear", command=create_grammar, bootstyle="success").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=dialog.destroy, bootstyle="danger").pack(side="left", padx=5)

    def validate_grammar(self):
        from tkinter import messagebox
        if not self.grammar:
            messagebox.showwarning("Advertencia", "No hay gramática para validar.")
            return

        is_valid = self.grammar.validate()

        msg = "✓ La gramática es VÁLIDA.\n\n"
        if is_valid:
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
        if not self.grammar_display:
            return
        self.grammar_display.config(state="normal")
        self.grammar_display.delete("1.0", "end")

        if self.grammar:
            self.grammar_display.insert("end", str(self.grammar))
        else:
            self.grammar_display.insert("end", "No hay gramática cargada.")

        self.grammar_display.config(state="disabled")

    # ---------- Parser ----------
    def parse_string(self):
        from tkinter import messagebox
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Cargue una gramática primero.")
            return

        text = self.entry_parse.get().strip()
        if not text:
            messagebox.showwarning("Advertencia", "Ingrese una cadena para parsear.")
            return

        self.current_tree = None
        if self.export_tree_btn:
            self.export_tree_btn.config(state="disabled")

        tokens = list(text)
        if self.result_text:
            self.result_text.delete("1.0", "end")

        try:
            parser_type = self.parser_var.get()
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

    def _parse_cyk(self, tokens):
        acept, back = cyk_parse(self.grammar, tokens)

        if acept:
            self._insert_with_tag("Resultado: ✓ CADENA ACEPTADA\n\n", "success")
            try:
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

                if self.export_tree_btn:
                    self.export_tree_btn.config(state="normal")

                self._insert_with_tag("\nÁrbol de derivación:\n", "header")
                self._insert_tree_colored(self.current_tree)
            except Exception as e:
                import traceback
                traceback.print_exc()
                self._insert_with_tag(f"\n⚠️ Error al construir el árbol: {e}\n", "error")
                self.current_tree = None
                if self.export_tree_btn:
                    self.export_tree_btn.config(state="disabled")
        else:
            self._insert_with_tag("Resultado: ✗ CADENA RECHAZADA\n\n", "error")
            self._insert_with_tag("❌ La cadena no pertenece al lenguaje generado por la gramática.\n", "info")
            self._insert_with_tag("   No se puede construir un árbol de derivación.\n", "info")
            self.current_tree = None
            if self.export_tree_btn:
                self.export_tree_btn.config(state="disabled")

    def _insert_tree_colored(self, node, indent=0, is_last=True, prefix=""):
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        self._insert_with_tag(prefix + connector, "separator")
        if node.is_leaf():
            self._insert_with_tag(f'"{node.symbol}"', "tree_terminal")
        else:
            self._insert_with_tag(f'[{node.symbol}]', "tree_node")
        self.result_text.insert("end", "\n")
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            if isinstance(child, TreeNode):
                self._insert_tree_colored(child, indent + 1, is_last_child, prefix + extension)
            else:
                child_connector = "└── " if is_last_child else "├── "
                self._insert_with_tag(prefix + extension + child_connector, "separator")
                self._insert_with_tag(f'"{child}"', "tree_terminal")
                self.result_text.insert("end", "\n")

    def _parse_regular(self, tokens):
        acept, derivation = parse_regular(self.grammar, tokens)
        if acept:
            self._insert_with_tag("✓ CADENA ACEPTADA\n\n", "success")
            if derivation:
                try:
                    self.current_tree = self._build_tree_from_derivation(derivation, tokens)
                    if self.current_tree:
                        if self.export_tree_btn:
                            self.export_tree_btn.config(state="normal")
                        self._insert_with_tag("Árbol de derivación\n", "header")
                        self._insert_tree_colored(self.current_tree)
                    else:
                        if self.export_tree_btn:
                            self.export_tree_btn.config(state="disabled")
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    self.current_tree = None
                    if self.export_tree_btn:
                        self.export_tree_btn.config(state="disabled")
            else:
                self.current_tree = None
                if self.export_tree_btn:
                    self.export_tree_btn.config(state="disabled")
        else:
            self._insert_with_tag("✗ CADENA RECHAZADA\n\n", "error")
            self._insert_with_tag("❌ La cadena no pertenece al lenguaje generado por la gramática.\n", "info")
            self.current_tree = None
            if self.export_tree_btn:
                self.export_tree_btn.config(state="disabled")

    def _build_tree_from_derivation(self, derivation, tokens):
        if not derivation:
            return None
        root = TreeNode(self.grammar.S)
        current_node = root
        token_index = 0
        for step_num, (symbol, production) in enumerate(derivation):
            if " → " in production:
                parts = production.split(" → ")
                if len(parts) != 2:
                    continue
                left, right = parts
                right = right.strip()
                children = []
                i = 0
                next_nonterminal = None
                while i < len(right):
                    char = right[i]
                    if char in self.grammar.T:
                        if token_index < len(tokens):
                            children.append(TreeNode(tokens[token_index]))
                            token_index += 1
                    elif char in self.grammar.N:
                        next_nonterminal = TreeNode(char)
                        children.append(next_nonterminal)
                    i += 1
                current_node.children = children
                if next_nonterminal:
                    current_node = next_nonterminal
        return root

    def export_tree(self):
        from tkinter import messagebox
        if self.current_tree is None:
            messagebox.showwarning("Advertencia", "No hay árbol para exportar.\nPrimero debe parsear una cadena aceptada con CYK o Regular.")
            return
        content = self.current_tree.to_text()
        path, err = save_text_to_file(self, default_ext=".txt", title="Guardar Árbol", content=content)
        if err:
            messagebox.showerror("Error", f"No se pudo exportar:\n{err}")
            return
        messagebox.showinfo("Éxito", f"Árbol exportado:\n{path}")

    # ---------- Generador ----------
    def generate_strings(self):
        from tkinter import messagebox
        if not self.grammar:
            messagebox.showwarning("Advertencia", "Cargue una gramática primero.")
            return
        try:
            limit = int(self.gen_limit.get())
            depth = int(self.gen_depth.get())
            self.gen_text.delete("1.0", "end")
            strings = generate_shortest(self.grammar, limit=limit, max_depth=depth)
            for i, s in enumerate(strings, 1):
                self.gen_text.insert("end", f"{i:2d}. \"{s}\" (longitud: {len(s)})\n")
            if len(strings) < limit:
                self.gen_text.insert("end", f"\n⚠ Solo se generaron {len(strings)} cadenas (puede aumentar profundidad).\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar cadenas:\n{str(e)}")

    def export_strings(self):
        from tkinter import messagebox
        content = self.gen_text.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Advertencia", "No hay cadenas para exportar.")
            return
        lines = [line for line in content.splitlines() if line.strip() != ""]
        if not lines:
            messagebox.showwarning("Advertencia", "No hay cadenas para exportar.")
            return
        content_to_save = "\n".join(lines) + "\n"
        path, err = save_text_to_file(self, default_ext=".txt", title="Exportar Cadenas", content=content_to_save)
        if err:
            messagebox.showerror("Error", f"No se pudo exportar:\n{err}")
            return
        messagebox.showinfo("Éxito", "Cadenas exportadas correctamente.")
