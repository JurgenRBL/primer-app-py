
from pyairtable import Table
from typing import List, Optional
from models.producto import Producto
from config import (
    AIRTABLE_TOKEN,
    AIRTABLE_BASE_ID,
    AIRTABLE_TABLE_PRODUCTOS,
    AIRTABLE_TABLE_USUARIOS
)

class AirtableService:
    def __init__(self):
        self.productos_table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_TABLE_PRODUCTOS)
        self.usuarios_table = Table(AIRTABLE_TOKEN, AIRTABLE_BASE_ID, AIRTABLE_TABLE_USUARIOS)
    
    def get_all_productos(self) -> List[Producto]:
        try:
            records = self.productos_table.all()
            return [Producto.from_dict(record) for record in records]
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []
    
    def get_producto_by_id(self, record_id: str) -> Optional[Producto]:
        try:
            record = self.productos_table.get(record_id)
            return Producto.from_dict(record)
        except Exception as e:
            print(f"Error al obtener producto: {e}")
            return None
    
    def create_producto(self, producto: Producto) -> tuple[bool, str, Optional[Producto]]:
        try:
            data = producto.to_dict()
            del data["ID"]
            record = self.productos_table.create(data)
            return True, "Producto creado exitosamente", Producto.from_dict(record)
        except Exception as e:
            return False, f"Error al crear producto: {str(e)}", None
    
    def update_producto(self, record_id: str, producto: Producto) -> tuple[bool, str]:
        try:
            data = producto.to_dict()
            del data["ID"]
            self.productos_table.update(record_id, data)
            return True, "Producto actualizado exitosamente"
        except Exception as e:
            return False, f"Error al actualizar producto: {str(e)}"
    
    def delete_producto(self, record_id: str) -> tuple[bool, str]:
        try:
            self.productos_table.delete(record_id)
            return True, "Producto eliminado exitosamente"
        except Exception as e:
            return False, f"Error al eliminar producto: {str(e)}"
    
    def search_productos(self, query: str) -> List[Producto]:
        try:
            all_productos = self.get_all_productos()
            query = query.lower()
            return [
                p for p in all_productos
                if query in p.nombre.lower() or 
                   query in p.descripcion.lower() or 
                   query in p.categoria.lower()
            ]
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []
    
    def get_estadisticas(self) -> dict:
        try:
            productos = self.get_all_productos()
            total = len(productos)
            disponibles = sum(1 for p in productos if p.estado == "Disponible")
            agotados = sum(1 for p in productos if p.stock == 0)
            return {
                "total": total,
                "disponibles": disponibles,
                "agotados": agotados
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {"total": 0, "disponibles": 0, "agotados": 0}

