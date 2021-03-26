import os
import requests # a library for sending HTTP requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)
# Use the os.environ method to import the appropriate APP_SETTINGS variables,
# depending on our environment
app.config.from_object(os.environ['APP_SETTINGS'])
#print(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def index():
	errors = []
	results = {}
	if request.method == "POST":
		# get url that the user has entered
		''' TODO: Currently user has to ensure URL includes http:// 
		or https://. Otherwise application won’t detect 
		that it’s a valid URL.
		Let's fix that ^
		'''
		try:
			url = request.form['url'] # Extract user-entered URL from the form object
			r = requests.get(url) # Send a GET request to the URL
			print(r.text)
		except:
			errors.append(
				"Unable to get URL. Please make sure it's valid and try again."
			)
	return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__=='__main__':
	app.run()
