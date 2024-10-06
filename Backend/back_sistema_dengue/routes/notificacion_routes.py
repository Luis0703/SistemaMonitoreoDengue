from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.notificacion import Notificacion
from schemas.notificacion_schema import notificacion_schema, notificaciones_schema  # Asegúrate de importar el schema

notificacion_routes = Blueprint("notificacion_routes", __name__)

# Obtener todas las notificaciones
@notificacion_routes.route('/notificaciones', methods=['GET'])
def get_notificaciones():
    all_notificaciones = Notificacion.query.all()
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

# Crear una nueva notificación
@notificacion_routes.route('/notificaciones', methods=['POST'])
def add_notificacion():
    data = request.get_json()
    new_notificacion = Notificacion(
        Tipo_Notificacion=data.get('Tipo_Notificacion'),
        Fecha_Notificacion=data.get('Fecha_Notificacion'),
        Mensaje=data.get('Mensaje'),
        IdUsuario=data.get('IdUsuario'),
        IdUbigeo=data.get('IdUbigeo')
    )
    
    try:
        db.session.add(new_notificacion)
        db.session.commit()
        return make_response(jsonify({'message': 'Notificación creada con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear la notificación', 'status': 500, 'error': str(e)}), 500)

# Actualizar una notificación existente
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
