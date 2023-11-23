class Usuario:
  def __init__(self, nome, nickname, senha):
    self.__nome = nome
    self.__nickname = nickname
    self.__senha = senha

  @property
  def Nome(self):
    return self.__nome
  
  @property
  def Nickname(self):
    return self.__nickname
  
  @property
  def Senha(self):
    return self.__senha