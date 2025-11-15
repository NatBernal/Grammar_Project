import ttkbootstrap as ttk
from tkinter import scrolledtext, messagebox
from .utils import save_text_to_file

def build_grammar_tab(app, parent):
    """Construye la pestaña de Gramática y enlaza widgets al objeto app."""
    top_frame = ttk.Frame(parent)
    top_frame.pack(fill="x", pady=(0, 10))

    ttk.Button(
        top_frame,
        text="📂 Cargar Gramática (JSON)",
        command=app.load_grammar,
        bootstyle="info"
    ).pack(side="left", padx=5)

    ttk.Button(
        top_frame,
        text="💾 Guardar Gramática",
        command=app.save_grammar,
        bootstyle="success"
    ).pack(side="left", padx=5)

    ttk.Button(
        top_frame,
        text="➕ Nueva Gramática",
        command=app.new_grammar_dialog,
        bootstyle="primary"
    ).pack(side="left", padx=5)

    ttk.Button(
        top_frame,
        text="✓ Validar",
        command=app.validate_grammar,
        bootstyle="warning"
    ).pack(side="left", padx=5)

    label = ttk.Label(parent, text="Gramática Actual:", font=("Arial", 11, "bold"))
    label.pack(anchor="w")

    app.grammar_display = scrolledtext.ScrolledText(
        parent,
        height=20,
        font=("Courier", 10),
        wrap="word"
    )
    app.grammar_display.pack(fill="both", expand=True, pady=5)
    app.grammar_display.insert("1.0", "No hay gramática cargada. Use 'Cargar' o 'Nueva Gramática'.")
    app.grammar_display.config(state="disabled")
