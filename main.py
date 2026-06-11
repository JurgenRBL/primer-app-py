
import flet as ft
from services.firebase_auth import FirebaseAuthService
from services.airtable_service import AirtableService
from views.login import LoginView
from views.dashboard import DashboardView
from views.productos import ProductosView
from views.perfil import PerfilView
from config import (
    COLOR_PRIMARIO,
    COLOR_SECUNDARIO,
    COLOR_FONDO,
    COLOR_TEXTO,
    COLOR_EXITO
)

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema CCTV - Gestión de Inventario"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.bgcolor = COLOR_FONDO
        
        # Inicializar servicios
        self.auth_service = FirebaseAuthService()
        self.airtable_service = AirtableService()
        
        # Vistas
        self.login_view = LoginView(page, self.handle_login)
        self.dashboard_view: DashboardView | None = None
        self.productos_view: ProductosView | None = None
        self.perfil_view: PerfilView | None = None
        
        # Navigation rail index
        self.selected_index = 0
        
        # Iniciar en login
        self.show_login()
    
    def show_login(self):
        self.page.views.clear()
        self.page.views.append(self.login_view.build())
        self.page.update()
    
    def handle_login(self, email: str, password: str):
        success, message = self.auth_service.login(email, password)
        if success:
            self.show_main_app()
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(message),
                bgcolor=COLOR_EXITO
            )
            self.page.snack_bar.open = True
        else:
            self.login_view.show_error(message)
    
    def show_main_app(self):
        user_email = self.auth_service.get_user_email()
        
        # Inicializar vistas principales
        self.dashboard_view = DashboardView(self.page, self.airtable_service, user_email)
        self.productos_view = ProductosView(self.page, self.airtable_service)
        self.perfil_view = PerfilView(self.page, user_email, self.handle_logout)
        
        # Cargar datos iniciales
        self.dashboard_view.load_estadisticas()
        self.productos_view.load_productos()
        
        # Actualizar la página
        self.page.views.clear()
        self.page.views.append(
            ft.View(
                route="/",
                bgcolor=COLOR_FONDO,
                padding=0,
                controls=[
                    ft.Row(
                        [
                            # Navigation Rail
                            ft.Container(
                                content=ft.NavigationRail(
                                    selected_index=self.selected_index,
                                    label_type=ft.NavigationRailLabelType.ALL,
                                    min_width=100,
                                    min_extended_width=200,
                                    leading=ft.Column(
                                        [
                                            ft.Icon(
                                                ft.icons.SECURITY,
                                                size=40,
                                                color=COLOR_PRIMARIO
                                            ),
                                            ft.Text(
                                                "Sistema CCTV",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLOR_TEXTO
                                            )
                                        ],
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10
                                    ),
                                    group_alignment=-0.9,
                                    destinations=[
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.HOME_OUTLINED,
                                            selected_icon=ft.icons.HOME,
                                            label="Inicio"
                                        ),
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.INVENTORY_OUTLINED,
                                            selected_icon=ft.icons.INVENTORY,
                                            label="Gestión de Datos"
                                        ),
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.PERSON_OUTLINED,
                                            selected_icon=ft.icons.PERSON,
                                            label="Perfil"
                                        ),
                                        ft.NavigationRailDestination(
                                            icon=ft.icons.LOGOUT_OUTLINED,
                                            selected_icon=ft.icons.LOGOUT,
                                            label="Cerrar Sesión"
                                        )
                                    ],
                                    on_change=self.handle_navigation_change,
                                    bgcolor=ft.colors.WHITE,
                                    elevation=2
                                ),
                                padding=10
                            ),
                            ft.VerticalDivider(width=1),
                            # Content area
                            ft.Container(
                                content=self.get_content(),
                                expand=True,
                                padding=0
                            )
                        ],
                        expand=True
                    )
                ]
            )
        )
        self.page.update()
    
    def get_content(self):
        if self.selected_index == 0:
            return self.dashboard_view.build()
        elif self.selected_index == 1:
            return self.productos_view.build()
        elif self.selected_index == 2:
            return self.perfil_view.build()
        else:
            return ft.Container()
    
    def handle_navigation_change(self, e):
        if e.control.selected_index == 3:
            self.handle_logout()
        else:
            self.selected_index = e.control.selected_index
            # Recargar datos cuando se navega
            if self.selected_index == 0 and self.dashboard_view:
                self.dashboard_view.load_estadisticas()
            elif self.selected_index == 1 and self.productos_view:
                self.productos_view.load_productos()
            self.show_main_app()
    
    def handle_logout(self, e=None):
        self.auth_service.logout()
        self.selected_index = 0
        self.show_login()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Sesión cerrada correctamente"),
            bgcolor=COLOR_EXITO
        )
        self.page.snack_bar.open = True
        self.page.update()

def main(page: ft.Page):
    App(page)

if __name__ == "__main__":
    ft.app(target=main)

