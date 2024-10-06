from utils.db import db

class Predicciones(db.Model):
    __tablename__ = 'Predicciones'

    IdPrediccion = db.Column(db.Integer, primary_key=True)
    Fecha_Prediccion = db.Column(db.Date, nullable=False)
    Probabilidad_Brote = db.Column(db.Float, nullable=False)  # Se asume que es un porcentaje (por ejemplo, 0.75 para 75%)
    IdUbigeo = db.Column(db.Integer, nullable=False)  # Relación con la tabla Ubigeo

    def __init__(self, Fecha_Prediccion, Probabilidad_Brote, IdUbigeo):
        self.Fecha_Prediccion = Fecha_Prediccion
        self.Probabilidad_Brote = Probabilidad_Brote
        self.IdUbigeo = IdUbigeo
