import tkinter as tk
from tkinter import ttk


class TreeVisualizer(tk.Toplevel):
    """Ventana para visualizar gráficamente el árbol de derivación."""
    
    def __init__(self, parent, tree_root, title="Visualización del Árbol"):
        super().__init__(parent)
        self.title(title)
        self.geometry("900x700")
        self.tree_root = tree_root
        
        # Configuración de colores
        self.node_color = "#8e44ad"
        self.terminal_color = "#16a085"
        self.edge_color = "#7f8c8d"
        self.node_border = "#2c3e50"
        
        # Parámetros de dibujo
        self.node_radius = 20
        self.level_height = 100
        self.min_horizontal_gap = 20
        self.node_padding = 20  # Espacio mínimo entre bordes de nodos
        
        self._build_ui()
        self._calculate_positions()
        self._draw_tree()
        
    def _build_ui(self):
        """Construye la interfaz de la ventana."""
        # Frame para controles
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(fill="x")
        
        ttk.Label(
            control_frame,
            text="Árbol de Derivación",
            font=("Arial", 12, "bold")
        ).pack(side="left", padx=5)
        
        # Botones de control
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side="right")
        
        ttk.Button(
            button_frame,
            text="🔍 Zoom +",
            command=self._zoom_in
        ).pack(side="left", padx=2)
        
        ttk.Button(
            button_frame,
            text="🔍 Zoom -",
            command=self._zoom_out
        ).pack(side="left", padx=2)
        
        ttk.Button(
            button_frame,
            text="🔄 Reiniciar Vista",
            command=self._reset_view
        ).pack(side="left", padx=2)
        
        # Frame para el canvas con scrollbars
        canvas_frame = ttk.Frame(self)
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars - usar tkinter estándar
        v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical")
        v_scrollbar.pack(side="right", fill="y")
        
        h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Canvas
        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        
        v_scrollbar.config(command=self.canvas.yview)
        h_scrollbar.config(command=self.canvas.xview)
        
        # Bind para drag con el mouse
        self.canvas.bind("<ButtonPress-1>", self._on_drag_start)
        self.canvas.bind("<B1-Motion>", self._on_drag_motion)
        
        self._drag_data = {"x": 0, "y": 0}
        
    def _calculate_positions(self):
        """Calcula las posiciones de todos los nodos del árbol."""
        if not self.tree_root:
            return
        
        # Primero, calcular el ancho necesario para cada nodo
        self._calculate_widths(self.tree_root)
        
        # Luego, asignar posiciones x, y
        tree_width = self.tree_root._width * self.min_horizontal_gap
        start_x = max(tree_width / 2, 450)  # Centrar en el canvas
        start_y = 50
        
        self._assign_positions(self.tree_root, start_x, start_y, tree_width)
        
    def _calculate_widths(self, node):
        """Calcula recursivamente el ancho de cada subárbol."""
        if node.is_leaf():
            node._width = 1
            return 1
        
        if not node.children:
            node._width = 1
            return 1
        
        total_width = 0
        for child in node.children:
            if isinstance(child, type(node)):  # TreeNode
                total_width += self._calculate_widths(child)
            else:
                total_width += 1  # Terminal como string
        
        # Asegurar un ancho mínimo basado en el número de hijos
        node._width = max(total_width, len(node.children) * 1.5)
        return node._width
    
    def _assign_positions(self, node, x, y, width):
        """Asigna posiciones x, y a cada nodo."""
        node._x = x
        node._y = y
        
        if node.is_leaf() or not node.children:
            return
        
        # Calcular el ancho total necesario para todos los hijos
        children_info = []
        for child in node.children:
            if isinstance(child, type(node)):  # TreeNode
                child_width = child._width if hasattr(child, '_width') else 1
                children_info.append(('node', child, child_width))
            else:
                children_info.append(('terminal', child, 1))
        
        total_child_width = sum(info[2] for info in children_info)
        
        # Calcular el espacio total incluyendo padding entre nodos
        spacing = self.min_horizontal_gap + self.node_padding
        available_space = total_child_width * spacing
        start_x = x - available_space / 2
        
        current_x = start_x
        
        for child_type, child, child_width in children_info:
            child_space = child_width * spacing
            child_x = current_x + child_space / 2
            child_y = y + self.level_height
            
            if child_type == 'node':
                self._assign_positions(child, child_x, child_y, child_space)
            else:
                # Terminal como string - guardar posición
                if not hasattr(node, '_terminal_positions'):
                    node._terminal_positions = []
                node._terminal_positions.append((child, child_x, child_y))
            
            current_x += child_space
    
    def _draw_tree(self):
        """Dibuja el árbol en el canvas."""
        if not self.tree_root:
            return
        
        # Limpiar canvas
        self.canvas.delete("all")
        
        # Dibujar aristas primero (para que queden debajo)
        self._draw_edges(self.tree_root)
        
        # Dibujar nodos
        self._draw_nodes(self.tree_root)
        
        # Configurar región scrollable
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _draw_edges(self, node):
        """Dibuja las aristas del árbol."""
        if not hasattr(node, '_x'):
            return
        
        x1, y1 = node._x, node._y
        
        # Dibujar líneas a hijos TreeNode
        for child in node.children:
            if isinstance(child, type(node)) and hasattr(child, '_x'):
                x2, y2 = child._x, child._y
                self.canvas.create_line(
                    x1, y1 + self.node_radius,
                    x2, y2 - self.node_radius,
                    fill=self.edge_color,
                    width=2,
                    tags="edge"
                )
                self._draw_edges(child)
        
        # Dibujar líneas a terminales
        if hasattr(node, '_terminal_positions'):
            for terminal, x2, y2 in node._terminal_positions:
                self.canvas.create_line(
                    x1, y1 + self.node_radius,
                    x2, y2 - self.node_radius,
                    fill=self.edge_color,
                    width=2,
                    tags="edge"
                )
    
    def _draw_nodes(self, node):
        """Dibuja los nodos del árbol."""
        if not hasattr(node, '_x'):
            return
        
        x, y = node._x, node._y
        r = self.node_radius
        
        if node.is_leaf():
            # Nodo terminal (hoja)
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.terminal_color,
                outline=self.node_border,
                width=2,
                tags="node"
            )
            self.canvas.create_text(
                x, y,
                text=node.symbol,
                font=("Courier", 10, "bold"),
                fill="white",
                tags="node"
            )
        else:
            # Nodo no terminal
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=self.node_color,
                outline=self.node_border,
                width=2,
                tags="node"
            )
            self.canvas.create_text(
                x, y,
                text=node.symbol,
                font=("Arial", 11, "bold"),
                fill="white",
                tags="node"
            )
            
            # Dibujar hijos TreeNode
            for child in node.children:
                if isinstance(child, type(node)):
                    self._draw_nodes(child)
            
            # Dibujar terminales
            if hasattr(node, '_terminal_positions'):
                for terminal, tx, ty in node._terminal_positions:
                    self.canvas.create_oval(
                        tx - r, ty - r, tx + r, ty + r,
                        fill=self.terminal_color,
                        outline=self.node_border,
                        width=2,
                        tags="node"
                    )
                    self.canvas.create_text(
                        tx, ty,
                        text=terminal,
                        font=("Courier", 10, "bold"),
                        fill="white",
                        tags="node"
                    )
    
    def _zoom_in(self):
        """Aumenta el zoom del árbol."""
        self.node_radius = min(self.node_radius + 5, 50)
        self.level_height = min(self.level_height + 10, 150)
        self.min_horizontal_gap = min(self.min_horizontal_gap + 15, 150)
        self.node_padding = min(self.node_padding + 5, 60)
        self._calculate_positions()
        self._draw_tree()
    
    def _zoom_out(self):
        """Reduce el zoom del árbol."""
        self.node_radius = max(self.node_radius - 5, 15)
        self.level_height = max(self.level_height - 10, 40)
        self.min_horizontal_gap = max(self.min_horizontal_gap - 15, 50)
        self.node_padding = max(self.node_padding - 5, 20)
        self._calculate_positions()
        self._draw_tree()
    
    def _reset_view(self):
        """Reinicia los valores de zoom."""
        self.node_radius = 30
        self.level_height = 100
        self.min_horizontal_gap = 80
        self._calculate_positions()
        self._draw_tree()
    
    def _on_drag_start(self, event):
        """Inicia el arrastre del canvas."""
        self.canvas.scan_mark(event.x, event.y)
    
    def _on_drag_motion(self, event):
        """Mueve el canvas al arrastrar."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)