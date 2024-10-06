from utils.db import db

class Notificacion(db.Model):
    __tablename__ = 'Notificacion'

    IdNotificacion = db.Column(db.Integer, primary_key=True)
    Tipo_Notificacion = db.Column(db.String(100), nullable=False)
    Fecha_Notificacion = db.Column(db.Date, nullable=False)
    Mensaje = db.Column(db.Text, nullable=False)
    IdUsuario = db.Column(db.Integer, nullable=False)  # Relación con la tabla Usuario
    IdUbigeo = db.Column(db.Integer, nullable=False)   # Relación con la tabla Ubigeo

    def __init__(self, Tipo_Notificacion, Fecha_Notificacion, Mensaje, IdUsuario, IdUbigeo):
        self.Tipo_Notificacion = Tipo_Notificacion
        self.Fecha_Notificacion = Fecha_Notificacion
        self.Mensaje = Mensaje
        self.IdUsuario = IdUsuario
        self.IdUbigeo = IdUbigeo
