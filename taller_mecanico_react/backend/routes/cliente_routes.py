from flask import Blueprint, request, jsonify
from models.cliente import Cliente
from db import db

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'telefono': c.telefono,
        'email': c.email,
        'direccion': c.direccion
    } for c in clientes])

@cliente_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify({
        'id': cliente.id,
        'nombre': cliente.nombre,
        'telefono': cliente.telefono,
        'email': cliente.email,
        'direccion': cliente.direccion
    })

@cliente_bp.route('/', methods=['POST'])
def create_cliente():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    try:
        nuevo = Cliente(
            nombre=data.get('nombre'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            direccion=data.get('direccion')
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'message': 'Cliente creado', 'id': nuevo.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    cliente = Cliente.query.get_or_404(id)
    try:
        cliente.nombre = data.get('nombre')
        cliente.telefono = data.get('telefono')
        cliente.email = data.get('email')
        cliente.direccion = data.get('direccion')
        db.session.commit()
        return jsonify({'message': 'Cliente actualizado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        # Eliminar reparaciones y vehículos asociados
        for vehiculo in cliente.lista_vehiculos:
            for reparacion in vehiculo.reparaciones:
                db.session.delete(reparacion)
        for vehiculo in cliente.lista_vehiculos:
            db.session.delete(vehiculo)
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Cliente eliminado'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
