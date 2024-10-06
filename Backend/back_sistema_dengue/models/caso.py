from utils.db import db

class Caso(db.Model):
    __tablename__ = 'Caso'

    IdCaso = db.Column(db.Integer, primary_key=True)
    IdUbigeo = db.Column(db.Integer, nullable=False)  # Relación con la tabla Región
    Enfermedad = db.Column(db.String(100), nullable=False)
    Diagnostico = db.Column(db.String(255), nullable=False)
    Año = db.Column(db.Integer, nullable=False)
    Semana = db.Column(db.Integer, nullable=False)
    Edad = db.Column(db.Integer, nullable=False)
    TipoEdad = db.Column(db.String(20), nullable=False)  # Tipo de edad (por ejemplo, "años", "meses")
    Sexo = db.Column(db.String(10), nullable=False)  # Sexo (por ejemplo, "M" o "F")

    def __init__(self, IdUbigeo, Enfermedad, Diagnostico, Año, Semana, Edad, TipoEdad, Sexo):
        self.IdUbigeo = IdUbigeo
        self.Enfermedad = Enfermedad
        self.Diagnostico = Diagnostico
        self.Año = Año
        self.Semana = Semana
        self.Edad = Edad
        self.TipoEdad = TipoEdad
        self.Sexo = Sexo
