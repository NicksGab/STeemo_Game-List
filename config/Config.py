import os

TITULO_DO_PROJETO = 'STeemo'
PATH_JSON_JOGOS = os.path.dirname(os.path.abspath(__file__)).replace('\config', '') + r'\json\jogos.json'
PATH_JSON_USUARIOS = os.path.dirname(os.path.abspath(__file__)).replace('\config', '') + r'\json\usuarios.json'
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)).replace('\config', '') + r'\uploads'