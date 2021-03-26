import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)
# Use the os.environ method to import the appropriate APP_SETTINGS variables,
# depending on our environment
app.config.from_object(os.environ['APP_SETTINGS'])
#print(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result

#	@app.route('/')
#	def hello():
#		return "Hello World"

@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__=='__main__':
	app.run()
