
import flet as ft
from models.producto import Producto
from config import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_EXITO,
    COLOR_ERROR,
    COLOR_ADVERTENCIA
)

class ProductosView:
    def __init__(self, page: ft.Page, airtable_service):
        self.page = page
        self.airtable_service = airtable_service
        self.productos: list[Producto] = []
        self.editing_id: str | None = None
        
        # Form fields
        self.nombre_field = ft.TextField(label="Nombre", width=300, border_radius=10)
        self.descripcion_field = ft.TextField(label="Descripción", width=300, border_radius=10, multiline=True)
        self.precio_field = ft.TextField(label="Precio", width=300, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
        self.stock_field = ft.TextField(label="Stock", width=300, border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
        self.categoria_field = ft.TextField(label="Categoría", width=300, border_radius=10)
        self.estado_field = ft.Dropdown(
            label="Estado",
            width=300,
            border_radius=10,
            options=[
                ft.dropdown.Option("Disponible"),
                ft.dropdown.Option("Agotado"),
                ft.dropdown.Option("Descontinuado")
            ],
            value="Disponible"
        )
        self.search_field = ft.TextField(
            label="Buscar producto...",
            prefix_icon=ft.icons.SEARCH,
            border_radius=10,
            on_change=self.handle_search
        )
        
        # Table
        self.productos_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Categoría")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Stock")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[],
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            vertical_lines=ft.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.BorderSide(1, ft.colors.GREY_300)
        )
        
        self.loading = ft.ProgressRing(visible=False, color=COLOR_PRIMARIO)
    
    def clear_form(self):
        self.nombre_field.value = ""
        self.descripcion_field.value = ""
        self.precio_field.value = ""
        self.stock_field.value = ""
        self.categoria_field.value = ""
        self.estado_field.value = "Disponible"
        self.editing_id = None
    
    def load_productos(self, productos_list: list[Producto] | None = None):
        self.loading.visible = True
        self.page.update()
        
        if productos_list is None:
            self.productos = self.airtable_service.get_all_productos()
        else:
            self.productos = productos_list
        
        self.productos_table.rows = []
        for producto in self.productos:
            self.productos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto.nombre)),
                        ft.DataCell(ft.Text(producto.categoria)),
                        ft.DataCell(ft.Text(f"${producto.precio:.2f}")),
                        ft.DataCell(ft.Text(str(producto.stock))),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(producto.estado, color=ft.colors.WHITE, size=12, weight=ft.FontWeight.BOLD),
                                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                border_radius=20,
                                bgcolor=COLOR_EXITO if producto.estado == "Disponible" else COLOR_ERROR if producto.estado == "Agotado" else COLOR_ADVERTENCIA
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_color=COLOR_PRIMARIO,
                                        tooltip="Editar",
                                        on_click=lambda e, p=producto: self.edit_producto(p)
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color=COLOR_ERROR,
                                        tooltip="Eliminar",
                                        on_click=lambda e, p=producto: self.confirm_delete(p)
                                    )
                                ],
                                spacing=5
                            )
                        )
                    ]
                )
            )
        
        self.loading.visible = False
        self.page.update()
    
    def handle_search(self, e):
        query = self.search_field.value.strip()
        if query:
            productos = self.airtable_service.search_productos(query)
            self.load_productos(productos)
        else:
            self.load_productos()
    
    def edit_producto(self, producto: Producto):
        self.editing_id = producto.id
        self.nombre_field.value = producto.nombre
        self.descripcion_field.value = producto.descripcion
        self.precio_field.value = str(producto.precio)
        self.stock_field.value = str(producto.stock)
        self.categoria_field.value = producto.categoria
        self.estado_field.value = producto.estado
        self.page.update()
    
    def confirm_delete(self, producto: Producto):
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def delete_producto(e):
            dialog.open = False
            self.page.update()
            success, message = self.airtable_service.delete_producto(producto.id)
            self.show_snackbar(message, success)
            if success:
                self.load_productos()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Eliminación"),
            content=ft.Text(f"¿Estás seguro de que deseas eliminar el producto '{producto.nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.TextButton("Eliminar", on_click=delete_producto, style=ft.ButtonStyle(color=COLOR_ERROR))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def handle_save(self, e):
        # Validaciones
        if not self.nombre_field.value.strip():
            self.show_snackbar("El nombre es obligatorio", False)
            return
        
        if not self.categoria_field.value.strip():
            self.show_snackbar("La categoría es obligatoria", False)
            return
        
        try:
            precio = float(self.precio_field.value) if self.precio_field.value else 0.0
        except ValueError:
            self.show_snackbar("Precio inválido", False)
            return
        
        try:
            stock = int(self.stock_field.value) if self.stock_field.value else 0
        except ValueError:
            self.show_snackbar("Stock inválido", False)
            return
        
        if precio < 0:
            self.show_snackbar("El precio no puede ser negativo", False)
            return
        
        if stock < 0:
            self.show_snackbar("El stock no puede ser negativo", False)
            return
        
        producto = Producto(
            nombre=self.nombre_field.value.strip(),
            descripcion=self.descripcion_field.value.strip(),
            precio=precio,
            stock=stock,
            categoria=self.categoria_field.value.strip(),
            estado=self.estado_field.value
        )
        
        if self.editing_id:
            success, message = self.airtable_service.update_producto(self.editing_id, producto)
        else:
            success, message, _ = self.airtable_service.create_producto(producto)
        
        self.show_snackbar(message, success)
        if success:
            self.clear_form()
            self.load_productos()
    
    def show_snackbar(self, message: str, success: bool):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=COLOR_EXITO if success else COLOR_ERROR
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Row(
                        [
                            ft.Text(
                                "Gestión de Productos",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXTO
                            ),
                            self.loading
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    # Search
                    ft.Container(
                        content=self.search_field,
                        width=500
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    # Form
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Nuevo/Editar Producto",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXTO
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Row(
                                    [
                                        self.nombre_field,
                                        self.categoria_field
                                    ],
                                    spacing=20,
                                    wrap=True
                                ),
                                ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                                ft.Row(
                                    [
                                        self.precio_field,
                                        self.stock_field,
                                        self.estado_field
                                    ],
                                    spacing=20,
                                    wrap=True
                                ),
                                ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                                self.descripcion_field,
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            text="Guardar",
                                            icon=ft.icons.SAVE,
                                            bgcolor=COLOR_PRIMARIO,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self.handle_save
                                        ),
                                        ft.ElevatedButton(
                                            text="Limpiar",
                                            icon=ft.icons.CLEAR,
                                            bgcolor=ft.colors.GREY_400,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=lambda e: self.clear_form()
                                        )
                                    ],
                                    spacing=15
                                )
                            ],
                            spacing=0
                        ),
                        padding=25,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                            offset=ft.Offset(0, 4)
                        )
                    ),
                    ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                    # Table
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Listado de Productos",
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_TEXTO
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Container(
                                    content=self.productos_table,
                                    scroll=ft.ScrollMode.AUTO,
                                    expand=True
                                )
                            ],
                            expand=True
                        ),
                        padding=25,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                            offset=ft.Offset(0, 4)
                        ),
                        expand=True
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            padding=30,
            expand=True
        )

