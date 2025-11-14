class TreeNode:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []


    def is_leaf(self):
        return len(self.children) == 0


    def to_text(self, indent=0, is_last=True, prefix=""):
        """
        Genera una representación visual del árbol con caracteres ASCII.
        
        Usa:
        ├── para nodos intermedios
        └── para el último nodo
        │   para líneas verticales
        """
        # Caracteres para el árbol
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        
        # Símbolo con formato (terminales entre comillas)
        symbol_str = f'"{self.symbol}"' if self.is_leaf() else f'[{self.symbol}]'
        
        result = prefix + connector + symbol_str + "\n"
        
        # Procesar hijos
        for i, child in enumerate(self.children):
            is_last_child = (i == len(self.children) - 1)
            if isinstance(child, TreeNode):
                result += child.to_text(indent + 1, is_last_child, prefix + extension)
            else:
                # Nodo terminal
                child_connector = "└── " if is_last_child else "├── "
                child_extension = "    " if is_last_child else "│   "
                result += prefix + extension + child_connector + f'"{child}"\n'
        
        return result


    def to_text_simple(self, indent=0):
        """Versión simple del árbol con indentación."""
        s = " " * indent + f"[{self.symbol}]\n"
        for c in self.children:
            if isinstance(c, TreeNode):
                s += c.to_text_simple(indent + 2)
            else:
                s += " " * (indent + 2) + f'"{c}"\n'
        return s


    def __repr__(self):
        return f"TreeNode({self.symbol})"