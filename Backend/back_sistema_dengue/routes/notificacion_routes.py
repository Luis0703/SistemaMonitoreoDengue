from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.notificacion import Notificacion
from schemas.notificacion_schema import notificacion_schema, notificaciones_schema  # Asegúrate de importar el schema

notificacion_routes = Blueprint("notificacion_routes", __name__)

# Obtener todas las notificaciones con filtros y orden
@notificacion_routes.route('/notificaciones', methods=['GET'])
def get_notificaciones():
    tipo = request.args.get('tipo')  # Filtrar por tipo de notificación
    fecha_inicio = request.args.get('fecha_inicio')  # Filtrar desde esta fecha
    fecha_fin = request.args.get('fecha_fin')  # Filtrar hasta esta fecha

    query = Notificacion.query

    if tipo:
        query = query.filter(Notificacion.Tipo_Notificacion == tipo)
    if fecha_inicio:
        query = query.filter(Notificacion.Fecha_Notificacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Notificacion.Fecha_Notificacion <= fecha_fin)

    query = query.order_by(Notificacion.Fecha_Notificacion.desc())  # Ordenar por fecha descendente

    all_notificaciones = query.all()
    result = notificaciones_schema.dump(all_notificaciones)

    return make_response(jsonify({'message': 'Lista de notificaciones', 'status': 200, 'data': result}), 200)

# Obtener una notificación por su ID
@notificacion_routes.route('/notificaciones/<id>', methods=['GET'])
def get_notificacion(id):
    notificacion = Notificacion.query.get(id)
    if not notificacion:
        return make_response(jsonify({'message': 'Notificación no encontrada', 'status': 404}), 404)
    result = notificacion_schema.dump(notificacion)
    return make_response(jsonify({'message': 'Notificación encontrada', 'status': 200, 'data': result}), 200)

# Crear una nueva notificación con validaciones
@notificacion_routes.route('/notificaciones', methods=['POST'])
def add_notificacion():
    data = request.get_json()

    # Validar campos requeridos
    required_fields = ['Tipo_Notificacion', 'Fecha_Notificacion', 'Mensaje', 'IdUsuario', 'IdUbigeo']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return make_response(jsonify({'message': f'Campos faltantes: {", ".join(missing_fields)}', 'status': 400}), 400)

    new_notificacion = Notificacion(
        Tipo_Notificacion=data['Tipo_Notificacion'],
        Fecha_Notificacion=data['Fecha_Notificacion'],
        Mensaje=data['Mensaje'],
        IdUsuario=data['IdUsuario'],
        IdUbigeo=data['IdUbigeo']
    )

    try:
        db.session.add(new_notificacion)
        db.session.commit()
        return make_response(jsonify({'message': 'Notificación creada con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear la notificación', 'status': 500, 'error': str(e)}), 500)

# Actualizar una notificación existente con validaciones
@notificacion_routes.route('/notificaciones/<id>', methods=['PUT'])
def update_notificacion(id):
    notificacion = Notificacion.query.get(id)
    if not notificacion:
        return make_response(jsonify({'message': 'Notificación no encontrada', 'status': 404}), 404)

    data = request.get_json()
    notificacion.Tipo_Notificacion = data.get('Tipo_Notificacion', notificacion.Tipo_Notificacion)
    notificacion.Fecha_Notificacion = data.get('Fecha_Notificacion', notificacion.Fecha_Notificacion)
    notificacion.Mensaje = data.get('Mensaje', notificacion.Mensaje)
    notificacion.IdUsuario = data.get('IdUsuario', notificacion.IdUsuario)
    notificacion.IdUbigeo = data.get('IdUbigeo', notificacion.IdUbigeo)

    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Notificación actualizada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar la notificación', 'status': 500, 'error': str(e)}), 500)

# Eliminar una notificación
@notificacion_routes.route('/notificaciones/<id>', methods=['DELETE'])
def delete_notificacion(id):
    notificacion = Notificacion.query.get(id)
    if not notificacion:
        return make_response(jsonify({'message': 'Notificación no encontrada', 'status': 404}), 404)

    try:
        db.session.delete(notificacion)
        db.session.commit()
        return make_response(jsonify({'message': 'Notificación eliminada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar la notificación', 'status': 500, 'error': str(e)}), 500)

# Obtener notificaciones recientes
@notificacion_routes.route('/notificaciones/recientes', methods=['GET'])
def get_recent_notificaciones():
    limit = request.args.get('limit', 5, type=int)  # Limitar resultados, por defecto 10
    recent_notificaciones = Notificacion.query.order_by(Notificacion.Fecha_Notificacion.desc()).limit(limit).all()
    result = notificaciones_schema.dump(recent_notificaciones)
    return make_response(jsonify({'message': 'Últimas notificaciones', 'status': 200, 'data': result}), 200)

# Obtener notificaciones asociadas a un usuario
@notificacion_routes.route('/notificaciones/usuario', methods=['GET'])
def get_user_notificaciones():
    user_id = request.args.get('user_id')  # Asume que esto proviene de un token o sesión
    if not user_id:
        return make_response(jsonify({'message': 'Usuario no autenticado', 'status': 401}), 401)

    user_notificaciones = Notificacion.query.filter_by(IdUsuario=user_id).all()
    result = notificaciones_schema.dump(user_notificaciones)
    return make_response(jsonify({'message': 'Notificaciones del usuario', 'status': 200, 'data': result}), 200)

