import tkinter as tk
from tkinter import filedialog, messagebox

def save_text_to_file(parent, default_ext=".txt", title="Guardar archivo", content=""):
    path = filedialog.asksaveasfilename(
        title=title,
        defaultextension=default_ext,
        filetypes=[("Text files", f"*{default_ext}"), ("All files", "*.*")]
    )
    if not path:
        return None, "cancelled"
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path, None
    except Exception as e:
        return None, str(e)


def configure_result_text_tags(text_widget):
    """Configura tags de color/estilo en un ScrolledText (igual que antes)."""
    text_widget.tag_config("header", foreground="#2c3e50", font=("Arial", 11, "bold"))
    text_widget.tag_config("success", foreground="#27ae60", font=("Courier", 10, "bold"))
    text_widget.tag_config("error", foreground="#e74c3c", font=("Courier", 10, "bold"))
    text_widget.tag_config("info", foreground="#3498db", font=("Courier", 10))
    text_widget.tag_config("separator", foreground="#95a5a6", font=("Courier", 10))
    text_widget.tag_config("tree_node", foreground="#8e44ad", font=("Courier", 10, "bold"))
    text_widget.tag_config("tree_terminal", foreground="#16a085", font=("Courier", 10))
    text_widget.tag_config("derivation", foreground="#2980b9", font=("Courier", 10))
