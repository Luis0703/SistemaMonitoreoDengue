# routes/usuarios_routes.py
from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from models.usuarios import Usuario
from schemas.usuarios_schema import usuario_schema, usuarios_schema
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity


usuarios_routes = Blueprint("usuarios_routes", __name__)

# Obtener todos los usuarios
@usuarios_routes.route('/usuarios', methods=['GET'])
def get_usuarios():
    all_usuarios = Usuario.query.all()
    result = usuarios_schema.dump(all_usuarios)
    return make_response(jsonify({'message': 'Lista de usuarios', 'status': 200, 'data': result}), 200)

# Crear un nuevo usuario
@usuarios_routes.route('/usuarios', methods=['POST'])
def add_usuario():
    nombre_usuario = request.json.get('nombre_usuario')
    email = request.json.get('email')
    contrasena = request.json.get('contrasena')  # Asegúrate de recibir 'contrasena', no 'contrasena_hash'
    
    if not nombre_usuario or not email or not contrasena:
        return make_response(jsonify({'message': 'Faltan datos', 'status': 400}), 400)
    
    # Verificar si el usuario o email ya existen
    if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
        return make_response(jsonify({'message': 'El nombre de usuario ya existe', 'status': 400}), 400)
    if Usuario.query.filter_by(email=email).first():
        return make_response(jsonify({'message': 'El email ya está registrado', 'status': 400}), 400)
    
    new_usuario = Usuario(nombre_usuario, email, contrasena)
    
    try:
        db.session.add(new_usuario)
        db.session.commit()
        return make_response(jsonify({'message': 'Usuario creado con éxito', 'status': 201}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error al crear el usuario', 'status': 500, 'error': str(e)}), 500)

# Obtener un usuario por ID
@usuarios_routes.route('/usuarios/<id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if not usuario:
        return make_response(jsonify({'message': 'Usuario no encontrado', 'status': 404}), 404)
    result = usuario_schema.dump(usuario)
    return make_response(jsonify({'message': 'Usuario encontrado', 'status': 200, 'data': result}), 200)

# Ruta de login
@usuarios_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nombre_usuario = data.get('nombre_usuario')
    contrasena = data.get('contrasena')

    if not nombre_usuario or not contrasena:
        return jsonify({'message': 'Faltan datos', 'status': 400}), 400

    usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()

    if usuario and usuario.verificar_contrasena(contrasena):
        access_token = create_access_token(identity=usuario.id)
        return jsonify({'message': 'Inicio de sesión exitoso', 'status': 200, 'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Nombre de usuario o contraseña incorrectos', 'status': 401}), 401
    
# Ruta protegida
@usuarios_routes.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    usuario_id = get_jwt_identity()
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({'message': 'Usuario no encontrado', 'status': 404}), 404
    result = usuario_schema.dump(usuario)
    return jsonify({'message': 'Perfil de usuario', 'status': 200, 'data': result}), 200