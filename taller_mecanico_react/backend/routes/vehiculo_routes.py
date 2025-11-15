from flask import Blueprint, request, jsonify
from models.vehiculo import Vehiculo
from db import db
from models.cliente import Cliente

vehiculo_bp = Blueprint('vehiculo_bp', __name__)

@vehiculo_bp.route('/', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([{
        'id': v.id,
        'marca': v.marca,
        'modelo': v.modelo,
        'patente': v.patente,
        'anio': v.anio,
        'cliente_id': v.cliente_id
    } for v in vehiculos])

@vehiculo_bp.route('/<int:id>', methods=['GET'])
def get_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    return jsonify({
        'id': vehiculo.id,
        'marca': vehiculo.marca,
        'modelo': vehiculo.modelo,
        'patente': vehiculo.patente,
        'anio': vehiculo.anio,
        'cliente_id': vehiculo.cliente_id
    })

@vehiculo_bp.route('/', methods=['POST'])
def create_vehiculo():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    cliente_id = data.get('cliente_id')
    if not cliente_id:
        return jsonify({'error': 'El campo cliente_id es obligatorio'}), 400

    cliente = Cliente.query.get(cliente_id)
    if not cliente:
        return jsonify({'error': 'El cliente especificado no existe'}), 404

    try:
        nuevo = Vehiculo(
            marca=data.get('marca'),
            modelo=data.get('modelo'),
            patente=data.get('patente'),
            anio=data.get('anio'),
            cliente_id=cliente_id
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'message': 'Vehículo creado', 'id': nuevo.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@vehiculo_bp.route('/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    vehiculo = Vehiculo.query.get_or_404(id)
    try:
        vehiculo.marca = data.get('marca', vehiculo.marca)
        vehiculo.modelo = data.get('modelo', vehiculo.modelo)
        vehiculo.patente = data.get('patente', vehiculo.patente)
        vehiculo.anio = data.get('anio', vehiculo.anio)
        vehiculo.cliente_id = data.get('cliente_id', vehiculo.cliente_id)
        db.session.commit()
        return jsonify({'message': 'Vehículo actualizado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@vehiculo_bp.route('/<int:id>', methods=['DELETE'])
def delete_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    try:
        db.session.delete(vehiculo)
        db.session.commit()
        return jsonify({'message': 'Vehículo eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
