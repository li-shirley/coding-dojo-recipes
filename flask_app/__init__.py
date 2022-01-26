from flask import Flask
app = Flask(__name__)
app.secret_key = "cookingtime"

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app) 