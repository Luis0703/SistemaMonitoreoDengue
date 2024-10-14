from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.caso import Caso
from models.region import Region

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
        Anio=data.get('Anio'),
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
    caso.Anio = data.get('Anio', caso.Anio)
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

# Endpoint para obtener los datos del mapa de calor
@caso_routes.route('/casos/mapa-calor', methods=['GET'])
def get_casos_mapa_calor():
    # Filtros opcionales
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    departamento = request.args.get('departamento')
    provincia = request.args.get('provincia')
    distrito = request.args.get('distrito')

    # Base de la consulta: unir Caso y Región por el campo IdUbigeo
    query = db.session.query(Region.Latitud, Region.Longitud, db.func.count(Caso.IdCaso).label('cantidad_casos')) \
        .join(Caso, Caso.IdUbigeo == Region.IdUbigeo) \
        .group_by(Region.Latitud, Region.Longitud)

    # Aplicar filtros si están presentes
    if fecha_inicio and fecha_fin:
        query = query.filter(Caso.Anio >= fecha_inicio, Caso.Anio <= fecha_fin)
    
    if departamento:
        query = query.filter(Region.Departamento == departamento)
    
    if provincia:
        query = query.filter(Region.Provincia == provincia)
    
    if distrito:
        query = query.filter(Region.Distrito == distrito)

    # Ejecutar la consulta
    resultados = query.all()

    # Formatear los datos para el mapa de calor
    heatmap_data = []
    for resultado in resultados:
        heatmap_data.append({
            'lat': resultado.Latitud,
            'lng': resultado.Longitud,
            'cantidad_casos': resultado.cantidad_casos  # Cantidad de casos en ese lugar
        })

    return make_response(jsonify({'message': 'Datos del mapa de calor', 'status': 200, 'data': heatmap_data}), 200)