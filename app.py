from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from controllers import cliente_bp, produto_bp, usuario_bp, pedido_bp, detalhePedido_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'gatopreto'  

jwt = JWTManager(app)

db.init_app(app)

app.register_blueprint(cliente_bp, url_prefix='/clientes')
app.register_blueprint(produto_bp, url_prefix='/produtos')
app.register_blueprint(usuario_bp, url_prefix='/usuarios')
app.register_blueprint(pedido_bp, url_prefix='/pedidos')
app.register_blueprint(detalhePedido_bp, url_prefix='/detalhepedidos')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
