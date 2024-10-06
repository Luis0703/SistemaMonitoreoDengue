from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.predicciones import Predicciones
from schemas.predicciones_schema import prediccion_schema, predicciones_schema  # Asegúrate de importar el schema

predicciones_routes = Blueprint("predicciones_routes", __name__)

# Obtener todas las predicciones
@predicciones_routes.route('/predicciones', methods=['GET'])
def get_predicciones():
    all_predicciones = Predicciones.query.all()
    result = predicciones_schema.dump(all_predicciones)
    return make_response(jsonify({'message': 'Lista de predicciones', 'status': 200, 'data': result}), 200)

# Obtener una predicción por su ID
@predicciones_routes.route('/predicciones/<id>', methods=['GET'])
def get_prediccion(id):
    prediccion = Predicciones.query.get(id)
    if not prediccion:
        return make_response(jsonify({'message': 'Predicción no encontrada', 'status': 404}), 404)
    result = prediccion_schema.dump(prediccion)
    return make_response(jsonify({'message': 'Predicción encontrada', 'status': 200, 'data': result}), 200)

# Crear una nueva predicción
@predicciones_routes.route('/predicciones', methods=['POST'])
def add_prediccion():
    data = request.get_json()
    new_prediccion = Predicciones(
        Fecha_Prediccion=data.get('Fecha_Prediccion'),
        Probabilidad_Brote=data.get('Probabilidad_Brote'),
        IdUbigeo=data.get('IdUbigeo')
    )
    
    try:
        db.session.add(new_prediccion)
        db.session.commit()
        return make_response(jsonify({'message': 'Predicción creada con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear la predicción', 'status': 500, 'error': str(e)}), 500)

# Actualizar una predicción existente
@predicciones_routes.route('/predicciones/<id>', methods=['PUT'])
def update_prediccion(id):
    prediccion = Predicciones.query.get(id)
    if not prediccion:
        return make_response(jsonify({'message': 'Predicción no encontrada', 'status': 404}), 404)

    data = request.get_json()
    prediccion.Fecha_Prediccion = data.get('Fecha_Prediccion', prediccion.Fecha_Prediccion)
    prediccion.Probabilidad_Brote = data.get('Probabilidad_Brote', prediccion.Probabilidad_Brote)
    prediccion.IdUbigeo = data.get('IdUbigeo', prediccion.IdUbigeo)
    
    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Predicción actualizada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar la predicción', 'status': 500, 'error': str(e)}), 500)

# Eliminar una predicción
@predicciones_routes.route('/predicciones/<id>', methods=['DELETE'])
def delete_prediccion(id):
    prediccion = Predicciones.query.get(id)
    if not prediccion:
        return make_response(jsonify({'message': 'Predicción no encontrada', 'status': 404}), 404)

    try:
        db.session.delete(prediccion)
        db.session.commit()
        return make_response(jsonify({'message': 'Predicción eliminada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar la predicción', 'status': 500, 'error': str(e)}), 500)
