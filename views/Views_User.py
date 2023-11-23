from flask import render_template, request, redirect, session, flash, url_for
from helpers.Helpers import FormularioUsuario, FormularioCadastro
from flask_bcrypt import generate_password_hash, check_password_hash



def Views_User(self, app):
  @app.route('/login')
  def login():
    proxima = request.args.get('proxima')

    form = FormularioUsuario()
  
    return render_template('login.html', proxima=proxima, form=form) 


  
  @app.route('/autenticar', methods=['Post'])
  def autenticar():
    form = FormularioUsuario(request.form)

    usuario = self.pegaUsuario(self.DB.GetUsuarioByNick(form.nickname.data))
    if not usuario:
      return redirect(url_for('cadastro'))
    senha = check_password_hash(usuario.Senha, form.senha.data)

    if usuario and senha:
      session['usuario_logado'] = usuario.Nickname
      flash('Bem vindo, ' + usuario.Nome + '!')

      proximaPagina = request.form['proxima']
      if proximaPagina == 'None' or not proximaPagina:
        proximaPagina = '/'
      return redirect(proximaPagina)

    flash('Falha na autenticação de usuário!')
    return redirect(url_for('login'))

  
  @app.route('/logout')
  def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!') 
    return redirect(url_for('index'))


  @app.route('/cadastro')
  def cadastro():
    proxima = request.args.get('proxima')

    form = FormularioCadastro()

    return render_template('cadastro.html', tituloPagina=self.tituloPagina, titulo='Cadastrar novo usuário', proxima=proxima, form=form)

  @app.route('/cadastrarUsuario', methods=['POST'])
  def cadastrarUsuario():
    form = FormularioCadastro(request.form)

    nome = form.nome.data
    nickname = form.nickname.data
    password = form.senha.data

    info = {"Name": nome,
            "Nickname": nickname,
            "Password": generate_password_hash(password).decode('utf-8')}

    self.registraNovoUsuario(info)

    session['usuario_logado'] = nickname

    return redirect(url_for('index'))