from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.caso import Caso
from models.region import Region
from schemas.caso_schema import caso_schema, casos_schema  # Asegúrate de importar el schema
from sqlalchemy import text

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

@caso_routes.route('/resumen', methods=['GET'])
def get_resumen():
    total_casos = Caso.query.count()
    alertas_activas = 10  # Valor estático como ejemplo
    zonas_controladas = 78  # Otro valor estático

    return jsonify({
        'totalCasos': total_casos,
        'alertasActivas': alertas_activas,
        'zonasControladas': zonas_controladas
    })

@caso_routes.route('/casos/tendencia', methods=['GET'])
def get_tendencia():
    # Envolver la consulta SQL en text()
    results = db.session.execute(
        text("""
        SELECT "Anio", COUNT(*) as count
        FROM public."Caso"
        GROUP BY "Anio"
        ORDER BY "Anio" DESC
        LIMIT 6
        """)
    )

    # Convertir los resultados en una lista de diccionarios
    tendencia = [{"anio": row[0], "casos": row[1]} for row in results]

    # Ordenar los resultados en orden ascendente de años para el gráfico
    tendencia = sorted(tendencia, key=lambda x: x["anio"])

    return jsonify(tendencia)



@caso_routes.route('/noticias', methods=['GET'])
def get_noticias():
    noticias = [
        "Nueva alerta en la región norte",
        "Actualización del sistema v2.3",
        "Campaña de prevención en escuelas"
    ]
    return jsonify(noticias)

@caso_routes.route('/consejos', methods=['GET'])
def get_consejos():
    consejos = [
        {"titulo": "Elimina agua estancada", "descripcion": "Revisa y vacía recipientes que puedan acumular agua."},
        {"titulo": "Usa repelente", "descripcion": "Aplica repelente de insectos en áreas expuestas de la piel."},
        {"titulo": "Mantén tu entorno limpio", "descripcion": "Limpia y desinfecta regularmente áreas propensas a mosquitos."}
    ]
    return jsonify(consejos)


