import ttkbootstrap as ttk
from tkinter import scrolledtext, messagebox, filedialog
from .utils import configure_result_text_tags, save_text_to_file
from services.tree import TreeNode

def build_parser_tab(app, parent):
    """Construye la pestaña del parser (y enlaza widgets a app)."""
    input_frame_outer = ttk.Frame(parent)
    input_frame_outer.pack(fill="x", pady=(0, 10))
    ttk.Label(input_frame_outer, text="Entrada", font=("Arial", 11, "bold")).pack(anchor="w", padx=5, pady=(5, 0))

    input_frame = ttk.Frame(parent, padding="10")
    input_frame.pack(fill="x", pady=(0, 10))

    ttk.Label(input_frame, text="Cadena:").grid(row=0, column=0, sticky="w")
    app.entry_parse = ttk.Entry(input_frame, width=60)
    app.entry_parse.grid(row=0, column=1, padx=10, sticky="ew")

    ttk.Button(
        input_frame,
        text="🔍 Parsear",
        command=app.parse_string,
        bootstyle="info"
    ).grid(row=0, column=2)

    input_frame.columnconfigure(1, weight=1)

    parser_frame = ttk.Frame(input_frame)
    parser_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="w")

    ttk.Label(parser_frame, text="Algoritmo:").pack(side="left", padx=(0, 10))
    app.parser_var = ttk.StringVar(value="auto")
    ttk.Radiobutton(parser_frame, text="Auto-detectar", variable=app.parser_var, value="auto").pack(side="left", padx=5)
    ttk.Radiobutton(parser_frame, text="CYK (Tipo 2)", variable=app.parser_var, value="cyk").pack(side="left", padx=5)
    ttk.Radiobutton(parser_frame, text="Regular (Tipo 3)", variable=app.parser_var, value="regular").pack(side="left", padx=5)

    result_frame_outer = ttk.Frame(parent)
    result_frame_outer.pack(fill="both", expand=True)

    title_frame = ttk.Frame(result_frame_outer)
    title_frame.pack(fill="x", padx=5, pady=(5, 0))

    ttk.Label(title_frame, text="Resultado del Análisis", font=("Arial", 11, "bold")).pack(side="left")

    app.export_tree_btn = ttk.Button(
        title_frame,
        text="💾 Exportar Árbol",
        command=app.export_tree,
        bootstyle="success",
        state="disabled"
    )
    app.export_tree_btn.pack(side="right", padx=5)

    result_frame = ttk.Frame(result_frame_outer, padding="10")
    result_frame.pack(fill="both", expand=True)

    app.result_text = scrolledtext.ScrolledText(
        result_frame,
        height=15,
        font=("Courier", 10)
    )
    app.result_text.pack(fill="both", expand=True)

    # configurar tags
    configure_result_text_tags(app.result_text)
