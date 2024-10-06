from utils.db import db

class Region(db.Model):
    __tablename__ = 'Region'

    IdUbigeo = db.Column(db.Integer, primary_key=True)
    Departamento = db.Column(db.String(100), nullable=False)
    Provincia = db.Column(db.String(100), nullable=False)
    Distrito = db.Column(db.String(100), nullable=False)
    Altitud = db.Column(db.Float, nullable=True)  # Si es un valor decimal
    Latitud = db.Column(db.Float, nullable=True)
    Longitud = db.Column(db.Float, nullable=True)

    def __init__(self, Departamento, Provincia, Distrito, Altitud=None, Latitud=None, Longitud=None):
        self.Departamento = Departamento
        self.Provincia = Provincia
        self.Distrito = Distrito
        self.Altitud = Altitud
        self.Latitud = Latitud
        self.Longitud = Longitud
