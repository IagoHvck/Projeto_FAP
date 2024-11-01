from . import db

class Categoria(db.Model):
    
    __tablename__ = "categorias"
    
    categoria_id = db.Column(db.Integer, primary_key=True)
    categoria_nome = db.Column(db.String(50), nullable=False)
    
    