from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Pedido

pedido_bp = Blueprint('pedidos', __name__)

@pedido_bp.route('/pedidos', methods=['POST'])
def criar_pedido():

    pedido = request.json

    if not all(key in pedido for key in ('data_compra', 'cliente_id')):
        return jsonify({'error': 'Os campos data_compra e cliente_id são obrigatórios.'}), 400

    try:
        _data_compra = datetime.strptime(pedido['data_compra'], '%Y-%m-%d').date()
        novo_pedido = Pedido(data_compra=_data_compra, cliente_id=pedido['cliente_id'])
        
        db.session.add(novo_pedido)
        db.session.commit()

        return jsonify({'id': novo_pedido.pedido_id, 'data_compra': novo_pedido.data_compra.strftime('%Y-%m-%d')}), 201
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar o pedido.', 'mensagem': str(e)}), 500

@pedido_bp.route('/pedidos', methods=['GET'])
def listar_pedidos():
    
    pedidos = Pedido.query.all()
    pedidos_lista = [{'id': p.pedido_id, 'data_compra': p.data_compra.strftime('%Y-%m-%d'), 'cliente_id': p.cliente_id} for p in pedidos]
    
    return jsonify(pedidos_lista), 200
