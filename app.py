from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave-secreta'  # Necessário para formulários
db = SQLAlchemy(app)

# Modelo inicial
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Produto {self.nome}>'

# Rota inicial
@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/<int:id>')
def produto(id):
    produto = Produto.query.get_or_404(id)
    return render_template('produto.html', produto=produto)

@app.route('/add', methods=['POST'])
def add_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    novo = Produto(nome=nome, descricao=descricao)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
