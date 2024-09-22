# schemas/usuarios_schemas.py
from utils.ma import ma
from models.usuarios import Usuario

class UsuarioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Usuario
        fields = ('id', 'nombre_usuario', 'email', 'contrasena_hash')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
