import os
import requests # a library for sending HTTP requests
import operator
import re # Hello my old friend
import nltk	# Natural Language Toolkit
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from stop_words import stops
from collections import Counter	# https://pymotw.com/3/collections/counter.html
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from worker import conn	# Connection established to the Redis Server in the worker.py file

''' Configuration section'''
app =  Flask(__name__)
# Use the os.environ method to import the appropriate APP_SETTINGS variables,
# depending on our environment
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # Why was this changed to true for the Text Processing section?
db = SQLAlchemy(app)
q = Queue(connection=conn)

from models import Result


def countAndSaveWords(url):
	"""
	TODO: add docstring
	"""
	errors = []

	try:
		r = requests.get(url) # Send a GET request to the URL
	except:
		errors.append(
			"Unable to get URL. Please make sure it's valid and try again."
		)
		return {'errors':  errors}

	# Let's process some text
	raw = BeautifulSoup(r.text, 'html.parser').get_text()
	nltk.data.path.append('./nltk_data/')	# set path
	tokens = nltk.word_tokenize(raw)
	text = nltk.Text(tokens)

	# Remove punctuation and count raw words
	non_punct = re.compile('.*[A-Za-z].*')
	raw_words = [w for w in text if non_punct.match(w)]
	raw_word_count = Counter(raw_words)

	# remove "stop words"
	no_stop_words = [w for w in raw_words if w.lower() not in stops]
	no_stop_words_count = Counter(no_stop_words)

	# save the results
	try:
		result = Result(
			url=url,
			result_all=raw_word_count,
			result_no_stop_words=no_stop_words_count
		)
		db.session.add(result)
		db.session.commit()
		return result.id
	except:
		errors.append("Unable to add item to database.")
		return {'errors': errors}

@app.route('/', methods=['GET', 'POST'])
def index():

	results = {}

	if request.method == "POST":

		'''
		Note: We need to import the countAndSaveWords function in our function index as the RQ package currently has 
		a bug, where it won’t find functions in the same module.
		'''
		from app import countAndSaveWords # this import solves a rq bug which currently exists
		url = request.form['url'] # Extract user-entered URL from the form object
		if not url[:8].startswith(('https://', 'http://')):
			# User no longer has to ensure URL starts with http:// or https://
			url = 'http://' + url

		''' Add a new job to the queue to run countAndSaveWords function '''
		job = q.enqueue_call(
			func=countAndSaveWords, args=(url,), result_ttl=5000
		)
		print(job.get_id())

	return render_template('index.html', results=results)

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
	"""
	View/app route for the results of our word frequency calculation
		Parameters:
			job_key(): ID of the the job in our queue
	"""
	# TODO: add some metadata so that if a website has been searched before, we just get that out of the db
	job = Job.fetch(job_key, connection=conn)

	if job.is_finished:
		''' Get the results for the job from the database '''
		result = Result.query.filter_by(id=job.result).first()	# job.result is the id/pk of result in the db
		results = sorted(
				result.result_no_stop_words.items(),
				key = operator.itemgetter(1),
				reverse = True
		)[:10]
		'''
		If we wanted to display the first N keyword:
		results = sorted(...)[:N]
		'''
		return jsonify(results)
	else:
		return "Nay!", 202

@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__=='__main__':
	app.run()
