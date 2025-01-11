from flask import Flask

app = Flask(__name__)

app.secret_key = 'klajdiiiiiaaaaaaoooo'

from my_app.controllers import user_controller
