from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, Cliente

cliente_bp = Blueprint('clientes', __name__)

users = {
    "1": "1",
    "2": "2"
}

@cliente_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('usuario')
    password = request.json.get('senha')

    if username not in users or users[username] != password:
        return jsonify({"msg": "Usuário ou senha incorretos"}), 401
        
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@cliente_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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
