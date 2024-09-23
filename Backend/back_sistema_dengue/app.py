from flask import Flask
from routes.casos_dengue_routes import casos_dengue_routes
from routes.usuarios_routes import usuarios_routes
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION_URI
from flask_cors import CORS
from utils.db import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = 'clavesecreta123'
app.config["JWT_SECRET_KEY"] = 'clavesecreta123'  

# Inicializa JWTManager
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800

# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)
jwt = JWTManager(app)  # Inicializa JWTManager

app.register_blueprint(casos_dengue_routes)
app.register_blueprint(usuarios_routes)  # Registra las rutas de usuarios

if __name__ == '__main__':
    app.run(debug=True)
