from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.reporte import Reporte
from schemas.reporte_schema import reporte_schema, reportes_schema  # Asegúrate de importar el schema

reporte_routes = Blueprint("reporte_routes", __name__)

# Obtener todos los reportes
@reporte_routes.route('/reportes', methods=['GET'])
def get_reportes():
    all_reportes = Reporte.query.all()
    result = reportes_schema.dump(all_reportes)
    return make_response(jsonify({'message': 'Lista de reportes', 'status': 200, 'data': result}), 200)

# Obtener un reporte por su ID
@reporte_routes.route('/reportes/<id>', methods=['GET'])
def get_reporte(id):
    reporte = Reporte.query.get(id)
    if not reporte:
        return make_response(jsonify({'message': 'Reporte no encontrado', 'status': 404}), 404)
    result = reporte_schema.dump(reporte)
    return make_response(jsonify({'message': 'Reporte encontrado', 'status': 200, 'data': result}), 200)

# Crear un nuevo reporte
@reporte_routes.route('/reportes', methods=['POST'])
def add_reporte():
    data = request.get_json()
    new_reporte = Reporte(
        Fecha_Reporte=data.get('Fecha_Reporte'),
        Tipo_Reporte=data.get('Tipo_Reporte'),
        IdUsuario=data.get('IdUsuario'),
        IdUbigeo=data.get('IdUbigeo')
    )
    
    try:
        db.session.add(new_reporte)
        db.session.commit()
        return make_response(jsonify({'message': 'Reporte creado con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear el reporte', 'status': 500, 'error': str(e)}), 500)

# Actualizar un reporte existente
@reporte_routes.route('/reportes/<id>', methods=['PUT'])
def update_reporte(id):
    reporte = Reporte.query.get(id)
    if not reporte:
        return make_response(jsonify({'message': 'Reporte no encontrado', 'status': 404}), 404)

    data = request.get_json()
    reporte.Fecha_Reporte = data.get('Fecha_Reporte', reporte.Fecha_Reporte)
    reporte.Tipo_Reporte = data.get('Tipo_Reporte', reporte.Tipo_Reporte)
    reporte.IdUsuario = data.get('IdUsuario', reporte.IdUsuario)
    reporte.IdUbigeo = data.get('IdUbigeo', reporte.IdUbigeo)
    
    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Reporte actualizado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar el reporte', 'status': 500, 'error': str(e)}), 500)

# Eliminar un reporte
@reporte_routes.route('/reportes/<id>', methods=['DELETE'])
def delete_reporte(id):
    reporte = Reporte.query.get(id)
    if not reporte:
        return make_response(jsonify({'message': 'Reporte no encontrado', 'status': 404}), 404)

    try:
        db.session.delete(reporte)
        db.session.commit()
        return make_response(jsonify({'message': 'Reporte eliminado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar el reporte', 'status': 500, 'error': str(e)}), 500)
