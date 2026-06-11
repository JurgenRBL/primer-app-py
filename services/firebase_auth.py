
import pyrebase
from typing import Optional, Dict, Any
from config import FIREBASE_CONFIG

class FirebaseAuthService:
    def __init__(self):
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.auth = self.firebase.auth()
        self.current_user: Optional[Dict[str, Any]] = None
    
    def login(self, email: str, password: str) -> tuple[bool, str]:
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            self.current_user = user
            return True, "Inicio de sesión exitoso"
        except Exception as e:
            error_msg = self._get_error_message(str(e))
            return False, error_msg
    
    def logout(self) -> tuple[bool, str]:
        try:
            self.current_user = None
            return True, "Sesión cerrada correctamente"
        except Exception as e:
            return False, f"Error al cerrar sesión: {str(e)}"
    
    def is_logged_in(self) -> bool:
        return self.current_user is not None
    
    def get_user_email(self) -> Optional[str]:
        if self.current_user:
            return self.current_user.get("email")
        return None
    
    def get_user_id(self) -> Optional[str]:
        if self.current_user:
            return self.current_user.get("localId")
        return None
    
    def _get_error_message(self, error: str) -> str:
        if "EMAIL_NOT_FOUND" in error:
            return "Correo electrónico no registrado"
        elif "INVALID_PASSWORD" in error:
            return "Contraseña incorrecta"
        elif "INVALID_EMAIL" in error:
            return "Formato de correo electrónico inválido"
        elif "USER_DISABLED" in error:
            return "Usuario deshabilitado"
        elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error:
            return "Demasiados intentos fallidos. Intenta más tarde"
        else:
            return "Error de autenticación. Verifica tus credenciales"

