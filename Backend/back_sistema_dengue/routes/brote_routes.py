from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.brote import Brote
from schemas.brote_schema import brote_schema, brotes_schema  # Asegúrate de importar el schema

brote_routes = Blueprint("brote_routes", __name__)

# Obtener todos los brotes
@brote_routes.route('/brotes', methods=['GET'])
def get_brotes():
    all_brotes = Brote.query.all()
    result = brotes_schema.dump(all_brotes)
    return make_response(jsonify({'message': 'Lista de brotes', 'status': 200, 'data': result}), 200)

# Obtener un brote por su ID
@brote_routes.route('/brotes/<id>', methods=['GET'])
def get_brote(id):
    brote = Brote.query.get(id)
    if not brote:
        return make_response(jsonify({'message': 'Brote no encontrado', 'status': 404}), 404)
    result = brote_schema.dump(brote)
    return make_response(jsonify({'message': 'Brote encontrado', 'status': 200, 'data': result}), 200)

# Crear un nuevo brote
@brote_routes.route('/brotes', methods=['POST'])
def add_brote():
    data = request.get_json()
    new_brote = Brote(
        Fecha_Inicio=data.get('Fecha_Inicio'),
        Fecha_Fin=data.get('Fecha_Fin'),
        Numero_Casos=data.get('Numero_Casos'),
        Gravedad=data.get('Gravedad'),
        IdUbigeo=data.get('IdUbigeo')
    )
    
    try:
        db.session.add(new_brote)
        db.session.commit()
        return make_response(jsonify({'message': 'Brote creado con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear el brote', 'status': 500, 'error': str(e)}), 500)

# Actualizar un brote existente
@brote_routes.route('/brotes/<id>', methods=['PUT'])
def update_brote(id):
    brote = Brote.query.get(id)
    if not brote:
        return make_response(jsonify({'message': 'Brote no encontrado', 'status': 404}), 404)

    data = request.get_json()
    brote.Fecha_Inicio = data.get('Fecha_Inicio', brote.Fecha_Inicio)
    brote.Fecha_Fin = data.get('Fecha_Fin', brote.Fecha_Fin)
    brote.Numero_Casos = data.get('Numero_Casos', brote.Numero_Casos)
    brote.Gravedad = data.get('Gravedad', brote.Gravedad)
    brote.IdUbigeo = data.get('IdUbigeo', brote.IdUbigeo)
    
    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Brote actualizado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar el brote', 'status': 500, 'error': str(e)}), 500)

# Eliminar un brote
@brote_routes.route('/brotes/<id>', methods=['DELETE'])
def delete_brote(id):
    brote = Brote.query.get(id)
    if not brote:
        return make_response(jsonify({'message': 'Brote no encontrado', 'status': 404}), 404)

    try:
        db.session.delete(brote)
        db.session.commit()
        return make_response(jsonify({'message': 'Brote eliminado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar el brote', 'status': 500, 'error': str(e)}), 500)
