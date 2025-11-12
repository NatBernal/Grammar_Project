import json
from typing import List, Dict


class Grammar:
    def __init__(self, N: List[str], T: List[str], P: List[Dict], S: str, gtype: str = "type2"):
        """
        Inicializa una gramática formal.
        
        Args:
            N: No terminales (variables)
            T: Terminales (alfabeto)
            P: Producciones [{"left": "A", "right": ["a", "B"]}, ...]
            S: Símbolo inicial
            gtype: "type2" (GLC) o "type3" (Regular)
        """
        self.N = list(N)
        self.T = list(T)
        self.P = list(P)
        self.S = S
        self.type = gtype

    @classmethod
    def from_dict(cls, d: Dict):
        """Crea una gramática desde un diccionario."""
        return cls(
            d.get("N", []), 
            d.get("T", []), 
            d.get("P", []), 
            d.get("S", "S"), 
            d.get("type", "type2")
        )

    def to_dict(self) -> Dict:
        """Convierte la gramática a diccionario para serialización."""
        return {
            "type": self.type, 
            "N": self.N, 
            "T": self.T, 
            "P": self.P, 
            "S": self.S
        }

    def save(self, path: str):
        """Guarda la gramática en un archivo JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str):
        """Carga una gramática desde un archivo JSON."""
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def validate(self) -> bool:
        """Validaciones básicas de la gramática.
        
        Verifica:
        - S pertenece a N
        - Lado izquierdo de producciones pertenece a N
        - Lado derecho solo contiene símbolos de N o T
        """
        if self.S not in self.N:
            return False
        
        for p in self.P:
            left = p.get("left")
            right = p.get("right", [])
            
            # ✅ CORRECCIÓN: Indentación correcta
            if left not in self.N:
                return False
            
            for sym in right:
                if sym not in self.N and sym not in self.T:
                    return False
        
        return True
    
    def __str__(self):
        """Representación legible de la gramática."""
        prods = "\n".join([f"  {p['left']} → {' '.join(p['right'])}" for p in self.P])
        return f"Gramática ({self.type}):\nN = {{{', '.join(self.N)}}}\nT = {{{', '.join(self.T)}}}\nS = {self.S}\nP:\n{prods}"