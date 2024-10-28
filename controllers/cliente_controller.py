from flask import Blueprint, request, jsonify
from models import db, Cliente, Produto, Pedido, DetalhePedido

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

    cliente = Cliente.query.all()
    cliente_lista = [{'id': c.cliente_id, 'cliente_nome': c.cliente_nome, 'cliente_email': c.cliente_email } for c in cliente]

    return jsonify(cliente_lista), 200

@cliente_bp.route('/clienteproduto', methods=['GET'])
def gerar_relatorio():

    relatorio = db.session.query(
        Cliente.cliente_nome.label('cliente_nome'),
        Produto.produto_nome.label('produto_nome')
    ).join(
        Pedido, Pedido.cliente_id == Cliente.cliente_id
    ).join(
        DetalhePedido, DetalhePedido.dp_pedido_id == Pedido.pedido_id
    ).join(
        Produto, Produto.produto_id == DetalhePedido.dp_produto_id
    ).all()

    pedido_lista = [{'produto_nome': c.produto_nome, 'cliente_nome': c.cliente_nome} for c in relatorio]

    return jsonify(pedido_lista), 200
