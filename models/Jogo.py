class Jogo:
  def __init__(self, args):
    self.__id = args[0]
    self.__nome = args[1]
    self.__categoria = args[2]
    self.__plataforma = args[3]

  @property
  def Id(self):
    return self.__id

  @property
  def Nome(self):
    return self.__nome  
  
  def setNome(self, nome):
    self.__nome = nome

  @property
  def Categoria(self):
    return self.__categoria
  
  def setCategoria(self, categoria):
    self.__categoria = categoria

  @property
  def Plataforma(self):
    return self.__plataforma
  
  def setPlataforma(self, plataforma):
    self.__plataforma = plataforma


  def __str__(self):
    return f'Jogo: {self.Nome}'