from utils.ma import ma  # Asumiendo que "ma" es la instancia de Marshmallow
from models.notificacion import Notificacion  # Asegúrate de importar el modelo "Notificación"

class NotificacionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Notificacion
        fields = ('IdNotificacion', 'Tipo_Notificacion', 'Fecha_Notificacion', 'Mensaje', 'IdUsuario', 'IdUbigeo')  # Campos a serializar

# Esquemas para una sola notificación y para varias notificaciones
notificacion_schema = NotificacionSchema()
notificaciones_schema = NotificacionSchema(many=True)
