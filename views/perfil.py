
import flet as ft
from config import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_ERROR
)

class PerfilView:
    def __init__(self, page: ft.Page, user_email: str, on_logout):
        self.page = page
        self.user_email = user_email
        self.on_logout = on_logout
    
    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Mi Perfil",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXTO
                    ),
                    ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        ft.icons.PERSON,
                                        size=100,
                                        color=COLOR_PRIMARIO
                                    ),
                                    padding=20,
                                    bgcolor=ft.colors.with_opacity(0.1, COLOR_PRIMARIO),
                                    border_radius=100,
                                    alignment=ft.alignment.center
                                ),
                                ft.Divider(height=30, color=ft.colors.TRANSPARENT),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Nombre",
                                            size=14,
                                            color=ft.colors.GREY_600
                                        ),
                                        ft.Text(
                                            self.user_email.split('@')[0],
                                            size=20,
                                            weight=ft.FontWeight.BOLD,
                                            color=COLOR_TEXTO
                                        )
                                    ],
                                    spacing=5,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Correo electrónico",
                                            size=14,
                                            color=ft.colors.GREY_600
                                        ),
                                        ft.Text(
                                            self.user_email,
                                            size=18,
                                            color=COLOR_TEXTO
                                        )
                                    ],
                                    spacing=5,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Rol",
                                            size=14,
                                            color=ft.colors.GREY_600
                                        ),
                                        ft.Text(
                                            "Administrador",
                                            size=18,
                                            color=COLOR_PRIMARIO,
                                            weight=ft.FontWeight.BOLD
                                        )
                                    ],
                                    spacing=5,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                                ft.ElevatedButton(
                                    text="Cerrar Sesión",
                                    icon=ft.icons.LOGOUT,
                                    width=250,
                                    height=50,
                                    bgcolor=COLOR_ERROR,
                                    color=ft.colors.WHITE,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=12),
                                        elevation={"pressed": 0, "": 2}
                                    ),
                                    on_click=self.on_logout
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0
                        ),
                        padding=40,
                        bgcolor=COLOR_TARJETA,
                        border_radius=20,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                            offset=ft.Offset(0, 4)
                        ),
                        alignment=ft.alignment.center
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            ),
            padding=30,
            expand=True
        )

