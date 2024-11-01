from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
from controllers import cliente_bp, produto_bp, usuario_bp, pedido_bp, detalhePedido_bp, categoria_bp
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = 'gatopreto'  

jwt = JWTManager(app)
migrate = Migrate(app, db)

db.init_app(app)

app.register_blueprint(cliente_bp, url_prefix='/clientes')
app.register_blueprint(produto_bp, url_prefix='/produtos')
app.register_blueprint(usuario_bp, url_prefix='/usuarios')
app.register_blueprint(pedido_bp, url_prefix='/pedidos')
app.register_blueprint(detalhePedido_bp, url_prefix='/detalhepedidos')
app.register_blueprint(categoria_bp, url_prefix='/categorias')

if __name__ == '__main__':
    app.run(debug=True)
