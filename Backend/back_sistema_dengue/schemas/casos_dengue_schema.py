from utils.ma import ma
from models.casos_dengue import CasosDengue

class CasosDengueSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CasosDengue
        fields = ('casos_dengue_id', 'departamento', 'provincia', 'distrito', 'localidad', 'enfermedad', 'ano', 'semana', 'diagnostic', 'diresa', 'ubigeo', 'localcod', 'edad', 'tipo_edad', 'sexo')

casoDengue_schema = CasosDengueSchema()
casosDengue_schema = CasosDengueSchema(many=True)