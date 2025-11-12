class TreeNode:
    def __init__(self, symbol, children=None):
        self.symbol = symbol
        self.children = children or []


    def is_leaf(self):
        return len(self.children) == 0


    def to_text(self, indent=0):
        s = " " * indent + str(self.symbol) + "\n"
        for c in self.children:
            if isinstance(c, TreeNode):
                s += c.to_text(indent + 1)
            else:
                s += " " * (indent + 1) + str(c) + "\n"
        return s


    def __repr__(self):
        return f"TreeNode({self.symbol})"