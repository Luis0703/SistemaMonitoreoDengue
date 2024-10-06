from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "Usuario"

    IdUsuario = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(50), nullable=False)
    CorreoElectronico = db.Column(db.String(100), unique=True, nullable=False)
    Contrasena = db.Column(db.Text, nullable=False)  # Nombre actualizado a 'contrasena'

    def __init__(self, Nombre, CorreoElectronico, Contrasena):
        self.Nombre = Nombre
        self.CorreoElectronico = CorreoElectronico
        self.Contrasena = generate_password_hash(Contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.Contrasena, contrasena)

