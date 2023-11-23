from cryptocode import encrypt, decrypt
from dotenv import load_dotenv
import os
load_dotenv()
 

class CryptoGuard:
  def __init__(self):
    self.__secretKey = os.getenv("SECRET_KEY")
  
  @property
  def SecretKey(self):
    return self.__secretKey

  def encrypt(self, text):
    encryptText = encrypt(message=text, password="buh")
    return encryptText

  def decrypt(self, text):
    decryptText = decrypt(text, password="buh")
    return decryptText

  def __str__(self):
    return "Objeto de cryptografia"