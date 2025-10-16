from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave-secreta'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
db = SQLAlchemy(app)

# -------- MODELOS -------- #
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

# -------- ROTAS -------- #

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/produto/<int:id>')
def produto(id):
    produto = Produto.query.get_or_404(id)
    avaliacoes = Avaliacao.query.filter_by(produto_id=id).all()
    return render_template('produto.html', produto=produto, avaliacoes=avaliacoes)

@app.route('/add', methods=['POST'])
def add_produto():
    nome = request.form['nome']
    descricao = request.form['descricao']
    imagem = request.files['imagem']

    filename = None
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    novo = Produto(nome=nome, descricao=descricao, imagem=filename)
    db.session.add(novo)
    db.session.commit()
    flash('Produto adicionado com sucesso!')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    produto = Produto.query.get_or_404(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']

        imagem = request.files['imagem']
        if imagem and imagem.filename:
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            produto.imagem = filename

        db.session.commit()
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('index'))

    return render_template('editar.html', produto=produto)

@app.route('/delete/<int:id>')
def delete_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/avaliar/<int:produto_id>', methods=['POST'])
def avaliar(produto_id):
    nota = int(request.form['nota'])
    comentario = request.form['comentario']
    avaliacao = Avaliacao(nota=nota, comentario=comentario, produto_id=produto_id)
    db.session.add(avaliacao)
    db.session.commit()
    flash('Avaliação registrada!')
    return redirect(url_for('produto', id=produto_id))

# Inicializa o banco
if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    if not os.path.exists(os.path.join('static', 'uploads')):
        os.makedirs(os.path.join('static', 'uploads'))
    with app.app_context():
        db.create_all()
    app.run(debug=True)