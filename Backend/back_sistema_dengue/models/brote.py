from utils.db import db

class Brote(db.Model):
    __tablename__ = 'Brote'

    IdBrote = db.Column(db.Integer, primary_key=True)
    Fecha_Inicio = db.Column(db.Date, nullable=False)
    Fecha_Fin = db.Column(db.Date, nullable=True)  # Puede que aún no haya terminado el brote
    Numero_Casos = db.Column(db.Integer, nullable=False)
    Gravedad = db.Column(db.String(50), nullable=False)  # Indica la gravedad del brote (por ejemplo, leve, moderado, severo)
    IdUbigeo = db.Column(db.Integer, nullable=False)  # Relación con la tabla de Región/Ubigeo

    def __init__(self, Fecha_Inicio, Fecha_Fin, Numero_Casos, Gravedad, IdUbigeo):
        self.Fecha_Inicio = Fecha_Inicio
        self.Fecha_Fin = Fecha_Fin
        self.Numero_Casos = Numero_Casos
        self.Gravedad = Gravedad
        self.IdUbigeo = IdUbigeo
