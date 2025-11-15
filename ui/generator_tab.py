import ttkbootstrap as ttk
from tkinter import scrolledtext, messagebox
from .utils import save_text_to_file

def build_generator_tab(app, parent):
    control_frame_outer = ttk.Frame(parent)
    control_frame_outer.pack(fill="x", pady=(0, 10))
    ttk.Label(control_frame_outer, text="Parámetros", font=("Arial", 11, "bold")).pack(anchor="w", padx=5, pady=(5, 0))

    control_frame = ttk.Frame(control_frame_outer, padding="10")
    control_frame.pack(fill="x")

    ttk.Label(control_frame, text="Número de cadenas:").grid(row=0, column=0, sticky="w", padx=5)
    app.gen_limit = ttk.Spinbox(control_frame, from_=1, to=50, width=10)
    app.gen_limit.set(10)
    app.gen_limit.grid(row=0, column=1, padx=5)

    ttk.Label(control_frame, text="Profundidad máxima:").grid(row=0, column=2, sticky="w", padx=5)
    app.gen_depth = ttk.Spinbox(control_frame, from_=5, to=30, width=10)
    app.gen_depth.set(12)
    app.gen_depth.grid(row=0, column=3, padx=5)

    ttk.Button(
        control_frame,
        text="⚡ Generar Cadenas",
        command=app.generate_strings,
        bootstyle="primary"
    ).grid(row=0, column=4, padx=10)

    result_frame_outer = ttk.Frame(parent)
    result_frame_outer.pack(fill="both", expand=True)

    title_frame = ttk.Frame(result_frame_outer)
    title_frame.pack(fill="x", padx=5, pady=(5, 0))

    ttk.Label(title_frame, text="Cadenas Generadas", font=("Arial", 11, "bold")).pack(side="left")

    ttk.Button(
        title_frame,
        text="💾 Exportar Cadenas",
        command=app.export_strings,
        bootstyle="success"
    ).pack(side="right", padx=5)

    result_frame = ttk.Frame(result_frame_outer, padding="10")
    result_frame.pack(fill="both", expand=True)

    app.gen_text = scrolledtext.ScrolledText(
        result_frame,
        height=20,
        font=("Courier", 10)
    )
    app.gen_text.pack(fill="both", expand=True)
