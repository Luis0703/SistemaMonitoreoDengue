from flask import Flask
from routes.usuarios_routes import usuarios_routes
from routes.region_routes import region_routes
from routes.caso_routes import caso_routes
from routes.brote_routes import brote_routes
from routes.reporte_routes import reporte_routes
from routes.notificacion_routes import notificacion_routes
from routes.predicciones_routes import predicciones_routes
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION_URI
from flask_cors import CORS
from utils.db import db
from flask_jwt_extended import JWTManager
from routes.noticia_routes import noticia_routes


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

app.register_blueprint(usuarios_routes)  # Registra las rutas de usuarios
app.register_blueprint(region_routes)
app.register_blueprint(caso_routes)
app.register_blueprint(brote_routes)
app.register_blueprint(reporte_routes)
app.register_blueprint(notificacion_routes)
app.register_blueprint(predicciones_routes)
app.register_blueprint(noticia_routes)


if __name__ == '__main__':
    app.run(debug=True)
