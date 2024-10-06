from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.caso import Caso
from schemas.caso_schema import caso_schema, casos_schema  # Asegúrate de importar el schema

caso_routes = Blueprint("caso_routes", __name__)

# Obtener todos los casos
@caso_routes.route('/casos', methods=['GET'])
def get_casos():
    all_casos = Caso.query.all()
    result = casos_schema.dump(all_casos)
    return make_response(jsonify({'message': 'Lista de casos', 'status': 200, 'data': result}), 200)

# Obtener un caso por su ID
@caso_routes.route('/casos/<id>', methods=['GET'])
def get_caso(id):
    caso = Caso.query.get(id)
    if not caso:
        return make_response(jsonify({'message': 'Caso no encontrado', 'status': 404}), 404)
    result = caso_schema.dump(caso)
    return make_response(jsonify({'message': 'Caso encontrado', 'status': 200, 'data': result}), 200)

# Crear un nuevo caso
@caso_routes.route('/casos', methods=['POST'])
def add_caso():
    data = request.get_json()
    new_caso = Caso(
        IdUbigeo=data.get('IdUbigeo'),
        Enfermedad=data.get('Enfermedad'),
        Diagnostico=data.get('Diagnostico'),
        Año=data.get('Año'),
        Semana=data.get('Semana'),
        Edad=data.get('Edad'),
        TipoEdad=data.get('TipoEdad'),
        Sexo=data.get('Sexo')
    )
    
    try:
        db.session.add(new_caso)
        db.session.commit()
        return make_response(jsonify({'message': 'Caso creado con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear el caso', 'status': 500, 'error': str(e)}), 500)

# Actualizar un caso existente
@caso_routes.route('/casos/<id>', methods=['PUT'])
def update_caso(id):
    caso = Caso.query.get(id)
    if not caso:
        return make_response(jsonify({'message': 'Caso no encontrado', 'status': 404}), 404)

    data = request.get_json()
    caso.IdUbigeo = data.get('IdUbigeo', caso.IdUbigeo)
    caso.Enfermedad = data.get('Enfermedad', caso.Enfermedad)
    caso.Diagnostico = data.get('Diagnostico', caso.Diagnostico)
    caso.Año = data.get('Año', caso.Año)
    caso.Semana = data.get('Semana', caso.Semana)
    caso.Edad = data.get('Edad', caso.Edad)
    caso.TipoEdad = data.get('TipoEdad', caso.TipoEdad)
    caso.Sexo = data.get('Sexo', caso.Sexo)
    
    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Caso actualizado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar el caso', 'status': 500, 'error': str(e)}), 500)

# Eliminar un caso
@caso_routes.route('/casos/<id>', methods=['DELETE'])
def delete_caso(id):
    caso = Caso.query.get(id)
    if not caso:
        return make_response(jsonify({'message': 'Caso no encontrado', 'status': 404}), 404)

    try:
        db.session.delete(caso)
        db.session.commit()
        return make_response(jsonify({'message': 'Caso eliminado con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar el caso', 'status': 500, 'error': str(e)}), 500)
