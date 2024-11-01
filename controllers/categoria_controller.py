from flask import Blueprint, jsonify, request
from models import Categoria, db  

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/categorias', methods=['POST'])
def criar_categoria():
    
    categoria = request.json
    
    nova_categoria = Categoria(
        categoria_nome=categoria['categoria_nome']
        )
    
    db.session.add(nova_categoria)
    db.session.commit()
    
    return jsonify({
        'id': nova_categoria.categoria_id,
        'categoria_nome': nova_categoria.categoria_nome
        }), 201

@categoria_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    
    categorias = Categoria.query.all()
    return jsonify([{
        'id': c.categoria_id, 
        'categoria_nome': c.categoria_nome
        } for c in categorias])

@categoria_bp.route('/categorias/<int:id>', methods=['PUT'])
def atualizar_categoria(id):
    
    categoria = Categoria.query.get(id)
    
    if not categoria:
        return jsonify({'Mensagem': 'Categoria não encontrada'}), 404
    
    dados = request.json
    categoria.categoria_nome = dados.get('categoria_nome', categoria.categoria_nome)
    
    db.session.commit()
    
    return jsonify({
        'id': categoria.categoria_id, 
        'categoria_nome': categoria.categoria_nome
        })

@categoria_bp.route('/categorias/<int:id>', methods=['DELETE'])
def deletar_categoria(id):
    
    categoria = Categoria.query.get(id)
    
    if not categoria:
        return jsonify({'Mensagem': 'Categoria não encontrada'}), 404
    
    db.session.delete(categoria)
    db.session.commit()
    
    return jsonify({'Mensagem': 'Categoria deletada com sucesso'}), 200
