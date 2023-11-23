from flask import render_template, request, redirect, session, flash, url_for


def Views(self, app):

  @app.route('/')
  def index():
    self.atualizaJogosRegistrados()
    return render_template('lista.html', tituloPagina=self.tituloPagina, titulo='Jogos', jogos=self.listaJogos)


  
  @app.route('/novo')
  def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('novo')))

    return render_template('novo.html', tituloPagina=self.tituloPagina, titulo='Novo jogo')
  
  @app.route('/criar', methods=['POST'])
  def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    plataforma = request.form['plataforma']

    existeJogo = self.pegaJogoPorNome(nome)
    print(existeJogo)
    if existeJogo:
      flash('Jogo já registrado!')
      return redirect(url_for('novo'))

    info = {
            'Name': nome, 
            'Category': categoria, 
            'Platform': plataforma
           }

    self.registraNovoJogo(info)

    return redirect(url_for('index'))


  
  @app.route('/editar/<int:id>')
  def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('editar')))

    jogo = self.pegaJogoPorId(id)

    return render_template('editar.html', tituloPagina=self.tituloPagina, titulo='Editando jogo', jogo=jogo)

  @app.route('/atualizar', methods=['POST'])
  def atualizar():
    jogo = self.pegaJogoPorId(request.form['id'])

    jogo.setNome(request.form['nome'])
    jogo.setCategoria(request.form['categoria'])
    jogo.setPlataforma(request.form['plataforma'])

    self.atualizaJogoNoBanco(jogo)

    return redirect(url_for('index'))
      
  
  @app.route('/deletar/<int:id>')
  def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login'))
  
    self.deletaJogoDoBanco(id)
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))
        
  
  @app.route('/login')
  def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima) 


  
  @app.route('/autenticar', methods=['Post'])
  def autenticar():
    usuario = self.pegaUsuario(self.DB.GetUsuarioByNick(request.form['usuario']))

    if usuario:
      if request.form['senha'] == usuario.Senha:
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
    return render_template('cadastro.html')

  @app.route('/cadastrarUsuario', methods=['POST'])
  def cadastrarUsuario():
    nome = request.form['nome']
    nickname = request.form['nickname']
    password = request.form['senha']

    info = {"Name": nome,
            "Nickname": nickname,
            "Password": self.cryptguard.encrypt(password)}

    self.registraNovoUsuario(info)

    session['usuario_logado'] = nickname

    return redirect(url_for('index'))




  @app.route('/backup')
  def atualizarBackup():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('atualizarBackup')))
  
    self.backupJson()
    return redirect(url_for('index'))

  @app.route('/restore_games_backup')
  def emergencyGamesBackup():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('emergencyGamesBackup')))
  
    self.restauraBackupJogos()
    return redirect(url_for('index'))

  @app.route('/restore_users_backup')
  def restauraBackupusuarios():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      return redirect(url_for('login', proxima=url_for('restauraBackupusuarios')))

    self.backupJson()
    return redirect(url_for('index'))