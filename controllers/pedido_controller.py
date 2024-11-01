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

@pedido_bp.route('/pedidos/<int:id>', methods=['PUT'])
def atualizar_pedido(id):
    
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    dados = request.json

    if 'data_compra' in dados:
        try:
            pedido.data_compra = datetime.strptime(dados['data_compra'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

    if 'cliente_id' in dados:
        pedido.cliente_id = dados['cliente_id']

    try:
        db.session.commit()
        return jsonify({
            'id': pedido.pedido_id,
            'data_compra': pedido.data_compra.strftime('%Y-%m-%d'),
            'cliente_id': pedido.cliente_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar o pedido.', 'mensagem': str(e)}), 500

@pedido_bp.route('/pedidos/<int:id>', methods=['DELETE'])
def deletar_pedido(id):
    
    pedido = Pedido.query.get(id)

    if not pedido:
        return jsonify({'error': 'Pedido não encontrado'}), 404

    try:
        db.session.delete(pedido)
        db.session.commit()
        return jsonify({'mensagem': 'Pedido deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao deletar o pedido.', 'mensagem': str(e)}), 500
