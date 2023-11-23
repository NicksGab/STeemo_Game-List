from flask import render_template, redirect, session, url_for, flash

def Views(self, app):

  @app.route('/') 
  def index():
    self.atualizaJogosRegistrados()
    return render_template('lista.html', tituloPagina=self.tituloPagina, titulo='Jogos', jogos=self.listaJogos)


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




  @app.route('/apagar/<string:tabela>')
  def apagar(tabela):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
      flash("Usuario não autenticado")
      return redirect(url_for('index'))
    
    response = self.apagaTabela(tabela)
    if response:
      flash(f"Registros excluídos de {tabela}!")
      return redirect(url_for('index'))
      
    flash(f"Não foi possível excluir os dados da tabela: {tabela}!")
    return redirect(url_for('index'))
    
