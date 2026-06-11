
import flet as ft
from config import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    COLOR_TARJETA,
    COLOR_TEXTO,
    COLOR_ERROR
)

class LoginView:
    def __init__(self, page: ft.Page, on_login_success):
        self.page = page
        self.on_login_success = on_login_success
        self.email_field = ft.TextField(
            label="Correo electrónico",
            width=350,
            border_radius=12,
            prefix_icon=ft.icons.EMAIL,
            text_style=ft.TextStyle(color=COLOR_TEXTO)
        )
        self.password_field = ft.TextField(
            label="Contraseña",
            width=350,
            border_radius=12,
            prefix_icon=ft.icons.LOCK,
            password=True,
            can_reveal_password=True,
            text_style=ft.TextStyle(color=COLOR_TEXTO)
        )
        self.error_text = ft.Text("", color=COLOR_ERROR, size=14)
        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            width=350,
            height=50,
            bgcolor=COLOR_PRIMARIO,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation={"pressed": 0, "": 2}
            ),
            on_click=self.handle_login
        )
        self.loading = ft.ProgressRing(visible=False, color=COLOR_PRIMARIO)
    
    def handle_login(self, e):
        self.error_text.value = ""
        self.login_button.disabled = True
        self.loading.visible = True
        self.page.update()
        
        email = self.email_field.value.strip()
        password = self.password_field.value.strip()
        
        # Validaciones básicas
        if not email:
            self.error_text.value = "Por favor ingrese su correo electrónico"
            self.login_button.disabled = False
            self.loading.visible = False
            self.page.update()
            return
        
        if not password:
            self.error_text.value = "Por favor ingrese su contraseña"
            self.login_button.disabled = False
            self.loading.visible = False
            self.page.update()
            return
        
        if len(password) < 6:
            self.error_text.value = "La contraseña debe tener al menos 6 caracteres"
            self.login_button.disabled = False
            self.loading.visible = False
            self.page.update()
            return
        
        # Llamar al callback de éxito
        self.on_login_success(email, password)
    
    def show_error(self, message: str):
        self.error_text.value = message
        self.login_button.disabled = False
        self.loading.visible = False
        self.page.update()
    
    def build(self) -> ft.View:
        return ft.View(
            route="/login",
            bgcolor=COLOR_FONDO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.icons.SECURITY,
                                size=80,
                                color=COLOR_PRIMARIO
                            ),
                            ft.Text(
                                "Sistema CCTV",
                                size=30,
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_TEXTO
                            ),
                            ft.Text(
                                "Gestión de Inventario",
                                size=16,
                                color=ft.colors.GREY_600
                            ),
                            ft.Divider(height=40, color=ft.colors.TRANSPARENT),
                            self.email_field,
                            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                            self.password_field,
                            ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                            self.error_text,
                            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                            ft.Stack(
                                [
                                    self.login_button,
                                    ft.Container(
                                        content=self.loading,
                                        alignment=ft.alignment.center,
                                        width=350,
                                        height=50
                                    )
                                ]
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10
                    ),
                    padding=40,
                    bgcolor=COLOR_TARJETA,
                    border_radius=20,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=10,
                        color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                        offset=ft.Offset(0, 4)
                    )
                )
            ]
        )

