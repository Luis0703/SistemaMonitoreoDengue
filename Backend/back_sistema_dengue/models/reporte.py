from utils.db import db

class Reporte(db.Model):
    __tablename__ = 'Reporte'

    IdReporte = db.Column(db.Integer, primary_key=True)
    Fecha_Reporte = db.Column(db.Date, nullable=False)
    Tipo_Reporte = db.Column(db.String(100), nullable=False)
    IdUsuario = db.Column(db.Integer, nullable=False)  # Relación con la tabla Usuario
    IdUbigeo = db.Column(db.Integer, nullable=False)   # Relación con la tabla Ubigeo

    def __init__(self, Fecha_Reporte, Tipo_Reporte, IdUsuario, IdUbigeo):
        self.Fecha_Reporte = Fecha_Reporte
        self.Tipo_Reporte = Tipo_Reporte
        self.IdUsuario = IdUsuario
        self.IdUbigeo = IdUbigeo
