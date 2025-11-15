from flask import Flask
from flask_cors import CORS
from db import db
from routes.cliente_routes import cliente_bp
from routes.vehiculo_routes import vehiculo_bp
from routes.reparacion_routes import reparacion_bp
import os

app = Flask(__name__)
CORS(app)

# ----------------------------
# Configuración de la base de datos
# ----------------------------
# Se toma la variable de entorno DATABASE_URL que Railway nos da
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    raise ValueError("No se encontró la variable de entorno DATABASE_URL")

# Ajuste para SQLAlchemy con mysqlconnector
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("mysql://", "mysql+mysqlconnector://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ----------------------------
# Clave secreta (opcional)
# ----------------------------
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_por_defecto')

# ----------------------------
# Inicializar la base de datos
# ----------------------------
db.init_app(app)

# ----------------------------
# Registrar rutas
# ----------------------------
app.register_blueprint(cliente_bp, url_prefix='/api/clientes')
app.register_blueprint(vehiculo_bp, url_prefix='/api/vehiculos')
app.register_blueprint(reparacion_bp, url_prefix='/api/reparaciones')

# ----------------------------
# Crear tablas y ejecutar app
# ----------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
