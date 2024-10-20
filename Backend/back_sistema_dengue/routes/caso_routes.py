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
def get_mapa_calor():
    # Obtener los parámetros de la solicitud
    anio_inicio = request.args.get('anio_inicio', type=int)
    semana_inicio = request.args.get('semana_inicio', type=int)
    anio_fin = request.args.get('anio_fin', type=int)
    semana_fin = request.args.get('semana_fin', type=int)
    
    # Construir la consulta de selección, solo obteniendo latitud, longitud y cantidad de casos
    query = db.session.query(
        Region.Latitud, 
        Region.Longitud, 
        db.func.count(Caso.IdCaso).label('cantidad_casos')
    ).join(Region, Caso.IdUbigeo == Region.IdUbigeo)

    # Aplicar los filtros de año y semana si están presentes
    if anio_inicio and semana_inicio and anio_fin and semana_fin:
        query = query.filter(
            Caso.Anio >= anio_inicio,
            Caso.Anio <= anio_fin,
            db.or_(
                db.and_(Caso.Anio == anio_inicio, Caso.Semana >= semana_inicio),
                db.and_(Caso.Anio == anio_fin, Caso.Semana <= semana_fin),
                db.and_(Caso.Anio > anio_inicio, Caso.Anio < anio_fin)
            )
        )

    # Agrupar por ubicación (latitud y longitud)
    query = query.group_by(Region.Latitud, Region.Longitud)

    # Ejecutar la consulta y obtener los resultados
    result = query.all()

    # Convertir los resultados a un formato adecuado para el mapa de calor
    data = [{'lat': r.Latitud, 'lng': r.Longitud, 'cantidad_casos': r.cantidad_casos} for r in result]

    return jsonify({'data': data})

