from flask import Blueprint, request, jsonify
from models import db, Produto

produto_bp = Blueprint('produtos', __name__)

@produto_bp.route('/produtos', methods=['POST'])
def criar_produto():

    produto = request.json

    novo_produto = Produto(
        produto_nome=produto.get('produto_nome'),
        produto_preco=produto.get('produto_preco')
        )
    
    db.session.add(novo_produto)
    db.session.commit()

    return jsonify({
        'id': novo_produto.produto_id, 
        'produto_nome': novo_produto.produto_nome, 
        'produto_preco': novo_produto.produto_preco
        }), 201

@produto_bp.route('/produtos', methods=['GET'])
def listar_produtos():

    produtos = Produto.query.all()  
    return jsonify([{
        'id': p.produto_id, 
        'produto_nome': p.produto_nome, 
        'produto_preco': p.produto_preco
        } for p in produtos]), 200

@produto_bp.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):

    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404

    dados = request.json
    if 'produto_nome' in dados:
        produto.produto_nome = dados['produto_nome']
    if 'produto_preco' in dados:
        produto.produto_preco = dados['produto_preco']

    db.session.commit()
    return jsonify({'Produto alterado': produto.produto_nome}), 200

@produto_bp.route('/produtos/<int:id>', methods=['DELETE'])
def excluir_produto(id):
    
    produto = Produto.query.get(id)

    if not produto:
        return jsonify({'Mensagem': 'Produto não encontrado'}), 404
    
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'Mensagem': 'Produto excluído'}), 200
