from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '3ec21baf9f0ed5d35f1b3ee214645d1e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21032396:Fab30cf22428dab2c8@csmysql.cs.cf.ac.uk:3306/c21032396_blogv1'
db = SQLAlchemy(app)

from flaskblog import routes
