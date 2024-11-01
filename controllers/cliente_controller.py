from flask import Blueprint, request, jsonify
from models import db, Cliente

cliente_bp = Blueprint('clientes', __name__)

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    
    cliente = request.json
    
    novo_cliente = Cliente(
        cliente_nome=cliente['cliente_nome'], 
        cliente_email=cliente['cliente_email']
        )

    db.session.add(novo_cliente)
    db.session.commit()

    return jsonify({'id': novo_cliente.cliente_id, 
                    'nome': novo_cliente.cliente_nome, 
                    'email': novo_cliente.cliente_email
                    }), 201

@cliente_bp.route('/clientes', methods=['GET'])
def listar_cliente():
    clientes = Cliente.query.all()
    cliente_lista = [{
        'id': c.cliente_id, 
        'cliente_nome': c.cliente_nome, 
        'cliente_email': c.cliente_email
        } for c in clientes]

    return jsonify(cliente_lista), 200

@cliente_bp.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({'Mensagem': 'Cliente não encontrado'}), 404
    
    dados = request.json
    cliente.cliente_nome = dados.get('cliente_nome', cliente.cliente_nome)
    cliente.cliente_email = dados.get('cliente_email', cliente.cliente_email)

    db.session.commit()

    return jsonify({
        'id': cliente.cliente_id, 
        'nome': cliente.cliente_nome, 
        'email': cliente.cliente_email
    }), 200

@cliente_bp.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    
    cliente = Cliente.query.get(id)
    
    if not cliente:
        return jsonify({'Mensagem': 'Cliente não encontrado'}), 404

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({'Mensagem': 'Cliente deletado com sucesso'}), 200
