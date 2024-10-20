# routes/region_routes.py

from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.region import Region  # Asegúrate de importar el modelo
from schemas.region_schema import region_schema, regions_schema  

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
    
# Nuevos Endpoints para los Filtros
@region_routes.route('/departamentos', methods=['GET'])
def get_departamentos():
    # Ordenar departamentos alfabéticamente
    departamentos = db.session.query(Region.Departamento).distinct().order_by(Region.Departamento.asc()).all()
    departamentos_list = [dept[0] for dept in departamentos]
    return jsonify({'departamentos': departamentos_list}), 200


@region_routes.route('/provincias', methods=['GET'])
def get_provincias():
    departamento = request.args.get('departamento')
    if not departamento:
        return jsonify({'error': 'Parámetro "departamento" requerido'}), 400
    # Ordenar provincias alfabéticamente
    provincias = db.session.query(Region.Provincia).filter_by(Departamento=departamento).distinct().order_by(Region.Provincia.asc()).all()
    provincias_list = [prov[0] for prov in provincias]
    return jsonify({'provincias': provincias_list}), 200


@region_routes.route('/distritos', methods=['GET'])
def get_distritos():
    provincia = request.args.get('provincia')
    if not provincia:
        return jsonify({'error': 'Parámetro "provincia" requerido'}), 400
    # Ordenar distritos alfabéticamente
    distritos = db.session.query(Region.Distrito).filter_by(Provincia=provincia).distinct().order_by(Region.Distrito.asc()).all()
    distritos_list = [dist[0] for dist in distritos]
    return jsonify({'distritos': distritos_list}), 200


# Obtener latitud y longitud de una región basada en los filtros
@region_routes.route('/regiones/coords', methods=['GET'])
def get_region_coords():
    departamento = request.args.get('departamento')
    provincia = request.args.get('provincia')
    distrito = request.args.get('distrito')

    # Construir la consulta dinámica basada en los filtros proporcionados
    query = Region.query

    if distrito:
        query = query.filter_by(Distrito=distrito)
    elif provincia:
        query = query.filter_by(Provincia=provincia)
    elif departamento:
        query = query.filter_by(Departamento=departamento)

    # Obtener la primera región que coincida con los filtros
    region = query.first()

    if not region:
        return jsonify({'error': 'Región no encontrada'}), 404

    # Devolver latitud y longitud
    return jsonify({'lat': region.Latitud, 'lng': region.Longitud}), 200
