
from datetime import datetime
from typing import Optional

class Producto:
    def __init__(self, id: Optional[str] = None, nombre: str = "", descripcion: str = "", 
                 fecha: Optional[str] = None, estado: str = "Disponible", precio: float = 0.0, 
                 stock: int = 0, categoria: str = ""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d")
        self.estado = estado
        self.precio = precio
        self.stock = stock
        self.categoria = categoria
    
    def to_dict(self) -> dict:
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Descripción": self.descripcion,
            "Fecha": self.fecha,
            "Estado": self.estado,
            "Precio": self.precio,
            "Stock": self.stock,
            "Categoría": self.categoria
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Producto":
        fields = data.get("fields", {})
        return cls(
            id=data.get("id"),
            nombre=fields.get("Nombre", ""),
            descripcion=fields.get("Descripción", ""),
            fecha=fields.get("Fecha", ""),
            estado=fields.get("Estado", "Disponible"),
            precio=fields.get("Precio", 0.0),
            stock=fields.get("Stock", 0),
            categoria=fields.get("Categoría", "")
        )
    
    def is_valid(self) -> tuple[bool, str]:
        if not self.nombre or not self.nombre.strip():
            return False, "El nombre del producto es obligatorio"
        if not self.categoria or not self.categoria.strip():
            return False, "La categoría es obligatoria"
        if self.precio < 0:
            return False, "El precio no puede ser negativo"
        if self.stock < 0:
            return False, "El stock no puede ser negativo"
        return True, ""

