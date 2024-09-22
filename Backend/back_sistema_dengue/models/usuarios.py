# models/usuarios.py

from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.Text, nullable=False)

    def __init__(self, nombre_usuario, email, contrasena):
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.contrasena_hash = generate_password_hash(contrasena)

    def verificar_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)

