from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import Produto, Avaliacao
import os

def init_routes(app):

    @app.route('/')
    def index():
            produtos = Produto.query.all()
            medias = []
            nomes = []
            for produto in produtos:
                avaliacoes = produto.avaliacoes
                if avaliacoes:
                    media = sum(a.nota for a in avaliacoes) / len(avaliacoes)
                else:
                    media = None
                medias.append(media)
                nomes.append(produto.nome)
            return render_template('index.html', produtos=produtos, medias=medias, nomes=nomes)

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
            imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

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
                imagem.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
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