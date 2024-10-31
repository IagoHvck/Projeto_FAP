from flask import Blueprint, request, jsonify
from models import db, Cliente

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    cliente = request.json
    novo_cliente = Cliente(cliente_nome=cliente['cliente_nome'], cliente_email=cliente['cliente_email'])

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({'id': novo_cliente.cliente_id, 'nome': novo_cliente.cliente_nome, 'email': novo_cliente.cliente_email}), 201

@cliente_bp.route('/clientes', methods=['GET'])
def listar_cliente():
    clientes = Cliente.query.all()
    cliente_lista = [{'id': c.cliente_id, 'cliente_nome': c.cliente_nome, 'cliente_email': c.cliente_email} for c in clientes]

    return jsonify(cliente_lista), 200
