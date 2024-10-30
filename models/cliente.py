from . import db

class Cliente(db.Model):
    
    __tablename__ = "clientes"

    cliente_id = db.Column(db.Integer, primary_key=True)
    cliente_nome = db.Column(db.String(50), nullable=False)
    cliente_email = db.Column(db.String(120), nullable=False, unique=True)