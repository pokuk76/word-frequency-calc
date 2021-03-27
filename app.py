import os
import requests # a library for sending HTTP requests
import operator
import re # Hello my old friend
import nltk
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter	# https://pymotw.com/3/collections/counter.html
from bs4 import BeautifulSoup

app =  Flask(__name__)
# Use the os.environ method to import the appropriate APP_SETTINGS variables,
# depending on our environment
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # Why was this changed to true for the Text Processing section?
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
			#print(r.text)
		except:
			errors.append(
				"Unable to get URL. Please make sure it's valid and try again."
			)
			return render_template('index.html', errors=errors)
		if r:
			# text processing
			raw = BeautifulSoup(r.text, 'html.parser').get_text()
			nltk.data.path.append('./nltk_data/')	# set path
			tokens = nltk.word_tokenize(raw)
			text = nltk.Text(tokens)

			# remove punctuation and count raw words
			non_punct = re.compile('.*[A-Za-z].*')
			raw_words = [w for w in text if non_punct.match(w)]
			raw_word_count = Counter(raw_words)

			# remove "stop words"
			no_stop_words = [w for w in raw_words if w.lower() not in stops]
			no_stop_words_count = Counter(no_stop_words)

			# save the results
			results = sorted(
				no_stop_words_count.items(),
				key = operator.itemgetter(1),
				reverse = True
			)
			'''
			If we wanted to display the first N keyword:
			results = sorted(...)[:N]
			'''
			try:
				result = Result(
					url=url,
					result_all=raw_word_count,
					result_no_stop_words=no_stop_words_count
				)
				db.session.add(result)
				db.session.commit()
			except:
				errors.append("Unable to add item to database.")
	return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__=='__main__':
	app.run()
