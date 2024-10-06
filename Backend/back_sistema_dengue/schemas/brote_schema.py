from utils.ma import ma  # Asumiendo que "ma" es la instancia de Marshmallow
from models.brote import Brote  # Asegúrate de importar el modelo "Brote"

class BroteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Brote
        fields = ('IdBrote', 'Fecha_Inicio', 'Fecha_Fin', 'Numero_Casos', 'Gravedad', 'IdUbigeo')  # Campos a serializar

# Esquemas para un solo brote y para varios brotes
brote_schema = BroteSchema()
brotes_schema = BroteSchema(many=True)
