from utils.db import db

class CasosDengue(db.Model):
    __tablename__ = "casos_dengue"

    casos_dengue_id =db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(50))
    provincia = db.Column(db.String(50))
    distrito = db.Column(db.String(50))
    localidad = db.Column(db.String(50))
    enfermedad = db.Column(db.String(100))
    ano = db.Column(db.SmallInteger)
    semana = db.Column(db.SmallInteger)
    diagnostic = db.Column(db.String(10))
    diresa = db.Column(db.SmallInteger)
    ubigeo = db.Column(db.String(10))
    localcod = db.Column(db.String(10))
    edad = db.Column(db.SmallInteger)
    tipo_edad = db.Column(db.String(1))
    sexo = db.Column(db.String(1))

    def __init__(self, departamento, provincia, distrito, localidad, enfermedad, ano, semana, diagnostic, diresa, ubigeo, localcod, edad, tipo_edad, sexo):
        self.departamento = departamento
        self.provincia = provincia
        self.distrito = distrito
        self.localidad = localidad
        self.enfermedad = enfermedad
        self.ano = ano
        self.semana = semana
        self.diagnostic = diagnostic
        self.diresa = diresa
        self.ubigeo = ubigeo
        self.localcod = localcod
        self.edad = edad
        self.tipo_edad = tipo_edad
        self.sexo = sexo
