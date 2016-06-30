from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# create the application object
app = Flask(__name__)

#get our configuration object
app.config.from_object('config')

#start up SQLAlchemy and Bootstrap
db = SQLAlchemy(app)
Bootstrap(app)


from app import views, models
