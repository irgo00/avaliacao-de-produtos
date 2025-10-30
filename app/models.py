from app import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.String(200))
    avaliacoes = db.relationship('Avaliacao', backref='produto', cascade="all, delete-orphan")

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)