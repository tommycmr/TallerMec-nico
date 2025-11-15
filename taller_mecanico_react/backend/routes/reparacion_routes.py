from flask import Blueprint, request, jsonify
from models.reparacion import Reparacion
from db import db
from datetime import datetime

reparacion_bp = Blueprint('reparacion_bp', __name__)

@reparacion_bp.route('/', methods=['GET'])
def get_reparaciones():
    reparaciones = Reparacion.query.all()
    return jsonify([{
        'id': r.id,
        'fecha': r.fecha,
        'descripcion_problema': r.descripcion_problema,
        'trabajos_realizados': r.trabajos_realizados,
        'costo': r.costo,
        'vehiculo_id': r.vehiculo_id
    } for r in reparaciones])

@reparacion_bp.route('/<int:id>', methods=['GET'])
def get_reparacion(id):
    reparacion = Reparacion.query.get_or_404(id)
    return jsonify({
        'id': reparacion.id,
        'fecha': reparacion.fecha,
        'descripcion_problema': reparacion.descripcion_problema,
        'trabajos_realizados': reparacion.trabajos_realizados,
        'costo': reparacion.costo,
        'vehiculo_id': reparacion.vehiculo_id
    })

@reparacion_bp.route('/', methods=['POST'])
def create_reparacion():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    fecha = data.get('fecha', datetime.now().strftime('%Y-%m-%d'))

    try:
        nueva = Reparacion(
            fecha=fecha,
            descripcion_problema=data.get('descripcion_problema'),
            trabajos_realizados=data.get('trabajos_realizados'),
            costo=data.get('costo'),
            vehiculo_id=data.get('vehiculo_id')
        )
        db.session.add(nueva)
        db.session.commit()
        return jsonify({'message': 'Reparación creada', 'id': nueva.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reparacion_bp.route('/<int:id>', methods=['PUT'])
def update_reparacion(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    reparacion = Reparacion.query.get_or_404(id)
    try:
        reparacion.fecha = data.get('fecha', reparacion.fecha)
        reparacion.descripcion_problema = data.get('descripcion_problema', reparacion.descripcion_problema)
        reparacion.trabajos_realizados = data.get('trabajos_realizados', reparacion.trabajos_realizados)
        reparacion.costo = data.get('costo', reparacion.costo)
        reparacion.vehiculo_id = data.get('vehiculo_id', reparacion.vehiculo_id)
        db.session.commit()
        return jsonify({'message': 'Reparación actualizada'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reparacion_bp.route('/<int:id>', methods=['DELETE'])
def delete_reparacion(id):
    reparacion = Reparacion.query.get_or_404(id)
    try:
        db.session.delete(reparacion)
        db.session.commit()
        return jsonify({'message': 'Reparación eliminada'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
