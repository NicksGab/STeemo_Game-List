from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from helpers.Helpers import recuperaImagem, deletaArquivo, FormularioJogos
from config.Config import *
import time

def Views_Game(self, app):

  @app.route('/novo')
  def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('novo')))

    form = FormularioJogos()

    return render_template('novo.html', tituloPagina=self.tituloPagina, titulo='Novo jogo', form=form)
  
  @app.route('/criar', methods=['POST'])
  def criar():
    form = FormularioJogos(request.form)

    if not form.validate_on_submit():
      return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    plataforma = form.plataforma.data

    existeJogo = self.pegaJogoPorNome(nome)

    if existeJogo:
      flash('Jogo já registrado!')
      return redirect(url_for('novo'))

    info = {
            'Name': nome, 
            'Category': categoria, 
            'Platform': plataforma
           }

    novoJogo = self.registraNovoJogo(info)

    arquivo = request.files['arquivo']
    timestamp = time.time()
    arquivo.save(f'{UPLOAD_PATH}/Capa{novoJogo.Id}-{timestamp}.jpg')

    return redirect(url_for('index'))


  
  @app.route('/editar/<int:id>')
  def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = self.pegaJogoPorId(id)

    form = FormularioJogos()
    form.nome.data = jogo.Nome
    form.categoria.data = jogo.Categoria
    form.plataforma.data = jogo.Plataforma

    capaJogo = recuperaImagem(id)

    return render_template('editar.html', tituloPagina=self.tituloPagina, titulo='Editando jogo', id=id, capaJogo=capaJogo, form=form)

  @app.route('/atualizar', methods=['POST'])
  def atualizar():
    form = FormularioJogos(request.form)

    if form.validate_on_submit():
      jogo = self.pegaJogoPorId(request.form['id'])

      jogo.setNome(form.nome.data)
      jogo.setCategoria(form.categoria.data)
      jogo.setPlataforma(form.plataforma.data)

      self.atualizaJogoNoBanco(jogo)

      arquivo = request.files['arquivo']
      deletaArquivo(jogo.Id)

      timestamp = time.time()
      arquivo.save(f'{UPLOAD_PATH}/Capa{jogo.Id}-{timestamp}.jpg')

      return redirect(url_for('index'))
    
    flash('Falha ao editar jogo')
    return redirect(url_for('index'))
      
  
  @app.route('/deletar/<int:id>')
  def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login'))
  
    self.deletaJogoDoBanco(id)
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))
        




  @app.route('/uploads/<nome_arquivo>')
  def imagemPadrao(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)