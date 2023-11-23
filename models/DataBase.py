from config.Config import *
from json import load, dump
import sqlite3

class DataBase:
  def __init__(self):
    self.CreateTables() 

  def Connection(self):
    return sqlite3.connect(r"database/STeemoDB.db")

  def CreateTables(self):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS jogos (
                      Game_ID INTEGER PRIMARY KEY,
                      Name TEXT NOT NULL,
                      Category TEXT NOT NULL,
                      Platform TEXT NOT NULL
                    );
                  """)
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS usuarios (
                      User_ID INTEGER PRIMARY KEY,
                      Name TEXT NOT NULL,
                      Nickname TEXT NOT NULL,
                      Password TEXT NOT NULL
                    );
                  """)

    connection.commit()
    cursor.close()
    connection.close() #



  def CreateJogo(self, jogo):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f"insert into jogos (Name, Category, Platform) values ('{jogo['Name']}','{jogo['Category']}','{jogo['Platform']}')")

    connection.commit()
    cursor.close()
    connection.close()

  def CreateUsuario(self, usuario):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f"insert into usuarios (Name, Nickname, Password) values ('{usuario['Name']}','{usuario['Nickname']}','{usuario['Password']}')")

    connection.commit()
    cursor.close()
    connection.close()

  
  def GetJogos(self): 
    connection = self.Connection()
    cursor = connection.cursor()

    jogos = cursor.execute('select * from jogos').fetchall()

    cursor.close()
    connection.close()

    return jogos

  def GetUsuarios(self): 
    connection = self.Connection()
    cursor = connection.cursor()

    usuarios = cursor.execute('select * from usuarios').fetchall()

    cursor.close()
    connection.close()

    return usuarios

  def GetUsuarioByNick(self, nick):
    connection = self.Connection()
    cursor = connection.cursor()

    usuario = cursor.execute(f'select * from usuarios where Nickname = "{nick}"').fetchall()

    cursor.close()
    connection.close()

    return usuario

  def GetJogoById(self, game_id):
    connection = self.Connection()
    cursor = connection.cursor()

    jogo = cursor.execute(f'select * from jogos where Game_ID = {game_id}').fetchall()

    cursor.close()
    connection.close()

    return jogo

  def GetJogoByName(self, name):
    connection = self.Connection()
    cursor = connection.cursor()

    jogo = cursor.execute(f"select * from jogos where Name = '{name}'").fetchall()

    cursor.close()
    connection.close()

    return jogo

  def UpdateJogo(self, jogo):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f"update jogos set Name = '{jogo.Nome}', Category = '{jogo.Categoria}', Platform = '{jogo.Plataforma}' where Game_Id = {jogo.Id}")

    connection.commit()
    cursor.close()
    connection.close()

  def UpdateUsuario(self, usuario):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f"update usuarios set Name = '{usuario.Nome}', Category = '{usuario.Categoria}', Platform = '{usuario.Plataforma}' where User_Id = {usuario.Id}")

    connection.commit()
    cursor.close()
    connection.close()


  def DeleteJogo(self, game_id):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f'delete from jogos where Game_ID = {game_id}')

    connection.commit()
    cursor.close()
    connection.close()

  def DeleteUsuario(self, user_id):
    connection = self.Connection()
    cursor = connection.cursor()

    cursor.execute(f'delete from usuarios where User_ID = {user_id}')

    connection.commit()
    cursor.close()
    connection.close()




  def TruncateTable(self, table):
    connection = self.Connection()
    cursor = connection.cursor()
    try:
      cursor.execute(f'Drop Table {table}')
      connection.commit()
      self.CreateTables()
      response = True
    except Exception as e:
      print(e)
      response = False
    finally:
      cursor.close()
      connection.close()

    return response

  def RestoreBackupJogos(self):
    connection = self.Connection()
    cursor = connection.cursor()

    self.TruncateTable('jogos')

    with open(PATH_JSON_JOGOS) as file:
      jogosJson = load(file)

    for jogoJson in jogosJson:
      self.CreateJogo(jogoJson)
  
    cursor.close()
    connection.close()

  def RestoreBackupUsuarios(self):
    connection = self.Connection()
    cursor = connection.cursor()

    self.TruncateTable('usuarios')

    with open(PATH_JSON_USUARIOS) as file:
      usuariosJson = load(file)

    for usuarioJson in usuariosJson:
      self.CreateUsuario(usuarioJson)
  
    cursor.close()
    connection.close()



  def backupUsuarios(self):
    i = 0
    usuarios = []
    usuariosDb = self.GetUsuarios()
    print('Iniciando backup de usuarios')

    if not usuariosDb:
      print("Nenhum usuário registrado ainda!")
    else:
      for usuarioDb in usuariosDb:
        i += 1
        print(f'Usuario {i} de {len(usuariosDb)}.')
  
        usuario = {
                  "ID": usuarioDb[0],
                   "Name": usuarioDb[1],
                   "Nickname": usuarioDb[2],
                   "Password": usuarioDb[3]
                  }
        usuarios.append(usuario)
          
      with open(PATH_JSON_USUARIOS, 'w') as file:
        dump(usuarios, file, indent=4)
    print('Backup de usuarios concluído com sucesso!\n')

  def backupJogos(self):
    i = 0
    jogos = []
    jogosDb = self.GetJogos()
    print('Iniciando backup de jogos')
    
    if not jogosDb:
      print("Nenhum jogo registrado ainda!")
    else:
      for jogoDb in jogosDb:
        i += 1
        print(f'Jogo {i} de {len(jogosDb)}.')

        jogo = {
                "ID": jogoDb[0],
                "Name": jogoDb[1],
                "Category": jogoDb[2],
                "Platform": jogoDb[3]
               }
        jogos.append(jogo)
        
      with open(PATH_JSON_JOGOS, 'w') as file:
        dump(jogos, file, indent=4)

    print('Backup de jogos concluído com sucesso!\n')


  def CreateBackup(self):
    print('\nIniciando backup...\n')
    try:

      self.backupUsuarios()

      self.backupJogos()

      print('\nBackup concluído com sucesso!\n')
    except Exception as e:
      print('\nFalha ao realizar backup!')
      print(e)