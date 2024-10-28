from flask import Blueprint, request, jsonify 
from models import db, Usuario

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():

    usuario = request.json
    novo_usuario = Usuario(usuario_login=usuario['usuario_login'], usuario_senha=usuario['usuario_senha'])
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({'id': novo_usuario.usuario_id, 'nome': novo_usuario.usuario_login}), 201

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    
    usuarios = Usuario.query.all() 
    usuarios_lista = [{'id': u.usuario_id, 'usuario_login': u.usuario_login} for u in usuarios]

    return jsonify(usuarios_lista), 200

@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.json
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado'}), 404

    usuario.usuario_login = dados['usuario_login']
    db.session.commit()

    return jsonify({'Usuário alterado': usuario.usuario_login})

@usuario_bp.route('/usuarios<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    usuario = Usuario.query.get(id)

    if not usuario:
        return jsonify({'Mensagem': 'Usuário não encontrado'})
    
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'Usuário excluido'}), 200


     
    

