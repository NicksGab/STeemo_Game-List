from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

from dotenv import load_dotenv
import os

from models.Jogo import Jogo
from models.Usuario import Usuario
from models.DataBase import DataBase

from views.Views_User import Views_User
from views.Views_Game import Views_Game
from views.Views import Views

from config.Config import *

load_dotenv(r".env/.Env")





class STeemo:
  
  def __init__(self):
    self.tituloPagina = TITULO_DO_PROJETO
    self.diretorioJsonJogos = PATH_JSON_JOGOS
    self.diretorioJsonUsuarios = PATH_JSON_USUARIOS

    self.DB = DataBase()

    self.DB.CreateBackup()

    self.app = Flask(__name__)
    self.app.secret_key = os.getenv("SECRET_KEY_APP")
    self.csrf = CSRFProtect(self.app)
    self.bcrypt = Bcrypt(self.app)

    self.views = Views(self, self.app)
    self.viewsUser = Views_User(self, self.app)
    self.viewsGame = Views_Game(self, self.app)

    self.app.run(debug=True)

    self.DB.CreateBackup()

  def atualizaJogosRegistrados(self):
    self.listaJogos = []

    jogos = self.DB.GetJogos()

    for jogo in jogos:
      self.listaJogos.append(Jogo(jogo))



  def registraNovoJogo(self, info):
    self.DB.CreateJogo(info)
    jogoDB = self.pegaJogoPorNome(info['Name'])
    return Jogo(jogoDB[0])

  def registraNovoUsuario(self, info):
    self.DB.CreateUsuario(info)

  def pegaUsuario(self, args):
    if not args:
      return None
    
    usuarioTemp = args[0]
    usuario = Usuario(usuarioTemp[1], 
                      usuarioTemp[2],
                      usuarioTemp[3])
    return usuario


  def pegaJogoPorId(self, game_id):
    jogolist = self.DB.GetJogoById(game_id)[0]

    jogo = Jogo(jogolist)

    return jogo
  
  def pegaJogoPorNome(self, nome):
    jogo = self.DB.GetJogoByName(nome)

    return jogo

  def atualizaJogoNoBanco(self, jogo):
    self.DB.UpdateJogo(jogo)


  def deletaJogoDoBanco(self, game_id):
    self.DB.DeleteJogo(game_id)


  def backupJson(self):
    self.DB.CreateBackup()

  def restauraBackupJogos(self):
    self.DB.RestoreBackupJogos()

  def restauraBackupusuarios(self):
    self.DB.RestoreBackupUsuarios()




  def apagaTabela(self, tabela):
    print('entrou app')
    return self.DB.TruncateTable(tabela)


if __name__ == '__main__': 
  STeemo()  