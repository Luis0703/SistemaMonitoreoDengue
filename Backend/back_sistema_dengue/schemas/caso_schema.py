from utils.ma import ma  # Asumiendo que "ma" es la instancia de Marshmallow
from models.caso import Caso  # Asegúrate de importar el modelo "Caso"

class CasoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Caso
        fields = ('IdCaso', 'IdUbigeo', 'Enfermedad', 'Diagnostico', 'Anio', 'Semana', 'Edad', 'TipoEdad', 'Sexo')  # Campos a serializar

# Esquemas para un solo caso y para varios casos
caso_schema = CasoSchema()
casos_schema = CasoSchema(many=True)
