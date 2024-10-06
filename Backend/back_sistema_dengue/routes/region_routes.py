from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.region import Region  # Asegúrate de importar el modelo
from schemas.region_schema import region_schema, regions_schema  # Asumiendo que tienes un schema definido

# Crear el Blueprint para las rutas de la región
region_routes = Blueprint("region_routes", __name__)

# Obtener todas las regiones
@region_routes.route('/regiones', methods=['GET'])
def get_regiones():
    all_regiones = Region.query.all()
    result = regions_schema.dump(all_regiones)
    return make_response(jsonify({'message': 'Lista de regiones', 'status': 200, 'data': result}), 200)

# Obtener una región por su ID
@region_routes.route('/regiones/<id>', methods=['GET'])
def get_region(id):
    region = Region.query.get(id)
    if not region:
        return make_response(jsonify({'message': 'Región no encontrada', 'status': 404}), 404)
    result = region_schema.dump(region)
    return make_response(jsonify({'message': 'Región encontrada', 'status': 200, 'data': result}), 200)

# Crear una nueva región
@region_routes.route('/regiones', methods=['POST'])
def add_region():
    data = request.get_json()
    new_region = Region(
        Departamento=data.get('Departamento'),
        Provincia=data.get('Provincia'),
        Distrito=data.get('Distrito'),
        Altitud=data.get('Altitud'),
        Latitud=data.get('Latitud'),
        Longitud=data.get('Longitud')
    )
    
    try:
        db.session.add(new_region)
        db.session.commit()
        return make_response(jsonify({'message': 'Región creada con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear la región', 'status': 500, 'error': str(e)}), 500)

# Actualizar una región existente
@region_routes.route('/regiones/<id>', methods=['PUT'])
def update_region(id):
    region = Region.query.get(id)
    if not region:
        return make_response(jsonify({'message': 'Región no encontrada', 'status': 404}), 404)

    data = request.get_json()
    region.Departamento = data.get('Departamento', region.Departamento)
    region.Provincia = data.get('Provincia', region.Provincia)
    region.Distrito = data.get('Distrito', region.Distrito)
    region.Altitud = data.get('Altitud', region.Altitud)
    region.Latitud = data.get('Latitud', region.Latitud)
    region.Longitud = data.get('Longitud', region.Longitud)
    
    try:
        db.session.commit()
        return make_response(jsonify({'message': 'Región actualizada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al actualizar la región', 'status': 500, 'error': str(e)}), 500)

# Eliminar una región
@region_routes.route('/regiones/<id>', methods=['DELETE'])
def delete_region(id):
    region = Region.query.get(id)
    if not region:
        return make_response(jsonify({'message': 'Región no encontrada', 'status': 404}), 404)

    try:
        db.session.delete(region)
        db.session.commit()
        return make_response(jsonify({'message': 'Región eliminada con éxito', 'status': 200}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al eliminar la región', 'status': 500, 'error': str(e)}), 500)
