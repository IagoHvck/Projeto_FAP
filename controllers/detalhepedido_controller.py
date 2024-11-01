from flask import Blueprint, request, jsonify
from models import db, DetalhePedido

detalhePedido_bp = Blueprint('detalhepedidos', __name__)

@detalhePedido_bp.route('/detalhepedidos', methods=['POST'])
def criar_detalhe_pedido():
    
    dados = request.json
    
    novo_detalhe_pedido = DetalhePedido(
        dt_pedido_id=dados['dt_pedido_id'],
        dt_produto_id=dados['dt_produto_id'],
        dt_valor=dados['dt_valor'],
        dt_desconto=dados.get('dt_desconto', 0)
    )
    
    db.session.add(novo_detalhe_pedido)
    db.session.commit()
    
    return jsonify({'id': novo_detalhe_pedido.dt_id}), 201

@detalhePedido_bp.route('/detalhepedidos', methods=['GET'])
def listar_detalhes_pedidos():
    
    detalhes = DetalhePedido.query.all()
    
    detalhes_lista = [{
        'id': d.dt_id,
        'pedido_id': d.dt_pedido_id,
        'produto_id': d.dt_produto_id,
        'valor': str(d.dt_valor),
        'desconto': str(d.dt_desconto)  
    } for d in detalhes]
    
    return jsonify(detalhes_lista), 200

@detalhePedido_bp.route('/detalhepedidos/<int:id>', methods=['PUT'])
def atualizar_detalhe_pedido(id):
    
    detalhe_pedido = DetalhePedido.query.get(id)
    
    if not detalhe_pedido:
        return jsonify({'Mensagem': 'Detalhe de pedido não encontrado'}), 404
    
    dados = request.json
    detalhe_pedido.dt_pedido_id = dados.get('dt_pedido_id', detalhe_pedido.dt_pedido_id)
    detalhe_pedido.dt_produto_id = dados.get('dt_produto_id', detalhe_pedido.dt_produto_id)
    detalhe_pedido.dt_valor = dados.get('dt_valor', detalhe_pedido.dt_valor)
    detalhe_pedido.dt_desconto = dados.get('dt_desconto', detalhe_pedido.dt_desconto)
    
    db.session.commit()
    
    return jsonify({
        'id': detalhe_pedido.dt_id,
        'pedido_id': detalhe_pedido.dt_pedido_id,
        'produto_id': detalhe_pedido.dt_produto_id,
        'valor': str(detalhe_pedido.dt_valor),
        'desconto': str(detalhe_pedido.dt_desconto)
    }), 200

@detalhePedido_bp.route('/detalhepedidos/<int:id>', methods=['DELETE'])
def deletar_detalhe_pedido(id):

    detalhe_pedido = DetalhePedido.query.get(id)
    
    if not detalhe_pedido:
        return jsonify({'Mensagem': 'Detalhe de pedido não encontrado'}), 404

    db.session.delete(detalhe_pedido)
    db.session.commit()

    return jsonify({'Mensagem': 'Detalhe de pedido deletado com sucesso'}), 200
