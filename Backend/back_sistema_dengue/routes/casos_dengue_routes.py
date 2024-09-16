from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.casos_dengue import CasosDengue
from schemas.casos_dengue_schema import casoDengue_schema, casosDengue_schema

casos_dengue_routes = Blueprint("casos_dengue_routes", __name__)

@casos_dengue_routes.route('/casosDengue', methods=['GET'])
def get_CasosDengue():
    # Limitar la consulta a solo los primeros 5 registros
    limited_casos_dengue = CasosDengue.query.limit(5).all()
    
    # Serializar los datos
    result = casosDengue_schema.dump(limited_casos_dengue)

    data = {
        'message': 'Primeros 5 Casos de Dengue',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)


"""
@casos_dengue_routes.route('/casosDengue', methods=['GET'])
def get_CasosDengue():
    all_casos_dengue = CasosDengue.query.all()
    result = casosDengue_schema.dump(all_casos_dengue)

    data = {
        'message': 'Todas las Casos de Dengue',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)
"""