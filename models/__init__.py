from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .produto import Produto
from .usuario import Usuario
from .pedido import Pedido
from .cliente import Cliente
from .detalhePedido import DetalhePedido
from .categoria import Categoria