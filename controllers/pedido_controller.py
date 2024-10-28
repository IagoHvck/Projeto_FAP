from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido

pedido_bp = Blueprint('pedidos', __name__)

@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():

    pedido = request.json
    _data_compra = datetime.strptime(pedido['data_compra'], '%Y-%m-%d').date()
    novo_pedido = Pedido(data_compra=_data_compra,
                         cliente_id=pedido['cliente_id'])
    db.session.add(novo_pedido)
    db.session.commit()

    return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra})

@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():

    pedidos = Pedido.query.all()
    pedidos_lista = [{'id': p.pedido_id, 'data_compra': p.data_compra.strftime('%Y-%m-%d'), 'cliente_id': p.cliente_id} for p in pedidos]
    
    return jsonify(pedidos_lista), 200
