from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from config.Config import *
import os


class FormularioJogos(FlaskForm):
  nome = StringField('Nome do Jogo', [validators.data_required(), validators.Length(min=1, max=50)])
  categoria = StringField('Categoria', [validators.data_required(), validators.Length(min=1, max=50)])
  plataforma = StringField('Plataforma', [validators.data_required(), validators.Length(min=1, max=50)])
  salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
  nickname = StringField('Nickname', [validators.data_required(), validators.Length(min=3, max=24)])
  senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=6, max=50)])
  login = SubmitField('Entrar')

class FormularioCadastro(FlaskForm):
  nome = StringField('Nome', [validators.data_required(), validators.Length(min=3, max=50)])
  nickname = StringField('Nickname', [validators.data_required(), validators.Length(min=3, max=24)])
  senha = PasswordField('Senha', [validators.data_required(), validators.Length(min=6, max=50)])
  cadastrar = SubmitField('Cadastrar')


def recuperaImagem(id):
    for nomeArquivo in os.listdir(UPLOAD_PATH):
      if f'Capa{id}' in nomeArquivo:
        return nomeArquivo

    return 'capa_padrao.jpg'

def deletaArquivo(id):
  arquivo = recuperaImagem(id)
  if arquivo != 'capa_padrao.jpg':
     os.remove(os.path.join(UPLOAD_PATH, arquivo))


