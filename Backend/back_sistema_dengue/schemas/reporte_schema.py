from utils.ma import ma  # Asumiendo que "ma" es la instancia de Marshmallow
from models.reporte import Reporte  # Asegúrate de importar el modelo "Reporte"

class ReporteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Reporte
        fields = ('IdReporte', 'Fecha_Reporte', 'Tipo_Reporte', 'IdUsuario', 'IdUbigeo')  # Campos a serializar

# Esquemas para un solo reporte y para varios reportes
reporte_schema = ReporteSchema()
reportes_schema = ReporteSchema(many=True)
