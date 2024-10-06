from utils.ma import ma  # Asumiendo que "ma" es la instancia de Marshmallow
from models.predicciones import Predicciones  # Asegúrate de importar el modelo "Predicciones"

class PrediccionesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Predicciones
        fields = ('IdPrediccion', 'Fecha_Prediccion', 'Probabilidad_Brote', 'IdUbigeo')  # Campos a serializar

# Esquemas para una sola predicción y para varias predicciones
prediccion_schema = PrediccionesSchema()
predicciones_schema = PrediccionesSchema(many=True)
