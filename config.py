import random, string, os

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

SECRET_KEY = randomword(25)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']