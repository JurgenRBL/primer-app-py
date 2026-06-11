
import flet as ft
from datetime import datetime
from config import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_ACENTO,
    COLOR_FONDO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_EXITO,
    COLOR_ERROR
)

class DashboardView:
    def __init__(self, page: ft.Page, airtable_service, user_email: str):
        self.page = page
        self.airtable_service = airtable_service
        self.user_email = user_email
        self.total_productos = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=COLOR_PRIMARIO)
        self.disponibles = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=COLOR_EXITO)
        self.agotados = ft.Text("0", size=40, weight=ft.FontWeight.BOLD, color=COLOR_ERROR)
        self.fecha_actual = ft.Text(
            datetime.now().strftime("%d/%m/%Y"),
            size=18,
            color=ft.colors.GREY_600
        )
        self.loading = ft.ProgressRing(visible=False, color=COLOR_PRIMARIO)
    
    def _build_stat_card(self, title: str, value_control: ft.Control, icon: ft.Icons, color: str) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, size=40, color=color),
                        padding=20,
                        bgcolor=ft.colors.with_opacity(0.1, color),
                        border_radius=15
                    ),
                    ft.Column(
                        [
                            ft.Text(title, size=16, color=ft.colors.GREY_600),
                            value_control
                        ],
                        spacing=5
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20
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
    
    def load_estadisticas(self):
        self.loading.visible = True
        self.page.update()
        
        estadisticas = self.airtable_service.get_estadisticas()
        self.total_productos.value = str(estadisticas["total"])
        self.disponibles.value = str(estadisticas["disponibles"])
        self.agotados.value = str(estadisticas["agotados"])
        self.fecha_actual.value = datetime.now().strftime("%d/%m/%Y")
        
        self.loading.visible = False
        self.page.update()
    
    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    # Header
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        f"Bienvenido, {self.user_email.split('@')[0]}!",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_TEXTO
                                    ),
                                    self.fecha_actual
                                ],
                                spacing=5
                            ),
                            ft.Container(
                                content=self.loading,
                                alignment=ft.alignment.center_right
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                    # Cards
                    ft.Row(
                        [
                            self._build_stat_card(
                                "Total Productos",
                                self.total_productos,
                                ft.icons.INVENTORY,
                                COLOR_PRIMARIO
                            ),
                            self._build_stat_card(
                                "Disponibles",
                                self.disponibles,
                                ft.icons.CHECK_CIRCLE,
                                COLOR_EXITO
                            ),
                            self._build_stat_card(
                                "Agotados",
                                self.agotados,
                                ft.icons.ERROR,
                                COLOR_ERROR
                            )
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                    ),
                    ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                    # Info card
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.INFO, size=30, color=COLOR_SECUNDARIO),
                                        ft.Text(
                                            "Información del Sistema",
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXTO
                                        )
                                    ],
                                    spacing=15
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Text(
                                    "Este sistema gestiona el inventario de productos de CCTV. "
                                    "Puedes agregar, editar, eliminar y buscar productos en la sección 'Gestión de Datos'.",
                                    size=16,
                                    color=ft.colors.GREY_600
                                )
                            ],
                            spacing=10
                        ),
                        padding=30,
                        bgcolor=COLOR_TARJETA,
                        border_radius=15,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                            offset=ft.Offset(0, 4)
                        )
                    )
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            ),
            padding=30,
            expand=True
        )

